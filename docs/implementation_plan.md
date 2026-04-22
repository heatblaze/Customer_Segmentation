# Implementation Plan — Retail Customer Segmentation Dashboard Upgrade

Upgrade the existing pipeline (RFM + KMeans) into an interactive Streamlit analytics dashboard with modern Plotly charts, cluster optimization, and auto-generated business insights.

---

## Proposed Changes

### Configuration

#### [MODIFY] config.py

Add `DATA_PATH`, `DELIMITER`, `DATE_FORMAT`, `MAX_K`, `DEFAULT_TOP_N`, and a `DASHBOARD` section (page title, icon, layout) so all tunables live in one place.

---

### Segmentation Engine

#### [NEW] segmentation_engine.py

Reusable module that replaces the inline logic in `process.py` and `segmentation.py`:

| Function | Purpose |
|---|---|
| `load_dataset(filepath)` | Read CSV with `;` delimiter, parse dates |
| `compute_rfm(df)` | Group by retailer → recency / frequency / monetary / range |
| `run_kmeans_clustering(features, n_clusters)` | Scale with `StandardScaler`, fit KMeans, return labels |
| `label_clusters(cluster_df)` | Rank clusters by monetary mean, assign Very High → Very Low |
| `run_segmentation_pipeline(filepath)` | Orchestrate all steps, return enriched DataFrame |

---

### Cluster Optimizer

#### [NEW] cluster_optimizer.py

| Function | Purpose |
|---|---|
| `compute_elbow_curve(features)` | KMeans inertia for k = 2..10 |
| `compute_silhouette_scores(features)` | Silhouette score for k = 2..10 |
| `select_optimal_clusters(features)` | Return best k (highest silhouette) |

---

### Insights Engine

#### [NEW] insights_engine.py

| Function | Purpose |
|---|---|
| `calculate_segment_distribution(df)` | Count + % of retailers per segment |
| `calculate_revenue_by_segment(df)` | Sum monetary per segment + % share |
| `get_top_retailers(df, n)` | Top N retailers by monetary |
| `generate_insights(df)` | Return list of human-readable insight sentences |

---

### Visualization

#### [NEW] visualization.py

All charts use **Plotly** with a dark template. Functions return `plotly.graph_objects.Figure` objects for direct use in Streamlit.

| Function | Chart |
|---|---|
| `plot_segment_distribution(df)` | Donut / Pie chart |
| `plot_revenue_by_segment(df)` | Horizontal bar chart |
| `plot_pca_clusters(df)` | 2D PCA scatter plot |
| `plot_top_retailers(df, n)` | Horizontal bar chart |
| `plot_rfm_distributions(df)` | Histogram subplots for recency, frequency, monetary |

---

### Dashboard

#### [NEW] dashboard.py

Streamlit app with sections:

1. **Sidebar** — Project info, optimal-k display, cluster-count selector
2. **KPI Cards** — Total retailers, total revenue, avg order value, # segments
3. **Segment Distribution** — Pie chart
4. **Cluster Visualization** — PCA scatter
5. **Retailer Leaderboard** — Styled dataframe
6. **Revenue Analysis** — Bar chart
7. **RFM Analytics** — Distribution histograms
8. **Business Insights** — Auto-generated insight cards

Uses `@st.cache_data` for dataset loading and pipeline caching.

---

### Dependencies

#### [MODIFY] requirements.txt

Add `plotly` and `streamlit` to the existing list.

---

## Verification Plan

1. Install dependencies: `pip install -r requirements.txt`
2. Launch: `streamlit run dashboard.py`
3. Verify all 8 sections render without errors at `http://localhost:8501`
4. Test sidebar cluster-count slider — charts should update dynamically
