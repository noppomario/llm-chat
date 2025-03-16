"""
プロンプトテンプレートのエディタUIを提供するモジュール。
Streamlitベースのインターフェースを実装し、テンプレートの編集機能を提供します。
"""

import streamlit as st
from datetime import datetime
from typing import Optional
from app.prompt_template_manager import PromptTemplateManager, PromptTemplate

class PromptTemplateEditorUI:
    """プロンプトテンプレートのUIコンポーネント"""

    def __init__(self):
        """
        PromptTemplateEditorUIのコンストラクタ。
        セッション状態とテンプレートマネージャーを初期化します。
        """
        self.initialize_session_state()
        self.template_manager = PromptTemplateManager()

    def initialize_session_state(self) -> None:
        """Streamlitのセッション状態を初期化します。"""
        if 'current_template' not in st.session_state:
            st.session_state.current_template = None
        if 'editor_content' not in st.session_state:
            st.session_state.editor_content = ""
        if 'show_preview' not in st.session_state:
            st.session_state.show_preview = False

    def render_template_selector(self) -> None:
        """テンプレート選択コントロールを描画します。"""
        templates = self.template_manager.list_templates()
        if templates:
            col1, col2 = st.columns([3, 1])
            with col1:
                selected_template = st.selectbox(
                    "テンプレートを選択",
                    templates,
                    index=0 if st.session_state.current_template is None else templates.index(st.session_state.current_template)
                )
            with col2:
                st.session_state.show_preview = st.checkbox(
                    "プレビューを表示",
                    value=st.session_state.show_preview
                )

            if selected_template != st.session_state.current_template:
                st.session_state.current_template = selected_template
                template = self.template_manager.get_template(selected_template)
                if template:
                    st.session_state.editor_content = template.content
                st.rerun()
        else:
            st.warning("利用可能なテンプレートがありません。")

    def _render_editor_content(self) -> None:
        """エディタの内容を描画します。"""
        new_content = st.text_area(
            "テンプレート内容",
            value=st.session_state.editor_content,
            height=400,
            key="template_editor"
        )

        if new_content != st.session_state.editor_content:
            st.session_state.editor_content = new_content

        # 操作ボタン
        col1, col2 = st.columns(2)
        with col1:
            if st.button("保存", use_container_width=True):
                if self.save_template(new_content):
                    st.success("テンプレートを保存しました。")
                    st.rerun()
        with col2:
            if st.button("キャンセルして終了", use_container_width=True):
                st.session_state.show_template_editor = False
                st.rerun()

    def render_preview(self) -> None:
        """プレビューパネルを描画します。"""
        st.markdown("### プレビュー")
        content = st.session_state.editor_content

        # プレースホルダーの値を入力するフォーム
        with st.expander("プレースホルダーの設定", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                history = st.text_area(
                    "会話履歴",
                    value="ユーザー: こんにちは\nアシスタント: はい、どうぞ。",
                    height=100
                )
            with col2:
                bot_name = st.text_input("ボット名", value="アシスタント")

        try:
            # プレースホルダーを置換してプレビューを表示
            preview = content.format(
                history=history,
                bot_name=bot_name
            )
            st.markdown("#### プレビュー結果")
            st.code(preview, language="text")
        except (KeyError, ValueError) as e:
            st.error(f"プレビューの生成に失敗しました: {e}")

    def save_template(self, content: str) -> bool:
        """
        テンプレートの内容を保存します。

        Args:
            content (str): 保存するテンプレート内容

        Returns:
            bool: 保存が成功した場合はTrue
        """
        if not self.template_manager.validate_template(content):
            st.error("テンプレートの形式が不正です。")
            return False

        template = self.template_manager.get_template(st.session_state.current_template)
        if not template:
            return False

        try:
            new_template = PromptTemplate(
                name=template.name,
                content=content,
                description=template.description,
                version=template.version,
                mode=template.mode,
                last_modified=datetime.now()
            )
            return self.template_manager.save_template(new_template)
        except Exception as e:
            st.error(f"テンプレートの保存に失敗しました: {e}")
            return False

    def render_editor(self) -> None:
        """メインパネルにエディタを描画します。"""
        if not st.session_state.current_template:
            st.info("テンプレートを選択してください。")
            return

        template = self.template_manager.get_template(st.session_state.current_template)
        if not template:
            st.error("テンプレートの読み込みに失敗しました。")
            return

        # テンプレート情報の表示
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            st.markdown(f"## {template.name}")
        with col2:
            st.markdown(f"**モード**: {template.mode}")
        with col3:
            st.markdown(f"**最終更新**: {template.last_modified.strftime('%Y-%m-%d %H:%M:%S')}")

        # エディタとプレビューの表示
        if st.session_state.show_preview:
            col1, col2 = st.columns(2)
            with col1:
                self._render_editor_content()
            with col2:
                self.render_preview()
        else:
            self._render_editor_content()

    def render(self) -> None:
        """エディタUIのメインレンダリングメソッド"""
        self.render_template_selector()
        self.render_editor()