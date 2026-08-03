import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from utils.charts import THEME, apply_theme
from utils.helper import get_year_range, get_country_list, get_attack_type_list, get_weapon_type_list, get_group_list
from utils.data_loader import filter_data


def show(df: pd.DataFrame):
    if df.empty:
        st.warning("No data available.")
        return

    st.markdown(
        """
        <div class="glass-card" style="text-align: center; padding: 2rem; margin-bottom: 2rem;">
            <h1 style="font-size: 2.2rem; margin-bottom: 0.3rem;">
                <span class="gradient-text">🌍 Global Threat Map</span>
            </h1>
            <p style="color: #94a3b8; max-width: 600px; margin: 0 auto;">
                Interactive visualization of global terrorism incidents with powerful filtering capabilities.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if "latitude" not in df.columns or "longitude" not in df.columns:
        st.warning("Geospatial data (latitude/longitude) not available in the dataset.")
        return

    map_df = df.dropna(subset=["latitude", "longitude", "year"])

    with st.expander("🔍 Filter Controls", expanded=True):
        col1, col2, col3, col4 = st.columns(4)

        years = get_year_range(df)
        with col1:
            year_range = st.slider(
                "Year Range",
                min_value=years[0],
                max_value=years[1],
                value=(years[0], years[1]),
            )

        countries_list = get_country_list(df)
        with col2:
            selected_countries = st.multiselect(
                "Countries (leave empty for all)",
                options=countries_list,
                default=[],
            )

        attack_types = get_attack_type_list(df)
        with col3:
            selected_attacks = st.multiselect(
                "Attack Types",
                options=attack_types,
                default=[],
            )

        weapon_types = get_weapon_type_list(df)
        with col4:
            selected_weapons = st.multiselect(
                "Weapon Types",
                options=weapon_types,
                default=[],
            )

        col1, col2 = st.columns(2)
        groups = get_group_list(df)
        with col1:
            selected_groups = st.multiselect(
                "Terrorist Groups",
                options=groups,
                default=[],
            )

    filtered = filter_data(
        map_df,
        years=year_range,
        countries=selected_countries if selected_countries else None,
        attack_types=selected_attacks if selected_attacks else None,
        weapon_types=selected_weapons if selected_weapons else None,
        groups=selected_groups if selected_groups else None,
    )

    st.markdown(
        f"""
        <div style="display: flex; gap: 1rem; flex-wrap: wrap; margin-bottom: 1rem;">
            <div class="custom-card" style="flex: 1; min-width: 120px; text-align: center; padding: 0.8rem;">
                <div style="font-size: 0.7rem; color: #94a3b8;">INCIDENTS</div>
                <div style="font-size: 1.5rem; font-weight: 700; color: #e2e8f0;">{len(filtered):,}</div>
            </div>
            <div class="custom-card" style="flex: 1; min-width: 120px; text-align: center; padding: 0.8rem;">
                <div style="font-size: 0.7rem; color: #94a3b8;">FATALITIES</div>
                <div style="font-size: 1.5rem; font-weight: 700; color: #ef4444;">{int(filtered['fatalities'].sum()):,}</div>
            </div>
            <div class="custom-card" style="flex: 1; min-width: 120px; text-align: center; padding: 0.8rem;">
                <div style="font-size: 0.7rem; color: #94a3b8;">INJURIES</div>
                <div style="font-size: 1.5rem; font-weight: 700; color: #f59e0b;">{int(filtered['injuries'].sum()):,}</div>
            </div>
            <div class="custom-card" style="flex: 1; min-width: 120px; text-align: center; padding: 0.8rem;">
                <div style="font-size: 0.7rem; color: #94a3b8;">COUNTRIES</div>
                <div style="font-size: 1.5rem; font-weight: 700; color: #10b981;">{filtered['country'].nunique()}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    sample_size = min(len(filtered), 10000)
    plot_df = filtered.sample(sample_size, random_state=42) if len(filtered) > sample_size else filtered

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
            lon=plot_df["longitude"],
            lat=plot_df["latitude"],
            text=plot_df["hover_text"],
            mode="markers",
            marker=dict(
                size=plot_df["size"].clip(2, 25),
                color=plot_df["fatalities"],
                colorscale=[
                    [0, "rgba(59, 130, 246, 0.4)"],
                    [0.3, "rgba(124, 58, 237, 0.6)"],
                    [0.6, "rgba(239, 68, 68, 0.8)"],
                    [1, "rgba(239, 68, 68, 1)"],
                ],
                showscale=True,
                colorbar=dict(
                    title="Fatalities",
                    thickness=15,
                    len=0.5,
                    x=1.02,
                    xpad=0,
                    tickfont=dict(color=THEME["text"]),
                    titlefont=dict(color=THEME["text"]),
                ),
                opacity=0.8,
            ),
            hovertemplate="%{text}<extra></extra>",
        )
    )

    fig.update_layout(
        mapbox=dict(
            style="carto-darkmatter",
            center=dict(lat=center_lat, lon=center_lon),
            zoom=1.5 if len(selected_countries) > 0 else 1,
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color=THEME["text"]),
        margin=dict(l=0, r=0, t=0, b=0),
        height=650,
        hoverlabel=dict(
            bgcolor=THEME["card"],
            font_size=11,
            font_family="Inter, sans-serif",
            bordercolor=THEME["accent"],
        ),
    )

    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displayModeBar": True,
            "modeBarButtonsToRemove": ["lasso2d", "select2d"],
            "displaylogo": False,
        },
    )
    st.markdown("</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        if "region" in filtered.columns:
            region_counts = filtered["region"].value_counts().head(10).reset_index()
            region_counts.columns = ["region", "count"]
            colors = px.colors.sequential.Viridis[: len(region_counts)]
            fig_reg = go.Figure(data=[
                go.Bar(
                    x=region_counts["count"],
                    y=region_counts["region"],
                    orientation="h",
                    marker=dict(color=colors, line=dict(width=0)),
                )
            ])
            fig_reg = apply_theme(fig_reg)
            fig_reg.update_layout(
                title=dict(text="Incidents by Region", font=dict(size=14), x=0.5),
                height=350,
                xaxis=dict(showgrid=True, gridcolor=THEME["grid"]),
                yaxis=dict(showgrid=False),
                showlegend=False,
            )
            st.plotly_chart(fig_reg, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        if "group_name" in filtered.columns:
            group_counts = filtered["group_name"].value_counts().head(10).reset_index()
            group_counts.columns = ["group_name", "count"]
            colors = px.colors.sequential.Viridis[: len(group_counts)]
            fig_grp = go.Figure(data=[
                go.Bar(
                    x=group_counts["count"],
                    y=group_counts["group_name"],
                    orientation="h",
                    marker=dict(color=colors, line=dict(width=0)),
                )
            ])
            fig_grp = apply_theme(fig_grp)
            fig_grp.update_layout(
                title=dict(text="Top Groups (Filtered View)", font=dict(size=14), x=0.5),
                height=350,
                xaxis=dict(showgrid=True, gridcolor=THEME["grid"]),
                yaxis=dict(showgrid=False),
                showlegend=False,
            )
            st.plotly_chart(fig_grp, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)
