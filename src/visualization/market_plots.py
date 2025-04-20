import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime, timedelta

# Set style for all plots
sns.set_theme(style="darkgrid")

def load_market_data(directory="data/market", tickers=None):
    """
    Load market data from CSV files.
    
    Parameters:
    - directory (str): Directory containing market data CSV files
    - tickers (list): List of tickers to load (default: all available)
    
    Returns:
    - dict: Dictionary with ticker symbols as keys and DataFrame of historical data as values
    """
    # Default tickers if none provided
    if tickers is None:
        tickers = ["GSPC", "DJI", "IXIC", "VIX"]
    
    data = {}
    
    # Load each ticker's data from CSV file
    for ticker in tickers:
        filename = f"{ticker}_daily.csv"
        filepath = os.path.join(directory, filename)
        
        try:
            if os.path.exists(filepath):
                # Load data and set index to datetime
                df = pd.read_csv(filepath)
                df['Date'] = pd.to_datetime(df['Date'])
                df.set_index('Date', inplace=True)
                
                # Add ticker to data dictionary
                data[ticker] = df
                print(f"Loaded {len(df)} records for {ticker}")
            else:
                print(f"File not found: {filepath}")
        
        except Exception as e:
            print(f"Error loading data for {ticker}: {e}")
    
    return data

def plot_index_price(data, ticker, start_date=None, end_date=None, 
                    price_column='Close', title=None, figsize=(12, 6), 
                    save_path=None, show=True):
    """
    Plot closing price for a market index.
    
    Parameters:
    - data (dict): Dictionary with ticker symbols as keys and DataFrame of historical data as values
    - ticker (str): Ticker symbol to plot
    - start_date (str): Start date in format 'YYYY-MM-DD' (default: earliest available)
    - end_date (str): End date in format 'YYYY-MM-DD' (default: latest available)
    - price_column (str): Column to plot (default: 'Close')
    - title (str): Plot title (default: auto-generated)
    - figsize (tuple): Figure size (width, height)
    - save_path (str): Path to save the figure (if None, don't save)
    - show (bool): Whether to display the plot
    
    Returns:
    - matplotlib.figure.Figure: The created figure
    """
    if ticker not in data:
        print(f"Error: Ticker {ticker} not found in data")
        return None
    
    # Get data for the ticker
    df = data[ticker]
    
    # Filter by date range if provided
    if start_date is not None:
        df = df[df.index >= pd.to_datetime(start_date)]
    
    if end_date is not None:
        df = df[df.index <= pd.to_datetime(end_date)]
    
    if len(df) == 0:
        print(f"Error: No data found for {ticker} in the specified date range")
        return None
    
    # Set default title if not provided
    if title is None:
        ticker_name = get_ticker_name(ticker)
        title = f"{ticker_name} ({ticker}) - {price_column} Price"
    
    # Create figure and plot
    fig, ax = plt.subplots(figsize=figsize)
    
    # Plot price
    ax.plot(df.index, df[price_column], linewidth=2)
    
    # Add labels and title
    ax.set_xlabel('Date')
    ax.set_ylabel(f'{price_column} Price')
    ax.set_title(title)
    
    # Add grid
    ax.grid(True, alpha=0.3)
    
    # Format y-axis with commas for thousands
    ax.get_yaxis().set_major_formatter(plt.matplotlib.ticker.StrMethodFormatter('{x:,.0f}'))
    
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)
    
    # Tight layout to ensure everything fits
    plt.tight_layout()
    
    # Save if requested
    if save_path is not None:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    # Show if requested
    if show:
        plt.show()
    else:
        plt.close()
    
    return fig

