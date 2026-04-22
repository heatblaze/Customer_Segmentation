import pandas as pd
from datetime import datetime
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import json
import logging

from config import CONFIG

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def run_segmentation(profile_data):
    """
    Process a single retailer profile for customer segmentation.
    Expects profile_data to be a dictionary matching the defined schema.
    """
    logging.info(f"Processing segmentation for Profile ID: {profile_data.get('profile_id')} - {profile_data.get('retailer_name')}")
    
    # Extract orders from the profile
    orders = profile_data.get('orders', [])
    if not orders:
        logging.warning("No orders found in the profile data.")
        return None
        
    df = pd.DataFrame(orders)
    
    # We assign the retailer name or ID to the orders so the groupby works seamlessly 
    # as it did in the original CSV-based logic
    retailer_identifier = profile_data.get('retailer_name', profile_data.get('profile_id', 'Unknown'))
    df['retailer'] = retailer_identifier

    # Convert order_date to datetime using the configured format
    df['order_date'] = pd.to_datetime(df['order_date'], format=CONFIG['DATE_FORMAT'])

    # Calculate total value for each row
    df['total_value'] = df['quantity'] * df['skuPrice']

    # Set today's date for recency calculation
    today = datetime.today()

    # Group by retailer to build RFM + Range Sold table
    rfm = df.groupby('retailer').agg({
        'order_date': lambda x: (today - x.max()).days,  # Recency
        'orderId': pd.Series.nunique,                   # Frequency
        'total_value': 'sum',                           # Monetary
        'sku': pd.Series.nunique                        # Range Sold
    }).reset_index()

    # Rename columns
    rfm.columns = ['retailer', 'recency', 'frequency', 'monetary', 'range']
    
    # Note: If we had multiple retailers, we'd scale across them. 
    # Since we are processing a single profile here, scaling and clustering 
    # against just ONE row doesn't make mathematical sense for KMeans.
    # However, to maintain the pipeline structure shown in the original process.py
    # we will apply the scaler and kmeans, but note that for a single retailer,
    # it will always fall into 1 cluster.
    
    # Normalize data for clustering
    scaler = StandardScaler()
    rfm_scaled = scaler.fit_transform(rfm[['recency', 'frequency', 'monetary', 'range']])

    # Run KMeans clustering
    # Handle single sample case (KMeans requires n_samples >= n_clusters)
    num_clusters = min(CONFIG['NUM_CLUSTERS'], len(rfm))
    
    if num_clusters < 1:
         logging.error("Not enough data to cluster.")
         return None
         
    kmeans = KMeans(n_clusters=num_clusters, random_state=42, n_init="auto")
    rfm['value_segment'] = kmeans.fit_predict(rfm_scaled)

    # Dynamically label clusters by average monetary value
    avg_monetary = rfm.groupby('value_segment')['monetary'].mean().sort_values(ascending=False)

    # Use configured labels
    label_base = CONFIG['LABELS'].copy()
    while len(label_base) < num_clusters:
        label_base.append(f"Segment {len(label_base) + 1}")

    # Create mapping from cluster to label
    segment_map = {seg: label_base[i] for i, seg in enumerate(avg_monetary.index)}
    rfm['value_label'] = rfm['value_segment'].map(segment_map)

    # Optional: Save or return
    output_dict = rfm.to_dict(orient='records')
    logging.info(f"Segmentation complete: {output_dict}")
    return output_dict

if __name__ == "__main__":
    # Test the refactored function with the mock profile
    try:
        with open('mock_profile.json', 'r') as f:
            mock_data = json.load(f)
        
        results = run_segmentation(mock_data)
        
        # Save output for segmentation.py to still use if needed for testing downstream
        if results:
            pd.DataFrame(results).to_csv("data/proccessed_segments.csv", index=False)
            logging.info("Saved test results to data/proccessed_segments.csv")
            
    except FileNotFoundError:
        logging.error("mock_profile.json not found. Cannot run test.")

