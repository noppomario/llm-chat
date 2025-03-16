"""
StreamlitベースのチャットボットUIを提供するモジュール。
ユーザーインターフェース、セッション管理、自動会話機能を担当します。
"""

import streamlit as st
import time
import os
import sys

# configモジュールのパスを追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import YOU, BOT, CURRENT_MODE, MODES
from main import LLMAPI, LLMAPIError

class ChatApplication:
    """
    StreamlitベースのチャットUIを管理するクラス。
    セッション状態、モード切り替え、自動会話機能を提供します。
    """

    def __init__(self):
        """
        ChatApplicationのコンストラクタ。
        セッション状態を初期化し、UIの基本設定を行います。
        """
        try:
            self.initialize_session_state()
            self.setup_page()
            self.llm = LLMAPI(mode=st.session_state.current_mode)
        except Exception as e:
            st.error(f"初期化エラー: {e}")
            raise

    def initialize_session_state(self):
        """
        Streamlitのセッション状態を初期化します。
        メッセージ履歴、自動会話設定、現在のモードを管理します。
        """
        # メッセージ関連
        if 'messages' not in st.session_state:
            st.session_state.messages = []
        if 'previous_messages' not in st.session_state:
            st.session_state.previous_messages = []
        
        # 設定関連
        if 'auto_conversation' not in st.session_state:
            st.session_state.auto_conversation = False
        if 'auto_interval' not in st.session_state:
            st.session_state.auto_interval = 5
        if 'current_mode' not in st.session_state:
            st.session_state.current_mode = CURRENT_MODE

    def setup_page(self):
        """
        ページの基本設定を行います。
        タイトル、アイコン、レイアウトを設定します。
        """
        st.set_page_config(
            page_title=f"AIチャット - {self.get_mode_text()}",
            page_icon="💭",
            layout="wide",
            menu_items={
                'Get Help': None,
                'Report a bug': None,
                'About': "AIチャット"
            }
        )
        st.title("AIチャット")

    def get_mode_text(self):
        """
        現在のモードの表示名を取得します。

        Returns:
            str: モードの表示名
        """
        return MODES[st.session_state.current_mode]['display_name']

    def render_mode_selector(self):
        """
        モード選択UIを描画します。
        モードが変更された場合、LLMAPIインスタンスを再初期化します。
        """
        mode = st.selectbox(
            "モード選択",
            list(MODES.keys()),
            format_func=lambda x: MODES[x]['display_name'],
            index=list(MODES.keys()).index(st.session_state.current_mode)
        )
        
        # モードが変更された場合の処理
        if mode != st.session_state.current_mode:
            st.session_state.current_mode = mode
            try:
                self.llm = LLMAPI(mode=mode)  # 新しいモードでLLMAPIを初期化
                st.session_state.messages = []  # メッセージ履歴をクリア
                st.rerun()  # ページを再読み込み
            except Exception as e:
                st.error(f"モード切り替えエラー: {e}")

    def render_auto_conversation_controls(self):
        """
        自動会話コントロールUIを描画します。
        1回自動ボタンと連続自動トグル、インターバル設定を提供します。
        """
        # 1回自動ボタン
        if st.button("1回自動", key="single_auto"):
            try:
                self.auto_conversation_once()
            except Exception as e:
                st.error(f"自動会話エラー: {e}")
        
        # 連続自動トグル
        auto_running = st.toggle("連続自動", value=st.session_state.auto_conversation)
        
        if auto_running != st.session_state.auto_conversation:
            st.session_state.auto_conversation = auto_running
            if auto_running:
                st.session_state.auto_interval = st.slider(
                    "インターバル（秒）",
                    min_value=1,
                    max_value=10,
                    value=5
                )

    def process_message(self, message, is_auto=False):
        """
        メッセージを処理し、APIからの応答を取得して表示します。

        Args:
            message (str): 処理するメッセージ
            is_auto (bool, optional): 自動会話によるメッセージかどうか

        Raises:
            LLMAPIError: API通信に失敗した場合
        """
        if not isinstance(message, str):
            raise ValueError("メッセージは文字列である必要があります")

        # ユーザーメッセージの追加（カギカッコ付き）
        user_message = f"「{message}」"
        st.session_state.messages.append({"role": "user", "content": user_message})
        
        # ユーザーメッセージを即時表示
        with st.chat_message("user"):
            st.write(user_message)
        
        # アシスタントのメッセージ枠を事前に表示
        with st.chat_message("assistant"):
            # 処理中のプレースホルダーを表示
            thinking_placeholder = st.empty()
            thinking_placeholder.write(f"{BOT}が考え中...")
            
            try:
                # APIリクエストを実行
                response = self.llm.request(message)
                
                if response and 'response' in response:
                    # プレースホルダーを応答で置き換え
                    thinking_placeholder.write(response['response'])
                    # メッセージ履歴に追加
                    st.session_state.messages.append(
                        {"role": "assistant", "content": response['response']}
                    )
                else:
                    thinking_placeholder.error("返答が正しく受信されませんでした。")
            except LLMAPIError as e:
                thinking_placeholder.error(f"APIエラー: {e}")
            except Exception as e:
                thinking_placeholder.error(f"予期しないエラー: {e}")

    def auto_conversation_once(self):
        """
        1回の自動会話を実行します。
        メッセージを自動生成し、APIに送信します。

        Raises:
            LLMAPIError: API通信に失敗した場合
        """
        try:
            next_message = self.llm.generate_next_message()
            self.process_message(next_message, is_auto=True)
        except Exception as e:
            st.error(f"自動会話生成エラー: {e}")

    def render_chat_interface(self):
        """
        チャットインターフェースを描画します。
        メッセージ履歴の表示、ユーザー入力、自動会話を管理します。
        """
        # チャット履歴の表示
        if len(st.session_state.messages) > 0:
            for message in st.session_state.messages[:-2] if len(st.session_state.messages) > 2 else st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.write(message["content"])

        # ユーザー入力の処理
        if prompt := st.chat_input(f"{YOU}のメッセージを入力"):
            try:
                self.process_message(prompt)
            except Exception as e:
                st.error(f"メッセージ処理エラー: {e}")

        # 連続自動会話の処理
        if st.session_state.auto_conversation:
            time.sleep(st.session_state.auto_interval)
            try:
                self.auto_conversation_once()
                st.rerun()
            except Exception as e:
                st.error(f"連続自動会話エラー: {e}")
                st.session_state.auto_conversation = False

    def run(self):
        """
        アプリケーションのメイン実行メソッド。
        サイドバーとメインインターフェースを描画します。
        """
        try:
            # サイドバーの設定
            with st.sidebar:
                st.markdown("### 基本設定")
                self.render_mode_selector()
                
                st.markdown("### 自動会話設定")
                self.render_auto_conversation_controls()
            
            # メインコンテンツ（チャットインターフェース）
            self.render_chat_interface()
        except Exception as e:
            st.error(f"アプリケーションエラー: {e}")

def main():
    """
    アプリケーションのエントリーポイント。
    ChatApplicationインスタンスを作成し実行します。
    """
    try:
        app = ChatApplication()
        app.run()
    except Exception as e:
        st.error(f"クリティカルエラー: {e}")

if __name__ == "__main__":
    main()