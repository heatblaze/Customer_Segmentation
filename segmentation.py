import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score
import matplotlib.pyplot as plt

from config import CONFIG

# 1. Load pre-processed data
try:
    df = pd.read_csv("data/proccessed_segments.csv")
    if len(df) == 0:
        print("Processed segments file is empty. Please run process.py first.")
        exit()
except FileNotFoundError:
    print("Processed segments file not found. Please run process.py first.")
    exit()

# 2. Separate features and ID
features = df.drop(columns=['retailer', 'value_segment', 'value_label'], errors='ignore')

# 3. Normalize features
scaler = StandardScaler()

# If there's only one row (like in our mock profile testing), 
# scaling and calculating metrics like Silhouette don't make sense.
if len(df) <= 1:
    print("Only 1 profile available. Advanced cluster evaluation/PCA requires > 1 data point.")
    print(f"Profile segmented as: {df['value_label'].iloc[0]}")
    exit()

features_scaled = scaler.fit_transform(features)

# === Cluster Evaluation Loop ===

# Only test up to the number of samples we have
max_clusters = min(10, len(df))
if max_clusters < 2:
    print(f"Not enough data points ({len(df)}) to perform cluster evaluations. Need at least 2.")
    exit()

cluster_range = range(2, max_clusters + 1)  

sil_scores = []
dbi_scores = []
ch_scores = []

for k in cluster_range:
    # Use n_init="auto" to suppress warnings
    kmeans = KMeans(n_clusters=k, random_state=42, n_init="auto")
    labels = kmeans.fit_predict(features_scaled)
    
    # These scores require at least 2 clusters and >1 sample per cluster to be meaningful
    try:
        sil = silhouette_score(features_scaled, labels)
        dbi = davies_bouldin_score(features_scaled, labels)
        ch = calinski_harabasz_score(features_scaled, labels)
    except ValueError:
        sil, dbi, ch = 0, 0, 0
        
    sil_scores.append(sil)
    dbi_scores.append(dbi)
    ch_scores.append(ch)

# Plot evaluation metrics
plt.figure(figsize=(10, 6))
plt.plot(cluster_range, sil_scores, label='Silhouette Score (higher better)', marker='o')
plt.plot(cluster_range, dbi_scores, label='Davies-Bouldin Index (lower better)', marker='o')
plt.plot(cluster_range, ch_scores, label='Calinski-Harabasz Index (higher better)', marker='o')
plt.xlabel('Number of Clusters (k)')
plt.title('Cluster Evaluation Metrics for KMeans')
plt.legend()
plt.grid(True)
plt.show()

# 4. Color Mapping using Config
df['color'] = df['value_label'].map(CONFIG['LABEL_COLORS']).fillna(CONFIG['FALLBACK_COLOR'])

# 5. PCA for 2D visualization
# We need at least 2 samples to do 2-component PCA
n_comp = min(2, len(df), features.shape[1])
pca = PCA(n_components=n_comp)

if n_comp < 2:
    print("Not enough features/samples for 2D PCA representation.")
    exit()

pca_components = pca.fit_transform(features_scaled)

# 6. Loadings
loadings = pd.DataFrame(
    pca.components_.T,
    index=features.columns,
    columns=[f'PCA {i+1}' for i in range(n_comp)]
)

# Create Plots
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Bar chart
loadings.plot(kind='bar', ax=axes[0], title="Feature Contribution to PCA Axes")
axes[0].set_ylabel("Importance (Loading Value)")
axes[0].grid(True, axis='y')

# Scatter plot
for label in df['value_label'].unique():
    mask = df['value_label'] == label
    axes[1].scatter(
        pca_components[mask, 0],
        pca_components[mask, 1],
        label=label,
        color=df[mask]['color'].iloc[0],
        s=50,
        alpha=0.7
    )

axes[1].set_title("Customer Segments (via PCA)", fontsize=14)
axes[1].set_xlabel("PCA Component 1")
axes[1].set_ylabel("PCA Component 2")
axes[1].grid(True)
axes[1].legend(title='Customer Segment')

print("Results graphed!")
plt.tight_layout()
plt.show()
