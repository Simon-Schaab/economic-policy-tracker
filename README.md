# Economic Policy Impact Tracker

A Python-based tool for tracking economic indicators, market data, and bond yields to analyze the impact of policy decisions on the economy.

## Project Motivation

This project aims to create a data collection and analysis pipeline to track how economic policies influence various aspects of the economy. The primary focus is on tracking US economic indicators, market indices, and treasury yields to identify trends and correlations that emerge following policy changes.

## Current Features

- Automated data collection from multiple sources:
  - Stock market indices (S&P 500, DOW, NASDAQ, VIX) via Yahoo Finance
  - Treasury yield data (3M, 2Y, 5Y, 10Y, 30Y) via FRED API
  - Economic indicators (unemployment, inflation, GDP, etc.) via FRED API
- Configurable update process with command-line interface
- Data storage in structured CSV format

## Project Structure

```
economic-policy-tracker/
├── data/                  # Data storage
│   ├── market/            # Market data CSVs
│   ├── bonds/             # Bond data CSVs
│   └── indicators/        # Economic indicators CSVs
├── src/                   # Source code
│   ├── data_collection/   # Data retrieval modules
│   │   ├── market.py      # Market data collection
│   │   ├── bonds.py       # Bond data collection
│   │   └── indicators.py  # Economic indicators collection
│   ├── analysis/          # Analysis modules (coming soon)
│   └── visualization/     # Visualization components (coming soon)
├── test_market_data.py    # Test script for market data
├── test_bond_data.py      # Test script for bond data
├── test_economic_data.py  # Test script for economic indicators
├── update_data.py         # Unified data update script
├── requirements.txt       # Project dependencies
└── config.json            # Configuration (API keys, etc.)
```

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```
   python -m venv venv
   ```
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`
4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
5. Create a `config.json` file with your API keys or run the update script once to generate a template:
   ```
   python update_data.py
   ```

## Usage

### Updating Data

Run the unified update script to collect all data:
```
python update_data.py
```

Or specify which data to update:
```
python update_data.py --market    # Update only market data
python update_data.py --bonds     # Update only bond data
python update_data.py --indicators # Update only economic indicators
```

### Testing Individual Modules

Test specific data collection modules:
```
python test_market_data.py
python test_bond_data.py
python test_economic_data.py
```

## Technologies Used

- Python 3.x
- pandas: Data manipulation and analysis
- matplotlib/seaborn: Data visualization
- yfinance: Yahoo Finance API wrapper
- fredapi: Federal Reserve Economic Data API wrapper
- Streamlit: Dashboard (coming soon)

## Roadmap

- [x] Data collection modules for market, bonds, and economic indicators
- [x] Unified data update script
- [ ] Basic data analysis components
- [ ] Data visualization modules
- [ ] Interactive dashboard
- [ ] Event tagging system for policy announcements
- [ ] Correlation analysis between different economic metrics

## Learning Goals

This project is designed to build skills in:
- Python programming and data manipulation
- Economic data analysis
- API integration
- Data visualization
- Financial market understanding
