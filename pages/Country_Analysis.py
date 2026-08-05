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

    st.html(
        '''
        <div class="glass-card" style="text-align: center; padding: 2rem; margin-bottom: 2rem;">
            <h1 style="font-size: 2.2rem; margin-bottom: 0.3rem; display: flex; align-items: center; justify-content: center; gap: 0.5rem;">
                <svg xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="url(#globe-gradient)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <defs>
                        <linearGradient id="globe-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                            <stop offset="0%" stop-color="#a78bfa" />
                            <stop offset="100%" stop-color="#3b82f6" />
                        </linearGradient>
                    </defs>
                    <circle cx="12" cy="12" r="10"></circle>
                    <path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"></path>
                    <path d="M2 12h20"></path>
                </svg>
                <span class="gradient-text">Country Analysis</span>
            </h1>
            <p style="color: #94a3b8; max-width: 600px; margin: 0 auto;">
                Deep dive into terrorism activity by country with comprehensive analytics.
            </p>
        </div>
        '''
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
