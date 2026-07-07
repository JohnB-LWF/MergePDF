"""Theme tokens and style injection for the MergePDF Streamlit UI."""

from __future__ import annotations

import streamlit as st

THEME = {
    "background": "#0D0F12",
    "panel": "#111418",
    "accent": "#00E0FF",
    "accent_soft": "#0099B8",
    "text_primary": "#E8E8E8",
    "text_secondary": "#9AA0A6",
    "font": "JetBrains Mono, Fira Code, Hack, monospace",
    "gridline": "rgba(0, 224, 255, 0.08)",
}


def apply_theme() -> None:
    """Inject SOC-style CSS using theme tokens."""
    st.markdown(
        f"""
        <style>
            html, body, [class*="css"], [data-testid="stAppViewContainer"] {{
                font-family: {THEME["font"]};
                background-color: {THEME["background"]};
                color: {THEME["text_primary"]};
            }}

            [data-testid="stHeader"] {{
                background: transparent;
            }}

            [data-testid="stAppViewContainer"] {{
                background-image:
                    linear-gradient(to right, {THEME["gridline"]} 1px, transparent 1px),
                    linear-gradient(to bottom, {THEME["gridline"]} 1px, transparent 1px);
                background-size: 22px 22px;
            }}

            .soc-panel {{
                border: 1px solid {THEME["accent_soft"]};
                background: {THEME["panel"]};
                padding: 1rem;
                margin-bottom: 0.9rem;
            }}

            .soc-header-title {{
                color: {THEME["accent"]};
                font-size: 1.8rem;
                margin: 0;
            }}

            .soc-header-subtitle {{
                color: {THEME["text_secondary"]};
                margin-top: 0.25rem;
                margin-bottom: 0;
            }}

            .soc-console {{
                border: 1px solid {THEME["accent_soft"]};
                background: {THEME["background"]};
                color: {THEME["text_primary"]};
                padding: 0.75rem;
                min-height: 170px;
                white-space: pre-wrap;
                line-height: 1.45;
            }}

            .stButton > button {{
                border-radius: 0;
                border: 1px solid {THEME["accent"]};
                color: {THEME["accent"]};
                background: {THEME["panel"]};
                transition: all 0.18s ease-in-out;
            }}

            .stButton > button:hover {{
                color: {THEME["background"]};
                background: {THEME["accent"]};
                box-shadow: 0 0 14px {THEME["accent"]};
            }}

            .stFileUploader {{
                background: {THEME["panel"]};
                border-radius: 0;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )
