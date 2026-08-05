# pages/Attack_Prediction.py
import streamlit as st
import pandas as pd
from utils.charts import create_feature_importance_chart
from utils.helper import get_country_list, get_region_list, get_attack_type_list, get_weapon_type_list, get_group_list, get_target_type_list
from utils.preprocessing import train_prediction_model, predict_attack

def show(conn):
    if conn is None:
        st.warning("No data available.")
        return

    st.markdown(
        '''
        <div class="glass-card" style="text-align: center; padding: 2rem; margin-bottom: 2rem;">
            <h1 style="font-size: 2.2rem; margin-bottom: 0.3rem;">
                <span class="gradient-text">🤖 Attack Prediction</span>
            </h1>
            <p style="color: #94a3b8; max-width: 600px; margin: 0 auto;">
                Machine learning model that predicts the likelihood of casualties in a terrorist attack based on historical patterns.
            </p>
        </div>
        ''', unsafe_allow_html=True
    )

    with st.spinner("Training prediction model..."):
        model, encoders, feature_cols, accuracy = train_prediction_model(conn)

    if model is None:
        st.error("Could not train the prediction model. Please check the data.")
        return

    st.markdown(
        f'''
        <div style="display: flex; gap: 1rem; flex-wrap: wrap; margin-bottom: 1.5rem;">
            <div class="custom-card" style="flex: 1; min-width: 200px; text-align: center; padding: 1rem;">
                <div style="font-size: 0.7rem; color: #94a3b8; text-transform: uppercase;">Model Accuracy</div>
                <div style="font-size: 2rem; font-weight: 800; color: #10b981;">{accuracy:.1%}</div>
            </div>
            <div class="custom-card" style="flex: 1; min-width: 200px; text-align: center; padding: 1rem;">
                <div style="font-size: 0.7rem; color: #94a3b8; text-transform: uppercase;">Algorithm</div>
                <div style="font-size: 1.2rem; font-weight: 700; color: #a78bfa;">Random Forest</div>
            </div>
            <div class="custom-card" style="flex: 1; min-width: 200px; text-align: center; padding: 1rem;">
                <div style="font-size: 0.7rem; color: #94a3b8; text-transform: uppercase;">Features Used</div>
                <div style="font-size: 1.2rem; font-weight: 700; color: #e2e8f0;">{len(feature_cols)}</div>
            </div>
            <div class="custom-card" style="flex: 1; min-width: 200px; text-align: center; padding: 1rem;">
                <div style="font-size: 0.7rem; color: #94a3b8; text-transform: uppercase;">Prediction Target</div>
                <div style="font-size: 1rem; font-weight: 700; color: #f59e0b;">Fatality Likelihood</div>
            </div>
        </div>
        ''', unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)
    countries = get_country_list(conn)
    regions = get_region_list(conn)
    weapons = get_weapon_type_list(conn)
    targets = get_target_type_list(conn)
    attacks = get_attack_type_list(conn)
    groups = get_group_list(conn)

    with col1:
        pred_country = st.selectbox("Country", options=countries, index=countries.index("Iraq") if "Iraq" in countries else 0)
        pred_region = st.selectbox("Region", options=regions, index=regions.index("Middle East & North Africa") if "Middle East & North Africa" in regions else 0)
        pred_weapon = st.selectbox("Weapon Type", options=weapons, index=0)

    with col2:
        pred_target = st.selectbox("Target Type", options=targets, index=0)
        pred_attack = st.selectbox("Attack Type", options=attacks, index=0)
        pred_group = st.selectbox("Terrorist Group", options=groups, index=0)

    with col3:
        pred_success = st.selectbox("Attack Success (1=Yes, 0=No)", options=[1, 0], index=0)
        pred_suicide = st.selectbox("Suicide Attack (1=Yes, 0=No)", options=[0, 1], index=0)
        pred_fatalities_input = st.number_input("Potential Fatalities (estimate)", min_value=0, max_value=1000, value=5)
        pred_injuries_input = st.number_input("Potential Injuries (estimate)", min_value=0, max_value=5000, value=20)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🔮 Predict Attack Outcome", use_container_width=True):
        with st.spinner("Generating prediction..."):
            try:
                prediction, probability = predict_attack(model, encoders, feature_cols, pred_country, pred_region, pred_weapon, pred_target, pred_attack, pred_group, pred_success, pred_suicide, pred_fatalities_input, pred_injuries_input)
                st.markdown("---")
                st.markdown("## Prediction Results")
                
                result_col1, result_col2 = st.columns(2)
                fatality_risk = probability[1] * 100
                with result_col1:
                    if prediction == 1:
                        st.markdown(f'<div class="custom-card" style="text-align: center; padding: 2rem; border-color: rgba(239, 68, 68, 0.5);"><div style="font-size: 3rem;">⚠️</div><div style="font-size: 1.8rem; font-weight: 800; color: #ef4444; margin: 0.5rem 0;">FATALITIES PREDICTED</div><div style="font-size: 0.9rem; color: #94a3b8;">Based on the provided parameters, this attack scenario may result in casualties.</div></div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="custom-card" style="text-align: center; padding: 2rem; border-color: rgba(16, 185, 129, 0.5);"><div style="font-size: 3rem;">✅</div><div style="font-size: 1.8rem; font-weight: 800; color: #10b981; margin: 0.5rem 0;">NO FATALITIES PREDICTED</div><div style="font-size: 0.9rem; color: #94a3b8;">The model predicts this attack scenario may not result in fatalities.</div></div>', unsafe_allow_html=True)

                with result_col2:
                    st.markdown('<div class="custom-card" style="padding: 1.5rem;"><div style="font-size: 0.75rem; color: #94a3b8; text-transform: uppercase; margin-bottom: 1rem; letter-spacing: 0.05em;">Prediction Confidence</div>', unsafe_allow_html=True)
                    prob_no_fatality = probability[0] * 100
                    st.markdown(f'<div style="margin-bottom: 1rem;"><div style="display: flex; justify-content: space-between; font-size: 0.85rem; margin-bottom: 0.3rem;"><span style="color: #10b981;">No Fatality</span><span style="color: #e2e8f0; font-weight: 600;">{prob_no_fatality:.1f}%</span></div><div class="confidence-meter"><div class="confidence-meter-fill" style="width: {prob_no_fatality}%; background: linear-gradient(90deg, #10b981, #34d399);"></div></div></div>', unsafe_allow_html=True)
                    st.markdown(f'<div style="margin-bottom: 1.5rem;"><div style="display: flex; justify-content: space-between; font-size: 0.85rem; margin-bottom: 0.3rem;"><span style="color: #ef4444;">Fatality</span><span style="color: #e2e8f0; font-weight: 600;">{fatality_risk:.1f}%</span></div><div class="confidence-meter"><div class="confidence-meter-fill" style="width: {fatality_risk}%; background: linear-gradient(90deg, #ef4444, #f87171);"></div></div></div>', unsafe_allow_html=True)
                    risk_level = "CRITICAL" if fatality_risk > 75 else "HIGH" if fatality_risk > 50 else "MODERATE" if fatality_risk > 25 else "LOW"
                    risk_color = "#ef4444" if fatality_risk > 75 else "#f59e0b" if fatality_risk > 50 else "#3b82f6" if fatality_risk > 25 else "#10b981"
                    st.markdown(f'<div style="text-align: center; padding-top: 0.5rem;"><span class="threat-badge" style="background: {risk_color}20; color: {risk_color};">{risk_level} RISK</span></div></div>', unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown('<div class="custom-card">### Feature Importance', unsafe_allow_html=True)
                if hasattr(model, "feature_importances_"):
                    importances = model.feature_importances_
                    feat_imp_df = pd.DataFrame({"feature": feature_cols, "importance": importances}).sort_values("importance", ascending=False)
                    fig = create_feature_importance_chart(feat_imp_df["feature"].tolist(), feat_imp_df["importance"].tolist(), "What Drives the Prediction?", height=400)
                    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
                st.markdown("</div>", unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Prediction error: {str(e)}")
