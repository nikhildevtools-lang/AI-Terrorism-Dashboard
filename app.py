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
        border: 1px solid #ff2a5f !important;
        background: rgba(255, 42, 95, 0.08) !important;
        box-shadow: 0 0 15px rgba(255, 42, 95, 0.6), inset 0 0 10px rgba(255, 42, 95, 0.3) !important;
        color: #ff2a5f !important;
        border-radius: 8px !important;
        transition: all 0.3s ease !important;
    }}
    section[data-testid="stSidebar"] .stButton > button[kind="primary"] p {{
        color: #ff2a5f !important;
        font-weight: 600 !important;
    }}
    section[data-testid="stSidebar"] .stButton > button[kind="secondary"] {{
        background: transparent !important;
        box-shadow: none !important;
        border: none !important;
        color: #94a3b8 !important;
        text-align: left !important;
        justify-content: flex-start !important;
    }}
    section[data-testid="stSidebar"] .stButton > button[kind="secondary"] p {{
        color: #94a3b8 !important;
    }}
    section[data-testid="stSidebar"] .stButton > button[kind="secondary"]:hover {{
        background: rgba({rgb_channels}, 0.15) !important;
        border-color: rgba({rgb_channels}, 0.3) !important;
        color: #e2e8f0 !important;
    }}
    section[data-testid="stSidebar"] .stButton > button[kind="secondary"]:hover p {{
        color: #e2e8f0 !important;
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
