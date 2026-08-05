`python
# app.py
# app.py
import streamlit as st
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))

st.set_page_config(
    page_title="AI Terrorism Intelligence Dashboard",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

if "theme_accent" not in st.session_state:
    st.session_state.theme_accent = "#7c3aed"
    st.session_state.theme_accent_light = "#a78bfa"
    st.session_state.theme_gradient_end = "#3b82f6"

with open(Path(__file__).parent / "assets" / "style.css") as f:
    st.markdown(f.read(), unsafe_allow_html=True)

accent = st.session_state.theme_accent
accent_light = st.session_state.theme_accent_light
gradient_end = st.session_state.theme_gradient_end

def get_rgb_channels(hex_str):
    h = hex_str.lstrip('#')
    return f"{int(h[0:2], 16)}, {int(h[2:4], 16)}, {int(h[4:6], 16)}"

rgb_channels = get_rgb_channels(accent)

dynamic_css = f"""
<style>
    .stButton > button,
    .stProgress > div > div,
    button[kind="primary"] {{
        background: linear-gradient(135deg, {accent}, {gradient_end}) !important;
        box-shadow: 0 4px 15px rgba({rgb_channels}, 0.2) !important;
        transform: translateY(0);
        transition: transform 0.2s ease, box-shadow 0.2s ease !important;
    }}
    .stButton > button:hover,
    button[kind="primary"]:hover {{
        box-shadow: 0 8px 25px rgba({rgb_channels}, 0.5) !important;
        transform: translateY(-2px);
    }}
    div[data-testid="stMetric"]:hover,
    div[data-testid="stExpander"]:hover,
    .custom-card:hover {{
        border-color: rgba({rgb_channels}, 0.6) !important;
        box-shadow: 0 12px 40px rgba({rgb_channels}, 0.25) !important;
        transform: translateY(-4px);
    }}
    .gradient-text {{
        background: linear-gradient(135deg, {accent_light}, {gradient_end}) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
    }}
    .confidence-meter-fill {{
        background: linear-gradient(90deg, {accent}, {accent_light}) !important;
    }}
    div[data-testid="stSlider"] div[role="slider"] {{
        background: {accent} !important;
        box-shadow: 0 0 12px rgba({rgb_channels}, 0.6) !important;
    }}
    div[data-testid="stSlider"] div[data-baseweb="slider"] {{
        background: rgba({rgb_channels}, 0.25) !important;
    }}
    div[data-testid="stMultiSelect"] > div > div:hover,
    div[data-testid="stSelectbox"] > div > div:hover,
    div[data-testid="stTextInput"] input:focus,
    div[data-testid="stNumberInput"] input:focus {{
        border-color: {accent} !important;
        box-shadow: 0 0 0 2px rgba({rgb_channels}, 0.2) !important;
    }}
    section[data-testid="stSidebar"] .stButton > button[kind="primary"] {{
        border: none !important;
        background: #1A253C !important;
        box-shadow: none !important;
    }}
    section[data-testid="stSidebar"] .stButton > button[kind="secondary"]:hover {{
        background: rgba({rgb_channels}, 0.15) !important;
        border-color: rgba({rgb_channels}, 0.3) !important;
    }}
</style>
"""
st.markdown(dynamic_css, unsafe_allow_html=True)

from utils.data_loader import get_db_connection
from utils.helper import get_year_range

@st.cache_resource
def init_session_data():
    return get_db_connection()

conn = init_session_data()

if "data_loaded" not in st.session_state:
    st.session_state.data_loaded = conn is not None
    st.session_state.conn = conn

PAGES_MAIN = {
    "🏠 Dashboard": "Home",
    "🌍 Threat Map": "Global_Threat_Map",
    "💀 Country Analysis": "Country_Analysis",
    "📈 Attack Prediction": "Attack_Prediction",
    "📋 Forecasting": "Forecasting",
    "⚡ Intelligence Report": "AI_Report",
    "🗃️ Data Explorer": "Data_Explorer",
}

PAGES_SYSTEM = {
    "ℹ️ About": "About",
}

def navigate_to(page_name):
    st.session_state.current_page = page_name
    st.rerun()

if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"

with st.sidebar:
    st.markdown(
        """
        <div style="display: flex; align-items: center; gap: 0.8rem; padding: 1rem 0.5rem; margin-bottom: 0.5rem;">
            <div style="font-size: 2rem; background: linear-gradient(135deg, #1e3a8a, #3b82f6); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">🛡️</div>
            <div>
                <div style="font-family: 'Outfit', sans-serif; font-size: 1.1rem; font-weight: 800; color: #e2e8f0; line-height: 1.2;">
                    AI TERRORISM<br>
                    <span style="font-size: 0.7rem; font-weight: 600; color: #64748b;">INTELLIGENCE</span>
                </div>
            </div>
        </div>
        <div style="font-size: 0.65rem; color: #64748b; font-weight: 700; letter-spacing: 0.05em; padding-left: 0.5rem; margin-bottom: 1.5rem;">
            TERRORISM ANALYSIS PLATFORM
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <style>
        section[data-testid="stSidebar"] > div:first-child {
            padding-top: 0 !important;
        }
        .st-emotion-cache-1d391kg {
            padding-top: 0 !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    for label, page_file in PAGES_MAIN.items():
        is_active = (st.session_state.current_page == page_file)
        if st.button(
            label,
            key=f"nav_{page_file}",
            use_container_width=True,
            type="primary" if is_active else "secondary",
        ):
            navigate_to(page_file)

    st.markdown(
        """
        <div style="font-size: 0.65rem; color: #64748b; font-weight: 700; letter-spacing: 0.1em; padding-left: 0.5rem; margin: 1.5rem 0 0.5rem 0;">
            SYSTEM
        </div>
        """,
        unsafe_allow_html=True,
    )

    for label, page_file in PAGES_SYSTEM.items():
        is_active = (st.session_state.current_page == page_file)
        if st.button(
            label,
            key=f"nav_{page_file}",
            use_container_width=True,
            type="primary" if is_active else "secondary",
        ):
            navigate_to(page_file)

    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style="background: rgba(15, 23, 42, 0.4); border: 1px solid rgba(255, 255, 255, 0.05); border-radius: 12px; padding: 1rem; margin: 0.5rem;">
            <div style="font-size: 0.75rem; color: #cbd5e1; font-weight: 700; margin-bottom: 0.2rem;">
                Data Source <span style="color: #10b981; font-size: 0.6rem;">🟢</span>
            </div>
            <div style="font-size: 0.7rem; color: #94a3b8; margin-bottom: 1rem; line-height: 1.4;">
                Global Terrorism Database (GTD)
            </div>
            <div style="font-size: 0.7rem; color: #cbd5e1; font-weight: 700; margin-bottom: 0.2rem;">
                Last Updated
            </div>
            <div style="font-size: 0.7rem; color: #94a3b8;">
                May 21, 2025 10:30 AM
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

@st.dialog("Dataset Status")
def show_welcome_dialog():
    st.markdown(
        '''
        <div style="text-align: center;">
            <h3 style="margin-bottom: 0.5rem;">✅ Dataset is already loaded</h3>
            <p style="color: #94a3b8; font-size: 1rem;">
                <b>Source of Dataset:</b> https://www.kaggle.com/datasets/START-UMD/gtd
            </p>
        </div>
        ''', unsafe_allow_html=True
    )
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Okay", use_container_width=True, type="primary"):
            st.session_state.welcome_dialog_shown = True
            st.rerun()

if "welcome_dialog_shown" not in st.session_state:
    st.session_state.welcome_dialog_shown = False

def main():
    if not st.session_state.welcome_dialog_shown:
        show_welcome_dialog()
        
    page = st.session_state.current_page
    if page == "Home":
        from pages.Home import show
        show(conn)
    elif page == "Global_Threat_Map":
        from pages.Global_Threat_Map import show
        show(conn)
    elif page == "Country_Analysis":
        from pages.Country_Analysis import show
        show(conn)
    elif page == "Attack_Prediction":
        from pages.Attack_Prediction import show
        show(conn)
    elif page == "Forecasting":
        from pages.Forecasting import show
        show(conn)
    elif page == "AI_Report":
        from pages.AI_Report import show
        show(conn)
    elif page == "Data_Explorer":
        from pages.Data_Explorer import show
        show(conn)
    elif page == "About":
        from pages.About import show
        show()

if __name__ == "__main__":
    main()

`

