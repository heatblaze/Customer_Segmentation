import pandas as pd
from datetime import datetime, timedelta
import numpy as np

def calculate_6month_frequency_model():
    """
    Calculate the average order frequency for the last 6 months for each retailer.
    This version is designed for model/simulated data where we use the latest date
    in the dataset as the reference point.
    """
    
    # Load the original order data
    print("Loading order data...")
    df = pd.read_csv("data/order_data_all.csv", delimiter=';')
    
    # Convert order_date to datetime
    df['order_date'] = pd.to_datetime(df['order_date'], format='%m/%d/%y')
    
    # Set reference date (6 months ago from the latest date in the data)
    latest_date = df['order_date'].max()
    six_months_ago = latest_date - pd.DateOffset(months=6)
    
    print(f"Latest date in data: {latest_date}")
    print(f"6 months ago from latest: {six_months_ago}")
    
    # Filter orders from the last 6 months
    recent_orders = df[df['order_date'] >= six_months_ago].copy()
    
    if recent_orders.empty:
        print("No orders found in the last 6 months!")
        return None
    
    print(f"Orders in last 6 months: {len(recent_orders)}")
    print(f"Retailers with orders in last 6 months: {recent_orders['retailer'].nunique()}")
    
    # Calculate 6-month frequency metrics for each retailer
    print("Calculating 6-month frequency metrics...")
    
    # Group by retailer and calculate metrics for last 6 months
    six_month_metrics = recent_orders.groupby('retailer').agg({
        'orderId': pd.Series.nunique,  # Number of orders in last 6 months
        'order_date': ['min', 'max']   # First and last order dates in period
    }).reset_index()
    
    # Flatten column names
    six_month_metrics.columns = ['retailer', 'orders_6m', 'first_order_6m', 'last_order_6m']
    
    # Calculate the time span for each retailer in the 6-month period
    six_month_metrics['first_order_6m'] = pd.to_datetime(six_month_metrics['first_order_6m'])
    six_month_metrics['last_order_6m'] = pd.to_datetime(six_month_metrics['last_order_6m'])
    
    # Calculate days between first and last order in the 6-month period
    six_month_metrics['days_span_6m'] = (six_month_metrics['last_order_6m'] - six_month_metrics['first_order_6m']).dt.days
    
    # Calculate average order frequency (orders per month) for the last 6 months
    # If customer has only 1 order, we'll use a conservative estimate
    six_month_metrics['avg_frequency_6m'] = np.where(
        six_month_metrics['orders_6m'] == 1,
        1,  # If only 1 order, frequency is 1
        six_month_metrics['orders_6m'] / 6  # Orders per month over 6 months
    )
    
    # Alternative: Calculate frequency based on actual time span
    # This gives a more accurate measure for customers with multiple orders
    six_month_metrics['frequency_per_month_6m'] = np.where(
        six_month_metrics['days_span_6m'] == 0,
        six_month_metrics['orders_6m'],  # If all orders on same day
        (six_month_metrics['orders_6m'] / (six_month_metrics['days_span_6m'] / 30.44))  # Orders per month
    )
    
    # Handle infinite values (when days_span is 0)
    six_month_metrics['frequency_per_month_6m'] = six_month_metrics['frequency_per_month_6m'].replace([np.inf, -np.inf], np.nan)
    six_month_metrics['frequency_per_month_6m'] = six_month_metrics['frequency_per_month_6m'].fillna(six_month_metrics['orders_6m'])
    
    # Load existing segmentation data
    print("Loading existing segmentation data...")
    segments_df = pd.read_csv("data/proccessed_segments.csv")
    
    # Merge the 6-month frequency data with existing segments
    enhanced_segments = segments_df.merge(
        six_month_metrics[['retailer', 'orders_6m', 'avg_frequency_6m', 'frequency_per_month_6m']], 
        on='retailer', 
        how='left'
    )
    
    # Fill NaN values for retailers who had no orders in the last 6 months
    enhanced_segments['orders_6m'] = enhanced_segments['orders_6m'].fillna(0)
    enhanced_segments['avg_frequency_6m'] = enhanced_segments['avg_frequency_6m'].fillna(0)
    enhanced_segments['frequency_per_month_6m'] = enhanced_segments['frequency_per_month_6m'].fillna(0)
    
    # Save the enhanced segmentation data
    enhanced_segments.to_csv("data/enhanced_segments_model.csv", index=False)
    
    print(f"Enhanced segmentation data saved with {len(enhanced_segments)} retailers")
    print(f"Retailers with orders in last 6 months: {len(six_month_metrics)}")
    print(f"Retailers with no orders in last 6 months: {len(enhanced_segments) - len(six_month_metrics)}")
    
    # Print summary statistics
    print("\n6-Month Frequency Summary Statistics:")
    print(f"Average orders in last 6 months: {enhanced_segments['orders_6m'].mean():.2f}")
    print(f"Average frequency per month: {enhanced_segments['frequency_per_month_6m'].mean():.2f}")
    print(f"Max orders in last 6 months: {enhanced_segments['orders_6m'].max()}")
    print(f"Max frequency per month: {enhanced_segments['frequency_per_month_6m'].max():.2f}")
    
    return enhanced_segments

if __name__ == "__main__":
    enhanced_data = calculate_6month_frequency_model()
    if enhanced_data is not None:
        print("\nEnhanced segmentation complete! New features added:")
        print("- orders_6m: Number of orders in the last 6 months")
        print("- avg_frequency_6m: Average order frequency (orders per month) over 6 months")
        print("- frequency_per_month_6m: Frequency based on actual time span between orders")
        print("\nOutput saved to: data/enhanced_segments_model.csv") 