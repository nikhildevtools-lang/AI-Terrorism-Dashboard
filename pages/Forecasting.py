import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from utils.charts import THEME, create_forecast_chart, apply_theme
from utils.helper import format_number


def show(df: pd.DataFrame):
    if df.empty:
        st.warning("No data available.")
        return

    st.markdown(
        """
        <div class="glass-card" style="text-align: center; padding: 2rem; margin-bottom: 2rem;">
            <h1 style="font-size: 2.2rem; margin-bottom: 0.3rem;">
                <span class="gradient-text">📈 Forecasting</span>
            </h1>
            <p style="color: #94a3b8; max-width: 600px; margin: 0 auto;">
                Predict future terrorism trends using linear regression analysis on historical incident data.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if "year" not in df.columns:
        st.warning("Year data not available.")
        return

    yearly = df.groupby("year").agg(
        incidents=("year", "size"),
        fatalities=("fatalities", "sum"),
        injuries=("injuries", "sum"),
    ).reset_index()

    yearly = yearly.sort_values("year")

    with st.sidebar:
        st.markdown("## Forecast Settings")
        forecast_years = st.slider(
            "Forecast Years Ahead",
            min_value=1,
            max_value=20,
            value=5,
        )

    last_historical_year = yearly["year"].max()
    future_years = np.arange(last_historical_year + 1, last_historical_year + forecast_years + 1)

    col1, col2, col3 = st.columns(3)

    with col1:
        X_inc = yearly[["year"]].values
        y_inc = yearly["incidents"].values
        model_inc = LinearRegression()
        model_inc.fit(X_inc, y_inc)
        future_inc = model_inc.predict(future_years.reshape(-1, 1))
        future_inc = np.maximum(future_inc, 0)

        total_historical_inc = int(y_inc.sum())
        total_forecast_inc = int(future_inc.sum())
        inc_growth = ((future_inc.sum() / forecast_years) / (y_inc.sum() / len(y_inc)) - 1) * 100 if y_inc.sum() > 0 else 0

        st.markdown(
            f"""
            <div class="custom-card" style="text-align: center; padding: 1.2rem;">
                <div style="font-size: 0.7rem; color: #94a3b8; text-transform: uppercase;">Total Forecast Incidents</div>
                <div style="font-size: 1.8rem; font-weight: 800; color: #a78bfa;">{total_forecast_inc:,}</div>
                <div style="font-size: 0.75rem; color: {'#10b981' if inc_growth >= 0 else '#ef4444'};">
                    {'↑' if inc_growth >= 0 else '↓'} {abs(inc_growth):.1f}% avg annual change
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        X_fat = yearly[["year"]].values
        y_fat = yearly["fatalities"].values
        model_fat = LinearRegression()
        model_fat.fit(X_fat, y_fat)
        future_fat = model_fat.predict(future_years.reshape(-1, 1))
        future_fat = np.maximum(future_fat, 0)

        total_historical_fat = int(y_fat.sum())
        total_forecast_fat = int(future_fat.sum())
        fat_growth = ((future_fat.sum() / forecast_years) / (y_fat.sum() / len(y_fat)) - 1) * 100 if y_fat.sum() > 0 else 0

        st.markdown(
            f"""
            <div class="custom-card" style="text-align: center; padding: 1.2rem;">
                <div style="font-size: 0.7rem; color: #94a3b8; text-transform: uppercase;">Forecast Fatalities</div>
                <div style="font-size: 1.8rem; font-weight: 800; color: #ef4444;">{total_forecast_fat:,}</div>
                <div style="font-size: 0.75rem; color: {'#10b981' if fat_growth >= 0 else '#ef4444'};">
                    {'↑' if fat_growth >= 0 else '↓'} {abs(fat_growth):.1f}% avg annual change
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        X_inj = yearly[["year"]].values
        y_inj = yearly["injuries"].values
        model_inj = LinearRegression()
        model_inj.fit(X_inj, y_inj)
        future_inj = model_inj.predict(future_years.reshape(-1, 1))
        future_inj = np.maximum(future_inj, 0)

        total_historical_inj = int(y_inj.sum())
        total_forecast_inj = int(future_inj.sum())
        inj_growth = ((future_inj.sum() / forecast_years) / (y_inj.sum() / len(y_inj)) - 1) * 100 if y_inj.sum() > 0 else 0

        st.markdown(
            f"""
            <div class="custom-card" style="text-align: center; padding: 1.2rem;">
                <div style="font-size: 0.7rem; color: #94a3b8; text-transform: uppercase;">Forecast Injuries</div>
                <div style="font-size: 1.8rem; font-weight: 800; color: #f59e0b;">{total_forecast_inj:,}</div>
                <div style="font-size: 0.75rem; color: {'#10b981' if inj_growth >= 0 else '#ef4444'};">
                    {'↑' if inj_growth >= 0 else '↓'} {abs(inj_growth):.1f}% avg annual change
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    historical_df = yearly[["year", "incidents"]].copy()
    forecast_df = pd.DataFrame({"year": future_years, "incidents": future_inc.astype(int)})

    fig_incidents = create_forecast_chart(
        historical_df, forecast_df, "year", "incidents",
        "Incident Forecast", height=450,
    )
    st.plotly_chart(fig_incidents, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        hist_fat_df = yearly[["year", "fatalities"]].copy()
        fore_fat_df = pd.DataFrame({"year": future_years, "fatalities": future_fat.astype(int)})

        fig_fatalities = create_forecast_chart(
            hist_fat_df, fore_fat_df, "year", "fatalities",
            "Fatality Forecast", height=400,
        )
        st.plotly_chart(fig_fatalities, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        hist_inj_df = yearly[["year", "injuries"]].copy()
        fore_inj_df = pd.DataFrame({"year": future_years, "injuries": future_inj.astype(int)})

        fig_injuries = create_forecast_chart(
            hist_inj_df, fore_inj_df, "year", "injuries",
            "Injury Forecast", height=400,
        )
        st.plotly_chart(fig_injuries, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.markdown("### Forecast Data Table")

    forecast_table = pd.DataFrame({
        "Year": future_years.astype(int),
        "Predicted Incidents": future_inc.astype(int),
        "Predicted Fatalities": future_fat.astype(int),
        "Predicted Injuries": future_inj.astype(int),
    })

    col1, col2 = st.columns([3, 1])
    with col1:
        st.dataframe(forecast_table, use_container_width=True, hide_index=True)
    with col2:
        csv = forecast_table.to_csv(index=False)
        import base64
        b64 = base64.b64encode(csv.encode()).decode()
        st.markdown(
            f'<a href="data:file/csv;base64,{b64}" download="terrorism_forecast.csv" style="display: inline-block; padding: 0.5rem 1rem; background: linear-gradient(135deg, #7c3aed, #3b82f6); color: white; border-radius: 10px; text-decoration: none; font-weight: 600; font-size: 0.85rem; text-align: center; margin-top: 1.5rem;">Download Forecast CSV</a>',
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.markdown("### Trend Analysis")

    inc_r2 = model_inc.score(X_inc, y_inc)
    fat_r2 = model_fat.score(X_fat, y_fat)
    inj_r2 = model_inj.score(X_inj, y_inj)

    st.markdown(
        f"""
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">
            <div style="padding: 1rem; background: rgba(124, 58, 237, 0.05); border-radius: 12px;">
                <div style="font-size: 0.7rem; color: #94a3b8;">Incident Trend Fit (R²)</div>
                <div style="font-size: 1.3rem; font-weight: 700; color: #a78bfa;">{inc_r2:.3f}</div>
                <div style="font-size: 0.75rem; color: #94a3b8;">{'Strong trend' if inc_r2 > 0.7 else 'Moderate trend' if inc_r2 > 0.4 else 'Weak trend'}</div>
            </div>
            <div style="padding: 1rem; background: rgba(239, 68, 68, 0.05); border-radius: 12px;">
                <div style="font-size: 0.7rem; color: #94a3b8;">Fatality Trend Fit (R²)</div>
                <div style="font-size: 1.3rem; font-weight: 700; color: #ef4444;">{fat_r2:.3f}</div>
                <div style="font-size: 0.75rem; color: #94a3b8;">{'Strong trend' if fat_r2 > 0.7 else 'Moderate trend' if fat_r2 > 0.4 else 'Weak trend'}</div>
            </div>
            <div style="padding: 1rem; background: rgba(245, 158, 11, 0.05); border-radius: 12px;">
                <div style="font-size: 0.7rem; color: #94a3b8;">Injury Trend Fit (R²)</div>
                <div style="font-size: 1.3rem; font-weight: 700; color: #f59e0b;">{inj_r2:.3f}</div>
                <div style="font-size: 0.75rem; color: #94a3b8;">{'Strong trend' if inj_r2 > 0.7 else 'Moderate trend' if inj_r2 > 0.4 else 'Weak trend'}</div>
            </div>
        </div>
        <div style="margin-top: 1rem; padding: 1rem; background: rgba(16, 185, 129, 0.05); border-radius: 12px;">
            <div style="font-size: 0.85rem; color: #94a3b8; line-height: 1.6;">
                <b style="color: #e2e8f0;">Insight:</b> The forecasting model uses linear regression on {len(yearly)} years of historical data
                to predict trends for the next {forecast_years} years. 
                {'The strong R² values suggest a reliable trend.' if max(inc_r2, fat_r2, inj_r2) > 0.7 else 'The moderate R² values indicate that terrorism patterns are influenced by complex, non-linear factors beyond simple time trends.'}
                Forecast accuracy decreases for longer time horizons.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)
