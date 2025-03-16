# APIエンドポイントの設定
URL = 'http://localhost:11434/api/generate'  # Ollama APIのデフォルトエンドポイント

# アプリケーションの基本設定
YOU = 'ユーザー'  # ユーザーの表示名
BOT = 'アシスタント'  # ボットの表示名
MODEL = 'mistral'  # 使用するモデル名

# モード設定
MODE_NORMAL = 'normal'  # 通常モード（サンプルとして提供）
MODE_CUSTOM = 'custom'  # カスタムモード
CURRENT_MODE = MODE_NORMAL  # デフォルトモード

def message_generator(base_line):
    """会話メッセージの生成関数の例"""
    return base_line

# モードごとの設定
MODES = {
    MODE_NORMAL: {
        'display_name': '通常モード',
        'files': {
            'prompt_template': 'templates/prompts/normal/prompt_template.txt',
            'you_lines': 'templates/prompts/normal/default_you_lines.txt'
        },
        'response_end_marker': '」',  # 応答の終了を示すマーカー
        'message_generator': message_generator  # メッセージ生成関数
    },
    MODE_CUSTOM: {
        'display_name': 'カスタムモード',
        'files': {
            'prompt_template': 'templates/prompts/custom/prompt_template.txt',
            'you_lines': 'templates/prompts/custom/default_you_lines.txt'
        },
        'response_end_marker': '。'
    }
}

"""
設定ファイルの使い方：

1. このファイルの内容をconfig/__init__.pyにコピー
2. 以下の項目を環境に合わせて設定：
   - URL: APIエンドポイント
   - MODEL: 使用するモデル名
   - BOT: ボットの表示名
   - CURRENT_MODE: デフォルトモード

3. プロンプトファイルの配置：
   - 通常モード用のサンプルが templates/prompts/normal/ に用意されています
   - カスタムモード用のファイルは templates/prompts/custom/ に作成してください

4. モードの設定：
   - 各モードの設定をMODESディクショナリで定義
   - 必要に応じて新しいモードを追加可能

セキュリティに関する注意：
* センシティブな情報は直接このファイルに記載せず、
  実際の設定は`config/__init__.py`に記載してください
* プロンプトファイルも同様に、センシティブな情報は
  custom/ディレクトリ以下に配置してください
"""
