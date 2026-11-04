"""Zorvanta enterprise knowledge copilot."""

import streamlit as st

from components.shell import render_shell
from services.api_client import APIError, api_client
from utils.styles import inject_styles

st.set_page_config(
    page_title="Zorvanta | Knowledge Copilot",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_styles()
client = api_client()
render_shell(client)

st.markdown('<div class="topbar"><div><div class="eyebrow">Workspace intelligence</div><h1>Knowledge copilot</h1><p class="subtitle">Ask grounded questions across your governed enterprise knowledge.</p></div><div class="badge badge-indexed">● Systems operational</div></div>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []
if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = None

if not st.session_state.messages:
    st.markdown('<div class="card"><h3>Good afternoon. What would you like to find?</h3><p class="subtitle">Zorvanta answers from approved workspace sources and shows its evidence.</p></div>', unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="chat-window">', unsafe_allow_html=True)
    for index, message in enumerate(st.session_state.messages):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message["role"] == "assistant":
                if message.get("status") in {"guardrail_blocked", "pending_approval"}:
                    st.markdown(f'<div class="guardrail"><strong>{message.get("banner_title", "Action requires attention")}</strong><br>{message["content"]}</div>', unsafe_allow_html=True)
                sources = message.get("sources", [])
                if sources:
                    with st.expander(f"Sources · {len(sources)} evidence items"):
                        for source in sources:
                            st.markdown(f'<div class="source"><strong>{source.get("title", "Source")}</strong> · Page {source.get("page", "—")}<br>{source.get("snippet", "")}</div>', unsafe_allow_html=True)
                feedback = st.columns([.08, .08, .84])
                if feedback[0].button("👍", key=f"up-{index}", help="Helpful answer"):
                    st.toast("Thanks — feedback recorded.")
                if feedback[1].button("👎", key=f"down-{index}", help="Not helpful"):
                    st.toast("Thanks — feedback recorded.")
    st.markdown("</div>", unsafe_allow_html=True)

question = st.chat_input("Ask about policies, procedures, or workspace knowledge…")
if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)
    with st.chat_message("assistant"):
        with st.spinner("Searching governed knowledge…"):
            try:
                result = client.chat(question, st.session_state.conversation_id)
                st.session_state.conversation_id = result.get("conversation_id", st.session_state.conversation_id)
                status = result.get("status", "complete")
                banner = "Request routed to human approval" if status == "pending_approval" else "Request blocked by a safety guardrail"
                answer = result.get("answer", "No answer was returned.")
                st.session_state.messages.append({"role": "assistant", "content": answer, "sources": result.get("sources", []), "status": status, "banner_title": banner})
                st.rerun()
            except APIError as exc:
                st.error(str(exc))