`css
# assets/style.css
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Outfit:wght@400;500;600;700;800;900&display=swap');

:root {
    --bg: #080b10;
    --panel: #111722;
    --panel-2: #151d2a;
    --line: rgba(148, 163, 184, 0.18);
    --text: #e5edf6;
    --muted: #93a4b8;
    --blue: #38bdf8;
    --green: #34d399;
    --amber: #fbbf24;
    --red: #fb7185;
    --violet: #a78bfa;
    --cyan: #22d3ee;
}

* {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    letter-spacing: 0;
}

.stApp,
.main > div,
[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(circle at 12% 0%, rgba(56, 189, 248, 0.13), transparent 28rem),
        radial-gradient(circle at 88% 10%, rgba(52, 211, 153, 0.09), transparent 24rem),
        linear-gradient(180deg, #080b10 0%, #0b1118 52%, #080b10 100%);
}

.block-container {
    padding-top: 1.4rem !important;
    padding-bottom: 2.4rem !important;
    max-width: 1500px !important;
}

h1, h2, h3, h4, h5, h6 {
    font-family: 'Outfit', sans-serif !important;
    color: var(--text) !important;
    font-weight: 700 !important;
}

p, span, div, li, label {
    color: var(--muted);
}

section[data-testid="stSidebar"] {
    background: rgba(7, 10, 16, 0.96) !important;
    border-right: 1px solid var(--line) !important;
}

section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
section[data-testid="stSidebar"] div {
    color: var(--muted) !important;
}

[data-testid="stSidebarNav"] {
    display: none !important;
}

.brand-mark {
    width: 3rem;
    height: 3rem;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    border-radius: 14px;
    color: #061017 !important;
    font-weight: 800;
    background: linear-gradient(135deg, var(--blue), var(--green));
    box-shadow: 0 16px 34px rgba(56, 189, 248, 0.16);
    margin-bottom: 0.55rem;
}

.sidebar-title {
    font-family: 'Outfit', sans-serif !important;
    font-size: 1.15rem !important;
    font-weight: 800 !important;
    color: var(--text) !important;
    line-height: 1.25 !important;
}

.stButton > button {
    width: 100%;
    min-height: 2.55rem;
    background: transparent !important;
    color: #cbd5e1 !important;
    border: 1px solid transparent !important;
    border-radius: 8px !important;
    padding: 0.55rem 0.85rem !important;
    font-weight: 650 !important;
    text-align: left !important;
    transition: background 160ms ease, border-color 160ms ease, color 160ms ease, transform 160ms ease !important;
}

.stButton > button:hover {
    transform: translateX(2px) !important;
    color: var(--text) !important;
    background: rgba(56, 189, 248, 0.08) !important;
    border-color: rgba(56, 189, 248, 0.22) !important;
}

.home-hero {
    position: relative;
    overflow: hidden;
    padding: clamp(2rem, 4vw, 4.2rem);
    border: 1px solid rgba(148, 163, 184, 0.18);
    border-radius: 8px;
    background:
        linear-gradient(135deg, rgba(17, 24, 39, 0.96), rgba(15, 23, 42, 0.78)),
        repeating-linear-gradient(90deg, rgba(148, 163, 184, 0.06) 0 1px, transparent 1px 72px),
        repeating-linear-gradient(0deg, rgba(148, 163, 184, 0.05) 0 1px, transparent 1px 72px);
    box-shadow: 0 26px 60px rgba(0, 0, 0, 0.28);
    margin-bottom: 1.4rem;
}

.home-hero::after {
    content: "";
    position: absolute;
    inset: auto -15% -55% 35%;
    height: 15rem;
    background: linear-gradient(90deg, rgba(56, 189, 248, 0.18), rgba(52, 211, 153, 0.14), rgba(251, 191, 36, 0.08));
    transform: rotate(-7deg);
    pointer-events: none;
}

.hero-kicker,
.section-label {
    color: var(--green) !important;
    font-size: 0.76rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

.home-hero h1 {
    font-family: 'Outfit', sans-serif !important;
    color: #f8fafc !important;
    font-size: clamp(2.5rem, 4.5vw, 5rem);
    font-weight: 800 !important;
    line-height: 1.02;
    margin: 0.55rem 0 0.9rem;
    max-width: 980px;
}

.home-hero p {
    color: #b6c4d6 !important;
    font-size: 1.08rem;
    line-height: 1.65;
    max-width: 760px;
    margin: 0;
}

.hero-meta {
    display: flex;
    flex-wrap: wrap;
    gap: 0.65rem;
    margin-top: 1.6rem;
    max-width: 1020px;
}

.hero-meta span {
    color: #d7e1ec !important;
    background: rgba(8, 13, 20, 0.72);
    border: 1px solid rgba(148, 163, 184, 0.16);
    border-radius: 999px;
    padding: 0.42rem 0.7rem;
    font-size: 0.82rem;
    font-weight: 650;
}

.section-label {
    margin: 1.6rem 0 0.8rem;
}

.stat-card,
div[data-testid="stPlotlyChart"],
div[data-testid="stDataFrame"],
div[data-testid="stExpander"],
div[data-testid="stMetric"],
.custom-card,
.glass-card,
.report-container {
    background: rgba(17, 24, 34, 0.55) !important;
    backdrop-filter: blur(16px) !important;
    -webkit-backdrop-filter: blur(16px) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 16px !important;
    box-shadow: 0 16px 40px rgba(0, 0, 0, 0.25) !important;
}

.stat-card {
    min-height: 8.8rem;
    padding: 1rem !important;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    transition: transform 180ms ease, border-color 180ms ease, box-shadow 180ms ease;
}

.stat-card:hover,
div[data-testid="stPlotlyChart"]:hover,
.custom-card:hover {
    transform: translateY(-4px);
    border-color: rgba(255, 255, 255, 0.15) !important;
    box-shadow: 0 22px 50px rgba(0, 0, 0, 0.4) !important;
}

.stat-icon {
    align-self: flex-start;
    border-radius: 6px;
    padding: 0.24rem 0.42rem;
    font-size: 0.72rem !important;
    font-weight: 850;
    color: #071017 !important;
}

.stat-value {
    font-family: 'Outfit', sans-serif !important;
    color: #f8fafc !important;
    font-size: clamp(1.5rem, 2vw, 2.2rem) !important;
    line-height: 1.08 !important;
    font-weight: 800 !important;
    margin-top: 0.6rem;
    white-space: nowrap;
}

.stat-label {
    color: #93a4b8 !important;
    font-size: 0.73rem !important;
    text-transform: uppercase;
    font-weight: 750 !important;
    margin-top: 0.35rem;
}

.metric-blue .stat-icon { background: var(--blue); }
.metric-green .stat-icon { background: var(--green); }
.metric-red .stat-icon { background: var(--red); }
.metric-amber .stat-icon { background: var(--amber); }
.metric-violet .stat-icon { background: var(--violet); }
.metric-cyan .stat-icon { background: var(--cyan); }

div[data-testid="stPlotlyChart"] {
    padding: 0.7rem !important;
    margin-bottom: 1rem;
    overflow: hidden;
}

.js-plotly-plot .plotly .modebar {
    background: rgba(8, 11, 16, 0.82) !important;
    border-radius: 6px !important;
}

div[data-testid="stSelectbox"] > div > div,
div[data-testid="stMultiSelect"] > div > div,
div[data-testid="stTextInput"] input,
div[data-testid="stNumberInput"] input,
div[data-testid="stDateInput"] input {
    background: rgba(13, 18, 27, 0.98) !important;
    border: 1px solid rgba(148, 163, 184, 0.22) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
}

div[data-testid="stSelectbox"] > div > div:hover,
div[data-testid="stMultiSelect"] > div > div:hover,
div[data-testid="stTextInput"] input:focus,
div[data-testid="stNumberInput"] input:focus,
div[data-testid="stDateInput"] input:focus {
    border-color: rgba(56, 189, 248, 0.55) !important;
    box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.1) !important;
}

.stTabs [data-baseweb="tab-list"] {
    background: rgba(13, 18, 27, 0.96) !important;
    border-radius: 8px !important;
    padding: 0.25rem !important;
    border: 1px solid var(--line) !important;
}

.stTabs [data-baseweb="tab"] {
    color: #aebdd0 !important;
    border-radius: 6px !important;
    font-weight: 650 !important;
}

.stTabs [aria-selected="true"] {
    background: rgba(56, 189, 248, 0.12) !important;
    color: var(--text) !important;
}

.stAlert {
    background: rgba(17, 24, 34, 0.98) !important;
    border: 1px solid rgba(251, 191, 36, 0.24) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
}

.stProgress > div > div {
    background: linear-gradient(90deg, var(--blue), var(--green)) !important;
    border-radius: 999px !important;
}

.threat-badge {
    display: inline-block !important;
    padding: 0.25rem 0.75rem !important;
    border-radius: 999px !important;
    font-size: 0.75rem !important;
    font-weight: 800 !important;
    text-transform: uppercase !important;
}

.gradient-text {
    color: #f8fafc !important;
}

.data-source {
    text-align: center;
    padding: 1.5rem 0 0;
    font-size: 0.76rem;
    color: #65758a !important;
}

hr {
    border-color: rgba(148, 163, 184, 0.14) !important;
}

footer {
    display: none !important;
}

@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(14px); }
    to { opacity: 1; transform: translateY(0); }
}

.animate-in {
    animation: fadeInUp 0.48s ease forwards;
}

.delay-1 { animation-delay: 0.04s; }
.delay-2 { animation-delay: 0.08s; }
.delay-3 { animation-delay: 0.12s; }
.delay-4 { animation-delay: 0.16s; }
.delay-5 { animation-delay: 0.20s; }
.delay-6 { animation-delay: 0.24s; }


.sidebar-section-label {
    color: var(--green) !important;
    font-size: 0.7rem;
    font-weight: 850;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 0.65rem;
}

.dataset-status {
    background: rgba(13, 18, 27, 0.92);
    border: 1px solid rgba(56, 189, 248, 0.2);
    border-radius: 8px;
    padding: 0.75rem;
    margin-top: 0.8rem;
}

.dataset-status-label {
    color: #7dd3fc !important;
    font-size: 0.68rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

.dataset-status-name {
    color: var(--text) !important;
    font-size: 0.82rem;
    font-weight: 700;
    margin-top: 0.25rem;
    overflow-wrap: anywhere;
}

div[data-testid="stFileUploader"] {
    background: rgba(13, 18, 27, 0.78) !important;
    border: 1px dashed rgba(56, 189, 248, 0.26) !important;
    border-radius: 8px !important;
    padding: 0.75rem !important;
}

div[data-testid="stFileUploader"] section {
    background: transparent !important;
    border: 0 !important;
    padding: 0 !important;
}

div[data-testid="stFileUploader"] button {
    border-radius: 8px !important;
}

div[data-testid="stRadio"] label,
div[data-testid="stRadio"] p {
    color: #cbd5e1 !important;
}

@media (max-width: 900px) {
    .block-container {
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }

    .home-hero {
        padding: 1.4rem;
    }

    .hero-meta span {
        width: 100%;
    }

    .stat-card {
        min-height: 7.8rem;
    }
}
</style>

`

`python
# pages/AI_Report.py
# pages/AI_Report.py
import streamlit as st
import pandas as pd
from utils.helper import format_number, get_threat_level
from utils.data_loader import get_summary_stats

def show(conn):
    if conn is None: return

    st.markdown('''<div class="glass-card" style="text-align: center; padding: 2rem; margin-bottom: 2rem;"><h1 style="font-size: 2.2rem; margin-bottom: 0.3rem;"><span class="gradient-text">🧠 Intelligence Report</span></h1><p style="color: #94a3b8; max-width: 600px; margin: 0 auto;">Automatically generated strategic intelligence report based on Global Terrorism Database analysis.</p></div>''', unsafe_allow_html=True)

    with st.spinner("Generating intelligence report..."):
        stats = get_summary_stats(conn)
        yearly = conn.execute("SELECT year, COUNT(*) as count FROM gtd GROUP BY year ORDER BY year").df()
        from sklearn.linear_model import LinearRegression
        X = yearly[["year"]].values
        y = yearly["count"].values
        model = LinearRegression().fit(X, y)
        trend_direction = model.coef_[0]
        r2 = model.score(X, y)
        threat_level, threat_color = get_threat_level(stats["total_fatalities"], stats["total_incidents"])
        deadly_attacks = conn.execute("SELECT year, country, city, attack_type, group_name, fatalities, injuries FROM gtd ORDER BY fatalities DESC NULLS LAST LIMIT 5").df()
        
        recent_start = int(stats["year_range"].split(" - ")[1]) if " - " in stats["year_range"] else 1970
        recent_res = conn.execute(f"SELECT group_name FROM gtd WHERE year >= {recent_start} GROUP BY group_name ORDER BY COUNT(*) DESC LIMIT 1").fetchone()
        recent_top_group = recent_res[0] if recent_res else "Unknown"

    st.markdown(f'''
        <div class="report-container">
            <div style="text-align: center; margin-bottom: 2rem; padding-bottom: 1.5rem; border-bottom: 1px solid rgba(124, 58, 237, 0.15);">
                <div style="font-size: 0.7rem; color: #64748b; letter-spacing: 0.15em; text-transform: uppercase;">CLASSIFIED // INTELLIGENCE REPORT</div>
                <h1 style="font-size: 1.8rem; margin: 0.5rem 0;">Global Terrorism Intelligence Report</h1>
                <div style="display: flex; justify-content: center; gap: 2rem; flex-wrap: wrap; font-size: 0.85rem; color: #94a3b8;">
                    <span>Period: {stats["year_range"]}</span>
                </div>
            </div>
            <h2>1. Executive Summary</h2>
            <p>Total of <b style="color: #e2e8f0;">{format_number(stats["total_incidents"])}</b> terrorist incidents.</p>
            <h2>5. Deadliest Incidents</h2>
    ''', unsafe_allow_html=True)
    
    for _, row in deadly_attacks.iterrows():
        st.markdown(f"<div style='padding: 0.6rem 1rem; margin: 0.3rem 0; background: rgba(239, 68, 68, 0.05); border-radius: 8px; border-left: 3px solid #ef4444;'><b>{int(row['year'])}</b> - {row['country']}, {row.get('city', 'Unknown')} - <span style='color: #ef4444; font-weight: 700;'>{int(row['fatalities'])} fatalities</span></div>", unsafe_allow_html=True)

`

