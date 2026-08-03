import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np


THEME = {
    "bg": "#0a0a1a",
    "card": "#14142b",
    "card_hover": "#1a1a3e",
    "accent": "#7c3aed",
    "accent_light": "#a78bfa",
    "danger": "#ef4444",
    "warning": "#f59e0b",
    "success": "#10b981",
    "info": "#3b82f6",
    "text": "#e2e8f0",
    "text_muted": "#94a3b8",
    "grid": "#1e1e3a",
    "gradient_start": "#7c3aed",
    "gradient_end": "#3b82f6",
}


def apply_theme(fig: go.Figure) -> go.Figure:
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, -apple-system, sans-serif", color=THEME["text"]),
        margin=dict(l=20, r=20, t=40, b=20),
        hovermode="closest",
        hoverlabel=dict(
            bgcolor=THEME["card"],
            font_size=12,
            font_family="Inter, sans-serif",
            bordercolor=THEME["accent"],
        ),
    )
    return fig


def create_bar_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str = "",
    color: str = THEME["accent"],
    height: int = 400,
    sort_values: bool = True,
    top_n: int = None,
    orientation: str = "h",
) -> go.Figure:
    plot_df = df.copy()
    if top_n:
        plot_df = plot_df.head(top_n)
    if sort_values and orientation == "h":
        plot_df = plot_df.sort_values(y, ascending=True)

    fig = go.Figure()
    label_col = "y" if orientation == "h" else "x"
    value_col = "x" if orientation == "h" else "y"
    fig.add_trace(
        go.Bar(
            x=plot_df[y] if orientation == "h" else plot_df[x],
            y=plot_df[x] if orientation == "h" else plot_df[y],
            orientation=orientation,
            marker=dict(
                color=color,
                line=dict(color=color, width=0),
                opacity=0.85,
            ),
            hovertemplate=f"<b>%{{{label_col}}}</b><br>%{{{value_col}}}:,<extra></extra>",
        )
    )
    fig = apply_theme(fig)
    fig.update_layout(
        title=dict(text=title, font=dict(size=16, color=THEME["text"]), x=0.5),
        height=height,
        xaxis=dict(
            showgrid=True,
            gridcolor=THEME["grid"],
            gridwidth=0.5,
            tickfont=dict(size=10),
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor=THEME["grid"],
            gridwidth=0.5,
            tickfont=dict(size=10),
        ),
        showlegend=False,
        margin=dict(l=10, r=10, t=50, b=10),
    )
    return fig


def create_line_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str = "",
    color: str = THEME["accent"],
    height: int = 400,
) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=df[x],
            y=df[y],
            mode="lines+markers",
            line=dict(color=color, width=3),
            marker=dict(size=6, color=color, line=dict(width=2, color=color)),
            fill="tozeroy",
            fillcolor=f"rgba(124, 58, 237, 0.1)",
            hovertemplate=f"<b>%{{x}}</b><br>%{{y:,}}<extra></extra>",
        )
    )
    fig = apply_theme(fig)
    fig.update_layout(
        title=dict(text=title, font=dict(size=16, color=THEME["text"]), x=0.5),
        height=height,
        xaxis=dict(showgrid=True, gridcolor=THEME["grid"], gridwidth=0.5),
        yaxis=dict(showgrid=True, gridcolor=THEME["grid"], gridwidth=0.5),
        showlegend=False,
        margin=dict(l=10, r=10, t=50, b=10),
    )
    return fig


def create_pie_chart(
    df: pd.DataFrame,
    values: str,
    names: str,
    title: str = "",
    height: int = 400,
    top_n: int = 8,
) -> go.Figure:
    plot_df = df.head(top_n).copy()
    fig = go.Figure(
        data=[
            go.Pie(
                labels=plot_df[names],
                values=plot_df[values],
                hole=0.45,
                marker=dict(
                    colors=px.colors.sequential.Viridis[: len(plot_df)],
                    line=dict(color=THEME["bg"], width=2),
                ),
                textinfo="label+percent",
                textposition="outside",
                textfont=dict(size=11, color=THEME["text"]),
                hovertemplate="<b>%{label}</b><br>%{value:,} (%{percent})<extra></extra>",
            )
        ]
    )
    fig = apply_theme(fig)
    fig.update_layout(
        title=dict(text=title, font=dict(size=16, color=THEME["text"]), x=0.5),
        height=height,
        showlegend=False,
        margin=dict(l=10, r=10, t=50, b=10),
    )
    return fig


