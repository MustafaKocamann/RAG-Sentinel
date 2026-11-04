from __future__ import annotations

import html
from typing import Any

import streamlit as st


def page_header(eyebrow: str, title: str, subtitle: str) -> None:
    st.markdown(f'<div class="eyebrow">{eyebrow}</div><h1>{title}</h1><p class="subtitle">{subtitle}</p>', unsafe_allow_html=True)


def status_badge(status: str) -> str:
    label = {"ready": "Indexed", "indexed": "Indexed", "processing": "Processing", "failed": "Failed", "pending": "Uploaded", "uploaded": "Uploaded", "approved": "Approved", "rejected": "Rejected"}.get(status.lower(), status.title())
    return f'<span class="badge badge-{status.lower()}">{html.escape(label)}</span>'


def error_state(message: str) -> None:
    st.error(message)


def empty_state(message: str) -> None:
    st.info(message)