`python
# pages/Attack_Prediction.py
# pages/Attack_Prediction.py
import streamlit as st
import pandas as pd
from utils.charts import create_feature_importance_chart
from utils.helper import get_country_list, get_region_list, get_attack_type_list, get_weapon_type_list, get_group_list, get_target_type_list
from utils.preprocessing import train_prediction_model, predict_attack

def show(conn):
    if conn is None:
        st.warning("No data available.")
        return

    st.markdown(
        '''
        <div class="glass-card" style="text-align: center; padding: 2rem; margin-bottom: 2rem;">
            <h1 style="font-size: 2.2rem; margin-bottom: 0.3rem;">
                <span class="gradient-text">🤖 Attack Prediction</span>
            </h1>
            <p style="color: #94a3b8; max-width: 600px; margin: 0 auto;">
                Machine learning model that predicts the likelihood of casualties in a terrorist attack based on historical patterns.
            </p>
        </div>
        ''', unsafe_allow_html=True
    )

    with st.spinner("Training prediction model..."):
        model, encoders, feature_cols, accuracy = train_prediction_model(conn)

    if model is None:
        st.error("Could not train the prediction model. Please check the data.")
        return

    st.markdown(
        f'''
        <div style="display: flex; gap: 1rem; flex-wrap: wrap; margin-bottom: 1.5rem;">
            <div class="custom-card" style="flex: 1; min-width: 200px; text-align: center; padding: 1rem;">
                <div style="font-size: 0.7rem; color: #94a3b8; text-transform: uppercase;">Model Accuracy</div>
                <div style="font-size: 2rem; font-weight: 800; color: #10b981;">{accuracy:.1%}</div>
            </div>
            <div class="custom-card" style="flex: 1; min-width: 200px; text-align: center; padding: 1rem;">
                <div style="font-size: 0.7rem; color: #94a3b8; text-transform: uppercase;">Algorithm</div>
                <div style="font-size: 1.2rem; font-weight: 700; color: #a78bfa;">Random Forest</div>
            </div>
            <div class="custom-card" style="flex: 1; min-width: 200px; text-align: center; padding: 1rem;">
                <div style="font-size: 0.7rem; color: #94a3b8; text-transform: uppercase;">Features Used</div>
                <div style="font-size: 1.2rem; font-weight: 700; color: #e2e8f0;">{len(feature_cols)}</div>
            </div>
            <div class="custom-card" style="flex: 1; min-width: 200px; text-align: center; padding: 1rem;">
                <div style="font-size: 0.7rem; color: #94a3b8; text-transform: uppercase;">Prediction Target</div>
                <div style="font-size: 1rem; font-weight: 700; color: #f59e0b;">Fatality Likelihood</div>
            </div>
        </div>
        ''', unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)
    countries = get_country_list(conn)
    regions = get_region_list(conn)
    weapons = get_weapon_type_list(conn)
    targets = get_target_type_list(conn)
    attacks = get_attack_type_list(conn)
    groups = get_group_list(conn)

    with col1:
        pred_country = st.selectbox("Country", options=countries, index=countries.index("Iraq") if "Iraq" in countries else 0)
        pred_region = st.selectbox("Region", options=regions, index=regions.index("Middle East & North Africa") if "Middle East & North Africa" in regions else 0)
        pred_weapon = st.selectbox("Weapon Type", options=weapons, index=0)

    with col2:
        pred_target = st.selectbox("Target Type", options=targets, index=0)
        pred_attack = st.selectbox("Attack Type", options=attacks, index=0)
        pred_group = st.selectbox("Terrorist Group", options=groups, index=0)

    with col3:
        pred_success = st.selectbox("Attack Success (1=Yes, 0=No)", options=[1, 0], index=0)
        pred_suicide = st.selectbox("Suicide Attack (1=Yes, 0=No)", options=[0, 1], index=0)
        pred_fatalities_input = st.number_input("Potential Fatalities (estimate)", min_value=0, max_value=1000, value=5)
        pred_injuries_input = st.number_input("Potential Injuries (estimate)", min_value=0, max_value=5000, value=20)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🔮 Predict Attack Outcome", use_container_width=True):
        with st.spinner("Generating prediction..."):
            try:
                prediction, probability = predict_attack(model, encoders, feature_cols, pred_country, pred_region, pred_weapon, pred_target, pred_attack, pred_group, pred_success, pred_suicide, pred_fatalities_input, pred_injuries_input)
                st.markdown("---")
                st.markdown("## Prediction Results")
                
                result_col1, result_col2 = st.columns(2)
                fatality_risk = probability[1] * 100
                with result_col1:
                    if prediction == 1:
                        st.markdown(f'<div class="custom-card" style="text-align: center; padding: 2rem; border-color: rgba(239, 68, 68, 0.5);"><div style="font-size: 3rem;">⚠️</div><div style="font-size: 1.8rem; font-weight: 800; color: #ef4444; margin: 0.5rem 0;">FATALITIES PREDICTED</div><div style="font-size: 0.9rem; color: #94a3b8;">Based on the provided parameters, this attack scenario may result in casualties.</div></div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="custom-card" style="text-align: center; padding: 2rem; border-color: rgba(16, 185, 129, 0.5);"><div style="font-size: 3rem;">✅</div><div style="font-size: 1.8rem; font-weight: 800; color: #10b981; margin: 0.5rem 0;">NO FATALITIES PREDICTED</div><div style="font-size: 0.9rem; color: #94a3b8;">The model predicts this attack scenario may not result in fatalities.</div></div>', unsafe_allow_html=True)

                with result_col2:
                    st.markdown('<div class="custom-card" style="padding: 1.5rem;"><div style="font-size: 0.75rem; color: #94a3b8; text-transform: uppercase; margin-bottom: 1rem; letter-spacing: 0.05em;">Prediction Confidence</div>', unsafe_allow_html=True)
                    prob_no_fatality = probability[0] * 100
                    st.markdown(f'<div style="margin-bottom: 1rem;"><div style="display: flex; justify-content: space-between; font-size: 0.85rem; margin-bottom: 0.3rem;"><span style="color: #10b981;">No Fatality</span><span style="color: #e2e8f0; font-weight: 600;">{prob_no_fatality:.1f}%</span></div><div class="confidence-meter"><div class="confidence-meter-fill" style="width: {prob_no_fatality}%; background: linear-gradient(90deg, #10b981, #34d399);"></div></div></div>', unsafe_allow_html=True)
                    st.markdown(f'<div style="margin-bottom: 1.5rem;"><div style="display: flex; justify-content: space-between; font-size: 0.85rem; margin-bottom: 0.3rem;"><span style="color: #ef4444;">Fatality</span><span style="color: #e2e8f0; font-weight: 600;">{fatality_risk:.1f}%</span></div><div class="confidence-meter"><div class="confidence-meter-fill" style="width: {fatality_risk}%; background: linear-gradient(90deg, #ef4444, #f87171);"></div></div></div>', unsafe_allow_html=True)
                    risk_level = "CRITICAL" if fatality_risk > 75 else "HIGH" if fatality_risk > 50 else "MODERATE" if fatality_risk > 25 else "LOW"
                    risk_color = "#ef4444" if fatality_risk > 75 else "#f59e0b" if fatality_risk > 50 else "#3b82f6" if fatality_risk > 25 else "#10b981"
                    st.markdown(f'<div style="text-align: center; padding-top: 0.5rem;"><span class="threat-badge" style="background: {risk_color}20; color: {risk_color};">{risk_level} RISK</span></div></div>', unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown('<div class="custom-card">### Feature Importance', unsafe_allow_html=True)
                if hasattr(model, "feature_importances_"):
                    importances = model.feature_importances_
                    feat_imp_df = pd.DataFrame({"feature": feature_cols, "importance": importances}).sort_values("importance", ascending=False)
                    fig = create_feature_importance_chart(feat_imp_df["feature"].tolist(), feat_imp_df["importance"].tolist(), "What Drives the Prediction?", height=400)
                    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
                st.markdown("</div>", unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Prediction error: {str(e)}")

`

