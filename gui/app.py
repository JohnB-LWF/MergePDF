"""Streamlit app for MergePDF SOC-style GUI."""

from __future__ import annotations

import streamlit as st

from gui.components import (
    render_download_button,
    render_file_uploader,
    render_footer,
    render_header,
    render_merge_button,
    render_status_console,
    render_uploaded_file_list,
)
from gui.controller import merge_uploaded_pdfs
from gui.theme import apply_theme


def main() -> None:
    """Render the MergePDF Streamlit interface."""
    st.set_page_config(page_title="mergePDF()", page_icon=":page_facing_up:", layout="centered")
    apply_theme()

    if "console_messages" not in st.session_state:
        st.session_state.console_messages = ["> Ready."]
    if "output_pdf" not in st.session_state:
        st.session_state.output_pdf = None
    if "output_name" not in st.session_state:
        st.session_state.output_name = None

    render_header("mergePDF()", "Quickly combine multiple PDF documents")
    uploaded_files = render_file_uploader()
    render_uploaded_file_list([upload.name for upload in uploaded_files])

    merge_clicked = render_merge_button(disabled=len(uploaded_files) == 0)
    if merge_clicked:
        result = merge_uploaded_pdfs(uploaded_files=uploaded_files)
        st.session_state.console_messages = result.messages

        if result.success:
            st.session_state.output_pdf = result.output_bytes
            st.session_state.output_name = result.output_name
        else:
            st.session_state.output_pdf = None
            st.session_state.output_name = None

    render_status_console(st.session_state.console_messages)

    if st.session_state.output_pdf and st.session_state.output_name:
        render_download_button(
            data=st.session_state.output_pdf,
            file_name=st.session_state.output_name,
        )

    render_footer()


if __name__ == "__main__":
    main()
