# チャットボットアプリケーション

StreamlitベースのLLMチャットボットアプリケーションです。カスタマイズ可能なプロンプトテンプレートと自動会話機能を備えています。

## 機能

* 💬 LLM APIを使用したチャット機能
* 🔄 カスタマイズ可能なモード切り替え機能
* 🤖 自動会話機能
  * 1回自動：ボタンクリックで1回の自動会話
  * 連続自動：設定した間隔で自動的に会話を継続
* 🌐 Streamlitベースのウェブインターフェース

## プロジェクト構造

```plaintext
.
├── app/                    # アプリケーションパッケージ
│   ├── __init__.py        # パッケージ初期化
│   ├── streamlit_app.py   # Streamlitアプリケーション
│   └── main.py           # コアロジック
├── config/                # 設定パッケージ
│   └── config.example.py  # 設定ファイルのテンプレート
└── templates/            # テンプレートファイル
    └── prompts/          # プロンプトテンプレート
        ├── normal/       # 通常モード用（サンプルとして参照）
        └── custom/       # カスタムモード用
```

## 必要要件

* Python 3.6以上
* Streamlit
* Requests

## セットアップ手順

1. リポジトリのクローン：

```bash
git clone [リポジトリURL]
cd [プロジェクトディレクトリ]
```

2. 必要なパッケージをインストール：

```bash
pip install -r requirements.txt
```

3. 設定ファイルの準備：

```bash
# config/__init__.pyを作成：
# config.example.pyをコピーして作成し、必要な設定を行う
cp config/config.example.py config/__init__.py

# 以下の項目を編集：
# - APIエンドポイント
# - モデル名
# - ボット名
# - モードごとの設定
```

⚠️ 重要：config/__init__.pyはセンシティブな情報を含むため、Gitで管理されません。

4. プロンプトテンプレートの準備：

```bash
# プロンプトディレクトリの作成（必要に応じて）
mkdir -p templates/prompts/custom

# プロンプトファイルの作成
# templates/prompts/normal/を参考に以下のファイルを作成：
# - prompt_template.txt：ボットの性格や応答スタイルを定義
# - default_you_lines.txt：自動会話用のメッセージ一覧
```

## モードの設定

config/__init__.pyで各モードの詳細設定が可能です：

```python
MODES = {
    'mode_name': {
        'display_name': '表示名',
        'files': {
            'prompt_template': 'テンプレートファイルのパス',
            'you_lines': '会話ラインファイルのパス'
        },
        'response_end_marker': '応答終了マーカー',
        'message_generator': 特殊なメッセージ生成関数（オプション）
    }
}
```

## セキュリティ対策

このリポジトリは以下のファイルを含みません：

1. 設定ファイル

* config/__init__.py（センシティブな設定を含むため、.gitignoreで除外）
* config.example.pyには汎用的な設定例のみを記載
* 実際の設定はconfig/__init__.pyに記載し、ローカルでのみ管理

2. プロンプトテンプレート

* normal/ディレクトリには汎用的なサンプルのみを提供
* custom/ディレクトリ以下は.gitignoreで管理（センシティブな情報を含む可能性があるため）

## ファイル管理の注意点

1. config/__init__.py

* Gitで管理されないファイル
* センシティブな情報（APIキー、モデル設定等）を含む
* ローカル環境でのみ管理
* バックアップが必要な場合は、別の安全な方法で保管

2. カスタムプロンプト

* templates/prompts/custom/以下のファイルはGitで管理されない
* 必要に応じてローカルでバックアップを作成

## カスタマイズ

### プロンプトテンプレート

* `templates/prompts/normal/`のサンプルを参考に作成
* 各モードごとに専用のテンプレートを配置可能
* 基本的なプロンプト形式はサンプルに準拠

### 自動会話設定

* デフォルトの会話ラインをカスタマイズ可能
* モードごとに異なる会話スタイルを定義可能
* message_generator関数で会話生成ロジックをカスタマイズ可能

## 使用方法

1. アプリケーションを起動：

```bash
streamlit run app/streamlit_app.py
```

2. ブラウザで`http://localhost:8501`を開きます

## ライセンス

MITライセンス
