import streamlit as st

from components.shell import render_shell
from components.ui import empty_state, error_state, page_header, status_badge
from services.api_client import APIError, api_client
from utils.styles import inject_styles

st.set_page_config(page_title="Approvals | Zorvanta", page_icon="✓", layout="wide")
inject_styles()
client = api_client()
render_shell(client)
page_header("Governance", "Human approvals", "Review sensitive actions before they are permitted in your workspace.")

try:
    approvals = client.approvals()
except APIError as exc:
    error_state(str(exc))
    approvals = []
pending, history = st.tabs(["Pending queue", "Decision history"])
with pending:
    rows = [a for a in approvals if a.get("status") == "pending"]
    if not rows:
        empty_state("Your approval queue is clear.")
    for approval in rows:
        with st.container(border=True):
            st.markdown(f"### {approval.get('question', 'Approval request')}")
            st.caption(f"Requested by {approval.get('requester', 'Unknown')} · {approval.get('created_at', '')}")
            comment = st.text_input("Reviewer comment (optional)", key=f"comment-{approval['id']}")
            approve, reject = st.columns(2)
            if approve.button("Approve request", key=f"approve-{approval['id']}", type="primary"):
                try:
                    client.decide_approval(approval["id"], True, comment)
                    st.success("Approval recorded.")
                    st.rerun()
                except APIError as exc:
                    error_state(str(exc))
            if reject.button("Reject request", key=f"reject-{approval['id']}"):
                try:
                    client.decide_approval(approval["id"], False, comment)
                    st.warning("Request rejected.")
                    st.rerun()
                except APIError as exc:
                    error_state(str(exc))
with history:
    past = [a for a in approvals if a.get("status") != "pending"]
    if not past:
        empty_state("No decisions have been recorded.")
    for approval in past:
        st.markdown(f"{status_badge(approval.get('status', ''))} **{approval.get('question', '')}** · {approval.get('reviewer', 'System')}", unsafe_allow_html=True)
