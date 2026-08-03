import io
from pathlib import Path

import pandas as pd
import numpy as np
# pyrefly: ignore [missing-import]
import streamlit as st


DATA_DIR = Path(__file__).resolve().parents[1] / "data"
DEFAULT_DATASET = "globalterrorismdb_0718dist.csv"


def list_local_csv_files() -> list[str]:
    if not DATA_DIR.exists():
        return []
    return sorted(path.name for path in DATA_DIR.glob("*.csv"))


def _read_csv_with_fallback(source) -> pd.DataFrame:
    for encoding in ("utf-8", "latin1"):
        try:
            if hasattr(source, "seek"):
                source.seek(0)
            return pd.read_csv(source, encoding=encoding, low_memory=False)
        except UnicodeDecodeError:
            continue
    if hasattr(source, "seek"):
        source.seek(0)
    return pd.read_csv(source, low_memory=False)


@st.cache_data
def load_data(filename: str | None = None) -> pd.DataFrame:
    selected_file = filename or DEFAULT_DATASET
    data_path = DATA_DIR / selected_file
    if not data_path.exists():
        st.error(f"Dataset not found. Please place '{selected_file}' in the data/ directory.")
        return pd.DataFrame()

    return _read_csv_with_fallback(data_path)


@st.cache_data
def get_clean_data(filename: str | None = None) -> pd.DataFrame:
    df = load_data(filename)
    if df.empty:
        return df
    return clean_gtd_data(df)


@st.cache_data
def get_clean_uploaded_data(file_name: str, file_bytes: bytes) -> pd.DataFrame:
    if not file_bytes:
        return pd.DataFrame()
    df = _read_csv_with_fallback(io.BytesIO(file_bytes))
    if df.empty:
        return df
    return clean_gtd_data(df)


def clean_gtd_data(df: pd.DataFrame) -> pd.DataFrame:
    column_map = {
        "iyear": "year",
        "imonth": "month",
        "iday": "day",
        "country_txt": "country",
        "region_txt": "region",
        "provstate": "province",
        "city": "city",
        "latitude": "latitude",
        "longitude": "longitude",
        "attacktype1_txt": "attack_type",
        "targtype1_txt": "target_type",
        "gname": "group_name",
        "weaptype1_txt": "weapon_type",
        "nkill": "fatalities",
        "nwound": "injuries",
        "success": "success",
        "suicide": "suicide",
        "crit1": "criterion_1",
        "crit2": "criterion_2",
        "crit3": "criterion_3",
        "doubtterr": "doubt_terrorism",
        "multiple": "multiple_attacks",
        "individual": "individual_attack",
        "property": "property_damage",
        "ishostkid": "hostage_related",
        "nhostkid": "hostages_taken",
        "nhostkidus": "us_hostages",
        "nhours": "hours_held",
        "ndays": "days_held",
        "ransom": "ransom_paid",
        "ransomamt": "ransom_amount",
        "ransomamtus": "ransom_amount_usd",
        "ransompaid": "ransom_paid_amount",
        "ransompaidus": "ransom_paid_usd",
        "natlty1_txt": "nationality",
        "weapsubtype1_txt": "weapon_subtype",
        "attacktype2_txt": "attack_type_2",
        "weaptype2_txt": "weapon_type_2",
        "targtype2_txt": "target_type_2",
        "gsubname": "group_subname",
        "gname2": "group_name_2",
        "addnotes": "additional_notes",
        "scite1": "source_1",
        "scite2": "source_2",
        "scite3": "source_3",
        "dbsource": "database_source",
        "INT_LOG": "int_logistical",
        "INT_IDEO": "int_ideological",
        "INT_MISC": "int_misc",
        "INT_ANY": "int_any",
        "related": "related_incidents",
        "summary": "summary",
        "motive": "motive",
    }

    # Avoid duplicate columns by dropping target column names that already exist
    # in the dataframe and will be overwritten by a rename of a different column.
    for k, v in column_map.items():
        if k in df.columns and v in df.columns and k != v:
            df = df.drop(columns=[v])

    rename_map = {k: v for k, v in column_map.items() if k in df.columns}
    df = df.rename(columns=rename_map)

    essential = ["year", "country", "region", "latitude", "longitude", "attack_type", "group_name", "weapon_type"]
    existing_essential = [c for c in essential if c in df.columns]

    df = df.dropna(subset=existing_essential, how="all")

    fill_cols = {
        "fatalities": 0,
        "injuries": 0,
        "success": 0,
        "suicide": 0,
        "hostages_taken": 0,
        "days_held": 0,
        "ransom_amount": 0,
        "property_damage": 0,
    }
    for col, val in fill_cols.items():
        if col in df.columns:
            df[col] = df[col].fillna(val).astype(int)

    text_cols = ["city", "province", "target_type", "nationality", "weapon_subtype",
                 "attack_type_2", "weapon_type_2", "target_type_2", "group_subname",
                 "group_name_2", "additional_notes", "summary", "motive"]
    for col in text_cols:
        if col in df.columns:
            df[col] = df[col].fillna("Unknown")

    if "group_name" in df.columns:
        df["group_name"] = df["group_name"].replace({"Unknown": "Unknown"}, regex=False)
        df["group_name"] = df["group_name"].fillna("Unknown")

    if "day" in df.columns:
        df["day"] = df["day"].clip(1, 31)

    if "month" in df.columns:
        df["month"] = df["month"].clip(1, 12)

    if all(c in df.columns for c in ["year", "month", "day"]):
        df["date"] = pd.to_datetime(
            df[["year", "month", "day"]].astype(str).agg("-".join, axis=1),
            errors="coerce",
        )
    elif "year" in df.columns:
        df["date"] = pd.to_datetime(df["year"], format="%Y", errors="coerce")

    return df


