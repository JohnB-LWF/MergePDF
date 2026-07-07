"""Reusable Streamlit UI components for MergePDF GUI."""

from __future__ import annotations

from typing import Any, Sequence

import streamlit as st

from gui.theme import THEME


def render_header(title: str, subtitle: str) -> None:
    """Render the top header panel."""
    st.markdown(
        f"""
        <div class="soc-panel">
            <h1 class="soc-header-title">{title}</h1>
            <p class="soc-header-subtitle">{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_file_uploader() -> list[Any]:
    """Render and return uploaded PDF files."""
    return st.file_uploader(
        "Drop PDFs here",
        type=["pdf"],
        accept_multiple_files=True,
        help="Drag and drop one or more PDF files in the merge order you want.",
    )


def render_uploaded_file_list(file_names: Sequence[str]) -> None:
    """Render the currently queued file list."""
    if not file_names:
        return

    joined = "\n".join(f"> {index + 1:02d} | {name}" for index, name in enumerate(file_names))
    st.markdown(
        f"""
        <div class="soc-panel">
            <div style="color:{THEME["text_secondary"]};margin-bottom:0.35rem;">QUEUE</div>
            <div class="soc-console">{joined}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_merge_button(disabled: bool) -> bool:
    """Render merge button and return click state."""
    return st.button("Merge PDFs", disabled=disabled, use_container_width=True)


def render_status_console(messages: Sequence[str]) -> None:
    """Render terminal-style status output."""
    text = "\n".join(messages) if messages else "> Awaiting input..."
    st.markdown(
        f"""
        <div class="soc-panel">
            <div style="color:{THEME["text_secondary"]};margin-bottom:0.35rem;">CONSOLE</div>
            <div class="soc-console">{text}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_download_button(data: bytes, file_name: str) -> None:
    """Render output download control."""
    st.download_button(
        label=f"Download {file_name}",
        data=data,
        file_name=file_name,
        mime="application/pdf",
        use_container_width=True,
    )


def render_footer() -> None:
    """Render footer links."""
    st.markdown(
        """
        <div style="color:#9AA0A6;margin-top:0.5rem;">
            github.com/JohnB-LWF/MergePDF
        </div>
        """,
        unsafe_allow_html=True,
    )
