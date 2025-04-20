import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import os

def get_market_data(tickers=None, period="1y", interval="1d"):
    """
    Retrieve market data for specified tickers using Yahoo Finance.
    
    Parameters:
    - tickers (list): List of ticker symbols to retrieve (default: major indices)
    - period (str): Time period to retrieve ('1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max')
    - interval (str): Data interval ('1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo')
    
    Returns:
    - dict: Dictionary with ticker symbols as keys and DataFrame of historical data as values
    """
    # Default to major indices if no tickers provided
    if tickers is None:
        tickers = [
            "^GSPC",  # S&P 500
            "^DJI",   # Dow Jones Industrial Average
            "^IXIC",  # NASDAQ Composite
            "^VIX"    # Volatility Index
        ]
    
    # Dictionary to store results
    data = {}
    
    # Retrieve data for each ticker
    for ticker in tickers:
        try:
            print(f"Retrieving data for {ticker}...")
            ticker_data = yf.Ticker(ticker)
            hist = ticker_data.history(period=period, interval=interval)
            
            # Keep only relevant columns
            if not hist.empty:
                hist = hist[["Open", "High", "Low", "Close", "Volume"]]
                data[ticker] = hist
                print(f"Successfully retrieved {len(hist)} records for {ticker}")
            else:
                print(f"No data found for {ticker}")
        
        except Exception as e:
            print(f"Error retrieving data for {ticker}: {e}")
    
    return data

def save_market_data(data, directory="data/market"):
    """
    Save market data to CSV files.
    
    Parameters:
    - data (dict): Dictionary with ticker symbols as keys and DataFrame of historical data as values
    - directory (str): Directory to save CSV files
    
    Returns:
    - list: List of saved file paths
    """
    # Create directory if it doesn't exist
    os.makedirs(directory, exist_ok=True)
    
    saved_files = []
    
    # Save each ticker's data to a CSV file
    for ticker, df in data.items():
        # Clean ticker symbol for filename
        clean_ticker = ticker.replace("^", "")
        filename = f"{clean_ticker}_daily.csv"
        filepath = os.path.join(directory, filename)
        
        # Save to CSV
        df.to_csv(filepath)
        saved_files.append(filepath)
        print(f"Saved {len(df)} records to {filepath}")
    
    return saved_files

def update_market_data():
    """
    Update market data for major indices.
    
    Returns:
    - list: List of saved file paths
    """
    # Get market data
    data = get_market_data()
    
    # Save market data
    saved_files = save_market_data(data)
    
    return saved_files

if __name__ == "__main__":
    # If run directly, update market data
    update_market_data()