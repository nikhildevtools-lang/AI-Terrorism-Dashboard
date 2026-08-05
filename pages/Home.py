# pages/Home.py
import streamlit as st
from utils.charts import THEME, create_bar_chart, create_line_chart, create_pie_chart, create_heatmap, create_treemap
from utils.helper import format_number
from utils.data_loader import get_summary_stats

def show(conn):
    if conn is None:
        st.warning("No data available. Please upload the GTD dataset.")
        return

    stats = get_summary_stats(conn)

    st.html("""
<style>
    .premium-hero-container {
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        justify-content: space-between;
        background: linear-gradient(270deg, rgba(6, 17, 29, 0.8), rgba(13, 34, 56, 0.8), rgba(27, 21, 69, 0.8), rgba(36, 29, 99, 0.8));
        background-size: 400% 400%;
        animation: bgShift 15s ease infinite;
        border-radius: 20px;
        padding: 3.5rem 4rem;
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.4), inset 0 0 0 1px rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        margin-bottom: 2.5rem;
    }

    @keyframes bgShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .premium-hero-left {
        flex: 1.2;
        min-width: 300px;
        z-index: 2;
        padding-right: 2rem;
    }

    .premium-hero-right {
        flex: 0.8;
        min-width: 300px;
        display: flex;
        justify-content: center;
        align-items: center;
        position: relative;
        z-index: 2;
        min-height: 400px;
    }

    .premium-hero-title {
        font-size: clamp(2.5rem, 4vw, 3.5rem);
        font-weight: 800;
        line-height: 1.15;
        margin-bottom: 1.2rem;
        font-family: 'Outfit', sans-serif;
        color: #f8fafc;
        text-shadow: 0 0 30px rgba(56, 189, 248, 0.3);
    }

    .premium-hero-title .ai-highlight {
        background: linear-gradient(135deg, #38bdf8, #a78bfa, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        filter: drop-shadow(0 0 15px rgba(167, 139, 250, 0.4));
    }

    .premium-hero-subtitle {
        color: #94a3b8;
        font-size: 1.05rem;
        line-height: 1.6;
        max-width: 90%;
        margin: 0;
    }

    /* Ambient Lighting */
    .ambient-glow-1 {
        position: absolute;
        top: -20%;
        left: -10%;
        width: 300px;
        height: 300px;
        background: radial-gradient(circle, rgba(56, 189, 248, 0.15) 0%, transparent 70%);
        border-radius: 50%;
        filter: blur(40px);
        z-index: 1;
    }
    .ambient-glow-2 {
        position: absolute;
        bottom: -20%;
        right: -10%;
        width: 400px;
        height: 400px;
        background: radial-gradient(circle, rgba(167, 139, 250, 0.15) 0%, transparent 70%);
        border-radius: 50%;
        filter: blur(50px);
        z-index: 1;
    }

    /* Holographic Earth */
    .holo-globe-container {
        position: relative;
        width: 320px;
        height: 320px;
        perspective: 1200px;
        animation: floatGlobe 6s ease-in-out infinite;
    }

    @keyframes floatGlobe {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-15px); }
    }

    .holo-core {
        position: absolute;
        inset: 10%;
        border-radius: 50%;
        background: radial-gradient(circle at 35% 35%, rgba(56, 189, 248, 0.15), rgba(27, 21, 69, 0.9) 70%, #030712 100%);
        box-shadow: 0 0 50px rgba(56, 189, 248, 0.3), inset 0 0 50px rgba(167, 139, 250, 0.4);
        border: 1px solid rgba(56, 189, 248, 0.2);
        animation: pulseCore 4s infinite alternate;
    }

    .holo-wireframe {
        position: absolute;
        inset: 10%;
        border-radius: 50%;
        background-image: 
            repeating-linear-gradient(0deg, transparent 0%, transparent 9%, rgba(56, 189, 248, 0.4) 10%),
            repeating-linear-gradient(90deg, transparent 0%, transparent 9%, rgba(167, 139, 250, 0.4) 10%);
        background-size: 24px 24px;
        mask-image: radial-gradient(circle at 50% 50%, white 35%, transparent 65%);
        -webkit-mask-image: radial-gradient(circle at 50% 50%, white 35%, transparent 65%);
        animation: scrollWireframe 30s linear infinite;
        opacity: 0.85;
    }

    /* Rings */
    .holo-ring-1, .holo-ring-2 {
        position: absolute;
        inset: 0;
        border-radius: 50%;
        border: 2px solid rgba(167, 139, 250, 0.4);
        box-shadow: 0 0 20px rgba(167, 139, 250, 0.3), inset 0 0 20px rgba(167, 139, 250, 0.2);
        transform-style: preserve-3d;
    }
    .holo-ring-1 {
        animation: rotateRing1 20s linear infinite;
        border-top-color: transparent;
        border-bottom-color: transparent;
    }
    .holo-ring-2 {
        inset: -8%;
        border: 1px dashed rgba(56, 189, 248, 0.5);
        box-shadow: 0 0 15px rgba(56, 189, 248, 0.2);
        animation: rotateRing2 30s linear infinite reverse;
    }

    /* Nodes & Network SVG */
    .holo-network {
        position: absolute;
        inset: 10%;
        border-radius: 50%;
        animation: rotateNetwork 40s linear infinite;
        z-index: 5;
    }
    
    .holo-network svg {
        width: 100%;
        height: 100%;
        overflow: visible;
    }

    .node {
        fill: #ffffff;
        filter: drop-shadow(0 0 6px #38bdf8);
        animation: blinkNode 3s infinite alternate;
    }
    .node-primary {
        fill: #f8fafc;
        filter: drop-shadow(0 0 10px #a78bfa);
        animation: blinkNode 2s infinite alternate;
    }

    .arc {
        fill: none;
        stroke: rgba(56, 189, 248, 0.6);
        stroke-width: 1px;
        stroke-dasharray: 4, 4;
        animation: pulseArc 4s linear infinite;
    }
    .arc-solid {
        fill: none;
        stroke: rgba(167, 139, 250, 0.5);
        stroke-width: 1.5px;
    }

    @keyframes pulseCore {
        0% { box-shadow: 0 0 40px rgba(56, 189, 248, 0.3), inset 0 0 40px rgba(167, 139, 250, 0.4); }
        100% { box-shadow: 0 0 60px rgba(56, 189, 248, 0.5), inset 0 0 60px rgba(167, 139, 250, 0.6); }
    }
    @keyframes scrollWireframe {
        0% { background-position: 0px 0px; }
        100% { background-position: 240px 0px; }
    }
    @keyframes rotateRing1 {
        0% { transform: rotateX(65deg) rotateY(15deg) rotateZ(0deg); }
        100% { transform: rotateX(65deg) rotateY(15deg) rotateZ(360deg); }
    }
    @keyframes rotateRing2 {
        0% { transform: rotateX(75deg) rotateY(-15deg) rotateZ(0deg); }
        100% { transform: rotateX(75deg) rotateY(-15deg) rotateZ(360deg); }
    }
    @keyframes rotateNetwork {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    @keyframes blinkNode {
        0%, 100% { opacity: 0.4; }
        50% { opacity: 1; }
    }
    @keyframes pulseArc {
        to { stroke-dashoffset: -16; }
    }

    @media (max-width: 900px) {
        .premium-hero-container {
            flex-direction: column;
            padding: 2.5rem;
        }
        .premium-hero-left {
            padding-right: 0;
            text-align: center;
            margin-bottom: 3rem;
            max-width: 100%;
        }
        .premium-hero-subtitle {
            margin: 0 auto;
        }
        .holo-globe-container {
            width: 260px;
            height: 260px;
        }
    }
</style>

<div class="premium-hero-container">
    <div class="ambient-glow-1"></div>
    <div class="ambient-glow-2"></div>
    
    <div class="premium-hero-left">
        <h1 class="premium-hero-title">
            <span class="ai-highlight">AI</span> Terrorism Intelligence<br>Dashboard
        </h1>
        <p class="premium-hero-subtitle">
            Advanced analytics platform leveraging machine learning to analyze, predict, and visualize global terrorism patterns from the Global Terrorism Database (GTD).
        </p>
    </div>
    
    <div class="premium-hero-right">
        <div class="holo-globe-container">
            <div class="holo-ring-2"></div>
            <div class="holo-ring-1"></div>
            <div class="holo-core"></div>
            <div class="holo-wireframe"></div>
            
            <div class="holo-network">
                <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
                    <!-- Arcs -->
                    <path d="M 25 35 Q 50 10 75 35" class="arc" />
                    <path d="M 75 35 Q 85 60 55 75" class="arc-solid" />
                    <path d="M 55 75 Q 30 70 25 35" class="arc" />
                    <path d="M 40 50 Q 60 30 70 65" class="arc-solid" />
                    
                    <!-- Nodes -->
                    <circle cx="25" cy="35" r="2" class="node" style="animation-delay: 0s;" />
                    <circle cx="75" cy="35" r="2.5" class="node-primary" style="animation-delay: 1s;" />
                    <circle cx="55" cy="75" r="1.5" class="node" style="animation-delay: 0.5s;" />
                    <circle cx="40" cy="50" r="3" class="node-primary" style="animation-delay: 1.5s;" />
                    <circle cx="70" cy="65" r="2" class="node" style="animation-delay: 0.2s;" />
                </svg>
            </div>
        </div>
    </div>
</div>
""")

    st.markdown("## Key Metrics")

    cols = st.columns(6)
    metrics = [
        ("💀", format_number(stats["total_incidents"]), "Total Incidents"),
        ("🌍", stats["total_countries"], "Countries"),
        ("⚰️", format_number(stats["total_fatalities"]), "Fatalities"),
        ("🏥", format_number(stats["total_injuries"]), "Injuries"),
        ("👥", format_number(stats["total_groups"]), "Terrorist Groups"),
        ("🔫", stats["total_attack_types"], "Attack Types"),
    ]

    for idx, (icon, value, label) in enumerate(metrics):
        with cols[idx]:
            st.html(
                f'''
                <div class="custom-card stat-card animate-in delay-{idx + 1}">
                    <div class="stat-icon">{icon}</div>
                    <div class="stat-value">{value}</div>
                    <div class="stat-label">{label}</div>
                </div>
                '''
            )

    st.html("<br>")
    col1, col2 = st.columns(2)

    with col1:
        st.html('<div class="custom-card animate-in delay-3">')
        yearly = conn.execute("SELECT year, COUNT(*) as count FROM gtd GROUP BY year ORDER BY year").df()
        if yearly is not None and not yearly.empty:
            fig = create_line_chart(yearly, "year", "count", "Attacks by Year", THEME["accent"])
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("No data available for Attacks by Year.")
        st.html("</div>")

    with col2:
        st.html('<div class="custom-card animate-in delay-4">')
        top_countries = conn.execute("SELECT country, COUNT(*) as count FROM gtd GROUP BY country ORDER BY count DESC LIMIT 10").df()
        if top_countries is not None and not top_countries.empty:
            fig = create_bar_chart(top_countries, "country", "count", "Top 10 Affected Countries", THEME["danger"], orientation="h")
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("No data available for Top Countries.")
        st.html("</div>")

    col1, col2 = st.columns(2)

    with col1:
        st.html('<div class="custom-card animate-in delay-5">')
        attack_counts = conn.execute("SELECT attack_type, COUNT(*) as count FROM gtd GROUP BY attack_type ORDER BY count DESC LIMIT 8").df()
        if attack_counts is not None and not attack_counts.empty:
            fig = create_pie_chart(attack_counts, "count", "attack_type", "Attack Type Distribution")
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("No data available for Attack Types.")
        st.html("</div>")

    with col2:
        st.html('<div class="custom-card animate-in delay-6">')
        weapon_counts = conn.execute("SELECT weapon_type, COUNT(*) as count FROM gtd GROUP BY weapon_type ORDER BY count DESC LIMIT 8").df()
        if weapon_counts is not None and not weapon_counts.empty:
            fig = create_pie_chart(weapon_counts, "count", "weapon_type", "Weapon Type Distribution")
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("No data available for Weapon Types.")
        st.html("</div>")

    st.html("<br>")
    col1, col2 = st.columns(2)

    with col1:
        st.html('<div class="custom-card">')
        top_groups = conn.execute("SELECT group_name, COUNT(*) as count FROM gtd GROUP BY group_name ORDER BY count DESC LIMIT 10").df()
        if top_groups is not None and not top_groups.empty:
            fig = create_bar_chart(top_groups, "group_name", "count", "Top 10 Terrorist Groups", THEME["warning"], orientation="h")
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("No data available for Terrorist Groups.")
        st.html("</div>")

    with col2:
        st.html('<div class="custom-card">')
        heatmap_data = conn.execute("SELECT year, region, COUNT(*) as count FROM gtd GROUP BY year, region").df()
        if heatmap_data is not None and not heatmap_data.empty:
            fig = create_heatmap(heatmap_data, "year", "region", "count", "Regional Activity Heatmap", height=450)
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("No data available for Regional Heatmap.")
        st.html("</div>")

    st.html("<br>")

    st.html('<div class="custom-card">')
    treemap_data = conn.execute("SELECT region, country, group_name, COUNT(*) as count FROM gtd GROUP BY region, country, group_name ORDER BY count DESC LIMIT 100").df()
    if treemap_data is not None and not treemap_data.empty:
        fig = create_treemap(treemap_data, ["region", "country", "group_name"], "count", "Global Terrorism Overview - Region → Country → Group")
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    else:
        st.info("No data available for Global Overview.")
    st.html("</div>")

    st.html(
        '''
        <div style="text-align: center; padding: 2rem 0 0 0; font-size: 0.75rem; color: #475569;">
            Data Source: Global Terrorism Database (GTD) | National Consortium for the Study of Terrorism and Responses to Terrorism (START)
        </div>
        '''
    )
