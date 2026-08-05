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
