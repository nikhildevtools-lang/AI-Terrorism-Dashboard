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
                <span class="gradient-text">Global Threat Map</span>
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

    if not plot_df.empty:
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
    else:
        plot_df["size"] = []
        plot_df["hover_text"] = []

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
