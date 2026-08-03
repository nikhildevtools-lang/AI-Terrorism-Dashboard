import streamlit as st


def show():
    st.title("ℹ About")
    st.caption(
        "Information about the AI Terrorism Intelligence Dashboard project."
    )

    st.divider()

    # ==========================
    # Project Overview
    # ==========================
    st.subheader("📖 Project Overview")

    st.write(
        """
The **AI Terrorism Intelligence Dashboard** is an advanced analytics platform
that uses **Machine Learning**, **Data Visualization**, and the
**Global Terrorism Database (GTD)** to analyze worldwide terrorism incidents.

The dashboard transforms raw historical data into meaningful intelligence
through interactive charts, predictive analytics, forecasting models,
and automated reports for researchers, analysts, and policymakers.
"""
    )

    st.divider()

    # ==========================
    # Dataset
    # ==========================

    st.subheader("🌍 Dataset Information")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Years", "1970–2017")
    c2.metric("Incidents", "180K+")
    c3.metric("Countries", "200+")
    c4.metric("Attributes", "120+")

    st.info(
        """
**Global Terrorism Database (GTD)**

The GTD is the world's largest open-source database of terrorist attacks,
maintained by the National Consortium for the Study of Terrorism and
Responses to Terrorism (START).
"""
    )

    st.divider()

    # ==========================
    # Technology Stack
    # ==========================

    st.subheader("🛠 Technology Stack")

    col1, col2 = st.columns(2)

    with col1:
        st.success("🖥 Frontend\n\nStreamlit")
        st.success("📊 Visualization\n\nPlotly")
        st.success("🧠 Machine Learning\n\nScikit-learn")

    with col2:
        st.success("📂 Data Processing\n\nPandas + NumPy")
        st.success("💾 Model Storage\n\nJoblib")
        st.success("🐍 Language\n\nPython")

    st.divider()

    # ==========================
    # Machine Learning
    # ==========================

    st.subheader("🤖 Machine Learning Models")

    with st.expander("Attack Prediction Model", expanded=True):
        st.write("""
**Algorithm:** Random Forest Classifier

Predicts attack severity and estimated fatalities using historical
terrorism data and incident characteristics.
""")

    with st.expander("Trend Forecasting"):
        st.write("""
**Algorithm:** Linear Regression

Forecasts future terrorism trends and analyzes long-term changes in
incident frequency.
""")

    st.divider()

    # ==========================
    # Features
    # ==========================

    st.subheader("✨ Key Features")

    features = [
        "🌍 Interactive Global Threat Map",
        "📊 Country-wise Analytics",
        "🤖 AI Attack Prediction",
        "📈 Trend Forecasting",
        "🧠 Automated Intelligence Report",
        "🔍 Data Explorer & Filtering",
        "📉 Statistical Analysis",
        "🌙 Modern Dark Dashboard",
        "📱 Responsive Interface",
    ]

    left, right = st.columns(2)

    for i, feature in enumerate(features):
        if i % 2 == 0:
            left.success(feature)
        else:
            right.success(feature)

    st.divider()

    # ==========================
    # Dashboard Modules
    # ==========================

    st.subheader("📌 Dashboard Modules")

    modules = {
        "🏠 Dashboard": "Overall statistics and KPIs",
        "🌍 Global Threat Map": "Interactive world map",
        "🌎 Country Analysis": "Country-specific insights",
        "🤖 Prediction": "AI attack prediction",
        "📈 Forecast": "Future trend analysis",
        "🧠 Intelligence Report": "Automated strategic report",
        "🔎 Data Explorer": "Search and filter incidents",
    }

    for title, desc in modules.items():
        with st.container(border=True):
            st.markdown(f"### {title}")
            st.write(desc)

    st.divider()

    # ==========================
    # Author
    # ==========================

    st.subheader("👨‍💻 About This Project")

    st.write(
        """
This dashboard was developed as an academic project demonstrating the use of
Machine Learning, Data Analytics, and Interactive Visualization for
terrorism intelligence analysis.

It combines modern Python libraries with analytical techniques to transform
historical terrorism data into actionable insights.
"""
    )

    st.divider()

    st.caption(
        "AI Terrorism Intelligence Dashboard • Version 1.0 • Built with Python, Streamlit, Plotly & Scikit-learn"
    )