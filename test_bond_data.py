# test_bond_data.py
from src.data_collection.bonds import update_bond_data

def main():
    # Replace with your actual FRED API key
    api_key = "82d409501103259bdf36d073dca65469"
    
    print("Updating bond data...")
    saved_files = update_bond_data(api_key)
    print(f"Successfully updated {len(saved_files)} bond data files.")

if __name__ == "__main__":
    main()