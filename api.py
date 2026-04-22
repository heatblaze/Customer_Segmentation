from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np
import json
from segmentation_engine import run_segmentation_pipeline
from insights_engine import (
    generate_insights,
    generate_personas, 
    calculate_segment_distribution, 
    calculate_revenue_by_segment,
    get_top_retailers
)
from config import CONFIG

app = FastAPI(title="Customer Segmentation API")

# Enable CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Customer Segmentation API is running"}

@app.get("/segments")
def get_segments(
    algorithm: str = Query("kmeans", enum=["kmeans", "hdbscan", "gmm"]),
    n_clusters: int = Query(5, ge=2, le=10),
    use_enhanced: bool = True
):
    """Run segmentation and return full dataset + insights."""
    try:
        # Run pipeline
        df, model, scaled = run_segmentation_pipeline(
            n_clusters=n_clusters, 
            algorithm=algorithm, 
            use_enhanced=use_enhanced
        )
        
        # Calculate clustering quality (Silhouette Score)
        from sklearn.metrics import silhouette_score
        try:
            # Silhouette is slow for large datasets, so we sample if needed
            sample_size = min(len(scaled), 5000)
            if sample_size > 100:
                indices = np.random.choice(len(scaled), sample_size, replace=False)
                score = float(silhouette_score(scaled[indices], df.iloc[indices]["value_segment"]))
            else:
                score = 0.0
        except:
            score = 0.0
            
        # Prepare insights
        insights = generate_insights(df)
        personas = generate_personas(df)
        distribution = calculate_segment_distribution(df).to_dict(orient="records")
        revenue = calculate_revenue_by_segment(df).to_dict(orient="records")
        
        # Leaderboard
        leaderboard = get_top_retailers(df, n=20).to_dict(orient="records")
        
        # RFM Distributions (Histograms)
        rfm_distributions = {}
        for metric in ["recency", "frequency", "monetary"]:
            counts, bins = np.histogram(df[metric], bins=20)
            rfm_distributions[metric] = {
                "counts": counts.tolist(),
                "bins": bins.tolist()
            }
            
        # Basic stats
        stats = {
            "total_retailers": len(df),
            "total_revenue": float(df["monetary"].sum()),
            "avg_monetary": float(df["monetary"].mean()),
            "segments_found": int(df["value_segment"].nunique())
        }
        
        # Headers/Features for profiles
        feature_cols = ["recency", "frequency", "monetary", "range_sold"]
        
        return {
            "status": "success",
            "metadata": {
                "algorithm": algorithm,
                "n_clusters": n_clusters,
                "use_enhanced": use_enhanced,
                "silhouette_score": score
            },
            "stats": stats,
            "distribution": distribution,
            "revenue": revenue,
            "leaderboard": leaderboard,
            "rfm_distributions": rfm_distributions,
            "insights": insights,
            "personas": personas,
            "data": df.head(500).to_dict(orient="records")
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/retailer/{retailer_id}")
def get_retailer(retailer_id: int):
    """Get detailed profile for a single retailer."""
    df = run_segmentation_pipeline(use_enhanced=True) # Defaults
    retailer = df[df["retailer"] == retailer_id]
    
    if retailer.empty:
        return {"status": "error", "message": "Retailer not found"}
        
    return {
        "status": "success",
        "data": retailer.to_dict(orient="records")[0]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
