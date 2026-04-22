"""
Retail Customer Segmentation — Streamlit Dashboard
───────────────────────────────────────────────────
Launch:  streamlit run dashboard.py
"""

import streamlit as st
import pandas as pd

from config import CONFIG
from segmentation_engine import run_segmentation_pipeline
from cluster_optimizer import (
    compute_elbow_curve,
    compute_silhouette_scores,
    select_optimal_clusters,
)
from insights_engine import (
    calculate_segment_distribution,
    calculate_revenue_by_segment,
    get_top_retailers,
    generate_insights,
)
from visualization import (
    plot_segment_distribution,
    plot_revenue_by_segment,
    plot_pca_clusters,
    plot_top_retailers,
    plot_rfm_distributions,
)

# ── Page config ───────────────────────────────────────────────────────────────

st.set_page_config(
    page_title=CONFIG["DASHBOARD"]["PAGE_TITLE"],
    page_icon=CONFIG["DASHBOARD"]["PAGE_ICON"],
    layout=CONFIG["DASHBOARD"]["LAYOUT"],
)

# ── Custom CSS ────────────────────────────────────────────────────────────────

st.markdown(
    """
    <style>
    /* ── Global ─────────────────────────────────────── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    .block-container { padding-top: 1.5rem; padding-bottom: 1rem; }

    /* ── KPI Cards ──────────────────────────────────── */
    .kpi-card {
        background: linear-gradient(135deg, #1e1b4b 0%, #312e81 100%);
        border-radius: 16px;
        padding: 1.4rem 1.6rem;
        text-align: center;
        border: 1px solid rgba(99, 102, 241, .25);
        box-shadow: 0 4px 24px rgba(99, 102, 241, .12);
        transition: transform .2s ease, box-shadow .2s ease;
    }
    .kpi-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 32px rgba(99, 102, 241, .22);
    }
    .kpi-value {
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(90deg, #818cf8, #22d3ee);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: .15rem;
    }
    .kpi-label {
        font-size: .85rem;
        color: #a5b4fc;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: .05em;
    }

    /* ── Section headers ────────────────────────────── */
    .section-header {
        font-size: 1.35rem;
        font-weight: 700;
        color: #e0e7ff;
        margin-top: 2rem;
        margin-bottom: .6rem;
        padding-bottom: .4rem;
        border-bottom: 2px solid #4338ca;
    }

    /* ── Insight cards ──────────────────────────────── */
    .insight-card {
        background: linear-gradient(135deg, #1e1b4b 0%, #1e293b 100%);
        border-left: 4px solid #818cf8;
        border-radius: 10px;
        padding: 1rem 1.2rem;
        margin-bottom: .7rem;
        font-size: .92rem;
        color: #cbd5e1;
        line-height: 1.55;
    }

    /* ── Sidebar ────────────────────────────────────── */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f0a2e 0%, #1e1b4b 100%);
    }
    section[data-testid="stSidebar"] .stMarkdown h1,
    section[data-testid="stSidebar"] .stMarkdown h2,
    section[data-testid="stSidebar"] .stMarkdown h3 { color: #e0e7ff; }

    /* All sidebar body text, labels, paragraphs */
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stMarkdown li,
    section[data-testid="stSidebar"] .stMarkdown span,
    section[data-testid="stSidebar"] .stMarkdown strong,
    section[data-testid="stSidebar"] .stMarkdown code {
        color: #e2e8f0 !important;
    }
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] .stSlider label,
    section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] {
        color: #e2e8f0 !important;
    }
    section[data-testid="stSidebar"] .stSlider [data-testid="stTickBarMin"],
    section[data-testid="stSidebar"] .stSlider [data-testid="stTickBarMax"] {
        color: #a5b4fc !important;
    }
    section[data-testid="stSidebar"] hr {
        border-color: rgba(165, 180, 252, .25);
    }

    /* ── Dataframe table ────────────────────────────── */
    .stDataFrame { border-radius: 12px; overflow: hidden; }
    </style>
    """,
    unsafe_allow_html=True,
)


# ── Cached loaders ────────────────────────────────────────────────────────────

@st.cache_data(show_spinner="Running segmentation pipeline …")
def load_segmented_data(n_clusters: int) -> pd.DataFrame:
    return run_segmentation_pipeline(n_clusters=n_clusters)


@st.cache_data(show_spinner="Finding optimal cluster count …")
def load_optimal_k() -> int:
    raw_df = run_segmentation_pipeline()
    feature_cols = ["recency", "frequency", "monetary", "range_sold"]
    return select_optimal_clusters(raw_df[feature_cols])


