# utils/preprocessing.py
import pandas as pd
import numpy as np
import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib
from pathlib import Path

def prepare_prediction_data(conn):
    df = conn.execute("SELECT country, region, weapon_type, target_type, attack_type, group_name, success, suicide, fatalities, injuries, multiple_attacks, property_damage FROM gtd").df()
    feature_cols = []
    encoders = {}

    cat_features = {
        "country": "country",
        "region": "region",
        "weapon_type": "weapon_type",
        "target_type": "target_type",
        "attack_type": "attack_type",
        "group_name": "group_name",
    }

    X = pd.DataFrame()

    for col, src in cat_features.items():
        if src in df.columns:
            le = LabelEncoder()
            X[col] = le.fit_transform(df[src].fillna("Unknown").astype(str))
            encoders[col] = le
            feature_cols.append(col)

    for c in ["success", "suicide", "fatalities", "injuries", "multiple_attacks", "property_damage"]:
        if c in df.columns:
            X[c] = df[c].fillna(0).astype(int)
            feature_cols.append(c)

    y = (df["fatalities"] > 0).astype(int) if "fatalities" in df.columns else pd.Series(np.zeros(len(df)))

    X = X.fillna(0)
    return X, y, feature_cols, encoders

@st.cache_data
def train_prediction_model(_conn):
    X, y, feature_cols, encoders = prepare_prediction_data(_conn)
    if X.shape[1] == 0:
        return None, None, None, None

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=15,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1,
        class_weight="balanced",
    )
    model.fit(X_train, y_train)

    accuracy = model.score(X_test, y_test)
    return model, encoders, feature_cols, accuracy

def predict_attack(
    model, encoders: dict, feature_cols: list, country: str, region: str,
    weapon: str, target: str, attack_type: str, group: str, success: int,
    suicide: int, fatalities: int, injuries: int,
):
    input_data = {}
    country_enc = encoders.get("country")
    region_enc = encoders.get("region")
    weapon_enc = encoders.get("weapon_type")
    target_enc = encoders.get("target_type")
    attack_enc = encoders.get("attack_type")
    group_enc = encoders.get("group_name")

    if country_enc and "country" in feature_cols:
        input_data["country"] = country_enc.transform([country])[0] if country in country_enc.classes_ else -1
    if region_enc and "region" in feature_cols:
        input_data["region"] = region_enc.transform([region])[0] if region in region_enc.classes_ else -1
    if weapon_enc and "weapon_type" in feature_cols:
        input_data["weapon_type"] = weapon_enc.transform([weapon])[0] if weapon in weapon_enc.classes_ else -1
    if target_enc and "target_type" in feature_cols:
        input_data["target_type"] = target_enc.transform([target])[0] if target in target_enc.classes_ else -1
    if attack_enc and "attack_type" in feature_cols:
        input_data["attack_type"] = attack_enc.transform([attack_type])[0] if attack_type in attack_enc.classes_ else -1
    if group_enc and "group_name" in feature_cols:
        input_data["group_name"] = group_enc.transform([group])[0] if group in group_enc.classes_ else -1

    for c, val in [("success", success), ("suicide", suicide), ("fatalities", fatalities), ("injuries", injuries)]:
        if c in feature_cols:
            input_data[c] = val

    for col in feature_cols:
        if col not in input_data:
            input_data[col] = 0

    input_df = pd.DataFrame([input_data])[feature_cols]

    prediction = model.predict(input_df)[0]
    probability = model.predict_proba(input_df)[0]

    return prediction, probability
