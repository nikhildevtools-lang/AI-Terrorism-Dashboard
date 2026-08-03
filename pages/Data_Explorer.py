# pyrefly: ignore [missing-import]
import streamlit as st
import pandas as pd
from utils.charts import THEME, create_bar_chart, create_line_chart, create_pie_chart, apply_theme
from utils.helper import format_number


def show(df: pd.DataFrame):
    if df.empty:
        st.warning("No data available.")
        return

    st.markdown(
        """
        <div class="glass-card" style="text-align: center; padding: 2rem; margin-bottom: 2rem;">
            <h1 style="font-size: 2.2rem; margin-bottom: 0.3rem;">
                <span class="gradient-text">📊 Data Explorer</span>
            </h1>
            <p style="color: #94a3b8; max-width: 600px; margin: 0 auto;">
                Powerful data exploration tool with search, filter, sort, and pagination capabilities.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="custom-card">', unsafe_allow_html=True)

    display_cols = [c for c in [
        "year", "month", "day", "country", "region", "city", "province",
        "latitude", "longitude", "attack_type", "target_type", "group_name",
        "weapon_type", "fatalities", "injuries", "success", "suicide",
    ] if c in df.columns]

    explorer_df = df[display_cols].copy()

    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        search_term = st.text_input("Search", placeholder="Search by country, group, city, attack type...")

    with col2:
        if "attack_type" in explorer_df.columns:
            attack_filter = st.multiselect(
                "Attack Type", options=sorted(explorer_df["attack_type"].dropna().unique()),
                default=[], key="explorer_attack"
            )
        else:
            attack_filter = []

    with col3:
        sort_col = st.selectbox("Sort by", options=display_cols, index=0)
        sort_asc = st.checkbox("Ascending", value=False)

    filtered = explorer_df.copy()

    if search_term:
        search_term_lower = search_term.lower()
        mask = pd.Series(False, index=filtered.index)
        for col in filtered.select_dtypes(include=["object"]).columns:
            mask |= filtered[col].fillna("").astype(str).str.lower().str.contains(search_term_lower, na=False)
        filtered = filtered[mask]

    if attack_filter:
        filtered = filtered[filtered["attack_type"].isin(attack_filter)]

    if sort_col in filtered.columns:
        filtered = filtered.sort_values(by=sort_col, ascending=sort_asc)

    st.markdown(
        f"""
        <div style="display: flex; gap: 1rem; flex-wrap: wrap; margin: 0.5rem 0 1rem 0;">
            <div style="font-size: 0.85rem; color: #94a3b8;">
                Showing: <b style="color: #e2e8f0;">{len(filtered):,}</b> of <b style="color: #e2e8f0;">{len(explorer_df):,}</b> records
            </div>
            <div style="font-size: 0.85rem; color: #94a3b8;">
                Columns: <b style="color: #e2e8f0;">{len(display_cols)}</b>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    page_size = st.selectbox("Rows per page", options=[25, 50, 100, 200], index=0)
    total_pages = max(1, (len(filtered) + page_size - 1) // page_size)

    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        if total_pages > 1:
            page = st.number_input("Page", min_value=1, max_value=total_pages, value=1)
        else:
            page = 1

    start_idx = (page - 1) * page_size
    end_idx = min(start_idx + page_size, len(filtered))
    page_df = filtered.iloc[start_idx:end_idx]

    st.dataframe(page_df, use_container_width=True, hide_index=True)

    st.markdown(
        f"<div style='text-align: center; font-size: 0.8rem; color: #64748b; padding: 0.5rem 0;'>"
        f"Page {page} of {total_pages} | Showing rows {start_idx + 1}-{end_idx} of {len(filtered):,}"
        f"</div>",
        unsafe_allow_html=True,
    )

    csv_full = explorer_df.to_csv(index=False)
    csv_filtered = filtered.to_csv(index=False)
    import base64
    b64_full = base64.b64encode(csv_full.encode()).decode()
    b64_filtered = base64.b64encode(csv_filtered.encode()).decode()

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            f'<a href="data:file/csv;base64,{b64_filtered}" download="filtered_terrorism_data.csv" style="display: block; text-align: center; padding: 0.6rem; background: linear-gradient(135deg, #7c3aed, #3b82f6); color: white; border-radius: 10px; text-decoration: none; font-weight: 600; font-size: 0.85rem;">Download Filtered Data</a>',
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            f'<a href="data:file/csv;base64,{b64_full}" download="full_terrorism_data.csv" style="display: block; text-align: center; padding: 0.6rem; background: rgba(124, 58, 237, 0.15); color: #a78bfa; border: 1px solid rgba(124, 58, 237, 0.3); border-radius: 10px; text-decoration: none; font-weight: 600; font-size: 0.85rem;">Download Full Dataset</a>',
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("### Quick Visualizations")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        if "attack_type" in filtered.columns:
            counts = filtered["attack_type"].value_counts().head(8).reset_index()
            counts.columns = ["attack_type", "count"]
            fig = create_bar_chart(counts, "attack_type", "count", "Attack Types (Filtered)", THEME["accent"], 350, orientation="h")
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        if "country" in filtered.columns:
            counts = filtered["country"].value_counts().head(10).reset_index()
            counts.columns = ["country", "count"]
            fig = create_bar_chart(counts, "country", "count", "Countries (Filtered)", THEME["danger"], 350, orientation="h")
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        if "year" in filtered.columns:
            yearly = filtered.groupby("year").size().reset_index(name="count")
            fig = create_line_chart(yearly, "year", "count", "Yearly Trend (Filtered)", THEME["info"], 350)
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        if "group_name" in filtered.columns:
            counts = filtered["group_name"].value_counts().head(8).reset_index()
            counts.columns = ["group_name", "count"]
            fig = create_pie_chart(counts, "count", "group_name", "Top Groups (Filtered)", 350)
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)