def create_animated_bubble_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    size: str,
    color: str,
    title: str = "",
    height: int = 500,
) -> go.Figure:
    fig = px.scatter(
        df,
        x=x,
        y=y,
        size=size,
        color=color,
        hover_name=color,
        log_x=True,
        size_max=60,
        title=title,
        color_continuous_scale="Viridis",
    )
    fig.update_traces(marker=dict(line=dict(width=1, color="white")), opacity=0.8)
    fig = apply_theme(fig)
    fig.update_layout(height=height)
    return fig


def create_heatmap(
    df: pd.DataFrame,
    x: str,
    y: str,
    z: str,
    title: str = "",
    height: int = 500,
) -> go.Figure:
    pivot = df.pivot_table(index=y, columns=x, values=z, aggfunc="sum", fill_value=0)
    fig = go.Figure(
        data=go.Heatmap(
            z=pivot.values,
            x=pivot.columns,
            y=pivot.index,
            colorscale="Viridis",
            hovertemplate="Year: %{x}<br>%{y}: %{z:,}<extra></extra>",
        )
    )
    fig = apply_theme(fig)
    fig.update_layout(
        title=dict(text=title, font=dict(size=16, color=THEME["text"]), x=0.5),
        height=height,
        xaxis=dict(title="", tickangle=-45),
        yaxis=dict(title=""),
        margin=dict(l=10, r=10, t=50, b=10),
    )
    return fig


def create_area_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str = "",
    color: str = THEME["accent"],
    height: int = 400,
) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=df[x],
            y=df[y],
            mode="lines",
            line=dict(color=color, width=2),
            fill="tozeroy",
            fillcolor=f"rgba(124, 58, 237, 0.15)",
            hovertemplate=f"<b>%{{x}}</b><br>%{{y:,}}<extra></extra>",
        )
    )
    fig = apply_theme(fig)
    fig.update_layout(
        title=dict(text=title, font=dict(size=16, color=THEME["text"]), x=0.5),
        height=height,
        xaxis=dict(showgrid=True, gridcolor=THEME["grid"]),
        yaxis=dict(showgrid=True, gridcolor=THEME["grid"]),
        showlegend=False,
        margin=dict(l=10, r=10, t=50, b=10),
    )
    return fig


def create_sunburst_chart(
    df: pd.DataFrame,
    path: list,
    values: str,
    title: str = "",
    height: int = 500,
) -> go.Figure:
    fig = px.sunburst(
        df,
        path=path,
        values=values,
        title=title,
        color_continuous_scale="Viridis",
    )
    fig.update_traces(marker=dict(line=dict(color=THEME["bg"], width=1.5)))
    fig = apply_theme(fig)
    fig.update_layout(
        title=dict(text=title, font=dict(size=16, color=THEME["text"]), x=0.5),
        height=height,
        margin=dict(l=10, r=10, t=50, b=10),
    )
    return fig


def create_treemap(
    df: pd.DataFrame,
    path: list,
    values: str,
    title: str = "",
    height: int = 500,
) -> go.Figure:
    fig = px.treemap(
        df,
        path=path,
        values=values,
        title=title,
        color=values,
        color_continuous_scale="Viridis",
    )
    fig.update_traces(
        textinfo="label+value+percent root",
        textfont=dict(size=12),
        marker=dict(line=dict(color=THEME["bg"], width=1)),
    )
    fig = apply_theme(fig)
    fig.update_layout(
        title=dict(text=title, font=dict(size=16, color=THEME["text"]), x=0.5),
        height=height,
        margin=dict(l=10, r=10, t=50, b=10),
    )
    return fig


