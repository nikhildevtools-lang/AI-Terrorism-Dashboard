# pages/Forecasting.py
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from utils.charts import create_forecast_chart

def show(conn):
    if conn is None:
        st.warning("No data available.")
        return

    st.markdown(
        '''
        <div class="glass-card" style="text-align: center; padding: 2rem; margin-bottom: 2rem;">
            <h1 style="font-size: 2.2rem; margin-bottom: 0.3rem;">
                <span class="gradient-text">Forecasting</span>
            </h1>
            <p style="color: #94a3b8; max-width: 600px; margin: 0 auto;">
                Predict future terrorism trends using linear regression analysis on historical incident data.
            </p>
        </div>
        ''', unsafe_allow_html=True
    )

    yearly = conn.execute("SELECT year, COUNT(*) as incidents, SUM(fatalities) as fatalities, SUM(injuries) as injuries FROM gtd GROUP BY year ORDER BY year").df()

    with st.sidebar:
        st.markdown("## Forecast Settings")
        forecast_years = st.slider("Forecast Years Ahead", min_value=1, max_value=20, value=5)

    last_historical_year = yearly["year"].max()
    future_years = np.arange(last_historical_year + 1, last_historical_year + forecast_years + 1)

    col1, col2, col3 = st.columns(3)

    def fit_and_predict(col):
        X = yearly[["year"]].values
        y = yearly[col].values
        model = LinearRegression().fit(X, y)
        future = np.maximum(model.predict(future_years.reshape(-1, 1)), 0)
        growth = ((future.sum() / forecast_years) / (y.sum() / len(y)) - 1) * 100 if y.sum() > 0 else 0
        return model, future, growth, X, y

    model_inc, future_inc, inc_growth, X_inc, y_inc = fit_and_predict("incidents")
    with col1:
        st.markdown(f'<div class="custom-card" style="text-align: center; padding: 1.2rem;"><div style="font-size: 0.7rem; color: #94a3b8; text-transform: uppercase;">Total Forecast Incidents</div><div style="font-size: 1.8rem; font-weight: 800; color: #a78bfa;">{int(future_inc.sum()):,}</div><div style="font-size: 0.75rem; color: {"#10b981" if inc_growth >= 0 else "#ef4444"};">{"↑" if inc_growth >= 0 else "↓"} {abs(inc_growth):.1f}% avg annual change</div></div>', unsafe_allow_html=True)

    model_fat, future_fat, fat_growth, X_fat, y_fat = fit_and_predict("fatalities")
    with col2:
        st.markdown(f'<div class="custom-card" style="text-align: center; padding: 1.2rem;"><div style="font-size: 0.7rem; color: #94a3b8; text-transform: uppercase;">Forecast Fatalities</div><div style="font-size: 1.8rem; font-weight: 800; color: #ef4444;">{int(future_fat.sum()):,}</div><div style="font-size: 0.75rem; color: {"#10b981" if fat_growth >= 0 else "#ef4444"};">{"↑" if fat_growth >= 0 else "↓"} {abs(fat_growth):.1f}% avg annual change</div></div>', unsafe_allow_html=True)

    model_inj, future_inj, inj_growth, X_inj, y_inj = fit_and_predict("injuries")
    with col3:
        st.markdown(f'<div class="custom-card" style="text-align: center; padding: 1.2rem;"><div style="font-size: 0.7rem; color: #94a3b8; text-transform: uppercase;">Forecast Injuries</div><div style="font-size: 1.8rem; font-weight: 800; color: #f59e0b;">{int(future_inj.sum()):,}</div><div style="font-size: 0.75rem; color: {"#10b981" if inj_growth >= 0 else "#ef4444"};">{"↑" if inj_growth >= 0 else "↓"} {abs(inj_growth):.1f}% avg annual change</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    fig_incidents = create_forecast_chart(yearly[["year", "incidents"]], pd.DataFrame({"year": future_years, "incidents": future_inc.astype(int)}), "year", "incidents", "Incident Forecast", height=450)
    st.plotly_chart(fig_incidents, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        fig_fatalities = create_forecast_chart(yearly[["year", "fatalities"]], pd.DataFrame({"year": future_years, "fatalities": future_fat.astype(int)}), "year", "fatalities", "Fatality Forecast", height=400)
        st.plotly_chart(fig_fatalities, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        fig_injuries = create_forecast_chart(yearly[["year", "injuries"]], pd.DataFrame({"year": future_years, "injuries": future_inj.astype(int)}), "year", "injuries", "Injury Forecast", height=400)
        st.plotly_chart(fig_injuries, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="custom-card">### Trend Analysis', unsafe_allow_html=True)
    inc_r2 = model_inc.score(X_inc, y_inc)
    st.markdown(f'<div style="padding: 1rem; background: rgba(124, 58, 237, 0.05); border-radius: 12px;"><div style="font-size: 1.3rem; font-weight: 700; color: #a78bfa;">Incident Trend Fit (R²): {inc_r2:.3f}</div></div></div>', unsafe_allow_html=True)