`python
# pages/Country_Analysis.py
# pages/Country_Analysis.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils.charts import THEME, create_bar_chart, create_line_chart, create_pie_chart, create_treemap, apply_theme
from utils.helper import format_number, get_country_list, get_threat_level

def show(conn):
    if conn is None:
        st.warning("No data available.")
        return

    st.markdown(
        '''
        <div class="glass-card" style="text-align: center; padding: 2rem; margin-bottom: 2rem;">
            <h1 style="font-size: 2.2rem; margin-bottom: 0.3rem;">
                <span class="gradient-text">🌎 Country Analysis</span>
            </h1>
            <p style="color: #94a3b8; max-width: 600px; margin: 0 auto;">
                Deep dive into terrorism activity by country with comprehensive analytics.
            </p>
        </div>
        ''', unsafe_allow_html=True
    )

    countries = get_country_list(conn)
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        selected_country = st.selectbox("Select a Country", options=countries, index=countries.index("Iraq") if "Iraq" in countries else 0)

    c_esc = selected_country.replace("'", "''")
    res = conn.execute(f"SELECT COUNT(*), SUM(fatalities), SUM(injuries), COUNT(DISTINCT group_name), MIN(year), MAX(year) FROM gtd WHERE country='{c_esc}'").fetchone()
    
    if not res or res[0] == 0:
        st.warning(f"No data available for {selected_country}.")
        return

    total_incidents = res[0]
    total_fatalities = int(res[1] or 0)
    total_injuries = int(res[2] or 0)
    total_groups = res[3] or 0
    threat_level, threat_color = get_threat_level(total_fatalities, total_incidents)
    year_range = f"{res[4]} - {res[5]}"

    st.markdown(
        f'''
        <div style="display: flex; gap: 1rem; flex-wrap: wrap; margin-bottom: 1rem;">
            <div class="custom-card" style="flex: 1; min-width: 140px; text-align: center; padding: 1rem;">
                <div style="font-size: 1.8rem; font-weight: 800; color: #ef4444;">{total_fatalities:,}</div>
                <div style="font-size: 0.75rem; color: #94a3b8; text-transform: uppercase;">Fatalities</div>
            </div>
            <div class="custom-card" style="flex: 1; min-width: 140px; text-align: center; padding: 1rem;">
                <div style="font-size: 1.8rem; font-weight: 800; color: #f59e0b;">{total_injuries:,}</div>
                <div style="font-size: 0.75rem; color: #94a3b8; text-transform: uppercase;">Injuries</div>
            </div>
            <div class="custom-card" style="flex: 1; min-width: 140px; text-align: center; padding: 1rem;">
                <div style="font-size: 1.8rem; font-weight: 800; color: #e2e8f0;">{total_incidents:,}</div>
                <div style="font-size: 0.75rem; color: #94a3b8; text-transform: uppercase;">Incidents</div>
            </div>
            <div class="custom-card" style="flex: 1; min-width: 140px; text-align: center; padding: 1rem;">
                <div style="font-size: 1.8rem; font-weight: 800; color: #a78bfa;">{total_groups}</div>
                <div style="font-size: 0.75rem; color: #94a3b8; text-transform: uppercase;">Groups</div>
            </div>
            <div class="custom-card" style="flex: 1; min-width: 140px; text-align: center; padding: 1rem;">
                <div style="font-size: 0.7rem; color: #94a3b8; text-transform: uppercase;">Threat Level</div>
                <div style="font-size: 1.3rem; font-weight: 800; color: {threat_color};">{threat_level}</div>
            </div>
            <div class="custom-card" style="flex: 1; min-width: 140px; text-align: center; padding: 1rem;">
                <div style="font-size: 0.7rem; color: #94a3b8; text-transform: uppercase;">Data Range</div>
                <div style="font-size: 1.1rem; font-weight: 700; color: #e2e8f0;">{year_range}</div>
            </div>
        </div>
        ''', unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        yearly = conn.execute(f"SELECT year, COUNT(*) as incidents, SUM(fatalities) as fatalities, SUM(injuries) as injuries FROM gtd WHERE country='{c_esc}' GROUP BY year ORDER BY year").df()
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=yearly["year"], y=yearly["incidents"], mode="lines+markers", name="Incidents", line=dict(color=THEME["accent"], width=3), marker=dict(size=6), yaxis="y"))
        fig.add_trace(go.Scatter(x=yearly["year"], y=yearly["fatalities"], mode="lines+markers", name="Fatalities", line=dict(color=THEME["danger"], width=2), marker=dict(size=5), yaxis="y2"))
        fig.update_layout(title=dict(text="Yearly Trend: Incidents & Fatalities", font=dict(size=14, color=THEME["text"]), x=0.5), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(family="Inter, sans-serif", color=THEME["text"]), height=350, hovermode="x unified", hoverlabel=dict(bgcolor=THEME["card"], font_size=11, bordercolor=THEME["accent"]), legend=dict(font=dict(color=THEME["text"]), bgcolor="rgba(0,0,0,0.3)", orientation="h", y=1.1), xaxis=dict(showgrid=True, gridcolor=THEME["grid"]), yaxis=dict(title="Incidents", showgrid=True, gridcolor=THEME["grid"], titlefont=dict(color=THEME["accent"])), yaxis2=dict(title="Fatalities", overlaying="y", side="right", showgrid=False, titlefont=dict(color=THEME["danger"])), margin=dict(l=10, r=10, t=50, b=10))
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        attack_counts = conn.execute(f"SELECT attack_type, COUNT(*) as count FROM gtd WHERE country='{c_esc}' GROUP BY attack_type ORDER BY count DESC LIMIT 8").df()
        fig = create_pie_chart(attack_counts, "count", "attack_type", "Attack Type Distribution", height=350)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        group_counts = conn.execute(f"SELECT group_name, COUNT(*) as count FROM gtd WHERE country='{c_esc}' GROUP BY group_name ORDER BY count DESC LIMIT 10").df()
        fig = create_bar_chart(group_counts, "group_name", "count", "Top Terrorist Groups", THEME["warning"], height=350, orientation="h")
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        weapon_counts = conn.execute(f"SELECT weapon_type, COUNT(*) as count FROM gtd WHERE country='{c_esc}' GROUP BY weapon_type ORDER BY count DESC LIMIT 8").df()
        fig = create_pie_chart(weapon_counts, "count", "weapon_type", "Weapon Type Distribution", height=350)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        target_counts = conn.execute(f"SELECT target_type, COUNT(*) as count FROM gtd WHERE country='{c_esc}' GROUP BY target_type ORDER BY count DESC LIMIT 8").df()
        fig = create_bar_chart(target_counts, "target_type", "count", "Target Types", THEME["info"], height=350, orientation="h")
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        city_counts = conn.execute(f"SELECT city, COUNT(*) as count FROM gtd WHERE country='{c_esc}' GROUP BY city ORDER BY count DESC LIMIT 10").df()
        fig = create_bar_chart(city_counts, "city", "count", "Most Affected Cities", THEME["accent"], height=350, orientation="h")
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    map_data = conn.execute(f"SELECT latitude, longitude, year, fatalities, city, attack_type FROM gtd WHERE country='{c_esc}' AND latitude IS NOT NULL AND longitude IS NOT NULL").df()
    if not map_data.empty:
        fig_map = go.Figure()
        fatalities_max = map_data["fatalities"].max() if map_data["fatalities"].max() > 0 else 1
        fig_map.add_trace(go.Scattermapbox(
            lat=map_data["latitude"], lon=map_data["longitude"], mode="markers",
            marker=dict(size=map_data["fatalities"].clip(1, 50) / fatalities_max * 20 + 5, color=map_data["fatalities"], colorscale="Viridis", showscale=True, colorbar=dict(title="Fatalities", thickness=10, len=0.3, tickfont=dict(color=THEME["text"], size=9), titlefont=dict(color=THEME["text"], size=9)), opacity=0.8),
            text=map_data.apply(lambda r: f"<b>{r.get('city', 'Unknown')}</b><br>Year: {int(r['year'])}<br>Fatalities: {int(r['fatalities'])}<br>Attack: {r.get('attack_type', 'Unknown')}", axis=1),
            hovertemplate="%{text}<extra></extra>",
        ))
        fig_map.update_layout(mapbox=dict(style="carto-darkmatter", center=dict(lat=map_data["latitude"].mean(), lon=map_data["longitude"].mean()), zoom=4), paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=0, r=0, t=0, b=0), height=450, hoverlabel=dict(bgcolor=THEME["card"], font_size=10, bordercolor=THEME["accent"]))
        st.plotly_chart(fig_map, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.markdown(f"### Incident Table - {selected_country}")
    display_df = conn.execute(f"SELECT year, month, day, city, province, attack_type, target_type, group_name, weapon_type, fatalities, injuries, success FROM gtd WHERE country='{c_esc}' LIMIT 100").df()
    if not display_df.empty:
        st.dataframe(display_df, use_container_width=True, hide_index=True)

    csv = display_df.to_csv(index=False)
    import base64
    b64 = base64.b64encode(csv.encode()).decode()
    st.markdown(f'<a href="data:file/csv;base64,{b64}" download="{selected_country}_terrorism_data.csv" style="display: inline-block; padding: 0.5rem 1.5rem; background: linear-gradient(135deg, #7c3aed, #3b82f6); color: white; border-radius: 10px; text-decoration: none; font-weight: 600; font-size: 0.85rem; margin-top: 0.5rem;">Download Full CSV</a>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

`

`python
# pages/Data_Explorer.py
# pages/Data_Explorer.py
import streamlit as st

def show(conn):
    if conn is None: return

    st.markdown('''<div class="glass-card" style="text-align: center; padding: 2rem; margin-bottom: 2rem;"><h1 style="font-size: 2.2rem; margin-bottom: 0.3rem;"><span class="gradient-text">📊 Data Explorer</span></h1></div>''', unsafe_allow_html=True)

    st.markdown('<div class="custom-card">', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2, 1, 1])
    with col1: search_term = st.text_input("Search", placeholder="Search...")
    with col2:
        attack_types = [r[0] for r in conn.execute("SELECT DISTINCT attack_type FROM gtd").fetchall()]
        attack_filter = st.multiselect("Attack Type", options=attack_types, default=[])
    with col3:
        sort_col = st.selectbox("Sort by", options=["year", "fatalities", "country"], index=0)
        sort_asc = st.checkbox("Ascending", value=False)

    where_conds = ["1=1"]
    if search_term:
        s = search_term.lower().replace("'", "''")
        cols = ["country", "city", "group_name", "attack_type", "weapon_type", "target_type", "province"]
        where_conds.append("(" + " OR ".join([f"LOWER(CAST({c} AS VARCHAR)) LIKE '%{s}%'" for c in cols]) + ")")
    if attack_filter:
        a_str = ",".join(["'" + a.replace("'", "''") + "'" for a in attack_filter])
        where_conds.append(f"attack_type IN ({a_str})")
        
    where = " AND ".join(where_conds)
    order = f"ORDER BY {sort_col} {'ASC' if sort_asc else 'DESC'}"

    page_size = st.selectbox("Rows per page", options=[25, 50, 100], index=0)
    total_records = conn.execute(f"SELECT COUNT(*) FROM gtd WHERE {where}").fetchone()[0]
    total_pages = max(1, (total_records + page_size - 1) // page_size)
    page = st.number_input("Page", min_value=1, max_value=total_pages, value=1)
    
    start_idx = (page - 1) * page_size
    page_df = conn.execute(f"SELECT year, month, day, country, city, attack_type, group_name, weapon_type, fatalities FROM gtd WHERE {where} {order} LIMIT {page_size} OFFSET {start_idx}").df()
    
    st.dataframe(page_df, use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)

`

