import streamlit as st

from components.shell import render_shell
from components.ui import empty_state, error_state, page_header, status_badge
from services.api_client import APIError, api_client
from utils.styles import inject_styles

st.set_page_config(page_title="Documents | Zorvanta", layout="wide")
inject_styles()
client = api_client()
render_shell(client)
page_header("Knowledge operations", "Documents", "Review indexed sources, processing state, and workspace coverage.")

if st.button("Refresh documents"):
    st.cache_data.clear()
try:
    documents = client.documents()
except APIError as exc:
    error_state(str(exc))
    documents = []

left, right = st.columns([3, 1])
with left:
    query = st.text_input("Search documents", placeholder="Search by filename or title…", label_visibility="collapsed")
with right:
    filter_status = st.selectbox("Status", ["All", "Uploaded", "Processing", "Indexed", "Failed"], label_visibility="collapsed")

status_map = {"Uploaded": {"uploaded", "pending"}, "Processing": {"processing"}, "Indexed": {"ready", "indexed"}, "Failed": {"failed"}}
filtered = [d for d in documents if query.lower() in d.get("title", "").lower() and (filter_status == "All" or d.get("status") in status_map.get(filter_status, set()))]
if not filtered:
    empty_state("No documents match the current filters.")
else:
    for doc in filtered:
        col1, col2, col3, col4 = st.columns([4, 1.2, 1, .8])
        col1.markdown(f"**{doc.get('title', 'Untitled')}**<br><small>{doc.get('id', '')} · v{doc.get('current_version', 1)}</small>", unsafe_allow_html=True)
        col2.markdown(status_badge(doc.get("status", "unknown")), unsafe_allow_html=True)
        col3.caption(str(doc.get("created_at", ""))[:10])
        col4.button("•••", key=f"doc-{doc.get('id')}", help="Document actions")
        st.divider()
