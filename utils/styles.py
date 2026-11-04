import streamlit as st


def inject_styles() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@600;700;800&display=swap');
        :root { --navy:#0B2A4A; --teal:#13B8A6; --ink:#14263D; --muted:#6D7B8C; --line:#E4EAF0; --surface:#F6F8FB; }
        html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; color:var(--ink); }
        h1,h2,h3 { font-family:'Manrope', sans-serif; color:var(--navy); letter-spacing:-.02em; }
        .block-container { max-width:1420px; padding:2rem 3rem 4rem; }
        [data-testid="stSidebar"] { background:var(--navy); border-right:0; }
        [data-testid="stSidebar"] * { color:#D7E5F0 !important; }
        [data-testid="stSidebar"] .stRadio label { border-radius:10px; padding:.55rem .7rem; }
        [data-testid="stSidebar"] .stRadio label:hover { background:#173E60; }
        .zorvanta-brand { color:white; font:800 1.35rem Manrope; letter-spacing:-.04em; padding:.4rem 0 2rem; }
        .zorvanta-brand span { color:#33D6C1; }
        .topbar { display:flex; justify-content:space-between; align-items:center; padding-bottom:1.5rem; border-bottom:1px solid var(--line); margin-bottom:2rem; }
        .eyebrow { color:var(--teal); font-weight:700; font-size:.75rem; text-transform:uppercase; letter-spacing:.12em; }
        .subtitle { color:var(--muted); margin-top:-.7rem; }
        .card { background:white; border:1px solid var(--line); border-radius:14px; padding:1.15rem 1.3rem; box-shadow:0 5px 18px rgba(11,42,74,.04); }
        .kpi { min-height:115px; } .kpi-label { color:var(--muted); font-size:.82rem; } .kpi-value { color:var(--navy); font:800 1.8rem Manrope; margin-top:.3rem; }
        .badge { display:inline-block; padding:.25rem .55rem; border-radius:99px; font-size:.72rem; font-weight:700; }
        .badge-ready,.badge-indexed,.badge-approved { color:#087A6E; background:#DDF7F1; } .badge-processing,.badge-pending { color:#946200; background:#FFF2CF; } .badge-failed,.badge-rejected { color:#A3303A; background:#FDE5E6; }
        .chat-window { max-height:520px; overflow-y:auto; padding:.2rem .3rem .6rem; }
        .source { background:var(--surface); border-left:3px solid var(--teal); padding:.65rem .8rem; border-radius:0 8px 8px 0; margin:.4rem 0; font-size:.82rem; }
        .guardrail { background:#FFF5E7; border:1px solid #F3D49C; border-radius:12px; padding:1rem 1.1rem; color:#7B5100; }
        div.stButton > button { border-radius:8px; font-weight:600; border:1px solid var(--line); }
        div.stButton > button[kind="primary"] { background:var(--navy); border-color:var(--navy); }
        </style>
        """,
        unsafe_allow_html=True,
    )
