from fredapi import Fred
import pandas as pd
import os
from datetime import datetime, timedelta

def get_economic_indicators(api_key, indicators=None, start_date=None, end_date=None):
    """
    Retrieve economic indicator data from FRED API.
    
    Parameters:
    - api_key (str): FRED API key
    - indicators (dict): Dictionary of {name: series_id} to retrieve (default: key economic indicators)
    - start_date (str): Start date in format 'YYYY-MM-DD' (default: 5 years ago)
    - end_date (str): End date in format 'YYYY-MM-DD' (default: today)
    
    Returns:
    - dict: Dictionary with indicator names as keys and DataFrame of historical data as values
    """
    # Initialize FRED API client
    fred = Fred(api_key=api_key)
    
    # Default to key economic indicators if none provided
    if indicators is None:
        indicators = {
            "Unemployment_Rate": "UNRATE",           # Unemployment Rate
            "CPI_Inflation": "CPIAUCSL",             # Consumer Price Index for All Urban Consumers
            "Core_CPI": "CPILFESL",                  # CPI for All Urban Consumers: All Items Less Food & Energy
            "GDP_Growth": "A191RL1Q225SBEA",         # Real GDP Growth Rate
            "Industrial_Production": "INDPRO",       # Industrial Production Index
            "Consumer_Sentiment": "UMCSENT",         # University of Michigan: Consumer Sentiment
            "Retail_Sales": "RSXFS",                 # Retail Sales
            "Housing_Starts": "HOUST",               # Housing Starts
            "Initial_Claims": "ICSA",                # Initial Claims for Unemployment Insurance
            "Fed_Funds_Rate": "FEDFUNDS"             # Federal Funds Effective Rate
        }
    
    # Set default dates if not provided
    if end_date is None:
        end_date = datetime.now().strftime('%Y-%m-%d')
    
    if start_date is None:
        # Default to five years of data for economic indicators
        start_date = (datetime.now() - timedelta(days=5*365)).strftime('%Y-%m-%d')
    
    # Dictionary to store results
    data = {}
    
    # Retrieve data for each indicator
    for name, series_id in indicators.items():
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
                
                # Add frequency information
                info = fred.get_series_info(series_id)
                if 'frequency' in info:
                    df['Frequency'] = info['frequency']
                if 'units' in info:
                    df['Units'] = info['units']
                
                data[name] = df
                print(f"Successfully retrieved {len(df)} records for {name}")
            else:
                print(f"No data found for {name} (Series: {series_id})")
        
        except Exception as e:
            print(f"Error retrieving data for {name} (Series: {series_id}): {e}")
    
    return data

def calculate_inflation_rate(data):
    """
    Calculate year-over-year inflation rate from CPI data.
    
    Parameters:
    - data (DataFrame): CPI data from FRED
    
    Returns:
    - DataFrame: Year-over-year inflation rate
    """
    if 'CPI_Inflation' not in data:
        print("CPI data not found, cannot calculate inflation rate")
        return None
    
    # Get CPI data
    cpi = data['CPI_Inflation'].copy()
    
    # Calculate year-over-year percentage change
    cpi['Inflation_Rate'] = cpi['Value'].pct_change(periods=12) * 100
    
    # Drop rows with NaN values (first 12 months will have NaN)
    cpi = cpi.dropna(subset=['Inflation_Rate'])
    
    return cpi

def calculate_gdp_growth_qoq(data):
    """
    Process quarterly GDP growth data.
    
    Parameters:
    - data (DataFrame): GDP growth data from FRED
    
    Returns:
    - DataFrame: Processed GDP growth data
    """
    if 'GDP_Growth' not in data:
        print("GDP data not found, cannot process GDP growth")
        return None
    
    # Get GDP data
    gdp = data['GDP_Growth'].copy()
    
    # FRED's A191RL1Q225SBEA is already quarter-over-quarter annualized
    # Just rename for clarity
    gdp = gdp.rename(columns={'Value': 'GDP_Growth_QoQ_Annualized'})
    
    return gdp

def save_economic_data(data, directory="data/indicators"):
    """
    Save economic indicator data to CSV files.
    
    Parameters:
    - data (dict): Dictionary with indicator names as keys and DataFrame of historical data as values
    - directory (str): Directory to save CSV files
    
    Returns:
    - list: List of saved file paths
    """
    # Create directory if it doesn't exist
    os.makedirs(directory, exist_ok=True)
    
    saved_files = []
    
    # Save each indicator's data to a CSV file
    for name, df in data.items():
        filename = f"{name}.csv"
        filepath = os.path.join(directory, filename)
        
        # Save to CSV
        df.to_csv(filepath)
        saved_files.append(filepath)
        print(f"Saved {len(df)} records to {filepath}")
    
    return saved_files

def update_economic_indicators(api_key):
    """
    Update economic indicator data.
    
    Parameters:
    - api_key (str): FRED API key
    
    Returns:
    - list: List of saved file paths
    """
    # Get economic indicator data
    data = get_economic_indicators(api_key)
    
    # Calculate derived indicators
    inflation_data = calculate_inflation_rate(data)
    if inflation_data is not None:
        data['Inflation_Rate_YoY'] = inflation_data
    
    gdp_data = calculate_gdp_growth_qoq(data)
    if gdp_data is not None:
        data['GDP_Growth_QoQ'] = gdp_data
    
    # Save economic data
    saved_files = save_economic_data(data)
    
    return saved_files

if __name__ == "__main__":
    # If run directly, prompt for API key and update economic data
    api_key = input("Enter your FRED API key: ")
    update_economic_indicators(api_key)