`python
# pages/Forecasting.py
# pages/Forecasting.py
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from utils.charts import create_forecast_chart

def show(conn):
    if conn is None:
        st.warning("No data available.")
        return

    st.markdown(
        '''
        <div class="glass-card" style="text-align: center; padding: 2rem; margin-bottom: 2rem;">
            <h1 style="font-size: 2.2rem; margin-bottom: 0.3rem;">
                <span class="gradient-text">📈 Forecasting</span>
            </h1>
            <p style="color: #94a3b8; max-width: 600px; margin: 0 auto;">
                Predict future terrorism trends using linear regression analysis on historical incident data.
            </p>
        </div>
        ''', unsafe_allow_html=True
    )

    yearly = conn.execute("SELECT year, COUNT(*) as incidents, SUM(fatalities) as fatalities, SUM(injuries) as injuries FROM gtd GROUP BY year ORDER BY year").df()

    with st.sidebar:
        st.markdown("## Forecast Settings")
        forecast_years = st.slider("Forecast Years Ahead", min_value=1, max_value=20, value=5)

    last_historical_year = yearly["year"].max()
    future_years = np.arange(last_historical_year + 1, last_historical_year + forecast_years + 1)

    col1, col2, col3 = st.columns(3)

    def fit_and_predict(col):
        X = yearly[["year"]].values
        y = yearly[col].values
        model = LinearRegression().fit(X, y)
        future = np.maximum(model.predict(future_years.reshape(-1, 1)), 0)
        growth = ((future.sum() / forecast_years) / (y.sum() / len(y)) - 1) * 100 if y.sum() > 0 else 0
        return model, future, growth, X, y

    model_inc, future_inc, inc_growth, X_inc, y_inc = fit_and_predict("incidents")
    with col1:
        st.markdown(f'<div class="custom-card" style="text-align: center; padding: 1.2rem;"><div style="font-size: 0.7rem; color: #94a3b8; text-transform: uppercase;">Total Forecast Incidents</div><div style="font-size: 1.8rem; font-weight: 800; color: #a78bfa;">{int(future_inc.sum()):,}</div><div style="font-size: 0.75rem; color: {"#10b981" if inc_growth >= 0 else "#ef4444"};">{"↑" if inc_growth >= 0 else "↓"} {abs(inc_growth):.1f}% avg annual change</div></div>', unsafe_allow_html=True)

    model_fat, future_fat, fat_growth, X_fat, y_fat = fit_and_predict("fatalities")
    with col2:
        st.markdown(f'<div class="custom-card" style="text-align: center; padding: 1.2rem;"><div style="font-size: 0.7rem; color: #94a3b8; text-transform: uppercase;">Forecast Fatalities</div><div style="font-size: 1.8rem; font-weight: 800; color: #ef4444;">{int(future_fat.sum()):,}</div><div style="font-size: 0.75rem; color: {"#10b981" if fat_growth >= 0 else "#ef4444"};">{"↑" if fat_growth >= 0 else "↓"} {abs(fat_growth):.1f}% avg annual change</div></div>', unsafe_allow_html=True)

    model_inj, future_inj, inj_growth, X_inj, y_inj = fit_and_predict("injuries")
    with col3:
        st.markdown(f'<div class="custom-card" style="text-align: center; padding: 1.2rem;"><div style="font-size: 0.7rem; color: #94a3b8; text-transform: uppercase;">Forecast Injuries</div><div style="font-size: 1.8rem; font-weight: 800; color: #f59e0b;">{int(future_inj.sum()):,}</div><div style="font-size: 0.75rem; color: {"#10b981" if inj_growth >= 0 else "#ef4444"};">{"↑" if inj_growth >= 0 else "↓"} {abs(inj_growth):.1f}% avg annual change</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    fig_incidents = create_forecast_chart(yearly[["year", "incidents"]], pd.DataFrame({"year": future_years, "incidents": future_inc.astype(int)}), "year", "incidents", "Incident Forecast", height=450)
    st.plotly_chart(fig_incidents, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        fig_fatalities = create_forecast_chart(yearly[["year", "fatalities"]], pd.DataFrame({"year": future_years, "fatalities": future_fat.astype(int)}), "year", "fatalities", "Fatality Forecast", height=400)
        st.plotly_chart(fig_fatalities, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        fig_injuries = create_forecast_chart(yearly[["year", "injuries"]], pd.DataFrame({"year": future_years, "injuries": future_inj.astype(int)}), "year", "injuries", "Injury Forecast", height=400)
        st.plotly_chart(fig_injuries, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="custom-card">### Trend Analysis', unsafe_allow_html=True)
    inc_r2 = model_inc.score(X_inc, y_inc)
    st.markdown(f'<div style="padding: 1rem; background: rgba(124, 58, 237, 0.05); border-radius: 12px;"><div style="font-size: 1.3rem; font-weight: 700; color: #a78bfa;">Incident Trend Fit (R²): {inc_r2:.3f}</div></div></div>', unsafe_allow_html=True)

`

`python
# pages/Global_Threat_Map.py
# pages/Global_Threat_Map.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from utils.charts import THEME, apply_theme
from utils.helper import get_year_range, get_country_list, get_attack_type_list, get_weapon_type_list, get_group_list
from utils.data_loader import build_where_clause

def show(conn):
    if conn is None:
        st.warning("No data available.")
        return

    st.markdown(
        '''
        <div class="glass-card" style="text-align: center; padding: 2rem; margin-bottom: 2rem;">
            <h1 style="font-size: 2.2rem; margin-bottom: 0.3rem;">
                <span class="gradient-text">🌍 Global Threat Map</span>
            </h1>
            <p style="color: #94a3b8; max-width: 600px; margin: 0 auto;">
                Interactive visualization of global terrorism incidents with powerful filtering capabilities.
            </p>
        </div>
        ''', unsafe_allow_html=True
    )

    with st.expander("🔍 Filter Controls", expanded=True):
        col1, col2, col3, col4 = st.columns(4)

        years = get_year_range(conn)
        with col1:
            year_range = st.slider("Year Range", min_value=years[0], max_value=years[1], value=(years[0], years[1]))

        countries_list = get_country_list(conn)
        with col2:
            selected_countries = st.multiselect("Countries (leave empty for all)", options=countries_list, default=[])

        attack_types = get_attack_type_list(conn)
        with col3:
            selected_attacks = st.multiselect("Attack Types", options=attack_types, default=[])

        weapon_types = get_weapon_type_list(conn)
        with col4:
            selected_weapons = st.multiselect("Weapon Types", options=weapon_types, default=[])

        col1, col2 = st.columns(2)
        groups = get_group_list(conn)
        with col1:
            selected_groups = st.multiselect("Terrorist Groups", options=groups, default=[])

    where_clause = build_where_clause(year_range, selected_countries, None, selected_attacks, selected_weapons, selected_groups)
    
    stats_query = f"SELECT COUNT(*) as cnt, SUM(fatalities) as fat, SUM(injuries) as inj, COUNT(DISTINCT country) as cty FROM gtd WHERE {where_clause}"
    stats_res = conn.execute(stats_query).fetchone()
    inc_count = stats_res[0] or 0
    fat_count = int(stats_res[1] or 0)
    inj_count = int(stats_res[2] or 0)
    cty_count = stats_res[3] or 0

    st.markdown(
        f'''
        <div style="display: flex; gap: 1rem; flex-wrap: wrap; margin-bottom: 1rem;">
            <div class="custom-card" style="flex: 1; min-width: 120px; text-align: center; padding: 0.8rem;">
                <div style="font-size: 0.7rem; color: #94a3b8;">INCIDENTS</div>
                <div style="font-size: 1.5rem; font-weight: 700; color: #e2e8f0;">{inc_count:,}</div>
            </div>
            <div class="custom-card" style="flex: 1; min-width: 120px; text-align: center; padding: 0.8rem;">
                <div style="font-size: 0.7rem; color: #94a3b8;">FATALITIES</div>
                <div style="font-size: 1.5rem; font-weight: 700; color: #ef4444;">{fat_count:,}</div>
            </div>
            <div class="custom-card" style="flex: 1; min-width: 120px; text-align: center; padding: 0.8rem;">
                <div style="font-size: 0.7rem; color: #94a3b8;">INJURIES</div>
                <div style="font-size: 1.5rem; font-weight: 700; color: #f59e0b;">{inj_count:,}</div>
            </div>
            <div class="custom-card" style="flex: 1; min-width: 120px; text-align: center; padding: 0.8rem;">
                <div style="font-size: 0.7rem; color: #94a3b8;">COUNTRIES</div>
                <div style="font-size: 1.5rem; font-weight: 700; color: #10b981;">{cty_count}</div>
            </div>
        </div>
        ''', unsafe_allow_html=True
    )

    query_map = f"SELECT latitude, longitude, fatalities, injuries, year, country, city, attack_type, weapon_type, group_name, target_type FROM gtd WHERE {where_clause} AND latitude IS NOT NULL AND longitude IS NOT NULL USING SAMPLE 10000 (Reservoir, 42)"
    plot_df = conn.execute(query_map).df()

    plot_df["size"] = plot_df["fatalities"].clip(1, 100) + 3
    plot_df["hover_text"] = plot_df.apply(
        lambda row: (
            f"<b>{row.get('country', 'Unknown')}</b><br>"
            f"City: {row.get('city', 'Unknown')}<br>"
            f"Year: {int(row['year'])}<br>"
            f"Attack: {row.get('attack_type', 'Unknown')}<br>"
            f"Weapon: {row.get('weapon_type', 'Unknown')}<br>"
            f"Group: {row.get('group_name', 'Unknown')}<br>"
            f"Fatalities: {int(row['fatalities'])}<br>"
            f"Injuries: {int(row['injuries'])}<br>"
            f"Target: {row.get('target_type', 'Unknown')}"
        ),
        axis=1,
    )

    fig = go.Figure()
    center_lat = plot_df["latitude"].mean() if not plot_df.empty else 20
    center_lon = plot_df["longitude"].mean() if not plot_df.empty else 0

    fig.add_trace(
        go.Scattermapbox(
            lon=plot_df["longitude"], lat=plot_df["latitude"], text=plot_df["hover_text"], mode="markers",
            marker=dict(
                size=plot_df["size"].clip(2, 25), color=plot_df["fatalities"],
                colorscale=[[0, "rgba(59, 130, 246, 0.4)"], [0.3, "rgba(124, 58, 237, 0.6)"], [0.6, "rgba(239, 68, 68, 0.8)"], [1, "rgba(239, 68, 68, 1)"]],
                showscale=True,
                colorbar=dict(title="Fatalities", thickness=15, len=0.5, x=1.02, xpad=0, tickfont=dict(color=THEME["text"]), titlefont=dict(color=THEME["text"])),
                opacity=0.8,
            ), hovertemplate="%{text}<extra></extra>",
        )
    )

    fig.update_layout(
        mapbox=dict(style="carto-darkmatter", center=dict(lat=center_lat, lon=center_lon), zoom=1.5 if len(selected_countries) > 0 else 1),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(family="Inter, sans-serif", color=THEME["text"]),
        margin=dict(l=0, r=0, t=0, b=0), height=650,
        hoverlabel=dict(bgcolor=THEME["card"], font_size=11, font_family="Inter, sans-serif", bordercolor=THEME["accent"]),
    )

    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": True, "modeBarButtonsToRemove": ["lasso2d", "select2d"], "displaylogo": False})
    st.markdown("</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        region_counts = conn.execute(f"SELECT region, COUNT(*) as count FROM gtd WHERE {where_clause} GROUP BY region ORDER BY count DESC LIMIT 10").df()
        colors = px.colors.sequential.Viridis[: len(region_counts)]
        fig_reg = go.Figure(data=[go.Bar(x=region_counts["count"], y=region_counts["region"], orientation="h", marker=dict(color=colors, line=dict(width=0)))])
        fig_reg = apply_theme(fig_reg)
        fig_reg.update_layout(title=dict(text="Incidents by Region", font=dict(size=14), x=0.5), height=350, xaxis=dict(showgrid=True, gridcolor=THEME["grid"]), yaxis=dict(showgrid=False), showlegend=False)
        st.plotly_chart(fig_reg, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        group_counts = conn.execute(f"SELECT group_name, COUNT(*) as count FROM gtd WHERE {where_clause} GROUP BY group_name ORDER BY count DESC LIMIT 10").df()
        colors = px.colors.sequential.Viridis[: len(group_counts)]
        fig_grp = go.Figure(data=[go.Bar(x=group_counts["count"], y=group_counts["group_name"], orientation="h", marker=dict(color=colors, line=dict(width=0)))])
        fig_grp = apply_theme(fig_grp)
        fig_grp.update_layout(title=dict(text="Top Groups (Filtered View)", font=dict(size=14), x=0.5), height=350, xaxis=dict(showgrid=True, gridcolor=THEME["grid"]), yaxis=dict(showgrid=False), showlegend=False)
        st.plotly_chart(fig_grp, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

`

