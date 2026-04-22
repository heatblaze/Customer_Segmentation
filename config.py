"""
Configuration file for Customer Segmentation Dashboard
"""
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CONFIG = {
    # ── Data ──────────────────────────────────────────────
    "DATA_PATH": os.path.join(BASE_DIR, "data", "order_data_all.csv"),
    "DELIMITER": ";",
    "DATE_FORMAT": "%m/%d/%y",

    # ── Clustering ────────────────────────────────────────
    "NUM_CLUSTERS": 5,
    "MAX_K": 10,

    # ── RFM weights (reserved for future use) ─────────────
    "RFM_WEIGHTS": {
        "recency": 1.0,
        "frequency": 1.0,
        "monetary": 1.0,
        "range": 1.0,
    },

    # ── Labels & colours ──────────────────────────────────
    "LABELS": ["Very High", "High", "Medium", "Low", "Very Low"],
    "LABEL_COLORS": {
        "Very High": "#6366f1",   # indigo
        "High":      "#22d3ee",   # cyan
        "Medium":    "#facc15",   # amber
        "Low":       "#fb923c",   # orange
        "High Risk": "#f43f5e",   # rose  (alias kept for safety)
        "Very Low":  "#f43f5e",   # rose
    },
    "FALLBACK_COLOR": "#94a3b8",

    # ── Insights ──────────────────────────────────────────
    "DEFAULT_TOP_N": 10,

    # ── Dashboard ─────────────────────────────────────────
    "DASHBOARD": {
        "PAGE_TITLE": "Retail Customer Segmentation",
        "PAGE_ICON": "📊",
        "LAYOUT": "wide",
    },
}
