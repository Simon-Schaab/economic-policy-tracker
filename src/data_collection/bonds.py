from fredapi import Fred
import pandas as pd
import os
from datetime import datetime, timedelta

def get_bond_data(api_key, series_ids=None, start_date=None, end_date=None):
    """
    Retrieve bond data from FRED API.
    
    Parameters:
    - api_key (str): FRED API key
    - series_ids (dict): Dictionary of {name: series_id} to retrieve (default: Treasury yields)
    - start_date (str): Start date in format 'YYYY-MM-DD' (default: 1 year ago)
    - end_date (str): End date in format 'YYYY-MM-DD' (default: today)
    
    Returns:
    - dict: Dictionary with series names as keys and DataFrame of historical data as values
    """
    # Initialize FRED API client
    fred = Fred(api_key=api_key)
    
    # Default to key Treasury yields if no series provided
    if series_ids is None:
        series_ids = {
            "Treasury_3M": "DTB3",        # 3-Month Treasury Bill
            "Treasury_2Y": "DGS2",        # 2-Year Treasury Constant Maturity
            "Treasury_5Y": "DGS5",        # 5-Year Treasury Constant Maturity
            "Treasury_10Y": "DGS10",      # 10-Year Treasury Constant Maturity
            "Treasury_30Y": "DGS30",      # 30-Year Treasury Constant Maturity
            "Yield_Curve": "T10Y2Y"       # 10-Year Treasury Minus 2-Year Treasury
        }
    
    # Set default dates if not provided
    if end_date is None:
        end_date = datetime.now().strftime('%Y-%m-%d')
    
    if start_date is None:
        # Default to one year of data
        start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
    
    # Dictionary to store results
    data = {}
    
    # Retrieve data for each series
    for name, series_id in series_ids.items():
        try:
            print(f"Retrieving {name} (Series: {series_id})...")
            series_data = fred.get_series(series_id, start_date, end_date)
            
            # Convert Series to DataFrame with date index
            if not series_data.empty:
                df = pd.DataFrame(series_data)
                df.columns = ['Value']
                df.index.name = 'Date'
                
                # Add metadata
                df['Series_ID'] = series_id
                df['Description'] = name
                
                data[name] = df
                print(f"Successfully retrieved {len(df)} records for {name}")
            else:
                print(f"No data found for {name} (Series: {series_id})")
        
        except Exception as e:
            print(f"Error retrieving data for {name} (Series: {series_id}): {e}")
    
    return data

def save_bond_data(data, directory="data/bonds"):
    """
    Save bond data to CSV files.
    
    Parameters:
    - data (dict): Dictionary with series names as keys and DataFrame of historical data as values
    - directory (str): Directory to save CSV files
    
    Returns:
    - list: List of saved file paths
    """
    # Create directory if it doesn't exist
    os.makedirs(directory, exist_ok=True)
    
    saved_files = []
    
    # Save each series' data to a CSV file
    for name, df in data.items():
        filename = f"{name}.csv"
        filepath = os.path.join(directory, filename)
        
        # Save to CSV
        df.to_csv(filepath)
        saved_files.append(filepath)
        print(f"Saved {len(df)} records to {filepath}")
    
    return saved_files

def update_bond_data(api_key):
    """
    Update bond data for Treasury yields.
    
    Parameters:
    - api_key (str): FRED API key
    
    Returns:
    - list: List of saved file paths
    """
    # Get bond data
    data = get_bond_data(api_key)
    
    # Save bond data
    saved_files = save_bond_data(data)
    
    return saved_files

def plot_yield_curve(api_key, date=None):
    """
    Get data for plotting a yield curve at a specific date.
    
    Parameters:
    - api_key (str): FRED API key
    - date (str): Date in format 'YYYY-MM-DD' (default: most recent available date)
    
    Returns:
    - DataFrame: Data for plotting yield curve
    """
    # Series IDs for different maturities
    maturities = {
        "3-Month": "DTB3",
        "2-Year": "DGS2", 
        "5-Year": "DGS5",
        "10-Year": "DGS10",
        "30-Year": "DGS30"
    }
    
    # Initialize FRED API client
    fred = Fred(api_key=api_key)
    
    # Dictionary to store results
    data = {}
    
    # Get the latest date if not specified
    if date is None:
        # Get the 10-year yield to determine most recent date
        series = fred.get_series("DGS10")
        date = series.index[-1].strftime('%Y-%m-%d')
    
    # Get data for each maturity
    for label, series_id in maturities.items():
        try:
            # Get entire series first
            series = fred.get_series(series_id)
            
            # Find closest date with data
            if date in series.index:
                value = series[date]
            else:
                # Find nearest date
                nearest_date = min(series.index, key=lambda x: abs(x - pd.to_datetime(date)))
                value = series[nearest_date]
                date = nearest_date.strftime('%Y-%m-%d')
            
            data[label] = value
        
        except Exception as e:
            print(f"Error retrieving data for {label} (Series: {series_id}): {e}")
            data[label] = None
    
    # Convert to DataFrame
    df = pd.DataFrame(list(data.items()), columns=['Maturity', 'Yield'])
    
    # Add date information
    df['Date'] = date
    
    return df

if __name__ == "__main__":
    # If run directly, prompt for API key and update bond data
    api_key = input("Enter your FRED API key: ")
    update_bond_data(api_key)