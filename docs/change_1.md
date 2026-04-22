# Change 1 — Dashboard Upgrade

**Date:** 2026-03-12  
**Scope:** Upgraded the existing customer segmentation pipeline into a professional, interactive Streamlit analytics dashboard.

---

## Summary of Changes

The project previously consisted of standalone Python scripts (`process.py`, `segmentation.py`) that processed order data, ran KMeans clustering, and displayed static matplotlib charts. This upgrade transforms the project into a **modular, web-based analytics platform** with real-time interactivity.

---

## New Files Created

| File | Lines | Purpose |
|---|---|---|
| `segmentation_engine.py` | ~95 | Reusable RFM + KMeans pipeline |
| `cluster_optimizer.py` | ~50 | Elbow curve, silhouette scores, auto-optimal k |
| `insights_engine.py` | ~78 | Revenue analytics & natural-language insights |
| `visualization.py` | ~155 | Plotly chart functions (dark-themed) |
| `dashboard.py` | ~290 | Streamlit app assembling all modules |

## Modified Files

| File | Change |
|---|---|
| `config.py` | Added `DATA_PATH`, `DELIMITER`, `MAX_K`, `DASHBOARD` section, modernised colour palette |
| `requirements.txt` | Added `plotly` and `streamlit` |

---

## Detailed Module Breakdown

### 1. Segmentation Engine (`segmentation_engine.py`)

Replaces the inline logic from `process.py` and `segmentation.py` with a clean, importable module.

**Functions:**

| Function | Description |
|---|---|
| `load_dataset(filepath)` | Reads the `;`-delimited CSV, parses dates, computes `total_value` |
| `compute_rfm(df)` | Groups by retailer → calculates Recency, Frequency, Monetary, Range Sold |
| `run_kmeans_clustering(features, n_clusters)` | StandardScaler + KMeans, returns labels, scaler, and model |
| `label_clusters(cluster_df)` | Ranks clusters by average monetary value → assigns labels (Very High → Very Low) |
| `run_segmentation_pipeline(filepath, n_clusters)` | End-to-end orchestration: load → RFM → cluster → label → return DataFrame |

**Key design decisions:**
- Uses `df["order_date"].max() + 1 day` as the reference date for recency (not `datetime.today()`), ensuring deterministic results across runs.
- Stores scaled features as `*_scaled` columns on the DataFrame so downstream PCA can use them directly.

---

### 2. Cluster Optimizer (`cluster_optimizer.py`)

The original system hard-coded `k=5`. This module evaluates `k=2` through `k=10` and recommends the best.

**Functions:**

| Function | Description |
|---|---|
| `compute_elbow_curve(features)` | Returns `{k: inertia}` dictionary for elbow method |
| `compute_silhouette_scores(features)` | Returns `{k: silhouette_score}` dictionary |
| `select_optimal_clusters(features)` | Returns the `k` with the highest silhouette score |

The optimal k is displayed in the sidebar and pre-set as the default slider value.

---

### 3. Insights Engine (`insights_engine.py`)

Generates business-ready analytics and human-readable insight sentences.

**Functions:**

| Function | Description |
|---|---|
| `calculate_segment_distribution(df)` | Count and percentage of retailers per segment |
| `calculate_revenue_by_segment(df)` | Total revenue and percentage share per segment |
| `get_top_retailers(df, n)` | Top-N retailers ranked by monetary value |
| `generate_insights(df)` | Returns a list of HTML-formatted insight strings |

**Example insights generated:**
- "**Very High** value retailers contribute **72.2%** of total revenue (₹3,336,581,679)."
- "**High** segment represents **70.5%** of all retailers (3,789 out of 5,375)."
- "Top retailer (**8302997**) generated ₹16,866,613 in total revenue."

---

### 4. Visualization Module (`visualization.py`)

All charts use **Plotly** with a consistent dark theme (`plotly_dark`), transparent backgrounds, and the Inter font family.

**Functions:**

| Function | Chart Type |
|---|---|
| `plot_segment_distribution(df)` | Donut / pie chart |
| `plot_revenue_by_segment(df)` | Horizontal bar chart |
| `plot_pca_clusters(df)` | 2D PCA scatter plot with variance labels |
| `plot_top_retailers(df, n)` | Horizontal bar chart |
| `plot_rfm_distributions(df)` | Three-column histogram subplot |

All functions return `plotly.graph_objects.Figure` objects that Streamlit renders natively via `st.plotly_chart()`.

---

### 5. Dashboard (`dashboard.py`)

