# プロンプトテンプレートエディタ 実装仕様書

## 概要

StreamlitベースのLLMチャットボットアプリケーションに、
プロンプトテンプレートをUI上で編集できる機能を追加します。

## 機能要件

### 基本機能（Phase 1）

#### テンプレート管理

- 既存テンプレートの選択
- 新規テンプレート作成
- テンプレートの保存
- テンプレートの削除

#### エディタ機能

- テキスト編集
- シンタックスハイライト
- 変更の保存/破棄
- 基本的なバリデーション

### プレビュー機能（Phase 2）

- リアルタイムプレビュー表示
- プレースホルダーのハイライト
- プレースホルダーの入力テスト

### バックアップ機能（Phase 3）

- 自動バックアップ（変更時）
- バージョン履歴の保持
- 過去バージョンの復元

## 技術仕様

### 主要クラス構成

```python
class PromptTemplate:
    """プロンプトテンプレートを表現するクラス"""
    name: str           # テンプレート名
    content: str        # テンプレート内容
    description: str    # 説明文
    version: str        # バージョン
    last_modified: datetime  # 最終更新日時
    mode: str          # 関連付けられたモード

class PromptTemplateManager:
    """プロンプトテンプレートの管理を行うクラス"""
    def load_templates(self) -> None: ...
    def save_template(self, template: PromptTemplate) -> bool: ...
    def validate_template(self, content: str) -> bool: ...
    def _create_backup(self, template: PromptTemplate) -> None: ...

class PromptTemplateEditorUI:
    """プロンプトテンプレートのUIコンポーネント"""
    def render_template_selector(self) -> None: ...
    def render_editor(self) -> None: ...
    def render_preview(self) -> None: ...
```

### ファイル構造

```text
app/
├── chat_app.py                    # メインアプリケーション
├── prompt_template_manager.py     # テンプレート管理機能
├── prompt_template_editor.py      # テンプレート編集UI
└── pages/
    └── 1_prompt_template_settings.py  # テンプレート設定ページ

templates/
├── prompts/
│   ├── normal/
│   │   ├── prompt_template.txt
│   │   └── default_you_lines.txt
│   ├── custom/
│   │   └── ...
│   └── backups/
│       └── {template_name}/
│           └── {timestamp}_v{version}.txt
```

### UIコンポーネント

#### サイドバー

- テンプレート選択ドロップダウン
- 新規作成ボタン
- モード表示
- 保存/破棄ボタン

#### メインパネル

- テンプレート名入力フィールド
- 説明文入力フィールド
- テキストエディタ（シンタックスハイライト付き）
- プレビューパネル
- バージョン履歴表示

## 実装手順

### Phase 1: 基本機能

1. PromptTemplateManagerの実装

   - テンプレートのCRUD操作
   - ファイルシステムとの連携

2. PromptTemplateEditorUIの実装

   - Streamlitコンポーネントの配置
   - イベントハンドリング

3. バリデーション機能の実装

   - 構文チェック
   - 必須項目の確認

### Phase 2: プレビュー機能

1. プレビューパネルの実装

   - リアルタイム更新
   - プレースホルダー処理

2. テスト機能の実装

   - プレースホルダー値の入力UI
   - プレビュー生成

### Phase 3: バックアップ機能

1. バージョン管理システムの実装

   - 自動バックアップ
   - バージョン履歴管理

2. 復元機能の実装

   - バージョン選択UI
   - 復元処理

## エラーハンドリング

### 想定されるエラー

#### ファイル操作エラー

- 読み込み失敗
- 書き込み失敗
- 権限エラー

#### バリデーションエラー

- 不正なテンプレート構文
- 必須項目の欠落

#### 競合エラー

- 同時編集による競合
- バージョンの不一致

### エラー応答

- エラーメッセージの日本語化
- エラー発生箇所の特定
- リカバリー方法の提示

## セキュリティ考慮事項

### ファイルアクセス

- 許可されたディレクトリのみアクセス可能
- 適切なパーミッション設定

### 入力バリデーション

- 特殊文字のエスケープ
- サイズ制限の実装

### バックアップ保護

- バックアップファイルの暗号化
- アクセス制御

## パフォーマンス最適化

### 編集操作

- 差分保存による効率化
- 自動保存の適切な間隔設定

### プレビュー生成

- 遅延読み込みの実装
- キャッシュの活用

### バックアップ処理

- 非同期処理の活用
- 古いバージョンの自動クリーンアップ
