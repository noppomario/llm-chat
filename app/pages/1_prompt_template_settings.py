"""
プロンプトテンプレートの設定を行うページ
"""
import streamlit as st
from app.prompt_template_editor import PromptTemplateEditorUI

# ページ設定
st.set_page_config(
    page_title="プロンプトテンプレート設定",
    page_icon="📝",
    layout="wide",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': "プロンプトテンプレートの編集・管理"
    }
)

# ページタイトルの設定
st.markdown("""
# テンプレート設定
プロンプトテンプレートの編集・管理を行います。
""")

def main():
    """
    テンプレート設定ページのメイン処理
    """
    # テンプレートエディタの初期化と表示
    editor = PromptTemplateEditorUI()
    editor.render()

if __name__ == "__main__":
    main()