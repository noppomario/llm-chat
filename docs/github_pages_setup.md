# GitHub Pages設定ガイド

## MkDocsによるドキュメント管理

このプロジェクトでは、ドキュメントの管理にMkDocsを使用し、
GitHub Pagesでホスティングしています。

### 必要な設定ファイル

#### MkDocs設定

プロジェクトルートに`mkdocs.yml`を配置します：

```yaml
site_name: LLM Chat Documentation
site_description: LLMチャットボットのドキュメント
site_author: Team
theme:
  name: material
  language: ja
  features:
    - navigation.tabs
    - navigation.sections
    - navigation.expand
    - search.highlight

nav:
  - ホーム: index.md
  - 仕様書:
    - プロンプトエディタ: specifications/prompt_editor_spec.md

markdown_extensions:
  - pymdownx.highlight
  - pymdownx.superfences
  - pymdownx.tasklist
```

#### 依存関係

`requirements-docs.txt`にドキュメント生成用の依存関係を記述：

```text
mkdocs-material
```

### GitHub Actionsワークフロー

`.github/workflows/docs.yml`に以下の設定を追加：

```yaml
name: Deploy MkDocs to GitHub Pages

on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.x'
          
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements-docs.txt
          
      - name: Build and deploy documentation
        run: mkdocs build
          
      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        if: github.ref == 'refs/heads/main'
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./site
```

## セットアップ手順

### リポジトリの設定

1. GitHubリポジトリの"Settings" > "Pages"に移動
2. ソースを"GitHub Actions"に設定

### ブランチ保護の設定（オプション）

1. `gh-pages`ブランチを保護
2. 直接のプッシュを禁止
3. GitHub Actionsからのみ更新可能に設定

### ローカルでの確認方法

1. MkDocsのインストール

   ```bash
   pip install -r requirements-docs.txt
   ```

2. ローカルサーバーの起動

   ```bash
   mkdocs serve
   ```

3. ブラウザで確認

   ```text
   http://localhost:8000
   ```

## ドキュメント更新ワークフロー

### 編集手順

1. `docs/`ディレクトリ内のMarkdownファイルを編集
2. 新しいドキュメントを追加する場合は`mkdocs.yml`の`nav`セクションも更新

### プレビューと公開

1. ローカルでのプレビュー

   ```bash
   mkdocs serve
   ```

2. 変更のコミットとプッシュ

   ```bash
   git add .
   git commit -m "docs: ドキュメントの更新"
   git push origin main
   ```

3. デプロイの確認
   - GitHub Actionsの実行状況を確認
   - デプロイ完了後、GitHub PagesのURLでサイトを確認

## トラブルシューティング

### よくある問題と解決方法

#### ビルドエラー

- mkdocs.ymlの構文を確認
- 参照しているファイルの存在を確認
- Markdownの文法エラーをチェック

#### デプロイエラー

- GitHub Actionsのログを確認
- リポジトリの権限設定を確認
- `GITHUB_TOKEN`の権限を確認

#### 表示の問題

- ブラウザのキャッシュをクリア
- 相対パスが正しいか確認
- テーマの設定を確認
