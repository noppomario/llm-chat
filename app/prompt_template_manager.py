"""
プロンプトテンプレートの管理機能を提供するモジュール。
テンプレートのCRUD操作、バリデーション、バックアップを担当します。
"""

import os
import json
from datetime import datetime
from dataclasses import dataclass
from typing import Optional, List, Dict
import shutil
from app.paths import ROOT_DIR, get_prompt_path

@dataclass
class PromptTemplate:
    """プロンプトテンプレートを表現するデータクラス"""
    name: str
    content: str
    description: str = ""
    version: str = "1.0.0"
    mode: str = "normal"
    last_modified: datetime = None

    def __post_init__(self):
        """インスタンス生成後の初期化処理"""
        if self.last_modified is None:
            self.last_modified = datetime.now()

class PromptTemplateManager:
    """プロンプトテンプレートの管理を行うクラス"""

    def __init__(self):
        """
        PromptTemplateManagerのコンストラクタ
        """
        self.base_path = os.path.join(ROOT_DIR, "templates", "prompts")
        self.templates: Dict[str, PromptTemplate] = {}
        self.load_templates()

    def load_templates(self) -> None:
        """
        全てのテンプレートをロードします。
        使用可能なモードのテンプレートを読み込み、self.templatesディクショナリに格納します。
        """
        for mode in ["normal", "custom"]:
            try:
                template_path = get_prompt_path(mode, "prompt_template.txt")
                if os.path.exists(template_path):
                    with open(template_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        template = PromptTemplate(
                            name=f"{mode}_template",
                            content=content,
                            mode=mode,
                            last_modified=datetime.fromtimestamp(os.path.getmtime(template_path))
                        )
                        self.templates[template.name] = template
            except ValueError as e:
                print(f"無効なモードまたはファイル名です: {e}")
            except IOError as e:
                print(f"{mode}モードのテンプレート読み込みに失敗しました: {e}")
            except Exception as e:
                print(f"予期しないエラーが発生しました: {e}")

    def get_template(self, name: str) -> Optional[PromptTemplate]:
        """
        指定された名前のテンプレートを取得します。

        Args:
            name (str): テンプレート名

        Returns:
            Optional[PromptTemplate]: テンプレート。存在しない場合はNone。
        """
        return self.templates.get(name)

    def list_templates(self) -> List[str]:
        """
        利用可能なテンプレート名の一覧を返します。

        Returns:
            List[str]: テンプレート名のリスト
        """
        return list(self.templates.keys())

    def save_template(self, template: PromptTemplate) -> bool:
        """
        テンプレートを保存します。

        Args:
            template (PromptTemplate): 保存するテンプレート

        Returns:
            bool: 保存が成功した場合はTrue

        Raises:
            ValueError: テンプレート名が不正な場合
            IOError: ファイルの保存に失敗した場合
        """
        if not template.name or not template.content:
            raise ValueError("テンプレート名と内容は必須です")

        try:
            # テンプレートパスを取得
            template_path = get_prompt_path(template.mode, "prompt_template.txt")
            
            # バックアップを作成
            self._create_backup(template)

            # 必要なディレクトリを作成
            os.makedirs(os.path.dirname(template_path), exist_ok=True)

            # テンプレートを保存
            with open(template_path, 'w', encoding='utf-8') as f:
                f.write(template.content)
                
            # メモリ上のテンプレートを更新
            template.last_modified = datetime.now()
            self.templates[template.name] = template
            return True

        except ValueError as e:
            raise ValueError(f"無効なモードまたはファイル名です: {e}")
        except IOError as e:
            raise IOError(f"テンプレートの保存に失敗しました: {e}")
        except Exception as e:
            raise Exception(f"予期しないエラーが発生しました: {e}")

    def _create_backup(self, template: PromptTemplate) -> None:
        """
        テンプレートのバックアップを作成します。

        Args:
            template (PromptTemplate): バックアップするテンプレート
        """
        backup_dir = os.path.join(self.base_path, "backups", template.name)
        os.makedirs(backup_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(backup_dir, f"{timestamp}_v{template.version}.txt")

        try:
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(template.content)
        except IOError as e:
            print(f"バックアップの作成に失敗しました: {e}")

    def validate_template(self, content: str) -> bool:
        """
        テンプレートの内容を検証します。

        Args:
            content (str): 検証するテンプレート内容

        Returns:
            bool: 検証に成功した場合はTrue
        """
        # 基本的なバリデーション
        if not content:
            return False

        # プレースホルダーの形式チェック
        try:
            # 文字列フォーマットのテスト（例：{history}や{bot_name}が正しく機能するか）
            content.format(history="test", bot_name="test")
            return True
        except (KeyError, ValueError):
            return False

    def delete_template(self, name: str) -> bool:
        """
        テンプレートを削除します。

        Args:
            name (str): 削除するテンプレート名

        Returns:
            bool: 削除が成功した場合はTrue
        """
        template = self.templates.get(name)
        if not template:
            return False

        try:
            template_path = get_prompt_path(template.mode, "prompt_template.txt")
            if os.path.exists(template_path):
                os.remove(template_path)
            del self.templates[name]
            return True
        except (ValueError, OSError):
            return False