# ── Sidebar ───────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("## 📊 Segmentation Controls")
    st.markdown("---")

    optimal_k = load_optimal_k()
    st.markdown(f"**Suggested clusters (silhouette):** `{optimal_k}`")

    n_clusters = st.slider(
        "Number of clusters",
        min_value=2,
        max_value=CONFIG["MAX_K"],
        value=optimal_k,
        help="Adjust the number of segments for KMeans clustering.",
    )

    top_n = st.slider(
        "Top retailers to display",
        min_value=5,
        max_value=25,
        value=CONFIG["DEFAULT_TOP_N"],
    )

    st.markdown("---")
    st.markdown("### About")
    st.markdown(
        "Retail customer segmentation using **RFM analysis** and **KMeans clustering**. "
        "Built with Streamlit & Plotly."
    )


# ── Load data ─────────────────────────────────────────────────────────────────

df = load_segmented_data(n_clusters)

# ── Title ─────────────────────────────────────────────────────────────────────

st.markdown(
    "<h1 style='text-align:center; background:linear-gradient(90deg,#818cf8,#22d3ee);"
    "-webkit-background-clip:text;-webkit-text-fill-color:transparent;"
    "margin-bottom:.1rem;'>Retail Customer Segmentation</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='text-align:center;color:#94a3b8;margin-bottom:1.5rem;'>"
    "RFM Analysis &bull; KMeans Clustering &bull; Business Insights</p>",
    unsafe_allow_html=True,
)


# ── KPI Cards ─────────────────────────────────────────────────────────────────

total_retailers = len(df)
total_revenue = df["monetary"].sum()
avg_order_value = total_revenue / df["frequency"].sum() if df["frequency"].sum() else 0
num_segments = df["value_label"].nunique()

kpi_cols = st.columns(4)
kpis = [
    ("Total Retailers", f"{total_retailers:,}"),
    ("Total Revenue", f"₹{total_revenue:,.0f}"),
    ("Avg Order Value", f"₹{avg_order_value:,.0f}"),
    ("Segments", str(num_segments)),
]

for col, (label, value) in zip(kpi_cols, kpis):
    col.markdown(
        f'<div class="kpi-card"><div class="kpi-value">{value}</div>'
        f'<div class="kpi-label">{label}</div></div>',
        unsafe_allow_html=True,
    )


# ── Segment Distribution ─────────────────────────────────────────────────────

st.markdown('<div class="section-header">🍰 Segment Distribution</div>', unsafe_allow_html=True)
st.plotly_chart(plot_segment_distribution(df), use_container_width=True)


# ── Cluster Visualization ────────────────────────────────────────────────────

st.markdown('<div class="section-header">🔬 Cluster Visualization (PCA)</div>', unsafe_allow_html=True)
st.plotly_chart(plot_pca_clusters(df), use_container_width=True)


# ── Retailer Leaderboard ─────────────────────────────────────────────────────

st.markdown('<div class="section-header">🏆 Retailer Leaderboard</div>', unsafe_allow_html=True)

top_df = get_top_retailers(df, top_n)
display_df = top_df.copy()
display_df.index = range(1, len(display_df) + 1)
display_df.index.name = "Rank"

if "retailer" in display_df.columns:
    display_df["retailer"] = display_df["retailer"].astype(str)
if "monetary" in display_df.columns:
    display_df["monetary"] = display_df["monetary"].apply(lambda x: f"₹{x:,.0f}")

st.dataframe(display_df, use_container_width=True, height=420)


# ── Revenue Analysis ─────────────────────────────────────────────────────────

st.markdown('<div class="section-header">💰 Revenue Analysis</div>', unsafe_allow_html=True)

col_bar, col_table = st.columns([2, 1])
with col_bar:
    st.plotly_chart(plot_revenue_by_segment(df), use_container_width=True)
with col_table:
    rev_df = calculate_revenue_by_segment(df)
    rev_df["revenue"] = rev_df["revenue"].apply(lambda x: f"₹{x:,.0f}")
    rev_df.columns = ["Segment", "Revenue", "Share (%)"]
    st.dataframe(rev_df, use_container_width=True, hide_index=True)


# ── RFM Analytics ─────────────────────────────────────────────────────────────

st.markdown('<div class="section-header">📈 RFM Analytics</div>', unsafe_allow_html=True)
st.plotly_chart(plot_rfm_distributions(df), use_container_width=True)


# ── Business Insights ────────────────────────────────────────────────────────

st.markdown('<div class="section-header">💡 Business Insights</div>', unsafe_allow_html=True)

insights = generate_insights(df)
for insight in insights:
    st.markdown(f'<div class="insight-card">{insight}</div>', unsafe_allow_html=True)


# ── Top Retailers Chart ──────────────────────────────────────────────────────

st.markdown('<div class="section-header">🏅 Top Retailers by Revenue</div>', unsafe_allow_html=True)
st.plotly_chart(plot_top_retailers(df, top_n), use_container_width=True)