def plot_multiple_indices(data, tickers, start_date=None, end_date=None, 
                         price_column='Close', normalize=True, title=None, 
                         figsize=(12, 6), save_path=None, show=True):
    """
    Plot multiple market indices for comparison.
    
    Parameters:
    - data (dict): Dictionary with ticker symbols as keys and DataFrame of historical data as values
    - tickers (list): List of ticker symbols to plot
    - start_date (str): Start date in format 'YYYY-MM-DD' (default: earliest available)
    - end_date (str): End date in format 'YYYY-MM-DD' (default: latest available)
    - price_column (str): Column to plot (default: 'Close')
    - normalize (bool): Whether to normalize values to start at 100 for comparison
    - title (str): Plot title (default: auto-generated)
    - figsize (tuple): Figure size (width, height)
    - save_path (str): Path to save the figure (if None, don't save)
    - show (bool): Whether to display the plot
    
    Returns:
    - matplotlib.figure.Figure: The created figure
    """
    # Set default title if not provided
    if title is None:
        if normalize:
            title = f"Normalized {price_column} Price Comparison"
        else:
            title = f"{price_column} Price Comparison"
    
    # Create figure and plot
    fig, ax = plt.subplots(figsize=figsize)
    
    # Plot each ticker
    for ticker in tickers:
        if ticker not in data:
            print(f"Warning: Ticker {ticker} not found in data, skipping")
            continue
        
        # Get data for the ticker
        df = data[ticker].copy()
        
        # Filter by date range if provided
        if start_date is not None:
            df = df[df.index >= pd.to_datetime(start_date)]
        
        if end_date is not None:
            df = df[df.index <= pd.to_datetime(end_date)]
        
        if len(df) == 0:
            print(f"Warning: No data found for {ticker} in the specified date range, skipping")
            continue
        
        # Normalize data if requested
        if normalize:
            df[f'{price_column}_Normalized'] = (df[price_column] / df[price_column].iloc[0]) * 100
            plot_column = f'{price_column}_Normalized'
            ylabel = 'Normalized Price (First Day = 100)'
        else:
            plot_column = price_column
            ylabel = f'{price_column} Price'
        
        # Plot with ticker name as label
        ticker_name = get_ticker_name(ticker)
        ax.plot(df.index, df[plot_column], linewidth=2, label=f"{ticker_name} ({ticker})")
    
    # Add labels and title
    ax.set_xlabel('Date')
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    
    # Add grid and legend
    ax.grid(True, alpha=0.3)
    ax.legend()
    
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)
    
    # Tight layout to ensure everything fits
    plt.tight_layout()
    
    # Save if requested
    if save_path is not None:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    # Show if requested
    if show:
        plt.show()
    else:
        plt.close()
    
    return fig

def plot_volatility(data, start_date=None, end_date=None, window=20, 
                   title=None, figsize=(12, 8), save_path=None, show=True):
    """
    Plot VIX and calculate rolling volatility for major indices.
    
    Parameters:
    - data (dict): Dictionary with ticker symbols as keys and DataFrame of historical data as values
    - start_date (str): Start date in format 'YYYY-MM-DD' (default: earliest available)
    - end_date (str): End date in format 'YYYY-MM-DD' (default: latest available)
    - window (int): Rolling window for volatility calculation (default: 20 days)
    - title (str): Plot title (default: auto-generated)
    - figsize (tuple): Figure size (width, height)
    - save_path (str): Path to save the figure (if None, don't save)
    - show (bool): Whether to display the plot
    
    Returns:
    - matplotlib.figure.Figure: The created figure
    """
    # Set default title if not provided
    if title is None:
        title = f"Market Volatility (VIX and {window}-Day Rolling Volatility)"
    
    # Create figure with two subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=figsize, sharex=True)
    
    # Plot VIX if available
    if 'VIX' in data:
        df_vix = data['VIX'].copy()
        
        # Filter by date range if provided
        if start_date is not None:
            df_vix = df_vix[df_vix.index >= pd.to_datetime(start_date)]
        
        if end_date is not None:
            df_vix = df_vix[df_vix.index <= pd.to_datetime(end_date)]
        
        if len(df_vix) > 0:
            ax1.plot(df_vix.index, df_vix['Close'], color='red', linewidth=2)
            ax1.set_ylabel('VIX Value')
            ax1.set_title('CBOE Volatility Index (VIX)')
            ax1.grid(True, alpha=0.3)
    
    # Calculate and plot rolling volatility for major indices
    indices = ['GSPC', 'DJI', 'IXIC']
    colors = ['blue', 'green', 'purple']
    
    for ticker, color in zip(indices, colors):
        if ticker in data:
            df = data[ticker].copy()
            
            # Filter by date range if provided
            if start_date is not None:
                df = df[df.index >= pd.to_datetime(start_date)]
            
            if end_date is not None:
                df = df[df.index <= pd.to_datetime(end_date)]
            
            if len(df) > window:
                # Calculate daily returns
                df['Return'] = df['Close'].pct_change()
                
                # Calculate rolling volatility (annualized)
                df['Volatility'] = df['Return'].rolling(window=window).std() * np.sqrt(252)
                
                # Drop NaN values
                df = df.dropna()
                
                if len(df) > 0:
                    ticker_name = get_ticker_name(ticker)
                    ax2.plot(df.index, df['Volatility'], color=color, linewidth=2, label=f"{ticker_name} ({ticker})")
    
    # Set labels and add legend for second subplot
    ax2.set_xlabel('Date')
    ax2.set_ylabel(f'{window}-Day Rolling Volatility (Annualized)')
    ax2.set_title(f'{window}-Day Rolling Volatility of Major Indices')
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    
    # Format y-axis as percentage
    ax2.get_yaxis().set_major_formatter(plt.matplotlib.ticker.PercentFormatter(1.0))
    
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)
    
    # Set overall title
    fig.suptitle(title, fontsize=16)
    plt.subplots_adjust(top=0.9)
    
    # Tight layout to ensure everything fits
    plt.tight_layout()
    
    # Adjust for super title
    plt.subplots_adjust(top=0.9)
    
    # Save if requested
    if save_path is not None:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    # Show if requested
    if show:
        plt.show()
    else:
        plt.close()
    
    return fig

