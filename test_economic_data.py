# test_economic_data.py
from src.data_collection.indicators import update_economic_indicators

def main():
    # Replace with your actual FRED API key
    api_key = "82d409501103259bdf36d073dca65469"
    
    print("Updating economic indicator data...")
    saved_files = update_economic_indicators(api_key)
    print(f"Successfully updated {len(saved_files)} economic indicator files.")

if __name__ == "__main__":
    main()