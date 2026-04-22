"""
Cluster Optimizer
─────────────────
Evaluates KMeans for k = 2 … MAX_K using Inertia (Elbow) and
Silhouette Score, then selects the optimal cluster count.
"""

import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

from config import CONFIG


def _scale(features) -> np.ndarray:
    """Standardise features (helper)."""
    return StandardScaler().fit_transform(features)


def compute_elbow_curve(features) -> dict[int, float]:
    """Return {k: inertia} for k = 2 … MAX_K."""
    scaled = _scale(features)
    max_k = min(CONFIG["MAX_K"], len(scaled) - 1)
    results = {}
    for k in range(2, max_k + 1):
        km = KMeans(n_clusters=k, random_state=42, n_init="auto")
        km.fit(scaled)
        results[k] = km.inertia_
    return results


def compute_silhouette_scores(features) -> dict[int, float]:
    """Return {k: silhouette_score} for k = 2 … MAX_K."""
    scaled = _scale(features)
    max_k = min(CONFIG["MAX_K"], len(scaled) - 1)
    results = {}
    for k in range(2, max_k + 1):
        km = KMeans(n_clusters=k, random_state=42, n_init="auto")
        labels = km.fit_predict(scaled)
        results[k] = silhouette_score(scaled, labels)
    return results


def select_optimal_clusters(features) -> int:
    """Return the k with the highest silhouette score."""
    scores = compute_silhouette_scores(features)
    if not scores:
        return CONFIG["NUM_CLUSTERS"]
    return max(scores, key=scores.get)