def create_scatter_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str = "",
    color: str = THEME["accent"],
    height: int = 400,
    size_col: str = None,
) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=df[x],
            y=df[y],
            mode="markers",
            marker=dict(
                color=color,
                size=df[size_col] / df[size_col].max() * 30 + 5 if size_col and size_col in df.columns else 10,
                opacity=0.7,
                line=dict(width=1, color="white"),
            ),
            hovertemplate=f"<b>%{{x}}</b><br>%{{y:,}}<extra></extra>",
        )
    )
    fig = apply_theme(fig)
    fig.update_layout(
        title=dict(text=title, font=dict(size=16, color=THEME["text"]), x=0.5),
        height=height,
        xaxis=dict(showgrid=True, gridcolor=THEME["grid"]),
        yaxis=dict(showgrid=True, gridcolor=THEME["grid"]),
        showlegend=False,
        margin=dict(l=10, r=10, t=50, b=10),
    )
    return fig


def create_timeline_chart(
    df: pd.DataFrame,
    dates: str,
    values: str,
    title: str = "",
    color: str = THEME["accent"],
    height: int = 400,
) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=df[dates],
            y=df[values],
            mode="lines+markers",
            line=dict(color=color, width=2),
            marker=dict(size=5, color=color),
            fill="tozeroy",
            fillcolor=f"rgba(124, 58, 237, 0.1)",
            hovertemplate="%{x|%Y-%m-%d}<br>%{y:,}<extra></extra>",
        )
    )
    fig = apply_theme(fig)
    fig.update_layout(
        title=dict(text=title, font=dict(size=16, color=THEME["text"]), x=0.5),
        height=height,
        xaxis=dict(showgrid=True, gridcolor=THEME["grid"]),
        yaxis=dict(showgrid=True, gridcolor=THEME["grid"]),
        showlegend=False,
        margin=dict(l=10, r=10, t=50, b=10),
    )
    return fig


def create_forecast_chart(
    historical: pd.DataFrame,
    forecast: pd.DataFrame,
    x: str,
    y: str,
    title: str = "",
    height: int = 450,
) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=historical[x],
            y=historical[y],
            mode="lines+markers",
            name="Historical",
            line=dict(color=THEME["accent"], width=3),
            marker=dict(size=6, color=THEME["accent"]),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=forecast[x],
            y=forecast[y],
            mode="lines+markers",
            name="Forecast",
            line=dict(color=THEME["danger"], width=3, dash="dash"),
            marker=dict(size=6, color=THEME["danger"]),
        )
    )
    fig = apply_theme(fig)
    fig.update_layout(
        title=dict(text=title, font=dict(size=16, color=THEME["text"]), x=0.5),
        height=height,
        xaxis=dict(showgrid=True, gridcolor=THEME["grid"]),
        yaxis=dict(showgrid=True, gridcolor=THEME["grid"]),
        legend=dict(
            font=dict(color=THEME["text"]),
            bgcolor="rgba(0,0,0,0.3)",
            bordercolor=THEME["grid"],
        ),
        margin=dict(l=10, r=10, t=50, b=10),
    )
    return fig


def create_feature_importance_chart(
    features: list,
    importances: list,
    title: str = "Feature Importance",
    height: int = 400,
) -> go.Figure:
    df_imp = pd.DataFrame({"feature": features, "importance": importances})
    df_imp = df_imp.sort_values("importance", ascending=True)
    fig = go.Figure()
    colors = [THEME["accent"]] * len(df_imp)
    fig.add_trace(
        go.Bar(
            x=df_imp["importance"],
            y=df_imp["feature"],
            orientation="h",
            marker=dict(
                color=df_imp["importance"],
                colorscale="Viridis",
                line=dict(width=0),
            ),
            hovertemplate="<b>%{y}</b><br>Importance: %{x:.3f}<extra></extra>",
        )
    )
    fig = apply_theme(fig)
    fig.update_layout(
        title=dict(text=title, font=dict(size=16, color=THEME["text"]), x=0.5),
        height=height,
        xaxis=dict(showgrid=True, gridcolor=THEME["grid"]),
        yaxis=dict(showgrid=False),
        showlegend=False,
        margin=dict(l=10, r=10, t=50, b=10),
    )
    return fig
