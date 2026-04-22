# Walkthrough — Retail Customer Segmentation Dashboard

## What Was Built

Upgraded the existing RFM + KMeans pipeline into an interactive **Streamlit analytics dashboard** with 6 modules:

| File | Purpose |
|---|---|
| `config.py` | Centralised settings (paths, colours, dashboard config) |
| `segmentation_engine.py` | Reusable pipeline: load → RFM → KMeans → label |
| `cluster_optimizer.py` | Elbow + silhouette analysis, auto-selects optimal k |
| `insights_engine.py` | Revenue, distribution, top retailers, NL insights |
| `visualization.py` | Plotly charts (donut, bars, PCA scatter, histograms) |
| `dashboard.py` | Streamlit app assembling all sections |

---

## Verification Results

Dashboard launched successfully at `http://localhost:8501` — all sections render without errors.

### KPI Cards & Sidebar
![KPI cards with gradient styling and sidebar cluster controls](docs/screenshot_kpi_cards.png)

### Segment Distribution
![Donut chart showing segment distribution](docs/screenshot_segment_distribution.png)

### PCA Cluster Visualization
![PCA scatter plot with clusters](docs/screenshot_pca_clusters.png)

### Retailer Leaderboard
![Top retailers table](docs/screenshot_leaderboard.png)

### Revenue Analysis
![Revenue contribution bar chart](docs/screenshot_revenue_analysis.png)

### RFM Analytics
![RFM distribution histograms](docs/screenshot_rfm_analytics.png)

### Business Insights
![Auto-generated insight cards](docs/screenshot_business_insights.png)

### Top Retailers by Revenue
![Top retailers bar chart](docs/screenshot_top_retailers.png)

---

## How To Launch

```bash
streamlit run dashboard.py
```
