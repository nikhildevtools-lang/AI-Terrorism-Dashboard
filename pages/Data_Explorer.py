# pages/Data_Explorer.py
import streamlit as st

def show(conn):
    if conn is None: return

    st.markdown('''<div class="glass-card" style="text-align: center; padding: 2rem; margin-bottom: 2rem;"><h1 style="font-size: 2.2rem; margin-bottom: 0.3rem;"><span class="gradient-text">Data Explorer</span></h1></div>''', unsafe_allow_html=True)

    st.markdown('<div class="custom-card">', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2, 1, 1])
    with col1: search_term = st.text_input("Search", placeholder="Search...")
    with col2:
        attack_types = [r[0] for r in conn.execute("SELECT DISTINCT attack_type FROM gtd").fetchall()]
        attack_filter = st.multiselect("Attack Type", options=attack_types, default=[])
    with col3:
        sort_col = st.selectbox("Sort by", options=["year", "fatalities", "country"], index=0)
        sort_asc = st.checkbox("Ascending", value=False)

    where_conds = ["1=1"]
    if search_term:
        s = search_term.lower().replace("'", "''")
        cols = ["country", "city", "group_name", "attack_type", "weapon_type", "target_type", "province"]
        where_conds.append("(" + " OR ".join([f"LOWER(CAST({c} AS VARCHAR)) LIKE '%{s}%'" for c in cols]) + ")")
    if attack_filter:
        a_str = ",".join(["'" + a.replace("'", "''") + "'" for a in attack_filter])
        where_conds.append(f"attack_type IN ({a_str})")
        
    where = " AND ".join(where_conds)
    order = f"ORDER BY {sort_col} {'ASC' if sort_asc else 'DESC'}"

    page_size = st.selectbox("Rows per page", options=[25, 50, 100], index=0)
    total_records = conn.execute(f"SELECT COUNT(*) FROM gtd WHERE {where}").fetchone()[0]
    total_pages = max(1, (total_records + page_size - 1) // page_size)
    page = st.number_input("Page", min_value=1, max_value=total_pages, value=1)
    
    start_idx = (page - 1) * page_size
    page_df = conn.execute(f"SELECT year, month, day, country, city, attack_type, group_name, weapon_type, fatalities FROM gtd WHERE {where} {order} LIMIT {page_size} OFFSET {start_idx}").df()
    
    st.dataframe(page_df, use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)
