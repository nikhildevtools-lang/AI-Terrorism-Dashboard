# pyrefly: ignore [missing-import]
import streamlit as st
import pandas as pd
from utils.charts import (
    THEME,
    create_bar_chart,
    create_line_chart,
    create_pie_chart,
    create_heatmap,
    create_treemap,
)
from utils.helper import format_number
from utils.data_loader import get_summary_stats


def chart_panel(fig, key: str = None):
    with st.container():
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False}, key=key)


def show(df: pd.DataFrame):
    if df.empty:
        st.warning("No data available. Please upload the GTD dataset.")
        return

    stats = get_summary_stats(df)
    year_range = stats.get("year_range", "1970 - 2017")
    most_affected = stats.get("most_affected_country", "N/A")
    most_common_attack = stats.get("most_common_attack", "N/A")

    st.markdown(
        f"""
        <section class="home-hero animate-in">
            <div class="hero-kicker">Global Terrorism Database Intelligence</div>
            <h1>AI Terrorism Intelligence Dashboard</h1>
            <p>
                Analyze long-term incident patterns, discover regional hotspots, and generate a clearer
                operational picture from {format_number(stats["total_incidents"])} recorded GTD events.
            </p>
            <div class="hero-meta">
                <span>{year_range}</span>
                <span>{stats["total_countries"]} countries</span>
                <span>Top country: {most_affected}</span>
                <span>Common attack: {most_common_attack}</span>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="section-label">Key Metrics</div>', unsafe_allow_html=True)

    cols = st.columns(6)
    metrics = [
        ("INC", format_number(stats["total_incidents"]), "Total Incidents", "blue"),
        ("CTR", stats["total_countries"], "Countries", "green"),
        ("FAT", format_number(stats["total_fatalities"]), "Fatalities", "red"),
        ("INJ", format_number(stats["total_injuries"]), "Injuries", "amber"),
        ("GRP", format_number(stats["total_groups"]), "Groups", "violet"),
        ("ATK", stats["total_attack_types"], "Attack Types", "cyan"),
    ]

    for idx, (icon, value, label, tone) in enumerate(metrics):
        with cols[idx]:
            st.markdown(
                f"""
                <div class="stat-card metric-{tone} animate-in delay-{idx + 1}">
                    <div class="stat-icon">{icon}</div>
                    <div class="stat-value">{value}</div>
                    <div class="stat-label">{label}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown('<div class="section-label">Activity Overview</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        if "year" in df.columns:
            yearly = df.groupby("year").size().reset_index(name="count")
            fig = create_line_chart(yearly, "year", "count", "Attacks by Year", THEME["accent"])
            chart_panel(fig, "home_yearly_attacks")

    with col2:
        if "country" in df.columns:
            top_countries = df["country"].value_counts().head(10).reset_index()
            top_countries.columns = ["country", "count"]
            fig = create_bar_chart(
                top_countries,
                "country",
                "count",
                "Top 10 Affected Countries",
                THEME["danger"],
                orientation="h",
            )
            chart_panel(fig, "home_top_countries")

    st.markdown('<div class="section-label">Attack Composition</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        if "attack_type" in df.columns:
            attack_counts = df["attack_type"].value_counts().head(8).reset_index()
            attack_counts.columns = ["attack_type", "count"]
            fig = create_pie_chart(attack_counts, "count", "attack_type", "Attack Type Distribution")
            chart_panel(fig, "home_attack_types")

    with col2:
        if "weapon_type" in df.columns:
            weapon_counts = df["weapon_type"].value_counts().head(8).reset_index()
            weapon_counts.columns = ["weapon_type", "count"]
            fig = create_pie_chart(weapon_counts, "count", "weapon_type", "Weapon Type Distribution")
            chart_panel(fig, "home_weapon_types")

    st.markdown('<div class="section-label">Actor And Region Patterns</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        if "group_name" in df.columns:
            top_groups = df["group_name"].value_counts().head(10).reset_index()
            top_groups.columns = ["group_name", "count"]
            fig = create_bar_chart(
                top_groups,
                "group_name",
                "count",
                "Top 10 Terrorist Groups",
                THEME["warning"],
                orientation="h",
            )
            chart_panel(fig, "home_top_groups")

    with col2:
        if all(c in df.columns for c in ["year", "region"]):
            heatmap_data = df.groupby(["year", "region"]).size().reset_index(name="count")
            fig = create_heatmap(heatmap_data, "year", "region", "count", "Regional Activity Heatmap", height=450)
            chart_panel(fig, "home_region_heatmap")

    if "group_name" in df.columns and "region" in df.columns:
        st.markdown('<div class="section-label">Global Drilldown</div>', unsafe_allow_html=True)
        treemap_data = df.groupby(["region", "country", "group_name"]).size().reset_index(name="count")
        treemap_data = treemap_data.sort_values("count", ascending=False).head(100)
        fig = create_treemap(
            treemap_data,
            ["region", "country", "group_name"],
            "count",
            "Global Terrorism Overview - Region to Country to Group",
        )
        chart_panel(fig, "home_global_treemap")

    st.markdown(
        """
        <div class="data-source">
            Data Source: Global Terrorism Database (GTD) | National Consortium for the Study of Terrorism and Responses to Terrorism (START)
        </div>
        """,
        unsafe_allow_html=True,
    )
