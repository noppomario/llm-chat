# LLM Chat Documentation

## プロジェクト概要

StreamlitベースのLLMチャットボットアプリケーションです。
プロンプトテンプレートの管理や編集機能を備え、カスタマイズ可能なチャットインターフェースを提供します。

## 主な機能

- マルチモードチャットインターフェース
- プロンプトテンプレート管理
- 自動会話機能
- セッション管理
- カスタマイズ可能なUI

## ドキュメント構成

1. [プロンプトエディタ仕様書](specifications/prompt_editor_spec.md)
   - プロンプトエディタの詳細仕様
   - システムアーキテクチャ
   - 実装計画

2. [導入ガイド](getting_started.md)
   - インストール方法
   - 基本的な使い方
   - トラブルシューティング

3. [GitHub Pages設定](github_pages_setup.md)
   - MkDocsの設定
   - デプロイ方法
   - 運用管理

## セットアップ方法

```bash
# リポジトリのクローン
git clone <repository-url>

# 依存パッケージのインストール
pip install -r requirements.txt

# アプリケーションの起動
streamlit run app/main.py
```

## ドキュメントの生成方法

このドキュメントはMkDocsを使用して生成され、GitHub Pagesでホストされています。
ローカルでドキュメントを確認する場合は以下のコマンドを実行してください：

1. MkDocsのインストール

   ```bash
   pip install mkdocs-material
   ```

2. ローカルサーバーの起動

   ```bash
   mkdocs serve
   ```

3. ブラウザで確認

   ```text
   http://localhost:8000
   ```
