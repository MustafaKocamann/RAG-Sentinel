from __future__ import annotations

import os
import streamlit as st

from services.api_client import APIClient


def render_shell(client: APIClient) -> None:
    with st.sidebar:
        st.markdown('<div class="zorvanta-brand">zor<span>vanta</span></div>', unsafe_allow_html=True)
        st.caption("ENTERPRISE KNOWLEDGE COPILOT")
        st.divider()
        role = st.selectbox("Workspace", ["Northstar Workspace", "Acme Operations"])
        st.session_state["workspace"] = role
        st.session_state["role"] = st.selectbox("Access level", ["Employee", "Admin"], index=1)
        st.divider()
        st.page_link("app.py", label="Chat", icon="◈")
        st.page_link("pages/1_Upload_Documents.py", label="Upload documents", icon="⇧")
        st.page_link("pages/2_Documents.py", label="Documents", icon="▤")
        if st.session_state["role"] == "Admin":
            st.page_link("pages/3_Approvals.py", label="Approvals", icon="✓")
            st.page_link("pages/4_Metrics_Logs.py", label="Metrics & logs", icon="◌")
        st.divider()
        st.caption(f"API · {'MOCK' if client.mock else 'CONNECTED'}")
        st.caption(os.getenv("API_BASE_URL", "http://localhost:8000"))
