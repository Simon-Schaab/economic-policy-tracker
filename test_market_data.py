# test_market_data.py
from src.data_collection.market import update_market_data

def main():
    print("Updating market data...")
    saved_files = update_market_data()
    print(f"Successfully updated {len(saved_files)} market data files.")

if __name__ == "__main__":
    main()