`python
# pages/Home.py
# pages/Home.py
import streamlit as st
from utils.charts import THEME, create_bar_chart, create_line_chart, create_pie_chart, create_heatmap, create_treemap
from utils.helper import format_number
from utils.data_loader import get_summary_stats

def show(conn):
    if conn is None:
        st.warning("No data available. Please upload the GTD dataset.")
        return

    stats = get_summary_stats(conn)

    header_col1, header_col2 = st.columns([3, 1])
    with header_col1:
        st.markdown(
            '''
            <div style="padding-top: 0.5rem; margin-bottom: 2rem;">
                <h1 style="font-size: 2.2rem; margin-bottom: 0.5rem; font-family: 'Outfit', sans-serif; font-weight: 800; color: #e2e8f0; line-height: 1.2;">
                    <span style="background: linear-gradient(135deg, #a78bfa, #3b82f6); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">AI</span> Terrorism Intelligence Dashboard
                </h1>
                <p style="font-size: 0.95rem; color: #94a3b8; max-width: 800px; line-height: 1.5; margin-top: -0.2rem;">
                    Advanced analytics platform leveraging machine learning to analyze, predict, and visualize<br>
                    global terrorism patterns from the Global Terrorism Database (GTD).
                </p>
            </div>
            ''', unsafe_allow_html=True
        )
    
    with header_col2:
        st.markdown(
            '''
            <div style="display: flex; justify-content: flex-end; align-items: center; padding-top: 0.5rem; gap: 1rem;">
                <div style="background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 8px; padding: 0.4rem 0.8rem; display: flex; align-items: center; gap: 0.5rem; font-size: 0.75rem; color: #cbd5e1;">
                    <span>📅</span> May 21, 2025 - May 21, 2025 <span style="font-size: 0.6rem; margin-left: 0.5rem;">⌄</span>
                </div>
                <div style="background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 8px; padding: 0.4rem 0.6rem; display: flex; align-items: center; justify-content: center; cursor: pointer;">
                    🌙
                </div>
            </div>
            ''', unsafe_allow_html=True
        )

    st.markdown("## Key Metrics")

    cols = st.columns(6)
    metrics = [
        ("💀", format_number(stats["total_incidents"]), "Total Incidents"),
        ("🌍", stats["total_countries"], "Countries"),
        ("⚰️", format_number(stats["total_fatalities"]), "Fatalities"),
        ("🏥", format_number(stats["total_injuries"]), "Injuries"),
        ("👥", format_number(stats["total_groups"]), "Terrorist Groups"),
        ("🔫", stats["total_attack_types"], "Attack Types"),
    ]

    for idx, (icon, value, label) in enumerate(metrics):
        with cols[idx]:
            st.markdown(
                f'''
                <div class="custom-card stat-card animate-in delay-{idx + 1}">
                    <div class="stat-icon">{icon}</div>
                    <div class="stat-value">{value}</div>
                    <div class="stat-label">{label}</div>
                </div>
                ''', unsafe_allow_html=True
            )

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="custom-card animate-in delay-3">', unsafe_allow_html=True)
        yearly = conn.execute("SELECT year, COUNT(*) as count FROM gtd GROUP BY year ORDER BY year").df()
        fig = create_line_chart(yearly, "year", "count", "Attacks by Year", THEME["accent"])
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="custom-card animate-in delay-4">', unsafe_allow_html=True)
        top_countries = conn.execute("SELECT country, COUNT(*) as count FROM gtd GROUP BY country ORDER BY count DESC LIMIT 10").df()
        fig = create_bar_chart(top_countries, "country", "count", "Top 10 Affected Countries", THEME["danger"], orientation="h")
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="custom-card animate-in delay-5">', unsafe_allow_html=True)
        attack_counts = conn.execute("SELECT attack_type, COUNT(*) as count FROM gtd GROUP BY attack_type ORDER BY count DESC LIMIT 8").df()
        fig = create_pie_chart(attack_counts, "count", "attack_type", "Attack Type Distribution")
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="custom-card animate-in delay-6">', unsafe_allow_html=True)
        weapon_counts = conn.execute("SELECT weapon_type, COUNT(*) as count FROM gtd GROUP BY weapon_type ORDER BY count DESC LIMIT 8").df()
        fig = create_pie_chart(weapon_counts, "count", "weapon_type", "Weapon Type Distribution")
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        top_groups = conn.execute("SELECT group_name, COUNT(*) as count FROM gtd GROUP BY group_name ORDER BY count DESC LIMIT 10").df()
        fig = create_bar_chart(top_groups, "group_name", "count", "Top 10 Terrorist Groups", THEME["warning"], orientation="h")
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        heatmap_data = conn.execute("SELECT year, region, COUNT(*) as count FROM gtd GROUP BY year, region").df()
        fig = create_heatmap(heatmap_data, "year", "region", "count", "Regional Activity Heatmap", height=450)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    treemap_data = conn.execute("SELECT region, country, group_name, COUNT(*) as count FROM gtd GROUP BY region, country, group_name ORDER BY count DESC LIMIT 100").df()
    fig = create_treemap(treemap_data, ["region", "country", "group_name"], "count", "Global Terrorism Overview - Region → Country → Group")
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        '''
        <div style="text-align: center; padding: 2rem 0 0 0; font-size: 0.75rem; color: #475569;">
            Data Source: Global Terrorism Database (GTD) | National Consortium for the Study of Terrorism and Responses to Terrorism (START)
        </div>
        ''', unsafe_allow_html=True
    )

`

`text
# requirements.txt
streamlit==1.37.0
streamlit-extras==0.4.3
plotly==5.24.0
pandas==2.2.2
numpy==1.26.4
scikit-learn==1.5.1
joblib==1.4.2
scipy==1.14.1
pillow==10.4.0
duckdb==1.0.0

`