The main Streamlit application with custom CSS for a premium dark-themed interface.

**Dashboard sections (in order):**

1. **Sidebar** — Cluster count slider, top-N slider, optimal-k display, about section
2. **KPI Cards** — Total retailers, total revenue, avg order value, number of segments
3. **Segment Distribution** — Interactive donut chart
4. **Cluster Visualization** — PCA scatter coloured by segment
5. **Retailer Leaderboard** — Styled dataframe table
6. **Revenue Analysis** — Bar chart + summary table side-by-side
7. **RFM Analytics** — Recency / Frequency / Monetary histograms
8. **Business Insights** — Auto-generated insight cards with left-accent border
9. **Top Retailers by Revenue** — Horizontal bar chart

**Custom CSS highlights:**
- Gradient KPI cards with hover lift animation
- Indigo-to-dark gradient sidebar with high-contrast text
- Gradient title text (indigo → cyan)
- Insight cards with left border accent and dark glassmorphism background

**Caching:** `@st.cache_data` decorators on pipeline and optimizer calls so the 51 MB CSV is only processed once per cluster count.

---

### 6. Configuration (`config.py`)

New keys added:

| Key | Value | Purpose |
|---|---|---|
| `DATA_PATH` | `data/order_data_all.csv` | Auto-resolved absolute path |
| `DELIMITER` | `;` | CSV separator |
| `MAX_K` | `10` | Upper bound for cluster slider |
| `DEFAULT_TOP_N` | `10` | Default leaderboard size |
| `DASHBOARD` | `{PAGE_TITLE, PAGE_ICON, LAYOUT}` | Streamlit page config |

Colour palette updated to a modern scheme: indigo, cyan, amber, orange, rose.

---

## Dashboard Screenshots

### KPI Cards & Sidebar Controls
![KPI Cards and sidebar showing cluster controls with improved text visibility](docs/screenshot_kpi_cards.png)

### Segment Distribution (Donut Chart)
![Donut chart showing retailer distribution across Very High and High segments](docs/screenshot_segment_distribution.png)

### Cluster Visualization (PCA Scatter Plot)
![2D PCA scatter plot with clusters coloured by segment label](docs/screenshot_pca_clusters.png)

### Retailer Leaderboard
![Ranked table of top retailers by monetary value](docs/screenshot_leaderboard.png)

### Revenue Analysis
![Horizontal bar chart of revenue contribution by segment with summary table](docs/screenshot_revenue_analysis.png)

### RFM Analytics (Distribution Histograms)
![Three-panel histogram showing Recency, Frequency, and Monetary distributions](docs/screenshot_rfm_analytics.png)

### Business Insights Panel
![Auto-generated insight cards with revenue and distribution analysis](docs/screenshot_business_insights.png)

### Top Retailers by Revenue
![Horizontal bar chart of top 10 retailers ranked by total revenue](docs/screenshot_top_retailers.png)

---

## How to Run

```bash
# Install dependencies
pip install -r requirements.txt

# Launch the dashboard
streamlit run dashboard.py
```

The dashboard opens at `http://localhost:8501`. Use the sidebar to:
- Adjust the number of clusters (optimal k is auto-suggested)
- Control how many top retailers to display
- All charts update in real time

---

## Project Structure After Change

```
customer-segmentation-main/
├── config.py                  # Centralised configuration
├── segmentation_engine.py     # RFM + KMeans pipeline
├── cluster_optimizer.py       # Cluster evaluation & optimal-k
├── insights_engine.py         # Revenue analytics & NL insights
├── visualization.py           # Plotly chart functions
├── dashboard.py               # Streamlit dashboard (main entry)
├── requirements.txt           # Python dependencies
├── data/
│   └── order_data_all.csv     # Raw order dataset (~51 MB)
├── docs/
│   ├── change_1.md            # This document
│   ├── implementation_plan.md # Technical plan
│   ├── walkthrough.md         # Verification walkthrough
│   └── screenshot_*.png       # Dashboard screenshots
├── process.py                 # (Legacy) single-profile processor
├── segmentation.py            # (Legacy) matplotlib visualiser
└── README.md
```

---

## Technical Stack

| Component | Technology |
|---|---|
| Language | Python 3.11 |
| Data Processing | pandas, numpy |
| Machine Learning | scikit-learn (KMeans, PCA, StandardScaler, silhouette_score) |
| Visualisation | Plotly |
| Dashboard | Streamlit |
| Styling | Custom CSS (injected via `st.markdown`) |
