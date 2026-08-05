import pandas as pd
import streamlit as st
from typing import Any


def format_number(num: Any) -> str:
    try:
        num = float(num)
        if num >= 1_000_000_000:
            return f"{num / 1_000_000_000:.1f}B"
        if num >= 1_000_000:
            return f"{num / 1_000_000:.1f}M"
        if num >= 1_000:
            return f"{num / 1_000:.1f}K"
        return f"{int(num):,}"
    except (ValueError, TypeError):
        return "0"


def get_top_values(conn, column: str, n: int = 10) -> pd.DataFrame:
    try:
        return conn.execute(f"SELECT {column}, COUNT(*) as count FROM gtd GROUP BY {column} ORDER BY count DESC LIMIT {n}").df()
    except Exception:
        return pd.DataFrame()


def get_year_range(conn) -> tuple:
    try:
        res = conn.execute("SELECT MIN(year), MAX(year) FROM gtd").fetchone()
        if res and res[0] is not None:
            return (int(res[0]), int(res[1]))
    except Exception:
        pass
    return (1970, 2017)


def get_country_list(conn) -> list:
    try:
        return [r[0] for r in conn.execute("SELECT DISTINCT country FROM gtd WHERE country IS NOT NULL ORDER BY country").fetchall()]
    except Exception:
        return []


def get_region_list(conn) -> list:
    try:
        return [r[0] for r in conn.execute("SELECT DISTINCT region FROM gtd WHERE region IS NOT NULL ORDER BY region").fetchall()]
    except Exception:
        return []


def get_attack_type_list(conn) -> list:
    try:
        return [r[0] for r in conn.execute("SELECT DISTINCT attack_type FROM gtd WHERE attack_type IS NOT NULL ORDER BY attack_type").fetchall()]
    except Exception:
        return []


def get_weapon_type_list(conn) -> list:
    try:
        return [r[0] for r in conn.execute("SELECT DISTINCT weapon_type FROM gtd WHERE weapon_type IS NOT NULL ORDER BY weapon_type").fetchall()]
    except Exception:
        return []


def get_group_list(conn) -> list:
    try:
        return [r[0] for r in conn.execute("SELECT DISTINCT group_name FROM gtd WHERE group_name IS NOT NULL ORDER BY group_name").fetchall()]
    except Exception:
        return []


def get_target_type_list(conn) -> list:
    try:
        return [r[0] for r in conn.execute("SELECT DISTINCT target_type FROM gtd WHERE target_type IS NOT NULL ORDER BY target_type").fetchall()]
    except Exception:
        return []


def get_country_data(conn, country: str) -> pd.DataFrame:
    try:
        return conn.execute(f"SELECT * FROM gtd WHERE country = ?", (country,)).df()
    except Exception:
        return pd.DataFrame()


def get_region_data(conn, region: str) -> pd.DataFrame:
    try:
        return conn.execute(f"SELECT * FROM gtd WHERE region = ?", (region,)).df()
    except Exception:
        return pd.DataFrame()


def get_threat_level(fatalities: int, incidents: int) -> tuple:
    score = (fatalities * 0.6) + (incidents * 0.4)
    if score > 10000:
        return "CRITICAL", "#ff0040"
    if score > 5000:
        return "HIGH", "#ff6600"
    if score > 1000:
        return "ELEVATED", "#ffcc00"
    if score > 100:
        return "GUARDED", "#4dabf7"
    return "LOW", "#40c057"