@st.cache_data
def get_summary_stats(df: pd.DataFrame) -> dict:
    stats = {}
    stats["total_incidents"] = len(df)
    stats["total_countries"] = df["country"].nunique() if "country" in df.columns else 0
    stats["total_fatalities"] = int(df["fatalities"].sum()) if "fatalities" in df.columns else 0
    stats["total_injuries"] = int(df["injuries"].sum()) if "injuries" in df.columns else 0
    stats["total_groups"] = df["group_name"].nunique() if "group_name" in df.columns else 0
    stats["total_attack_types"] = df["attack_type"].nunique() if "attack_type" in df.columns else 0
    stats["total_weapons"] = df["weapon_type"].nunique() if "weapon_type" in df.columns else 0
    stats["year_range"] = f"{int(df['year'].min())} - {int(df['year'].max())}" if "year" in df.columns else "N/A"
    stats["most_affected_country"] = df["country"].mode().iloc[0] if "country" in df.columns and not df["country"].empty else "N/A"
    stats["most_active_group"] = df["group_name"].mode().iloc[0] if "group_name" in df.columns and not df["group_name"].empty else "N/A"
    stats["most_common_attack"] = df["attack_type"].mode().iloc[0] if "attack_type" in df.columns and not df["attack_type"].empty else "N/A"
    stats["most_common_weapon"] = df["weapon_type"].mode().iloc[0] if "weapon_type" in df.columns and not df["weapon_type"].empty else "N/A"
    return stats


@st.cache_data
def filter_data(
    df: pd.DataFrame,
    years: tuple = None,
    countries: list = None,
    regions: list = None,
    attack_types: list = None,
    weapon_types: list = None,
    groups: list = None,
) -> pd.DataFrame:
    filtered = df.copy()
    if years and len(years) == 2 and "year" in filtered.columns:
        filtered = filtered[(filtered["year"] >= years[0]) & (filtered["year"] <= years[1])]
    if countries and "country" in filtered.columns:
        filtered = filtered[filtered["country"].isin(countries)]
    if regions and "region" in filtered.columns:
        filtered = filtered[filtered["region"].isin(regions)]
    if attack_types and "attack_type" in filtered.columns:
        filtered = filtered[filtered["attack_type"].isin(attack_types)]
    if weapon_types and "weapon_type" in filtered.columns:
        filtered = filtered[filtered["weapon_type"].isin(weapon_types)]
    if groups and "group_name" in filtered.columns:
        filtered = filtered[filtered["group_name"].isin(groups)]
    return filtered