`python
# utils/charts.py
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np


THEME = {
    "bg": "#0a0a1a",
    "card": "rgba(20, 20, 43, 0.8)",
    "card_hover": "#1a1a3e",
    "accent": "#7c3aed",
    "accent_light": "#a78bfa",
    "danger": "#ef4444",
    "warning": "#f59e0b",
    "success": "#10b981",
    "info": "#3b82f6",
    "text": "#e2e8f0",
    "text_muted": "#94a3b8",
    "grid": "rgba(255, 255, 255, 0.08)",
    "gradient_start": "#7c3aed",
    "gradient_end": "#3b82f6",
}


def apply_theme(fig: go.Figure) -> go.Figure:
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, -apple-system, sans-serif", color=THEME["text"]),
        title=dict(font=dict(family="Outfit, sans-serif", size=18, color=THEME["text"])),
        margin=dict(l=20, r=20, t=40, b=20),
        hovermode="closest",
        hoverlabel=dict(
            bgcolor=THEME["card"],
            font_size=13,
            font_family="Outfit, sans-serif",
            bordercolor=THEME["accent"],
        ),
    )
    return fig


def create_bar_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str = "",
    color: str = THEME["accent"],
    height: int = 400,
    sort_values: bool = True,
    top_n: int = None,
    orientation: str = "h",
) -> go.Figure:
    plot_df = df.copy()
    if top_n:
        plot_df = plot_df.head(top_n)
    if sort_values and orientation == "h":
        plot_df = plot_df.sort_values(y, ascending=True)

    fig = go.Figure()
    label_col = "y" if orientation == "h" else "x"
    value_col = "x" if orientation == "h" else "y"
    fig.add_trace(
        go.Bar(
            x=plot_df[y] if orientation == "h" else plot_df[x],
            y=plot_df[x] if orientation == "h" else plot_df[y],
            orientation=orientation,
            marker=dict(
                color=color,
                line=dict(color=color, width=0),
                opacity=0.85,
            ),
            hovertemplate=f"<b>%{{{label_col}}}</b><br>%{{{value_col}}}:,<extra></extra>",
        )
    )
    fig = apply_theme(fig)
    fig.update_layout(
        title=dict(text=title, font=dict(size=16, color=THEME["text"]), x=0.5),
        height=height,
        xaxis=dict(
            showgrid=True,
            gridcolor=THEME["grid"],
            gridwidth=0.5,
            tickfont=dict(size=10),
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor=THEME["grid"],
            gridwidth=0.5,
            tickfont=dict(size=10),
        ),
        showlegend=False,
        margin=dict(l=10, r=10, t=50, b=10),
    )
    return fig


def create_line_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str = "",
    color: str = THEME["accent"],
    height: int = 400,
) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=df[x],
            y=df[y],
            mode="lines+markers",
            line=dict(color=color, width=3),
            marker=dict(size=6, color=color, line=dict(width=2, color=color)),
            fill="tozeroy",
            fillcolor=f"rgba(124, 58, 237, 0.1)",
            hovertemplate=f"<b>%{{x}}</b><br>%{{y:,}}<extra></extra>",
        )
    )
    fig = apply_theme(fig)
    fig.update_layout(
        title=dict(text=title, font=dict(size=16, color=THEME["text"]), x=0.5),
        height=height,
        xaxis=dict(showgrid=True, gridcolor=THEME["grid"], gridwidth=0.5),
        yaxis=dict(showgrid=True, gridcolor=THEME["grid"], gridwidth=0.5),
        showlegend=False,
        margin=dict(l=10, r=10, t=50, b=10),
    )
    return fig


def create_pie_chart(
    df: pd.DataFrame,
    values: str,
    names: str,
    title: str = "",
    height: int = 400,
    top_n: int = 8,
) -> go.Figure:
    plot_df = df.head(top_n).copy()
    fig = go.Figure(
        data=[
            go.Pie(
                labels=plot_df[names],
                values=plot_df[values],
                hole=0.45,
                marker=dict(
                    colors=px.colors.sequential.Viridis[: len(plot_df)],
                    line=dict(color=THEME["bg"], width=2),
                ),
                textinfo="label+percent",
                textposition="outside",
                textfont=dict(size=11, color=THEME["text"]),
                hovertemplate="<b>%{label}</b><br>%{value:,} (%{percent})<extra></extra>",
            )
        ]
    )
    fig = apply_theme(fig)
    fig.update_layout(
        title=dict(text=title, font=dict(size=16, color=THEME["text"]), x=0.5),
        height=height,
        showlegend=False,
        margin=dict(l=10, r=10, t=50, b=10),
    )
    return fig


def create_animated_bubble_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    size: str,
    color: str,
    title: str = "",
    height: int = 500,
) -> go.Figure:
    fig = px.scatter(
        df,
        x=x,
        y=y,
        size=size,
        color=color,
        hover_name=color,
        log_x=True,
        size_max=60,
        title=title,
        color_continuous_scale="Viridis",
    )
    fig.update_traces(marker=dict(line=dict(width=1, color="white")), opacity=0.8)
    fig = apply_theme(fig)
    fig.update_layout(height=height)
    return fig


def create_heatmap(
    df: pd.DataFrame,
    x: str,
    y: str,
    z: str,
    title: str = "",
    height: int = 500,
) -> go.Figure:
    pivot = df.pivot_table(index=y, columns=x, values=z, aggfunc="sum", fill_value=0)
    fig = go.Figure(
        data=go.Heatmap(
            z=pivot.values,
            x=pivot.columns,
            y=pivot.index,
            colorscale="Viridis",
            hovertemplate="Year: %{x}<br>%{y}: %{z:,}<extra></extra>",
        )
    )
    fig = apply_theme(fig)
    fig.update_layout(
        title=dict(text=title, font=dict(size=16, color=THEME["text"]), x=0.5),
        height=height,
        xaxis=dict(title="", tickangle=-45),
        yaxis=dict(title=""),
        margin=dict(l=10, r=10, t=50, b=10),
    )
    return fig


def create_area_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str = "",
    color: str = THEME["accent"],
    height: int = 400,
) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=df[x],
            y=df[y],
            mode="lines",
            line=dict(color=color, width=2),
            fill="tozeroy",
            fillcolor=f"rgba(124, 58, 237, 0.15)",
            hovertemplate=f"<b>%{{x}}</b><br>%{{y:,}}<extra></extra>",
        )
    )
    fig = apply_theme(fig)
    fig.update_layout(
        title=dict(text=title, font=dict(size=16, color=THEME["text"]), x=0.5),
        height=height,
        xaxis=dict(showgrid=True, gridcolor=THEME["grid"]),
        yaxis=dict(showgrid=True, gridcolor=THEME["grid"]),
        showlegend=False,
        margin=dict(l=10, r=10, t=50, b=10),
    )
    return fig


def create_sunburst_chart(
    df: pd.DataFrame,
    path: list,
    values: str,
    title: str = "",
    height: int = 500,
) -> go.Figure:
    fig = px.sunburst(
        df,
        path=path,
        values=values,
        title=title,
        color_continuous_scale="Viridis",
    )
    fig.update_traces(marker=dict(line=dict(color=THEME["bg"], width=1.5)))
    fig = apply_theme(fig)
    fig.update_layout(
        title=dict(text=title, font=dict(size=16, color=THEME["text"]), x=0.5),
        height=height,
        margin=dict(l=10, r=10, t=50, b=10),
    )
    return fig


def create_treemap(
    df: pd.DataFrame,
    path: list,
    values: str,
    title: str = "",
    height: int = 500,
) -> go.Figure:
    fig = px.treemap(
        df,
        path=path,
        values=values,
        title=title,
        color=values,
        color_continuous_scale="Viridis",
    )
    fig.update_traces(
        textinfo="label+value+percent root",
        textfont=dict(size=12),
        marker=dict(line=dict(color=THEME["bg"], width=1)),
    )
    fig = apply_theme(fig)
    fig.update_layout(
        title=dict(text=title, font=dict(size=16, color=THEME["text"]), x=0.5),
        height=height,
        margin=dict(l=10, r=10, t=50, b=10),
    )
    return fig


def create_scatter_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str = "",
    color: str = THEME["accent"],
    height: int = 400,
    size_col: str = None,
) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=df[x],
            y=df[y],
            mode="markers",
            marker=dict(
                color=color,
                size=df[size_col] / df[size_col].max() * 30 + 5 if size_col and size_col in df.columns else 10,
                opacity=0.7,
                line=dict(width=1, color="white"),
            ),
            hovertemplate=f"<b>%{{x}}</b><br>%{{y:,}}<extra></extra>",
        )
    )
    fig = apply_theme(fig)
    fig.update_layout(
        title=dict(text=title, font=dict(size=16, color=THEME["text"]), x=0.5),
        height=height,
        xaxis=dict(showgrid=True, gridcolor=THEME["grid"]),
        yaxis=dict(showgrid=True, gridcolor=THEME["grid"]),
        showlegend=False,
        margin=dict(l=10, r=10, t=50, b=10),
    )
    return fig


def create_timeline_chart(
    df: pd.DataFrame,
    dates: str,
    values: str,
    title: str = "",
    color: str = THEME["accent"],
    height: int = 400,
) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=df[dates],
            y=df[values],
            mode="lines+markers",
            line=dict(color=color, width=2),
            marker=dict(size=5, color=color),
            fill="tozeroy",
            fillcolor=f"rgba(124, 58, 237, 0.1)",
            hovertemplate="%{x|%Y-%m-%d}<br>%{y:,}<extra></extra>",
        )
    )
    fig = apply_theme(fig)
    fig.update_layout(
        title=dict(text=title, font=dict(size=16, color=THEME["text"]), x=0.5),
        height=height,
        xaxis=dict(showgrid=True, gridcolor=THEME["grid"]),
        yaxis=dict(showgrid=True, gridcolor=THEME["grid"]),
        showlegend=False,
        margin=dict(l=10, r=10, t=50, b=10),
    )
    return fig


def create_forecast_chart(
    historical: pd.DataFrame,
    forecast: pd.DataFrame,
    x: str,
    y: str,
    title: str = "",
    height: int = 450,
) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=historical[x],
            y=historical[y],
            mode="lines+markers",
            name="Historical",
            line=dict(color=THEME["accent"], width=3),
            marker=dict(size=6, color=THEME["accent"]),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=forecast[x],
            y=forecast[y],
            mode="lines+markers",
            name="Forecast",
            line=dict(color=THEME["danger"], width=3, dash="dash"),
            marker=dict(size=6, color=THEME["danger"]),
        )
    )
    fig = apply_theme(fig)
    fig.update_layout(
        title=dict(text=title, font=dict(size=16, color=THEME["text"]), x=0.5),
        height=height,
        xaxis=dict(showgrid=True, gridcolor=THEME["grid"]),
        yaxis=dict(showgrid=True, gridcolor=THEME["grid"]),
        legend=dict(
            font=dict(color=THEME["text"]),
            bgcolor="rgba(0,0,0,0.3)",
            bordercolor=THEME["grid"],
        ),
        margin=dict(l=10, r=10, t=50, b=10),
    )
    return fig


def create_feature_importance_chart(
    features: list,
    importances: list,
    title: str = "Feature Importance",
    height: int = 400,
) -> go.Figure:
    df_imp = pd.DataFrame({"feature": features, "importance": importances})
    df_imp = df_imp.sort_values("importance", ascending=True)
    fig = go.Figure()
    colors = [THEME["accent"]] * len(df_imp)
    fig.add_trace(
        go.Bar(
            x=df_imp["importance"],
            y=df_imp["feature"],
            orientation="h",
            marker=dict(
                color=df_imp["importance"],
                colorscale="Viridis",
                line=dict(width=0),
            ),
            hovertemplate="<b>%{y}</b><br>Importance: %{x:.3f}<extra></extra>",
        )
    )
    fig = apply_theme(fig)
    fig.update_layout(
        title=dict(text=title, font=dict(size=16, color=THEME["text"]), x=0.5),
        height=height,
        xaxis=dict(showgrid=True, gridcolor=THEME["grid"]),
        yaxis=dict(showgrid=False),
        showlegend=False,
        margin=dict(l=10, r=10, t=50, b=10),
    )
    return fig

`

