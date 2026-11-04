from __future__ import annotations

import os
import streamlit as st

from services.api_client import APIClient


def render_shell(client: APIClient) -> None:
    with st.sidebar:
        st.markdown('<div class="zorvanta-brand">zor<span>vanta</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-kicker">ENTERPRISE KNOWLEDGE COPILOT</div>', unsafe_allow_html=True)
        st.divider()
        st.markdown(
            '<div class="context-panel"><div class="context-title">Workspace context</div>'
            '<div class="context-copy">Active tenant and permission scope</div></div>',
            unsafe_allow_html=True,
        )
        role = st.selectbox("Workspace", ["Northstar Workspace", "Acme Operations"], key="workspace_selector")
        st.session_state["workspace"] = role
        st.session_state["role"] = st.selectbox(
            "Access level", ["Employee", "Admin"], index=1, key="access_level_selector"
        )
        st.markdown(
            f'<div class="access-status"><span class="access-dot"></span>'
            f'<span><strong>{st.session_state["role"]}</strong> access active</span></div>',
            unsafe_allow_html=True,
        )
        st.divider()
        st.page_link("app.py", label="Knowledge copilot")
        st.page_link("pages/1_Upload_Documents.py", label="Upload documents")
        st.page_link("pages/2_Documents.py", label="Document library")
        if st.session_state["role"] == "Admin":
            st.page_link("pages/3_Approvals.py", label="Approval center")
            st.page_link("pages/4_Metrics_Logs.py", label="Metrics & logs")
        st.divider()
        st.caption(f"API · {'MOCK' if client.mock else 'CONNECTED'}")
        st.caption(os.getenv("API_BASE_URL", "http://localhost:8000"))
