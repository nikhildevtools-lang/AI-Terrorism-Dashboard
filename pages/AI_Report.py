import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression

from utils.helper import format_number, get_threat_level
from utils.data_loader import get_summary_stats


def show(df: pd.DataFrame):

    if df.empty:
        st.warning("No data available.")
        return

    stats = get_summary_stats(df)

    year_values = pd.to_numeric(df["year"], errors="coerce")
    valid_years = year_values.dropna()

    trend_direction = 0
    r2 = 0

    if len(valid_years) > 1:
        yearly = (
            df.assign(year=year_values)
            .dropna(subset=["year"])
            .groupby("year")
            .size()
            .reset_index(name="count")
        )

        if len(yearly) > 1:
            X = yearly[["year"]]
            y = yearly["count"]

            model = LinearRegression()
            model.fit(X, y)

            trend_direction = model.coef_[0]
            r2 = model.score(X, y)

    threat_level, threat_color = get_threat_level(
        stats["total_fatalities"],
        stats["total_incidents"],
    )

    st.title("🧠 Global Terrorism Intelligence Report")
    st.caption("Automatically generated from the Global Terrorism Database")

    st.divider()

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Threat Level",
        threat_level,
    )

    c2.metric(
        "Trend",
        "Increasing" if trend_direction > 0 else "Decreasing",
    )

    c3.metric(
        "Model Reliability",
        f"{r2*100:.1f}%"
    )

    st.divider()

    st.subheader("Executive Summary")

    st.write(
        f"""
A total of **{format_number(stats["total_incidents"])}** incidents were recorded
across **{stats["total_countries"]}** countries.

The database reports:

- **{format_number(stats["total_fatalities"])} fatalities**
- **{format_number(stats["total_injuries"])} injuries**
- **{format_number(stats["total_groups"])} terrorist organizations**
- **{stats["total_attack_types"]} attack types**
- **{stats["total_weapons"]} weapon types**
"""
    )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Geographic Analysis")

        st.info(
            f"""
Most affected country:

**{stats["most_affected_country"]}**
"""
        )

    with col2:
        st.subheader("Groups")

        st.info(
            f"""
Most active group:

**{stats["most_active_group"]}**
"""
        )

    st.divider()

    st.subheader("Attack Methodology")

    c1, c2 = st.columns(2)

    c1.metric(
        "Most Common Attack",
        stats["most_common_attack"],
    )

    c2.metric(
        "Most Common Weapon",
        stats["most_common_weapon"],
    )

    st.divider()

    st.subheader("Deadliest Incidents")

    if "fatalities" in df.columns:

        cols = [
            "year",
            "country",
            "city",
            "attack_type",
            "group_name",
            "fatalities",
            "injuries",
        ]

        cols = [c for c in cols if c in df.columns]

        top = (
            df.nlargest(10, "fatalities")[cols]
            .reset_index(drop=True)
        )

        st.dataframe(
            top,
            use_container_width=True,
            hide_index=True,
        )

    st.divider()

    st.subheader("Recommendations")

    recommendations = [
        "Increase intelligence sharing between countries.",
        "Focus surveillance on high-risk regions.",
        "Improve emergency response capabilities.",
        "Strengthen protection of critical infrastructure.",
        "Use predictive analytics for resource allocation.",
    ]

    for r in recommendations:
        st.success(r)

    st.divider()

    st.download_button(
        "📥 Download Report",
        data=str(stats),
        file_name="terrorism_report.txt",
    )