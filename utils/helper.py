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


def get_top_values(df: pd.DataFrame, column: str, n: int = 10) -> pd.DataFrame:
    if column not in df.columns:
        return pd.DataFrame()
    return df[column].value_counts().head(n).reset_index()


def get_year_range(df: pd.DataFrame) -> tuple:
    if "year" not in df.columns:
        return (1970, 2017)
    return (int(df["year"].min()), int(df["year"].max()))


def get_country_list(df: pd.DataFrame) -> list:
    if "country" not in df.columns:
        return []
    return sorted(df["country"].dropna().unique().tolist())


def get_region_list(df: pd.DataFrame) -> list:
    if "region" not in df.columns:
        return []
    return sorted(df["region"].dropna().unique().tolist())


def get_attack_type_list(df: pd.DataFrame) -> list:
    if "attack_type" not in df.columns:
        return []
    return sorted(df["attack_type"].dropna().unique().tolist())


def get_weapon_type_list(df: pd.DataFrame) -> list:
    if "weapon_type" not in df.columns:
        return []
    return sorted(df["weapon_type"].dropna().unique().tolist())


def get_group_list(df: pd.DataFrame) -> list:
    if "group_name" not in df.columns:
        return []
    return sorted(df["group_name"].dropna().unique().tolist())


def get_target_type_list(df: pd.DataFrame) -> list:
    if "target_type" not in df.columns:
        return []
    return sorted(df["target_type"].dropna().unique().tolist())


def get_country_data(df: pd.DataFrame, country: str) -> pd.DataFrame:
    if "country" not in df.columns:
        return pd.DataFrame()
    return df[df["country"] == country].copy()


def get_region_data(df: pd.DataFrame, region: str) -> pd.DataFrame:
    if "region" not in df.columns:
        return pd.DataFrame()
    return df[df["region"] == region].copy()


def calculate_growth_rate(series: pd.Series) -> float:
    if len(series) < 2:
        return 0.0
    first = series.iloc[0]
    last = series.iloc[-1]
    if first == 0:
        return 0.0
    return ((last - first) / first) * 100


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


def create_download_link(df: pd.DataFrame, filename: str = "data.csv") -> str:
    csv = df.to_csv(index=False)
    import base64
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">Download CSV</a>'
    return href

def get_summary_stats(df: pd.DataFrame) -> dict:
    """
    Generate summary statistics for the dashboard.
    """

    stats = {
        "total_incidents": len(df),
        "total_countries": 0,
        "total_fatalities": 0,
        "total_injuries": 0,
        "total_groups": 0,
        "total_attack_types": 0,
    }

    # Country
    if "country" in df.columns:
        stats["total_countries"] = df["country"].nunique()
    elif "country_txt" in df.columns:
        stats["total_countries"] = df["country_txt"].nunique()

    # Fatalities
    if "fatalities" in df.columns:
        stats["total_fatalities"] = int(df["fatalities"].fillna(0).sum())
    elif "nkill" in df.columns:
        stats["total_fatalities"] = int(df["nkill"].fillna(0).sum())

    # Injuries
    if "injuries" in df.columns:
        stats["total_injuries"] = int(df["injuries"].fillna(0).sum())
    elif "nwound" in df.columns:
        stats["total_injuries"] = int(df["nwound"].fillna(0).sum())

    # Terrorist Groups
    if "group_name" in df.columns:
        stats["total_groups"] = df["group_name"].nunique()
    elif "gname" in df.columns:
        stats["total_groups"] = df["gname"].nunique()

    # Attack Types
    if "attack_type" in df.columns:
        stats["total_attack_types"] = df["attack_type"].nunique()
    elif "attacktype1_txt" in df.columns:
        stats["total_attack_types"] = df["attacktype1_txt"].nunique()

    return stats