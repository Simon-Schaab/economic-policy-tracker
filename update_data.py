# update_data.py
import argparse
import json
import os
import sys
from src.data_collection.market import update_market_data
from src.data_collection.bonds import update_bond_data
from src.data_collection.indicators import update_economic_indicators

def parse_arguments():
    """
    Parse command line arguments for the data update script.
    
    Returns:
    - argparse.Namespace: Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="Update economic data for trend tracking"
    )
    
    # Add arguments
    parser.add_argument(
        "--market", 
        action="store_true",
        help="Update market data only"
    )
    
    parser.add_argument(
        "--bonds", 
        action="store_true", 
        help="Update bond data only"
    )
    
    parser.add_argument(
        "--indicators", 
        action="store_true", 
        help="Update economic indicators only"
    )
    
    parser.add_argument(
        "--all", 
        action="store_true", 
        help="Update all data (default if no options specified)"
    )
    
    parser.add_argument(
        "--config", 
        type=str, 
        default="config.json",
        help="Path to configuration file (default: config.json)"
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    # If no update options specified, update all
    if not (args.market or args.bonds or args.indicators or args.all):
        args.all = True
    
    return args

def load_configuration(config_path):
    """
    Load configuration from a JSON file.
    
    Parameters:
    - config_path (str): Path to configuration file
    
    Returns:
    - dict: Configuration data
    """
    try:
        # Check if file exists
        if not os.path.exists(config_path):
            print(f"Error: Configuration file '{config_path}' not found.")
            
            # If it's the default config, create a template
            if config_path == "config.json":
                create_config_template(config_path)
                print(f"Created template configuration file at '{config_path}'.")
                print("Please edit this file to add your API keys.")
                sys.exit(1)
            else:
                sys.exit(1)
        
        # Open and read the file
        with open(config_path, 'r') as file:
            config = json.load(file)
        
        # Validate required keys
        if 'fred_api_key' not in config:
            print("Error: FRED API key not found in configuration file.")
            print("Please add your 'fred_api_key' to the configuration file.")
            sys.exit(1)
        
        return config
        
    except json.JSONDecodeError:
        print(f"Error: Configuration file '{config_path}' is not valid JSON.")
        sys.exit(1)
    except Exception as e:
        print(f"Error loading configuration: {e}")
        sys.exit(1)

def create_config_template(config_path):
    """
    Create a template configuration file.
    
    Parameters:
    - config_path (str): Path to create configuration file
    """
    template = {
        "fred_api_key": "YOUR_FRED_API_KEY_HERE",
        "update_frequency": {
            "market": "daily",
            "bonds": "daily",
            "indicators": "weekly"
        }
    }
    
    try:
        with open(config_path, 'w') as file:
            json.dump(template, file, indent=4)
    except Exception as e:
        print(f"Error creating configuration template: {e}")

def run_updates(args, config):
    """
    Run the requested data updates.
    
    Parameters:
    - args (argparse.Namespace): Command line arguments
    - config (dict): Configuration data
    
    Returns:
    - bool: Success status
    """
    success = True
    update_count = 0
    
    # Track which updates succeeded
    results = {
        "market": None,
        "bonds": None,
        "indicators": None
    }
    
    try:
        # Market data update
        if args.market or args.all:
            print("\n--- Updating Market Data ---")
            try:
                market_files = update_market_data()
                print(f"Successfully updated {len(market_files)} market data files.")
                results["market"] = True
                update_count += 1
            except Exception as e:
                print(f"Error updating market data: {e}")
                results["market"] = False
                success = False
        
        # Bond data update
        if args.bonds or args.all:
            print("\n--- Updating Bond Data ---")
            try:
                bond_files = update_bond_data(config['fred_api_key'])
                print(f"Successfully updated {len(bond_files)} bond data files.")
                results["bonds"] = True
                update_count += 1
            except Exception as e:
                print(f"Error updating bond data: {e}")
                results["bonds"] = False
                success = False
        
        # Economic indicators update
        if args.indicators or args.all:
            print("\n--- Updating Economic Indicators ---")
            try:
                indicator_files = update_economic_indicators(config['fred_api_key'])
                print(f"Successfully updated {len(indicator_files)} economic indicator files.")
                results["indicators"] = True
                update_count += 1
            except Exception as e:
                print(f"Error updating economic indicators: {e}")
                results["indicators"] = False
                success = False
        
    except KeyboardInterrupt:
        print("\nUpdate process interrupted by user.")
        return False
    
    # Print summary
    print("\n--- Update Summary ---")
    for update_type, result in results.items():
        if result is None:
            print(f"{update_type.capitalize()}: Not attempted")
        elif result:
            print(f"{update_type.capitalize()}: Success")
        else:
            print(f"{update_type.capitalize()}: Failed")
    
    print(f"\nCompleted {update_count} updates.")
    return success

def main():
    """
    Main entry point for the data update script.
    """
    print("===== Economic Data Update Tool =====")
    
    # Parse command line arguments
    args = parse_arguments()
    
    # Load configuration
    config = load_configuration(args.config)
    
    # Run updates
    success = run_updates(args, config)
    
    # Exit with appropriate status code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()