`python
# utils/data_loader.py
# utils/data_loader.py
import duckdb
import streamlit as st
from pathlib import Path
import pandas as pd

@st.cache_resource
def get_db_connection():
    data_path = Path("data/globalterrorismdb_0718dist.csv")
    if not data_path.exists():
        data_path = Path("AI_Terrorism_Dashboard/data/globalterrorismdb_0718dist.csv")
    if not data_path.exists():
        st.error("Dataset not found. Please place 'globalterrorismdb_0718dist.csv' in the data/ directory.")
        return None

    conn = duckdb.connect(':memory:')
    
    try:
        conn.execute(f"CREATE TABLE raw_gtd AS SELECT * FROM read_csv_auto('{data_path}', ignore_errors=true)")
    except Exception as e:
        st.error(f"Failed to load data: {e}")
        return None

    conn.execute('''
        CREATE TABLE gtd AS 
        SELECT 
            TRY_CAST(iyear AS INTEGER) AS year,
            TRY_CAST(imonth AS INTEGER) AS month,
            TRY_CAST(iday AS INTEGER) AS day,
            country_txt AS country,
            region_txt AS region,
            COALESCE(provstate, 'Unknown') AS province,
            COALESCE(city, 'Unknown') AS city,
            TRY_CAST(latitude AS DOUBLE) AS latitude,
            TRY_CAST(longitude AS DOUBLE) AS longitude,
            attacktype1_txt AS attack_type,
            COALESCE(targtype1_txt, 'Unknown') AS target_type,
            COALESCE(gname, 'Unknown') AS group_name,
            weaptype1_txt AS weapon_type,
            COALESCE(TRY_CAST(nkill AS INTEGER), 0) AS fatalities,
            COALESCE(TRY_CAST(nwound AS INTEGER), 0) AS injuries,
            COALESCE(TRY_CAST(success AS INTEGER), 0) AS success,
            COALESCE(TRY_CAST(suicide AS INTEGER), 0) AS suicide,
            COALESCE(TRY_CAST(multiple AS INTEGER), 0) AS multiple_attacks,
            COALESCE(TRY_CAST(property AS INTEGER), 0) AS property_damage,
            COALESCE(natlty1_txt, 'Unknown') AS nationality,
            COALESCE(weapsubtype1_txt, 'Unknown') AS weapon_subtype,
            COALESCE(attacktype2_txt, 'Unknown') AS attack_type_2,
            COALESCE(weaptype2_txt, 'Unknown') AS weapon_type_2,
            COALESCE(targtype2_txt, 'Unknown') AS target_type_2,
            COALESCE(gsubname, 'Unknown') AS group_subname,
            COALESCE(gname2, 'Unknown') AS group_name_2,
            COALESCE(addnotes, 'Unknown') AS additional_notes,
            COALESCE(scite1, 'Unknown') AS source_1,
            COALESCE(scite2, 'Unknown') AS source_2,
            COALESCE(scite3, 'Unknown') AS source_3,
            COALESCE(dbsource, 'Unknown') AS database_source,
            COALESCE(summary, 'Unknown') AS summary,
            COALESCE(motive, 'Unknown') AS motive,
            COALESCE(TRY_CAST(ishostkid AS INTEGER), 0) AS hostage_related,
            COALESCE(TRY_CAST(nhostkid AS INTEGER), 0) AS hostages_taken,
            COALESCE(TRY_CAST(nhours AS INTEGER), 0) AS hours_held,
            COALESCE(TRY_CAST(ndays AS INTEGER), 0) AS days_held,
            COALESCE(TRY_CAST(ransom AS INTEGER), 0) AS ransom_paid,
            COALESCE(TRY_CAST(ransomamt AS INTEGER), 0) AS ransom_amount
        FROM raw_gtd
        WHERE iyear IS NOT NULL 
    ''')
    
    conn.execute("DROP TABLE raw_gtd")
    return conn

@st.cache_data
def get_summary_stats(_conn) -> dict:
    if _conn is None:
        return {}
    res = _conn.execute('''
        SELECT 
            COUNT(*) as total_incidents,
            COUNT(DISTINCT country) as total_countries,
            SUM(fatalities) as total_fatalities,
            SUM(injuries) as total_injuries,
            COUNT(DISTINCT group_name) as total_groups,
            COUNT(DISTINCT attack_type) as total_attack_types,
            MIN(year) as min_year,
            MAX(year) as max_year
        FROM gtd
    ''').fetchone()
    
    top_country = _conn.execute("SELECT country FROM gtd GROUP BY country ORDER BY COUNT(*) DESC LIMIT 1").fetchone()
    top_group = _conn.execute("SELECT group_name FROM gtd GROUP BY group_name ORDER BY COUNT(*) DESC LIMIT 1").fetchone()
    top_attack = _conn.execute("SELECT attack_type FROM gtd GROUP BY attack_type ORDER BY COUNT(*) DESC LIMIT 1").fetchone()
    top_weapon = _conn.execute("SELECT weapon_type FROM gtd GROUP BY weapon_type ORDER BY COUNT(*) DESC LIMIT 1").fetchone()

    return {
        "total_incidents": res[0] or 0,
        "total_countries": res[1] or 0,
        "total_fatalities": int(res[2] or 0),
        "total_injuries": int(res[3] or 0),
        "total_groups": res[4] or 0,
        "total_attack_types": res[5] or 0,
        "year_range": f"{res[6]} - {res[7]}" if res[6] else "N/A",
        "most_affected_country": top_country[0] if top_country else "N/A",
        "most_active_group": top_group[0] if top_group else "N/A",
        "most_common_attack": top_attack[0] if top_attack else "N/A",
        "most_common_weapon": top_weapon[0] if top_weapon else "N/A"
    }

def build_where_clause(years=None, countries=None, regions=None, attack_types=None, weapon_types=None, groups=None):
    conditions = ["1=1"]
    if years and len(years) == 2:
        conditions.append(f"year BETWEEN {years[0]} AND {years[1]}")
    def esc(lst): return [str(x).replace("'", "''") for x in lst]
    if countries:
        conditions.append("country IN (" + ",".join(f"'{c}'" for c in esc(countries)) + ")")
    if regions:
        conditions.append("region IN (" + ",".join(f"'{r}'" for r in esc(regions)) + ")")
    if attack_types:
        conditions.append("attack_type IN (" + ",".join(f"'{a}'" for a in esc(attack_types)) + ")")
    if weapon_types:
        conditions.append("weapon_type IN (" + ",".join(f"'{w}'" for w in esc(weapon_types)) + ")")
    if groups:
        conditions.append("group_name IN (" + ",".join(f"'{g}'" for g in esc(groups)) + ")")
    return " AND ".join(conditions)

`

`python
# utils/helper.py
import pandas as pd
import streamlit as st
from typing import Any


def format_number(num: Any) -> str:
    try:
        num = float(num)
        if num >= 1_000_000_000:
            return f"{num / 1_000_000_000:.1f}B"
        if num >= 1_000_000:
            return f"{num / 1_000_000:.1f}M"
        if num >= 1_000:
            return f"{num / 1_000:.1f}K"
        return f"{int(num):,}"
    except (ValueError, TypeError):
        return "0"


def get_top_values(conn, column: str, n: int = 10) -> pd.DataFrame:
    try:
        return conn.execute(f"SELECT {column}, COUNT(*) as count FROM gtd GROUP BY {column} ORDER BY count DESC LIMIT {n}").df()
    except Exception:
        return pd.DataFrame()


def get_year_range(conn) -> tuple:
    try:
        res = conn.execute("SELECT MIN(year), MAX(year) FROM gtd").fetchone()
        if res and res[0] is not None:
            return (int(res[0]), int(res[1]))
    except Exception:
        pass
    return (1970, 2017)


def get_country_list(conn) -> list:
    try:
        return [r[0] for r in conn.execute("SELECT DISTINCT country FROM gtd WHERE country IS NOT NULL ORDER BY country").fetchall()]
    except Exception:
        return []


def get_region_list(conn) -> list:
    try:
        return [r[0] for r in conn.execute("SELECT DISTINCT region FROM gtd WHERE region IS NOT NULL ORDER BY region").fetchall()]
    except Exception:
        return []


def get_attack_type_list(conn) -> list:
    try:
        return [r[0] for r in conn.execute("SELECT DISTINCT attack_type FROM gtd WHERE attack_type IS NOT NULL ORDER BY attack_type").fetchall()]
    except Exception:
        return []


def get_weapon_type_list(conn) -> list:
    try:
        return [r[0] for r in conn.execute("SELECT DISTINCT weapon_type FROM gtd WHERE weapon_type IS NOT NULL ORDER BY weapon_type").fetchall()]
    except Exception:
        return []


def get_group_list(conn) -> list:
    try:
        return [r[0] for r in conn.execute("SELECT DISTINCT group_name FROM gtd WHERE group_name IS NOT NULL ORDER BY group_name").fetchall()]
    except Exception:
        return []


def get_target_type_list(conn) -> list:
    try:
        return [r[0] for r in conn.execute("SELECT DISTINCT target_type FROM gtd WHERE target_type IS NOT NULL ORDER BY target_type").fetchall()]
    except Exception:
        return []


def get_country_data(conn, country: str) -> pd.DataFrame:
    try:
        return conn.execute(f"SELECT * FROM gtd WHERE country = ?", (country,)).df()
    except Exception:
        return pd.DataFrame()


def get_region_data(conn, region: str) -> pd.DataFrame:
    try:
        return conn.execute(f"SELECT * FROM gtd WHERE region = ?", (region,)).df()
    except Exception:
        return pd.DataFrame()


def get_threat_level(fatalities: int, incidents: int) -> tuple:
    score = (fatalities * 0.6) + (incidents * 0.4)
    if score > 10000:
        return "CRITICAL", "#ff0040"
    if score > 5000:
        return "HIGH", "#ff6600"
    if score > 1000:
        return "ELEVATED", "#ffcc00"
    if score > 100:
        return "GUARDED", "#4dabf7"
    return "LOW", "#40c057"


`

`python
# utils/preprocessing.py
# utils/preprocessing.py
import pandas as pd
import numpy as np
import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib
from pathlib import Path

def prepare_prediction_data(conn):
    df = conn.execute("SELECT country, region, weapon_type, target_type, attack_type, group_name, success, suicide, fatalities, injuries, multiple_attacks, property_damage FROM gtd").df()
    feature_cols = []
    encoders = {}

    cat_features = {
        "country": "country",
        "region": "region",
        "weapon_type": "weapon_type",
        "target_type": "target_type",
        "attack_type": "attack_type",
        "group_name": "group_name",
    }

    X = pd.DataFrame()

    for col, src in cat_features.items():
        if src in df.columns:
            le = LabelEncoder()
            X[col] = le.fit_transform(df[src].fillna("Unknown").astype(str))
            encoders[col] = le
            feature_cols.append(col)

    for c in ["success", "suicide", "fatalities", "injuries", "multiple_attacks", "property_damage"]:
        if c in df.columns:
            X[c] = df[c].fillna(0).astype(int)
            feature_cols.append(c)

    y = (df["fatalities"] > 0).astype(int) if "fatalities" in df.columns else pd.Series(np.zeros(len(df)))

    X = X.fillna(0)
    return X, y, feature_cols, encoders

@st.cache_data
def train_prediction_model(_conn):
    X, y, feature_cols, encoders = prepare_prediction_data(_conn)
    if X.shape[1] == 0:
        return None, None, None, None

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=15,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1,
        class_weight="balanced",
    )
    model.fit(X_train, y_train)

    accuracy = model.score(X_test, y_test)
    return model, encoders, feature_cols, accuracy

def predict_attack(
    model, encoders: dict, feature_cols: list, country: str, region: str,
    weapon: str, target: str, attack_type: str, group: str, success: int,
    suicide: int, fatalities: int, injuries: int,
):
    input_data = {}
    country_enc = encoders.get("country")
    region_enc = encoders.get("region")
    weapon_enc = encoders.get("weapon_type")
    target_enc = encoders.get("target_type")
    attack_enc = encoders.get("attack_type")
    group_enc = encoders.get("group_name")

    if country_enc and "country" in feature_cols:
        input_data["country"] = country_enc.transform([country])[0] if country in country_enc.classes_ else -1
    if region_enc and "region" in feature_cols:
        input_data["region"] = region_enc.transform([region])[0] if region in region_enc.classes_ else -1
    if weapon_enc and "weapon_type" in feature_cols:
        input_data["weapon_type"] = weapon_enc.transform([weapon])[0] if weapon in weapon_enc.classes_ else -1
    if target_enc and "target_type" in feature_cols:
        input_data["target_type"] = target_enc.transform([target])[0] if target in target_enc.classes_ else -1
    if attack_enc and "attack_type" in feature_cols:
        input_data["attack_type"] = attack_enc.transform([attack_type])[0] if attack_type in attack_enc.classes_ else -1
    if group_enc and "group_name" in feature_cols:
        input_data["group_name"] = group_enc.transform([group])[0] if group in group_enc.classes_ else -1

    for c, val in [("success", success), ("suicide", suicide), ("fatalities", fatalities), ("injuries", injuries)]:
        if c in feature_cols:
            input_data[c] = val

    for col in feature_cols:
        if col not in input_data:
            input_data[col] = 0

    input_df = pd.DataFrame([input_data])[feature_cols]

    prediction = model.predict(input_df)[0]
    probability = model.predict_proba(input_df)[0]

    return prediction, probability

`