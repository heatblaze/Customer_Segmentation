"""
Visualization Module
────────────────────
Plotly-based chart functions returning Figure objects for Streamlit.
"""

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA

from config import CONFIG
from insights_engine import calculate_segment_distribution, calculate_revenue_by_segment, get_top_retailers

# ── Shared template ───────────────────────────────────────────────────────────

_TEMPLATE = "plotly_dark"
_COLORS = list(CONFIG["LABEL_COLORS"].values())


def _apply_defaults(fig: go.Figure) -> go.Figure:
    """Apply consistent styling to every chart."""
    fig.update_layout(
        template=_TEMPLATE,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", size=13),
        margin=dict(l=40, r=40, t=50, b=40),
    )
    return fig


# ── Chart functions ───────────────────────────────────────────────────────────

def plot_segment_distribution(df: pd.DataFrame) -> go.Figure:
    """Donut chart of retailer counts per segment."""
    dist = calculate_segment_distribution(df)
    color_map = CONFIG["LABEL_COLORS"]
    colors = [color_map.get(s, CONFIG["FALLBACK_COLOR"]) for s in dist["segment"]]

    fig = go.Figure(
        go.Pie(
            labels=dist["segment"],
            values=dist["count"],
            hole=0.5,
            marker=dict(colors=colors),
            textinfo="label+percent",
            textfont_size=13,
            hovertemplate="<b>%{label}</b><br>Retailers: %{value}<br>Share: %{percent}<extra></extra>",
        )
    )
    fig.update_layout(title="Segment Distribution", showlegend=True)
    return _apply_defaults(fig)


def plot_revenue_by_segment(df: pd.DataFrame) -> go.Figure:
    """Horizontal bar chart of revenue per segment."""
    rev = calculate_revenue_by_segment(df)
    color_map = CONFIG["LABEL_COLORS"]
    colors = [color_map.get(s, CONFIG["FALLBACK_COLOR"]) for s in rev["segment"]]

    fig = go.Figure(
        go.Bar(
            y=rev["segment"],
            x=rev["revenue"],
            orientation="h",
            marker_color=colors,
            text=rev["percentage"].apply(lambda p: f"{p}%"),
            textposition="auto",
            hovertemplate="<b>%{y}</b><br>Revenue: ₹%{x:,.0f}<extra></extra>",
        )
    )
    fig.update_layout(
        title="Revenue Contribution by Segment",
        xaxis_title="Revenue (₹)",
        yaxis_title="",
        yaxis=dict(autorange="reversed"),
    )
    return _apply_defaults(fig)


def plot_pca_clusters(df: pd.DataFrame) -> go.Figure:
    """2-D PCA scatter coloured by value_label."""
    feature_cols = [c for c in df.columns if c.endswith("_scaled")]
    if len(feature_cols) < 2:
        feature_cols = ["recency", "frequency", "monetary", "range_sold"]

    pca = PCA(n_components=2)
    components = pca.fit_transform(df[feature_cols].values)
    plot_df = pd.DataFrame(components, columns=["PC1", "PC2"])
    plot_df["Segment"] = df["value_label"].values
    plot_df["Retailer"] = df["retailer"].values

    color_map = CONFIG["LABEL_COLORS"]

    fig = px.scatter(
        plot_df,
        x="PC1",
        y="PC2",
        color="Segment",
        color_discrete_map=color_map,
        hover_data=["Retailer"],
        title="Cluster Visualization (PCA)",
        opacity=0.75,
    )
    fig.update_traces(marker=dict(size=7, line=dict(width=0.5, color="white")))
    fig.update_layout(
        xaxis_title=f"PC 1 ({pca.explained_variance_ratio_[0]*100:.1f}%)",
        yaxis_title=f"PC 2 ({pca.explained_variance_ratio_[1]*100:.1f}%)",
    )
    return _apply_defaults(fig)


def plot_top_retailers(df: pd.DataFrame, n: int = CONFIG["DEFAULT_TOP_N"]) -> go.Figure:
    """Horizontal bar chart of top-n retailers by monetary value."""
    top = get_top_retailers(df, n).sort_values("monetary")
    color_map = CONFIG["LABEL_COLORS"]
    colors = [color_map.get(lbl, CONFIG["FALLBACK_COLOR"]) for lbl in top["value_label"]]

    fig = go.Figure(
        go.Bar(
            y=top["retailer"].astype(str),
            x=top["monetary"],
            orientation="h",
            marker_color=colors,
            hovertemplate="<b>Retailer %{y}</b><br>Revenue: ₹%{x:,.0f}<extra></extra>",
        )
    )
    fig.update_layout(
        title=f"Top {n} Retailers by Revenue",
        xaxis_title="Revenue (₹)",
        yaxis_title="Retailer ID",
    )
    return _apply_defaults(fig)


def plot_rfm_distributions(df: pd.DataFrame) -> go.Figure:
    """Histograms for recency, frequency, and monetary."""
    metrics = ["recency", "frequency", "monetary"]
    titles = ["Recency (days)", "Frequency (orders)", "Monetary (₹)"]

    fig = make_subplots(rows=1, cols=3, subplot_titles=titles, horizontal_spacing=0.08)

    for i, (col, title) in enumerate(zip(metrics, titles), 1):
        fig.add_trace(
            go.Histogram(
                x=df[col],
                marker_color=_COLORS[i % len(_COLORS)],
                opacity=0.85,
                name=title,
                hovertemplate=f"{title}<br>Value: %{{x}}<br>Count: %{{y}}<extra></extra>",
            ),
            row=1,
            col=i,
        )

    fig.update_layout(
        title="RFM Metric Distributions",
        showlegend=False,
        height=380,
    )
    return _apply_defaults(fig)
