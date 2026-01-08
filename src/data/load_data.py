"""
Load and process Calgary economic data.
"""
import pandas as pd
import numpy as np
import os
from datetime import datetime

def load_alberta_gdp(csv_path):
    """
    Load Alberta GDP data from Statistics Canada CSV.
    """
    print(f"Loading Alberta GDP data from {csv_path}...")
    
    try:
        # Statistics Canada CSV has specific format
        df = pd.read_csv(csv_path, encoding='utf-8')
        
        # Find the relevant columns (varies by download)
        # Look for columns containing 'VALUE' and 'REF_DATE'
        value_col = [col for col in df.columns if 'VALUE' in col][0]
        date_col = [col for col in df.columns if 'REF_DATE' in col][0]
        
        # Clean data
        gdp_data = df[[date_col, value_col]].copy()
        gdp_data.columns = ['date', 'gdp']
        
        # Convert to datetime and numeric
        gdp_data['date'] = pd.to_datetime(gdp_data['date'])
        gdp_data['gdp'] = pd.to_numeric(gdp_data['gdp'], errors='coerce')
        
        # Remove NaN
        gdp_data = gdp_data.dropna()
        
        print(f"✓ Loaded {len(gdp_data)} quarters of GDP data")
        print(f"  Date range: {gdp_data['date'].min().date()} to {gdp_data['date'].max().date()}")
        
        return gdp_data
        
    except Exception as e:
        print(f"✗ Error loading GDP data: {e}")
        print("Please ensure CSV is downloaded from Statistics Canada Table 36-10-0222")
        return None

def load_calgary_employment(csv_path):
    """
    Load Calgary employment data from Statistics Canada CSV.
    """
    print(f"Loading Calgary employment data from {csv_path}...")
    
    try:
        df = pd.read_csv(csv_path, encoding='utf-8')
        
        # Find relevant columns
        value_col = [col for col in df.columns if 'VALUE' in col][0]
        date_col = [col for col in df.columns if 'REF_DATE' in col][0]
        
        # Clean data
        emp_data = df[[date_col, value_col]].copy()
        emp_data.columns = ['date', 'employment']
        
        # Convert to datetime and numeric
        emp_data['date'] = pd.to_datetime(emp_data['date'])
        emp_data['employment'] = pd.to_numeric(emp_data['employment'], errors='coerce')
        
        # Remove NaN
        emp_data = emp_data.dropna()
        
        print(f"✓ Loaded {len(emp_data)} months of employment data")
        print(f"  Date range: {emp_data['date'].min().date()} to {emp_data['date'].max().date()}")
        print(f"  Average employment: {emp_data['employment'].mean():,.0f}")
        
        return emp_data
        
    except Exception as e:
        print(f"✗ Error loading employment data: {e}")
        print("Please ensure CSV is downloaded from Statistics Canada Table 14-10-0323")
        return None

def merge_oil_economy_data(oil_data, gdp_data, emp_data):
    """
    Merge oil price data with Calgary economic data.
    """
    print("\nMerging oil and economic data...")
    
    # Prepare oil data (monthly average for merging with employment)
    oil_monthly = oil_data.set_index('date').resample('M').mean().reset_index()
    oil_monthly.columns = ['date', 'oil_price']
    
    # Convert GDP quarterly to monthly (forward fill)
    gdp_monthly = gdp_data.set_index('date').resample('M').ffill().reset_index()
    
    # Merge all datasets
    merged = pd.merge(oil_monthly, emp_data, on='date', how='inner')
    merged = pd.merge(merged, gdp_monthly, on='date', how='left')
    
    # Calculate growth rates
    merged['oil_return'] = merged['oil_price'].pct_change() * 100
    merged['emp_growth'] = merged['employment'].pct_change() * 100
    merged['gdp_growth'] = merged['gdp'].pct_change(4) * 100  # Year-over-year growth
    
    print(f"✓ Merged dataset: {len(merged)} months")
    print(f"  Final date range: {merged['date'].min().date()} to {merged['date'].max().date()}")
    
    return merged

if __name__ == "__main__":
    # Test the functions
    # Use absolute path relative to project root
    import sys
    import os
    
    # Add project root to Python path
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    DATA_PATH = os.path.join(project_root, "data", "raw")
    
    print("="*60)
    print("CALGARY ECONOMIC DATA LOADER")
    print("="*60)
    
    # Check if oil data exists
    oil_file = os.path.join(DATA_PATH, "wti_crude_prices_2010_2024.csv")
    if os.path.exists(oil_file):
        oil_data = pd.read_csv(oil_file)
        oil_data['date'] = pd.to_datetime(oil_data['date'])
        print(f"✓ Loaded oil data: {len(oil_data)} rows")
    else:
        print("⚠️  Oil price data not found")
        print(f"Expected: {oil_file}")
        oil_data = None
    
    # List expected Calgary data files
    print("\nExpected Canada data files:")
    print(f"1. {os.path.join(DATA_PATH, 'canada_gdp_quarterly.csv')}")
    print(f"2. {os.path.join(DATA_PATH, 'canada_employment_monthly.csv')}")
    
    print("\nTo download these datasets:")
    print("1. Canada GDP: Statistics Canada Table 36-10-0222")
    print("2. Canada Employment: Statistics Canada Table 14-10-0323")
  