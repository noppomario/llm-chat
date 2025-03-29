# Getting Started

## 環境構築

### 必要条件

- Python 3.8以上
- pip (Pythonパッケージマネージャー)
- Git

### インストール手順

1. リポジトリのクローン

   ```bash
   git clone <repository-url>
   cd llm-chat
   ```

2. 仮想環境の作成（推奨）

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
   ```

3. 依存パッケージのインストール

   ```bash
   pip install -r requirements.txt
   ```

4. 設定ファイルの準備

   ```bash
   cp config/config.example.py config/config.py
   # config.pyを編集して必要な設定を行う
   ```

5. アプリケーションの起動

   ```bash
   streamlit run app/main.py
   ```

## 基本的な使い方

### モードの選択

1. サイドバーの「モード選択」からモードを選択
2. 各モードは異なる特性と機能を持っています

   - Code: プログラミング支援
   - Architect: 設計支援
   - Ask: 一般的な質問対応
   - Debug: デバッグ支援

### チャットの使用

1. テキスト入力欄にメッセージを入力
2. Enterキーまたは送信ボタンでメッセージを送信
3. AIアシスタントからの応答を待つ

### 自動会話機能

1. 「1回自動」ボタン: 1回だけ自動で会話を生成
2. 「連続自動」トグル: 定期的に自動会話を生成
3. インターバル設定: 自動会話の間隔を調整

## トラブルシューティング

### よくある問題と解決方法

1. アプリケーションが起動しない

   - Python versionの確認
   - 依存パッケージの再インストール
   - ログの確認

2. APIエラーが発生する

   - 設定ファイルの確認
   - ネットワーク接続の確認
   - APIキーの有効性確認

3. 自動会話が動作しない

   - ブラウザのキャッシュクリア
   - アプリケーションの再起動
   - 設定の見直し

### サポート

問題が解決しない場合は、以下の手順で報告してください：

1. GitHubのIssueを作成
2. 問題の詳細な説明
3. 発生時の状況
4. エラーメッセージ（もしあれば）
5. 環境情報
