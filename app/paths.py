"""
ファイルパスの管理を行うモジュール。
プロジェクト全体で使用するパス関連の処理を集約します。
"""

import os

# プロジェクトのルートディレクトリを取得
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_config_path():
    """設定ファイルのパスを取得"""
    return os.path.join(ROOT_DIR, 'config')

def get_templates_path():
    """テンプレートディレクトリのパスを取得"""
    return os.path.join(ROOT_DIR, 'templates')

def get_prompt_path(mode, filename):
    """
    指定されたモードのプロンプトファイルの完全パスを取得

    Args:
        mode (str): モード名（'normal' or 'custom'）
        filename (str): ファイル名（'prompt_template.txt' or 'default_you_lines.txt'）

    Returns:
        str: プロンプトファイルの完全パス
    
    Raises:
        ValueError: モード名またはファイル名が不正な場合
    """
    if not mode or not filename:
        raise ValueError("モード名とファイル名は必須です")
    
    valid_modes = ['normal', 'custom']
    valid_files = ['prompt_template.txt', 'default_you_lines.txt']
    
    if mode not in valid_modes:
        raise ValueError(f"不正なモード名です: {mode}")
    if filename not in valid_files:
        raise ValueError(f"不正なファイル名です: {filename}")
    
    return os.path.join(ROOT_DIR, 'templates', 'prompts', mode, filename)
