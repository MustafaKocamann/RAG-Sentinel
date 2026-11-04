import streamlit as st


def inject_styles() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@600;700;800&display=swap');
        :root { --navy:#0A2540; --navy-2:#123D61; --teal:#00A99D; --teal-soft:#DDF5F1; --ink:#162A3D; --muted:#647487; --line:#DCE5ED; --surface:#F4F7FA; }
        html, body, [class*="css"] { font-family:'DM Sans', sans-serif; color:var(--ink); }
        h1,h2,h3 { font-family:'Manrope', sans-serif; color:var(--navy); letter-spacing:-.025em; font-weight:800; }
        h1 { font-size:2.35rem; line-height:1.15; } h2 { font-size:1.55rem; } h3 { font-size:1.05rem; }
        .block-container { max-width:1420px; padding:2.5rem 3.25rem 4rem; }
        [data-testid="stSidebar"] { background:linear-gradient(180deg,var(--navy) 0%, #071B30 100%); border-right:0; }
        [data-testid="stSidebarNav"] { display:none; }
        [data-testid="stSidebar"] * { color:#F4F8FB !important; }
        [data-testid="stSidebar"] .stRadio label { border-radius:10px; padding:.55rem .7rem; }
        [data-testid="stSidebar"] .stRadio label:hover { background:#173E60; }
        .zorvanta-brand { color:#FFFFFF; font:800 1.45rem Manrope; letter-spacing:-.045em; padding:.4rem 0 1.1rem; }
        .zorvanta-brand span { color:#3AD3C5; }
        .sidebar-kicker { color:#9CC1D8; font-size:.65rem; font-weight:800; letter-spacing:.13em; }
        .context-panel { background:rgba(255,255,255,.09); border:1px solid rgba(147,204,220,.28); border-left:3px solid #3AD3C5; border-radius:9px; padding:.8rem .85rem .75rem; margin:.25rem 0 .45rem; }
        .context-panel .context-title { color:#FFFFFF; font:700 .88rem Manrope; }
        .context-panel .context-copy { color:#B8D0DE; font-size:.72rem; margin-top:.22rem; }
        [data-testid="stSidebar"] [data-testid="stSelectbox"] { margin:.15rem 0 .7rem; }
        [data-testid="stSidebar"] [data-testid="stSelectbox"] label { color:#C9E1EC !important; font-size:.68rem; font-weight:800; text-transform:uppercase; letter-spacing:.1em; }
        [data-testid="stSidebar"] [data-testid="stSelectbox"] [data-baseweb="select"] > div { background:#173E60; border:2px solid #4ED8C8; border-radius:8px; min-height:2.7rem; box-shadow:0 0 0 2px rgba(78,216,200,.12), 0 4px 12px rgba(0,0,0,.24); }
        [data-testid="stSidebar"] [data-testid="stSelectbox"] [data-baseweb="select"] > div:hover { background:#1D527A; border-color:#7AF2E2; }
        [data-testid="stSidebar"] [data-testid="stSelectbox"] [data-baseweb="select"] > div:focus-within { background:#1D527A; border-color:#FFFFFF; box-shadow:0 0 0 3px rgba(78,216,200,.35); }
        [data-testid="stSidebar"] [data-testid="stSelectbox"] [data-baseweb="select"] * { color:#FFFFFF !important; font-weight:800; }
        [data-testid="stSidebar"] [data-testid="stSelectbox"] [data-baseweb="select"] svg { fill:#7AF2E2 !important; color:#7AF2E2 !important; }
        [data-testid="stSidebar"] [data-testid="stSelectbox"] label { color:#FFFFFF !important; font-size:.7rem; font-weight:800; text-transform:uppercase; letter-spacing:.11em; }
        .access-status { display:flex; align-items:center; gap:.45rem; background:#0F806F; border:1px solid #4ED8C8; border-radius:7px; padding:.52rem .7rem; color:#FFFFFF !important; font-size:.74rem; margin:.1rem 0 .35rem; }
        .access-status strong { color:#FFFFFF !important; }
        .access-dot { width:7px; height:7px; background:#4EE5D2; border-radius:50%; box-shadow:0 0 0 3px rgba(78,229,210,.16); }
        .topbar { display:flex; justify-content:space-between; align-items:flex-start; padding-bottom:1.75rem; border-bottom:1px solid var(--line); margin-bottom:2rem; }
        .eyebrow { color:var(--teal); font-weight:800; font-size:.68rem; text-transform:uppercase; letter-spacing:.14em; }
        .subtitle { color:var(--muted); margin-top:-.65rem; font-size:.95rem; }
        .card { background:white; border:1px solid var(--line); border-radius:12px; padding:1.35rem 1.45rem; box-shadow:0 8px 24px rgba(10,37,64,.055); }
        .kpi { min-height:115px; } .kpi-label { color:var(--muted); font-size:.82rem; } .kpi-value { color:var(--navy); font:800 1.8rem Manrope; margin-top:.3rem; }
        .badge { display:inline-block; padding:.25rem .55rem; border-radius:99px; font-size:.72rem; font-weight:700; }
        .badge-ready,.badge-indexed,.badge-approved { color:#087A6E; background:var(--teal-soft); } .badge-processing,.badge-pending { color:#8A5A00; background:#FFF1CF; } .badge-failed,.badge-rejected { color:#A3303A; background:#FDE5E6; }
        .chat-window { max-height:520px; overflow-y:auto; padding:.2rem .3rem .6rem; }
        .source { background:var(--surface); border-left:3px solid var(--teal); padding:.65rem .8rem; border-radius:0 8px 8px 0; margin:.4rem 0; font-size:.82rem; }
        .guardrail { background:#FFF5E7; border:1px solid #F3D49C; border-radius:12px; padding:1rem 1.1rem; color:#7B5100; }
        div.stButton > button { border-radius:7px; font-weight:700; border:1px solid var(--line); min-height:2.45rem; }
        div.stButton > button[kind="primary"] { background:var(--navy); border-color:var(--navy); color:white; }
        div.stButton > button[kind="primary"]:hover { background:var(--navy-2); border-color:var(--navy-2); }
        [data-testid="stSidebar"] .stCaption { color:#AFC9D8 !important; }
        @media (max-width: 800px) { .block-container { padding:1.5rem 1rem 3rem; } .topbar { display:block; } }
        </style>
        """,
        unsafe_allow_html=True,
    )