def get_ticker_name(ticker):
    """
    Get full name for ticker symbol.
    
    Parameters:
    - ticker (str): Ticker symbol
    
    Returns:
    - str: Full name of the index
    """
    ticker_names = {
        'GSPC': 'S&P 500',
        'DJI': 'Dow Jones Industrial Average',
        'IXIC': 'NASDAQ Composite',
        'VIX': 'CBOE Volatility Index'
    }
    
    return ticker_names.get(ticker, ticker)

def generate_market_report(output_dir="reports/market", start_date=None, end_date=None):
    """
    Generate a set of market visualizations and save them.
    
    Parameters:
    - output_dir (str): Directory to save visualizations
    - start_date (str): Start date in format 'YYYY-MM-DD' (default: 3 months ago)
    - end_date (str): End date in format 'YYYY-MM-DD' (default: today)
    
    Returns:
    - list: List of saved file paths
    """
    # Set default dates if not provided
    if end_date is None:
        end_date = datetime.now().strftime('%Y-%m-%d')
    
    if start_date is None:
        # Default to three months of data
        start_date = (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d')
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Load market data
    data = load_market_data()
    
    # List to track saved files
    saved_files = []
    
    # Generate individual index plots
    for ticker in data.keys():
        filename = f"{ticker}_price.png"
        filepath = os.path.join(output_dir, filename)
        
        # Plot and save
        plot_index_price(data, ticker, start_date, end_date, 
                         save_path=filepath, show=False)
        
        saved_files.append(filepath)
        print(f"Saved {filepath}")
    
    # Generate comparison plot
    filename = "index_comparison.png"
    filepath = os.path.join(output_dir, filename)
    
    # Plot and save
    plot_multiple_indices(data, ['GSPC', 'DJI', 'IXIC'], start_date, end_date, 
                         save_path=filepath, show=False)
    
    saved_files.append(filepath)
    print(f"Saved {filepath}")
    
    # Generate volatility plot
    filename = "volatility.png"
    filepath = os.path.join(output_dir, filename)
    
    # Plot and save
    plot_volatility(data, start_date, end_date, 
                   save_path=filepath, show=False)
    
    saved_files.append(filepath)
    print(f"Saved {filepath}")
    
    print(f"\nGenerated {len(saved_files)} market visualizations")
    return saved_files

if __name__ == "__main__":
    # If run directly, generate market report
    generate_market_report()