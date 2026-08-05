# utils/data_loader.py
import duckdb
import streamlit as st
from pathlib import Path
import pandas as pd

@st.cache_resource
def get_db_connection():
    data_path = Path("data/globalterrorismdb_0718dist.csv")
    if not data_path.exists():
        data_path = Path("AI_Terrorism_Dashboard/data/globalterrorismdb_0718dist.csv")
    if not data_path.exists():
        st.error("Dataset not found. Please place 'globalterrorismdb_0718dist.csv' in the data/ directory.")
        return None

    conn = duckdb.connect(':memory:')
    
    try:
        conn.execute(f"CREATE TABLE raw_gtd AS SELECT * FROM read_csv_auto('{data_path}', ignore_errors=true)")
    except Exception as e:
        st.error(f"Failed to load data: {e}")
        return None

    conn.execute('''
        CREATE TABLE gtd AS 
        SELECT 
            TRY_CAST(iyear AS INTEGER) AS year,
            TRY_CAST(imonth AS INTEGER) AS month,
            TRY_CAST(iday AS INTEGER) AS day,
            country_txt AS country,
            region_txt AS region,
            COALESCE(provstate, 'Unknown') AS province,
            COALESCE(city, 'Unknown') AS city,
            TRY_CAST(latitude AS DOUBLE) AS latitude,
            TRY_CAST(longitude AS DOUBLE) AS longitude,
            attacktype1_txt AS attack_type,
            COALESCE(targtype1_txt, 'Unknown') AS target_type,
            COALESCE(gname, 'Unknown') AS group_name,
            weaptype1_txt AS weapon_type,
            COALESCE(TRY_CAST(nkill AS INTEGER), 0) AS fatalities,
            COALESCE(TRY_CAST(nwound AS INTEGER), 0) AS injuries,
            COALESCE(TRY_CAST(success AS INTEGER), 0) AS success,
            COALESCE(TRY_CAST(suicide AS INTEGER), 0) AS suicide,
            COALESCE(TRY_CAST(multiple AS INTEGER), 0) AS multiple_attacks,
            COALESCE(TRY_CAST(property AS INTEGER), 0) AS property_damage,
            COALESCE(natlty1_txt, 'Unknown') AS nationality,
            COALESCE(weapsubtype1_txt, 'Unknown') AS weapon_subtype,
            COALESCE(attacktype2_txt, 'Unknown') AS attack_type_2,
            COALESCE(weaptype2_txt, 'Unknown') AS weapon_type_2,
            COALESCE(targtype2_txt, 'Unknown') AS target_type_2,
            COALESCE(gsubname, 'Unknown') AS group_subname,
            COALESCE(gname2, 'Unknown') AS group_name_2,
            COALESCE(addnotes, 'Unknown') AS additional_notes,
            COALESCE(scite1, 'Unknown') AS source_1,
            COALESCE(scite2, 'Unknown') AS source_2,
            COALESCE(scite3, 'Unknown') AS source_3,
            COALESCE(dbsource, 'Unknown') AS database_source,
            COALESCE(summary, 'Unknown') AS summary,
            COALESCE(motive, 'Unknown') AS motive,
            COALESCE(TRY_CAST(ishostkid AS INTEGER), 0) AS hostage_related,
            COALESCE(TRY_CAST(nhostkid AS INTEGER), 0) AS hostages_taken,
            COALESCE(TRY_CAST(nhours AS INTEGER), 0) AS hours_held,
            COALESCE(TRY_CAST(ndays AS INTEGER), 0) AS days_held,
            COALESCE(TRY_CAST(ransom AS INTEGER), 0) AS ransom_paid,
            COALESCE(TRY_CAST(ransomamt AS INTEGER), 0) AS ransom_amount
        FROM raw_gtd
        WHERE iyear IS NOT NULL 
    ''')
    
    conn.execute("DROP TABLE raw_gtd")
    return conn

@st.cache_data
def get_summary_stats(_conn) -> dict:
    if _conn is None:
        return {}
    res = _conn.execute('''
        SELECT 
            COUNT(*) as total_incidents,
            COUNT(DISTINCT country) as total_countries,
            SUM(fatalities) as total_fatalities,
            SUM(injuries) as total_injuries,
            COUNT(DISTINCT group_name) as total_groups,
            COUNT(DISTINCT attack_type) as total_attack_types,
            MIN(year) as min_year,
            MAX(year) as max_year
        FROM gtd
    ''').fetchone()
    
    top_country = _conn.execute("SELECT country FROM gtd GROUP BY country ORDER BY COUNT(*) DESC LIMIT 1").fetchone()
    top_group = _conn.execute("SELECT group_name FROM gtd GROUP BY group_name ORDER BY COUNT(*) DESC LIMIT 1").fetchone()
    top_attack = _conn.execute("SELECT attack_type FROM gtd GROUP BY attack_type ORDER BY COUNT(*) DESC LIMIT 1").fetchone()
    top_weapon = _conn.execute("SELECT weapon_type FROM gtd GROUP BY weapon_type ORDER BY COUNT(*) DESC LIMIT 1").fetchone()

    return {
        "total_incidents": res[0] or 0,
        "total_countries": res[1] or 0,
        "total_fatalities": int(res[2] or 0),
        "total_injuries": int(res[3] or 0),
        "total_groups": res[4] or 0,
        "total_attack_types": res[5] or 0,
        "year_range": f"{res[6]} - {res[7]}" if res[6] else "N/A",
        "most_affected_country": top_country[0] if top_country else "N/A",
        "most_active_group": top_group[0] if top_group else "N/A",
        "most_common_attack": top_attack[0] if top_attack else "N/A",
        "most_common_weapon": top_weapon[0] if top_weapon else "N/A"
    }

def build_where_clause(years=None, countries=None, regions=None, attack_types=None, weapon_types=None, groups=None):
    conditions = ["1=1"]
    if years and len(years) == 2:
        conditions.append(f"year BETWEEN {years[0]} AND {years[1]}")
    def esc(lst): return [str(x).replace("'", "''") for x in lst]
    if countries:
        conditions.append("country IN (" + ",".join(f"'{c}'" for c in esc(countries)) + ")")
    if regions:
        conditions.append("region IN (" + ",".join(f"'{r}'" for r in esc(regions)) + ")")
    if attack_types:
        conditions.append("attack_type IN (" + ",".join(f"'{a}'" for a in esc(attack_types)) + ")")
    if weapon_types:
        conditions.append("weapon_type IN (" + ",".join(f"'{w}'" for w in esc(weapon_types)) + ")")
    if groups:
        conditions.append("group_name IN (" + ",".join(f"'{g}'" for g in esc(groups)) + ")")
    return " AND ".join(conditions)
