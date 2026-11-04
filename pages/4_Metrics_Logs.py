import pandas as pd
import plotly.express as px
import streamlit as st

from components.shell import render_shell
from components.ui import error_state, page_header
from services.api_client import APIError, api_client
from utils.styles import inject_styles

st.set_page_config(page_title="Metrics & logs | Zorvanta", page_icon="◌", layout="wide")
inject_styles()
client = api_client()
render_shell(client)
page_header("Administration", "Metrics & logs", "Operational health, usage signals, and audit evidence for your tenant.")
try:
    metrics = client.metrics()
except APIError as exc:
    error_state(str(exc))
    metrics = {}

cards = [
    ("Total queries", f"{metrics.get('total_queries', 0):,}", "Last 30 days"),
    ("Avg latency", f"{metrics.get('avg_latency_ms', 0):,} ms", "P95 request time"),
    ("Error rate", f"{metrics.get('error_rate', 0):.1f}%", "Target < 2.0%"),
    ("Token usage", f"{metrics.get('token_usage', 0):,}", "Input + output"),
    ("Blocked requests", f"{metrics.get('blocked_requests', 0):,}", "Guardrail events"),
]
cols = st.columns(5)
for col, (label, value, note) in zip(cols, cards):
    col.markdown(f'<div class="card kpi"><div class="kpi-label">{label}</div><div class="kpi-value">{value}</div><small style="color:#6D7B8C">{note}</small></div>', unsafe_allow_html=True)

st.subheader("Usage trend")
trend = pd.DataFrame({"Day": pd.date_range("2026-10-29", periods=7), "Queries": [122, 161, 148, 204, 189, 221, 239], "Latency": [720, 810, 760, 920, 845, 800, 842]})
st.plotly_chart(px.area(trend, x="Day", y="Queries", color_discrete_sequence=["#13B8A6"]), use_container_width=True, config={"displayModeBar": False})
st.subheader("Audit events")
st.dataframe(pd.DataFrame([
    {"Timestamp": "2026-11-04 10:12", "Event": "approval_requested", "Actor": "ayse.demir", "Resource": "apr-1024"},
    {"Timestamp": "2026-11-04 09:48", "Event": "query_completed", "Actor": "mehmet.kaya", "Resource": "conversation-55"},
    {"Timestamp": "2026-11-03 17:20", "Event": "guardrail_blocked", "Actor": "system", "Resource": "conversation-52"},
]), use_container_width=True, hide_index=True)
st.link_button("Open Rius observability dashboard", "https://rius.observability.example.com", type="secondary")
