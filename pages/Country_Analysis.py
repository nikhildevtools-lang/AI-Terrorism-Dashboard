import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils.charts import (
    THEME, create_bar_chart, create_line_chart, create_pie_chart, create_treemap, apply_theme,
)
from utils.helper import format_number, get_country_list, get_country_data, get_threat_level


def show(df: pd.DataFrame):
    if df.empty:
        st.warning("No data available.")
        return

    st.markdown(
        """
        <div class="glass-card" style="text-align: center; padding: 2rem; margin-bottom: 2rem;">
            <h1 style="font-size: 2.2rem; margin-bottom: 0.3rem;">
                <span class="gradient-text">🌎 Country Analysis</span>
            </h1>
            <p style="color: #94a3b8; max-width: 600px; margin: 0 auto;">
                Deep dive into terrorism activity by country with comprehensive analytics.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    countries = get_country_list(df)

    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        selected_country = st.selectbox(
            "Select a Country",
            options=countries,
            index=countries.index("Iraq") if "Iraq" in countries else 0,
        )

    country_df = get_country_data(df, selected_country)

    if country_df.empty:
        st.warning(f"No data available for {selected_country}.")
        return

    total_fatalities = int(country_df["fatalities"].sum())
    total_injuries = int(country_df["injuries"].sum())
    total_incidents = len(country_df)
    total_groups = country_df["group_name"].nunique()
    threat_level, threat_color = get_threat_level(total_fatalities, total_incidents)
    year_range = f"{int(country_df['year'].min())} - {int(country_df['year'].max())}"

    st.markdown(
        f"""
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
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        yearly = country_df.groupby("year").agg(
            incidents=("year", "size"),
            fatalities=("fatalities", "sum"),
            injuries=("injuries", "sum"),
        ).reset_index()

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=yearly["year"], y=yearly["incidents"],
            mode="lines+markers", name="Incidents",
            line=dict(color=THEME["accent"], width=3),
            marker=dict(size=6),
            yaxis="y",
        ))
        fig.add_trace(go.Scatter(
            x=yearly["year"], y=yearly["fatalities"],
            mode="lines+markers", name="Fatalities",
            line=dict(color=THEME["danger"], width=2),
            marker=dict(size=5),
            yaxis="y2",
        ))
        fig.update_layout(
            title=dict(text="Yearly Trend: Incidents & Fatalities", font=dict(size=14, color=THEME["text"]), x=0.5),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter, sans-serif", color=THEME["text"]),
            height=350,
            hovermode="x unified",
            hoverlabel=dict(bgcolor=THEME["card"], font_size=11, bordercolor=THEME["accent"]),
            legend=dict(font=dict(color=THEME["text"]), bgcolor="rgba(0,0,0,0.3)", orientation="h", y=1.1),
            xaxis=dict(showgrid=True, gridcolor=THEME["grid"]),
            yaxis=dict(title="Incidents", showgrid=True, gridcolor=THEME["grid"], titlefont=dict(color=THEME["accent"])),
            yaxis2=dict(title="Fatalities", overlaying="y", side="right", showgrid=False, titlefont=dict(color=THEME["danger"])),
            margin=dict(l=10, r=10, t=50, b=10),
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        if "attack_type" in country_df.columns:
            attack_counts = country_df["attack_type"].value_counts().head(8).reset_index()
            attack_counts.columns = ["attack_type", "count"]
            fig = create_pie_chart(attack_counts, "count", "attack_type", "Attack Type Distribution", height=350)
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        if "group_name" in country_df.columns:
            group_counts = country_df["group_name"].value_counts().head(10).reset_index()
            group_counts.columns = ["group_name", "count"]
            fig = create_bar_chart(
                group_counts, "group_name", "count",
                "Top Terrorist Groups", THEME["warning"], height=350, orientation="h"
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        if "weapon_type" in country_df.columns:
            weapon_counts = country_df["weapon_type"].value_counts().head(8).reset_index()
            weapon_counts.columns = ["weapon_type", "count"]
            fig = create_pie_chart(weapon_counts, "count", "weapon_type", "Weapon Type Distribution", height=350)
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        if "target_type" in country_df.columns:
            target_counts = country_df["target_type"].value_counts().head(8).reset_index()
            target_counts.columns = ["target_type", "count"]
            fig = create_bar_chart(
                target_counts, "target_type", "count",
                "Target Types", THEME["info"], height=350, orientation="h"
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        if "city" in country_df.columns:
            city_counts = country_df["city"].value_counts().head(10).reset_index()
            city_counts.columns = ["city", "count"]
            fig = create_bar_chart(
                city_counts, "city", "count",
                "Most Affected Cities", THEME["accent"], height=350, orientation="h"
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    if "region" in country_df.columns:
        country_df["region"] = country_df["region"].fillna("Unknown")

    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    if all(c in country_df.columns for c in ["latitude", "longitude"]):
        map_data = country_df.dropna(subset=["latitude", "longitude", "year"])
        if not map_data.empty:
            fig_map = go.Figure()
            fatalities_max = map_data["fatalities"].max() if map_data["fatalities"].max() > 0 else 1
            fig_map.add_trace(go.Scattermapbox(
                lat=map_data["latitude"],
                lon=map_data["longitude"],
                mode="markers",
                marker=dict(
                    size=map_data["fatalities"].clip(1, 50) / fatalities_max * 20 + 5,
                    color=map_data["fatalities"],
                    colorscale="Viridis",
                    showscale=True,
                    colorbar=dict(
                        title="Fatalities", thickness=10, len=0.3,
                        tickfont=dict(color=THEME["text"], size=9),
                        titlefont=dict(color=THEME["text"], size=9),
                    ),
                    opacity=0.8,
                ),
                text=map_data.apply(
                    lambda r: f"<b>{r.get('city', 'Unknown')}</b><br>Year: {int(r['year'])}<br>Fatalities: {int(r['fatalities'])}<br>Attack: {r.get('attack_type', 'Unknown')}",
                    axis=1,
                ),
                hovertemplate="%{text}<extra></extra>",
            ))
            fig_map.update_layout(
                mapbox=dict(
                    style="carto-darkmatter",
                    center=dict(
                        lat=map_data["latitude"].mean(),
                        lon=map_data["longitude"].mean(),
                    ),
                    zoom=4,
                ),
                paper_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=0, r=0, t=0, b=0),
                height=450,
                hoverlabel=dict(bgcolor=THEME["card"], font_size=10, bordercolor=THEME["accent"]),
            )
            st.plotly_chart(
                fig_map, use_container_width=True,
                config={"displayModeBar": False},
            )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.markdown(f"### Incident Table - {selected_country}")
    display_cols = [c for c in ["year", "month", "day", "city", "province", "attack_type", "target_type", "group_name", "weapon_type", "fatalities", "injuries", "success"] if c in country_df.columns]
    if display_cols:
        display_df = country_df[display_cols].head(100).copy()
        st.dataframe(display_df, use_container_width=True, hide_index=True)

    csv = country_df[display_cols].to_csv(index=False)
    import base64
    b64 = base64.b64encode(csv.encode()).decode()
    st.markdown(
        f'<a href="data:file/csv;base64,{b64}" download="{selected_country}_terrorism_data.csv" style="display: inline-block; padding: 0.5rem 1.5rem; background: linear-gradient(135deg, #7c3aed, #3b82f6); color: white; border-radius: 10px; text-decoration: none; font-weight: 600; font-size: 0.85rem; margin-top: 0.5rem;">Download Full CSV</a>',
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)
