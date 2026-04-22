import pandas as pd
import numpy as np
import os
from segmentation_engine import load_dataset, compute_rfm
from config import CONFIG

def augment_dataset():
    print("Starting Data Augmentation...")
    
    # 1. Load base data and compute RFM
    df = load_dataset()
    rfm = compute_rfm(df)
    
    # Seed for reproducibility
    np.random.seed(42)
    n_retailers = len(rfm)
    
    print(f"Processing {n_retailers} retailers...")

    # 2. Add Behavioral Complexity
    # Avg_Session_Duration (minutes) - normally distributed around 15 mins
    rfm['avg_session_duration'] = np.random.normal(15, 5, n_retailers).clip(2, 60)
    
    # Abandoned_Carts - higher for high frequency users (simulating friction)
    rfm['abandoned_cart_rate'] = (np.random.beta(2, 5, n_retailers) * (1 + rfm['frequency'] / 50)).clip(0, 1)
    
    # Search_Intent_Score (0-100)
    rfm['search_intent_score'] = np.random.randint(0, 101, n_retailers)

    # 3. Add Engagement Complexity
    # Email_Open_Rate (0-1) - beta distribution
    rfm['email_open_rate'] = np.random.beta(2, 2, n_retailers)
    
    # Loyalty_Score (0-100)
    rfm['loyalty_score'] = (rfm['monetary'] / rfm['monetary'].max() * 50 + np.random.randint(0, 51, n_retailers)).clip(0, 100)

    # 4. Add Psychographic/Demographic Complexity
    # Income_Bracket (1-5)
    rfm['income_bracket'] = np.random.choice([1, 2, 3, 4, 5], n_retailers, p=[0.1, 0.3, 0.4, 0.15, 0.05])
    
    # City_Tier (1-3)
    rfm['city_tier'] = np.random.choice([1, 2, 3], n_retailers, p=[0.4, 0.4, 0.2])

    # 5. Add Temporal Complexity
    # Preferred_Shop_Time (0: Morning, 1: Afternoon, 2: Evening, 3: Night)
    rfm['preferred_shop_time'] = np.random.choice([0, 1, 2, 3], n_retailers)

    # 6. Save Enhanced Dataset
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'enhanced_data.csv')
    rfm.to_csv(output_path, index=False)
    
    print(f"Enhanced dataset saved to: {output_path}")
    print(f"New columns added: {list(rfm.columns[5:])}")

if __name__ == "__main__":
    augment_dataset()
