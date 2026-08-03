import streamlit as st
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))

st.set_page_config(
    page_title="AI Terrorism Intelligence Dashboard",
    page_icon="AI",
    layout="wide",
    initial_sidebar_state="expanded",
)

css_path = Path(__file__).parent / "assets" / "style.css"
st.markdown(css_path.read_text(encoding="utf-8"), unsafe_allow_html=True)

from utils.data_loader import get_clean_data, get_clean_uploaded_data, list_local_csv_files
from utils.helper import get_year_range


PAGES = {
    "Dashboard": "Home",
    "Threat Map": "Global_Threat_Map",
    "Country Analysis": "Country_Analysis",
    "Attack Prediction": "Attack_Prediction",
    "Forecasting": "Forecasting",
    "Intelligence Report": "AI_Report",
    "Data Explorer": "Data_Explorer",
    "About": "About",
}


def navigate_to(page_name):
    st.session_state.current_page = page_name
    st.rerun()


if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"

with st.sidebar:
    st.markdown(
        """
        <div style="text-align: center; padding: 1rem 0.5rem;">
            <div class="brand-mark">AI</div>
            <div class="sidebar-title">AI Intelligence<br>Dashboard</div>
            <div style="font-size: 0.7rem; color: #64748b; margin-top: 0.3rem; letter-spacing: 0.1em;">
                TERRORISM ANALYSIS PLATFORM
            </div>
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

    st.markdown("---")
    st.markdown('<div class="sidebar-section-label">Dataset Source</div>', unsafe_allow_html=True)

    local_files = list_local_csv_files()
    uploaded_file = st.file_uploader("Upload CSV dataset", type=["csv"], key="csv_dataset_upload")

    source_options = ["Offline data folder CSV"]
    if uploaded_file is not None:
        source_options.insert(0, "Uploaded CSV")

    selected_source = st.radio(
        "Which data do you want to use?",
        source_options,
        index=0,
        key="dataset_source_choice",
    )

    selected_local_file = None
    if selected_source == "Offline data folder CSV":
        if local_files:
            default_index = local_files.index("globalterrorismdb_0718dist.csv") if "globalterrorismdb_0718dist.csv" in local_files else 0
            selected_local_file = st.selectbox(
                "Data folder CSV",
                local_files,
                index=default_index,
                key="local_dataset_file",
            )
        else:
            st.error("No CSV files found in the data folder.")

    try:
        if selected_source == "Uploaded CSV" and uploaded_file is not None:
            df = get_clean_uploaded_data(uploaded_file.name, uploaded_file.getvalue())
            dataset_label = f"Uploaded: {uploaded_file.name}"
        elif selected_local_file:
            df = get_clean_data(selected_local_file)
            dataset_label = f"Offline: {selected_local_file}"
        else:
            df = get_clean_data()
            dataset_label = "Offline: default dataset"
    except Exception as exc:
        st.error(f"Could not load the selected CSV: {exc}")
        df = get_clean_data()
        dataset_label = "Offline: default dataset"

    st.session_state.data_loaded = not df.empty
    st.session_state.df = df
    st.session_state.dataset_label = dataset_label

    st.markdown(
        f"""
        <div class="dataset-status">
            <div class="dataset-status-label">Active dataset</div>
            <div class="dataset-status-name">{dataset_label}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    for label, page_file in PAGES.items():
        if st.button(label, key=f"nav_{page_file}", use_container_width=True):
            navigate_to(page_file)

    st.markdown("---")

    if not df.empty:
        year_range = get_year_range(df)
        st.markdown(
            f"""
            <div style="padding: 0.8rem; text-align: center; font-size: 0.75rem; color: #64748b;">
                <div>Data Coverage</div>
                <div style="font-size: 1rem; font-weight: 700; color: #e2e8f0; margin-top: 0.2rem;">
                    {year_range[0]} - {year_range[1]}
                </div>
                <div style="font-size: 0.7rem; margin-top: 0.3rem;">
                    {len(df):,} Incidents Recorded
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div style="padding: 1rem 0.5rem; text-align: center; font-size: 0.65rem; color: #475569;">
            AI Terrorism Intelligence Dashboard v1.0<br>
            Built with Streamlit and Machine Learning
        </div>
        """,
        unsafe_allow_html=True,
    )


def main():
    page = st.session_state.current_page
    if page == "Home":
        from pages.Home import show
        show(df)
    elif page == "Global_Threat_Map":
        from pages.Global_Threat_Map import show
        show(df)
    elif page == "Country_Analysis":
        from pages.Country_Analysis import show
        show(df)
    elif page == "Attack_Prediction":
        from pages.Attack_Prediction import show
        show(df)
    elif page == "Forecasting":
        from pages.Forecasting import show
        show(df)
    elif page == "AI_Report":
        from pages.AI_Report import show
        show(df)
    elif page == "Data_Explorer":
        from pages.Data_Explorer import show
        show(df)
    elif page == "About":
        from pages.About import show
        show()


if __name__ == "__main__":
    main()
