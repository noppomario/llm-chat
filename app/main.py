"""
LLMチャットボットのコアロジックを提供するモジュール。
外部APIとの通信、会話履歴の管理、自動会話の生成を担当します。
"""

import requests
import json
import random
import os
import sys

# configモジュールのパスを追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import URL, YOU, BOT, MODEL, CURRENT_MODE, MODES
from app.paths import get_prompt_path

class LLMAPIError(Exception):
    """LLM APIに関連するエラーを表すカスタム例外クラス"""
    pass

class LLMAPI:
    """
    LLMAPIクラスは、会話履歴を管理し、外部APIにリクエストを送信して応答を取得する機能を提供します。
    モードに応じたプロンプトテンプレートと会話ラインを管理し、自動会話機能もサポートします。
    """

    def __init__(self, mode=None):
        """
        LLMAPIのコンストラクタ。

        Args:
            mode (str, optional): 使用するモード。Noneの場合はCURRENT_MODEを使用。

        Raises:
            ValueError: 指定されたモードが不正な場合
        """
        if mode is not None and mode not in MODES:
            raise ValueError(f"不正なモード名です: {mode}")

        self.conversation_history = []  # 会話履歴を保持
        self.initial_prompt_sent = False  # 初回プロンプト送信フラグ
        self.current_mode = mode if mode is not None else CURRENT_MODE
        self.current_mode_config = MODES[self.current_mode]  # 現在のモード設定
        self.prompt_template = self.load_prompt_template()  # プロンプトテンプレートを読み込む
        self.default_you_lines = self.load_default_you_lines()  # デフォルトの会話ラインを読み込む

    def load_prompt_template(self):
        """
        現在のモードに応じたプロンプトテンプレートをファイルから読み込みます。

        Returns:
            str: プロンプトテンプレートの内容

        Raises:
            FileNotFoundError: テンプレートファイルが存在しない場合
            IOError: ファイル読み込みに失敗した場合
        """
        template_path = get_prompt_path(self.current_mode, 'prompt_template.txt')
        try:
            with open(template_path, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"プロンプトテンプレートが見つかりません: {template_path}")
        except IOError as e:
            raise IOError(f"プロンプトテンプレートの読み込みに失敗しました: {e}")

    def load_default_you_lines(self):
        """
        現在のモードに応じたデフォルトの会話ラインをファイルから読み込みます。

        Returns:
            list: デフォルトの会話ラインのリスト

        Raises:
            FileNotFoundError: 会話ラインファイルが存在しない場合
            IOError: ファイル読み込みに失敗した場合
        """
        lines_path = get_prompt_path(self.current_mode, 'default_you_lines.txt')
        try:
            with open(lines_path, 'r', encoding='utf-8') as file:
                return [line.strip() for line in file.readlines() if line.strip()]
        except FileNotFoundError:
            raise FileNotFoundError(f"会話ラインファイルが見つかりません: {lines_path}")
        except IOError as e:
            raise IOError(f"会話ラインファイルの読み込みに失敗しました: {e}")

    def request(self, user_input):
        """
        ユーザー入力を基に外部APIにリクエストを送信し、応答を取得します。

        Args:
            user_input (str): ユーザーの入力

        Returns:
            dict: APIからの応答オブジェクト

        Raises:
            LLMAPIError: API通信に失敗した場合
        """
        if not isinstance(user_input, str):
            raise ValueError("user_inputは文字列である必要があります")

        # 会話履歴に現在の入力を追加
        if user_input:
            self.conversation_history.append(f"{YOU}: {user_input}")

        # 履歴をまとめてプロンプトに追加
        prompt_history = "\n".join(self.conversation_history)

        # 初回のみテンプレートを使用
        if not self.initial_prompt_sent:
            prompt = self.prompt_template.format(
                history=prompt_history,
                bot_name=BOT
            )
            self.initial_prompt_sent = True
        else:
            prompt = prompt_history + f"\n{BOT}:"

        # リクエストボディ
        request_body = {
            'model': MODEL,
            'prompt': prompt,
            'stream': True,  # ストリーミングを有効化
        }

        try:
            response = requests.post(
                URL, 
                json=request_body, 
                stream=True, 
                headers={'Content-Type': 'application/json'},
                timeout=300  # タイムアウトを設定
            )
            response.raise_for_status()  # HTTPエラーをチェック

            full_response = ''
            response_received = False

            for chunk in response.iter_content(chunk_size=None):
                chunk_str = chunk.decode('utf-8')

                # 各チャンクごとに JSON をパース
                try:
                    json_chunk = json.loads(chunk_str)
                    response_text = json_chunk.get('response', '')

                    # レスポンスを蓄積
                    if response_text:
                        full_response += response_text

                    # 応答終了マーカーが含まれたら終了
                    if response_text and self.current_mode_config['response_end_marker'] in response_text:
                        response_received = True
                        response.close()  # ストリームを終了
                        response_obj = {'response': full_response.strip()}  # オブジェクト形式で返却
                        self.conversation_history.append(f"{BOT}: {response_obj['response']}")  # 履歴に追加
                        return response_obj  # オブジェクトを返す
                except json.JSONDecodeError:
                    # 部分的な JSON チャンクの場合は無視
                    continue

            # 最後まで到達した場合の処理
            if not response_received:
                response_obj = {'response': full_response.strip() or '予期しない形式の返答が返されました。'}
                self.conversation_history.append(f"{BOT}: {response_obj['response']}")
                return response_obj

        except requests.RequestException as error:
            raise LLMAPIError(f"APIリクエストに失敗しました: {error}")

    def generate_next_message(self):
        """
        会話ラインから次のメッセージを生成します。
        モードに応じたメッセージ生成関数がある場合はそれを使用し、
        ない場合はデフォルトの会話ラインからランダムに選択します。

        Returns:
            str: 生成されたメッセージ

        Raises:
            ValueError: 会話ラインが空の場合
        """
        if not self.default_you_lines:
            raise ValueError("会話ラインが空です")

        base_line = random.choice(self.default_you_lines)
        
        # モードの設定で生成方法が定義されている場合はその方法を使用
        if 'message_generator' in self.current_mode_config:
            return self.current_mode_config['message_generator'](base_line)
            
        # デフォルトはそのまま返す
        return base_line

    def auto_conversation(self, use_history=True):
        """
        自動的に会話を進行します。

        Args:
            use_history (bool): Trueの場合、会話履歴から生成。Falseの場合、定義済みラインから選択。

        Returns:
            dict: APIからの応答オブジェクト

        Raises:
            LLMAPIError: API通信に失敗した場合
        """
        if use_history:
            next_message = self.generate_next_message()
        else:
            next_message = random.choice(self.default_you_lines)

        return self.request(next_message)

def main():
    """
    メイン関数。ユーザーとの対話を開始し、ユーザー入力に応じてAPIリクエストを送信します。
    """
    try:
        llm = LLMAPI()
        print(f'{BOT}と会話を始めましょう！（終了するには "exit" と入力してください）')

        while True:
            user_input = input(f'{YOU}: ')
            if user_input.lower() == 'exit':
                print('会話を終了します。')
                break

            if user_input.strip() == '':
                response_obj = llm.auto_conversation()
            else:
                response_obj = llm.request(user_input)

            if response_obj and 'response' in response_obj:
                print(f"{BOT}: {response_obj['response']}\n")
            else:
                print(f'{BOT}: 返答が正しく受信されませんでした。\n')

    except Exception as e:
        print(f"エラーが発生しました: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
