"""
Insights Engine
───────────────
Generates business-ready analytics and natural-language insights
from the segmented DataFrame.
"""

import pandas as pd
import numpy as np
from config import CONFIG


def calculate_segment_distribution(df: pd.DataFrame) -> pd.DataFrame:
    """Count and percentage of retailers per value_label."""
    dist = df.groupby("value_label").agg(
        retailer_count=("retailer", "count"),
        color=("color", "first")
    ).reset_index()
    dist.columns = ["value_label", "retailer_count", "color"]
    dist["percentage"] = (dist["retailer_count"] / dist["retailer_count"].sum() * 100).round(1)
    return dist


def calculate_revenue_by_segment(df: pd.DataFrame) -> pd.DataFrame:
    """Total and percentage of monetary value per segment."""
    rev = df.groupby("value_label").agg(
        total_revenue=("monetary", "sum"),
        color=("color", "first")
    ).reset_index()
    rev.columns = ["value_label", "total_revenue", "color"]
    rev["percentage"] = (rev["total_revenue"] / rev["total_revenue"].sum() * 100).round(1)
    rev = rev.sort_values("total_revenue", ascending=False).reset_index(drop=True)
    return rev


def get_top_retailers(
    df: pd.DataFrame, n: int = CONFIG["DEFAULT_TOP_N"]
) -> pd.DataFrame:
    """Top n retailers ranked by monetary value."""
    cols = ["retailer", "monetary", "frequency", "recency", "range_sold", "value_label"]
    available = [c for c in cols if c in df.columns]
    return df.nlargest(n, "monetary")[available].reset_index(drop=True)


def generate_personas(df: pd.DataFrame) -> list[dict]:
    """
    Analyzes cluster centroids to generate descriptive behavioral personas.
    Returns a list of profile objects with names, traits, and significance.
    """
    personas = []
    
    # Calculate group means for all available numeric features
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    feature_cols = [c for c in numeric_cols if "_scaled" not in c and c != "retailer" and c != "value_segment"]
    
    # Group by both numeric ID and display label to keep them linked
    group_means = df.groupby(["value_segment", "value_label"])[feature_cols].mean()
    overall_means = df[feature_cols].mean()
    
    for (val_seg, val_lbl), means in group_means.iterrows():
        # Identify defining traits (where this group deviates most from the mean)
        deviations = (means / overall_means).sort_values(ascending=False)
        top_trait = deviations.index[0]
        bottom_trait = deviations.index[-1]
        
        # Comprehensive Naming Matrix
        if top_trait == "monetary":
            name = "High-Value Catalysts" if means["frequency"] > overall_means["frequency"] else "The Whale Investors"
            description = "Driven by significant transaction volume and consistent high spend."
        elif top_trait == "frequency":
            name = "Loyal Frequenters" if means["recency"] < overall_means["recency"] else "Churned Regulars"
            description = "High engagement retailers who order often but in smaller quantities."
        elif top_trait == "recency":
            name = "At-Risk Veterans" if means["monetary"] > overall_means["monetary"] else "Dormant Accounts"
            description = "Previously active retailers who haven't engaged in a significant period."
        elif top_trait == "range_sold":
            name = "Portfolio Diversifiers"
            description = "Retailers who purchase a wide variety of SKUs across categories."
        else:
            # Descriptive fallbacks for high cluster counts
            fallback_names = [
                "Sleeping Giants", "Rising Stars", "Occasional Opportunists", 
                "Trialists", "Steady Reliable", "Budget Navigators",
                "Fringe Accounts", "Growth Potential"
            ]
            idx = int(val_seg) % len(fallback_names)
            name = fallback_names[idx]
            description = "Observed behavioral pattern with specific niche characteristics."
        
        # Special logic for enhanced features if present
        if "search_intent_score" in means and means["search_intent_score"] > overall_means["search_intent_score"] * 1.2:
            name = "The Active Searchers"
            description = "Highly motivated retailers with high search intent and browsing activity."

        # Try to get color from the dataframe if present
        color = df[df["value_segment"] == val_seg]["color"].iloc[0] if "color" in df.columns else "#6366f1"

        personas.append({
            "label": val_lbl,
            "label_id": int(val_seg),
            "name": name,
            "description": description,
            "top_trait": top_trait.replace("_", " ").title(),
            "color": color,
            "score": round(float(means["monetary"] / overall_means["monetary"] * 10), 1),
            "stats": {k: round(float(v), 2) for k, v in means.items()}
        })
        
    # Sort by numeric label_id (Cluster ID)
    personas.sort(key=lambda x: x["label_id"])
    return personas


def generate_insights(df: pd.DataFrame) -> list[str]:
    """Return a list of human-readable insight sentences (HTML-safe)."""
    insights: list[str] = []
    
    # Revenue contribution per segment
    rev = calculate_revenue_by_segment(df)
    for _, row in rev.iterrows():
        insights.append(
            f"<b>{row['value_label']}</b> value retailers contribute "
            f"<b>{row['percentage']}%</b> of total revenue."
        )

    # Average frequency per segment
    avg_freq = df.groupby("value_label")["frequency"].mean()
    top_seg = avg_freq.idxmax()
    insights.append(
        f"<b>{top_seg}</b> retailers exhibit the highest purchase velocity."
    )

    return insights
