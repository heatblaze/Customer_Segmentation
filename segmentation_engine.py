"""
Segmentation Engine (V2 - Advanced)
───────────────────────────────────
Advanced clustering pipeline supporting KMeans, HDBSCAN, and GMM.
Handles complex datasets with behavioral and demographic features.
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.mixture import GaussianMixture
import hdbscan

from config import CONFIG


# ── Helpers ───────────────────────────────────────────────────────────────────

def load_dataset(filepath: str | None = None) -> pd.DataFrame:
    """Read the dataset. Automatically switches to enhanced data if available."""
    if filepath is None:
        enhanced_path = CONFIG["DATA_PATH"].replace("order_data_all.csv", "enhanced_data.csv")
        filepath = enhanced_path if os.path.exists(enhanced_path) else CONFIG["DATA_PATH"]
    
    # If it's the raw order data, we need computed RFM. 
    # If it's enhanced_data, it's already at retailer level.
    df = pd.read_csv(filepath)
    
    if "order_date" in df.columns:
        df["order_date"] = pd.to_datetime(df["order_date"], format=CONFIG["DATE_FORMAT"])
        if "quantity" in df.columns and "skuPrice" in df.columns:
            df["total_value"] = df["quantity"] * df["skuPrice"]
    
    return df


def compute_rfm(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate orders into one row per retailer if not already aggregated."""
    if "retailer" in df.columns and "recency" in df.columns:
        return df # Already aggregated (enhanced data)

    today = df["order_date"].max() + pd.Timedelta(days=1)

    rfm = df.groupby("retailer").agg(
        recency=("order_date", lambda x: (today - x.max()).days),
        frequency=("orderId", "nunique"),
        monetary=("total_value", "sum"),
        range_sold=("sku", "nunique"),
    ).reset_index()

    return rfm


def run_clustering(
    features: pd.DataFrame,
    algorithm: str = "kmeans",
    n_clusters: int = CONFIG["NUM_CLUSTERS"],
) -> tuple[np.ndarray, StandardScaler, any]:
    """Scale features and run the selected clustering algorithm."""
    scaler = StandardScaler()
    scaled = scaler.fit_transform(features)
    
    if algorithm == "kmeans":
        model = KMeans(n_clusters=n_clusters, random_state=42, n_init="auto")
        labels = model.fit_predict(scaled)
    elif algorithm == "hdbscan":
        # HDBSCAN finds its own cluster count, but we can tune min_cluster_size
        model = hdbscan.HDBSCAN(min_cluster_size=15, gen_min_span_tree=True)
        labels = model.fit_predict(scaled)
    elif algorithm == "gmm":
        model = GaussianMixture(n_components=n_clusters, random_state=42)
        model.fit(scaled)
        labels = model.predict(scaled)
        # GMM also provides probabilities which we could use later
    else:
        raise ValueError(f"Unknown algorithm: {algorithm}")
        
    return labels, scaler, model


def label_clusters(cluster_df: pd.DataFrame, algorithm: str = "kmeans") -> pd.DataFrame:
    """Assign human-readable value labels based on rank."""
    # Group by labels and use monetary as the primary ranking factor
    avg_monetary = (
        cluster_df.groupby("value_segment")["monetary"]
        .mean()
        .sort_values(ascending=False)
    )

    base_labels = CONFIG["LABELS"].copy()
    
    # HDBSCAN uses -1 for noise
    if -1 in avg_monetary.index:
        segment_map = {-1: "Outliers"}
        avg_monetary = avg_monetary.drop(-1)
    else:
        segment_map = {}

    while len(base_labels) < len(avg_monetary):
        fallback_names = [
            "Sleeping Giants", "Rising Stars", "Occasional Opportunists", 
            "Trialists", "Steady Reliable", "Budget Navigators",
            "Fringe Accounts", "Growth Potential"
        ]
        next_name = fallback_names[(len(base_labels) - 5) % len(fallback_names)]
        base_labels.append(next_name)

    for i, seg in enumerate(avg_monetary.index):
        segment_map[seg] = base_labels[i]

    cluster_df["value_label"] = cluster_df["value_segment"].map(segment_map)
    cluster_df["color"] = (
        cluster_df["value_label"]
        .map(CONFIG.get("LABEL_COLORS", {}))
        .fillna(CONFIG.get("FALLBACK_COLOR", "#94a3b8"))
    )
    return cluster_df


# ── Main Pipeline ─────────────────────────────────────────────────────────────

def run_segmentation_pipeline(
    filepath: str | None = None,
    n_clusters: int | None = None,
    algorithm: str = "kmeans",
    use_enhanced: bool = True
) -> pd.DataFrame:
    """End-to-end segmentation: load → augment → cluster → label → return."""
    n_clusters = n_clusters or CONFIG["NUM_CLUSTERS"]

    # 1. Load data
    data = load_dataset(filepath)
    
    # 2. Compute/Ensure RFM
    rfm = compute_rfm(data)
    
    # 3. Identify feature columns
    feature_cols = ["recency", "frequency", "monetary", "range_sold"]
    
    # If using enhanced data, add more features
    enhanced_cols = [
        'avg_session_duration', 'abandoned_cart_rate', 'search_intent_score', 
        'email_open_rate', 'loyalty_score', 'income_bracket', 'city_tier'
    ]
    
    available_enhanced = [c for c in enhanced_cols if c in rfm.columns]
    if use_enhanced and available_enhanced:
        feature_cols.extend(available_enhanced)

    # 4. Cluster
    labels, scaler, model = run_clustering(rfm[feature_cols], algorithm, n_clusters)
    rfm["value_segment"] = labels

    # 5. Label
    rfm = label_clusters(rfm, algorithm)

    # 6. Keep scaled features for PCA or visualization
    scaled = scaler.transform(rfm[feature_cols])
    for i, col in enumerate(feature_cols):
        rfm[f"{col}_scaled"] = scaled[:, i]

    return rfm, model, scaled
