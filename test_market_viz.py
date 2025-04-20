# test_market_viz.py
from src.visualization.market_plots import load_market_data, plot_index_price, plot_multiple_indices, plot_volatility

def main():
    print("Loading market data...")
    data = load_market_data()
    
    if not data:
        print("No market data found. Please run update_data.py first.")
        return
    
    print("\nGenerating sample visualizations...")
    
    # Plot S&P 500
    print("Plotting S&P 500...")
    plot_index_price(data, 'GSPC', title="S&P 500 - Last 3 Months")
    
    # Plot comparison of major indices
    print("Plotting index comparison...")
    plot_multiple_indices(data, ['GSPC', 'DJI', 'IXIC'], normalize=True, 
                         title="Major Indices Performance (Normalized)")
    
    # Plot volatility
    print("Plotting volatility...")
    plot_volatility(data, window=20, title="Market Volatility - VIX and 20-Day Rolling Volatility")
    
    print("\nVisualizations completed!")

if __name__ == "__main__":
    main()