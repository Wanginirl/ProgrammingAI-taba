import sys
import os
import json
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from dotenv import load_dotenv
import matplotlib

# Load environment variables from .env file
load_dotenv(Path('..').resolve() / '.env')

# Add project root to Python path
project_root = Path('..').resolve()
sys.path.append(str(project_root))

# Import project modules
from src.data_processing.db_manager import DatabaseManager
from src.data_processing.data_cleaner import DataCleaner
from src.data_collection.eurostat_collector import EurostatCollector

print("Step 1: Data Collection and Processing")
print("-" * 50)

# Initialize collectors and managers
collector = EurostatCollector()
db_manager = DatabaseManager()
cleaner = DataCleaner()

# Collect fresh data
print("\nCollecting education investment data...")
education_data_raw = collector.get_education_investment_data()
print(f"Collected {len(education_data_raw)} education investment records")

# Convert wide format to long format
print("\nConverting data format...")
year_columns = [str(year) for year in range(2012, 2022)]
education_data_long = pd.melt(
    education_data_raw,
    id_vars=['freq', 'unit', 'isced11', 'geo\\TIME_PERIOD'],
    value_vars=year_columns,
    var_name='year',
    value_name='value'
)

# Rename columns for clarity
education_data_long = education_data_long.rename(columns={'geo\\TIME_PERIOD': 'geo_time_period'})
education_data_long['year'] = education_data_long['year'].astype(int)

print("\nData shape after conversion:", education_data_long.shape)
print("\nFirst few rows of converted data:")
print(education_data_long.head())

# Analysis of Major EU Countries
print("\nAnalyzing major EU countries...")
major_countries = ['DE', 'FR', 'IT', 'ES', 'PL']
major_country_data = education_data_long[
    education_data_long['geo_time_period'].isin(major_countries)
]

# Debug: Print data availability
print("\nData availability for each country:")
for country in major_countries:
    country_data = major_country_data[major_country_data['geo_time_period'] == country]
    print(f"{country}: {len(country_data)} records")

# Country name mapping
country_names = {
    'DE': 'Germany',
    'FR': 'France',
    'IT': 'Italy',
    'ES': 'Spain',
    'PL': 'Poland'
}

# Create figure with larger size for better visibility
plt.figure(figsize=(15, 8))

# Define colors for each country
colors = {
    'DE': '#1f77b4',  # Blue
    'FR': '#ff7f0e',  # Orange
    'IT': '#2ca02c',  # Green
    'ES': '#d62728',  # Red
    'PL': '#9467bd'   # Purple
}

# Plot data for each country with explicit labels and styling
for country in major_countries:
    country_data = major_country_data[major_country_data['geo_time_period'] == country]
    if not country_data.empty:
        country_data = country_data.sort_values('year')
        plt.plot(country_data['year'], 
                country_data['value'],
                label=country_names[country],
                color=colors[country],
                marker='o',
                markersize=6,
                linewidth=2,
                linestyle='-')
        print(f"Plotted data for {country_names[country]}")

# Customize plot appearance
plt.title('Education Investment Trends in Major EU Countries', 
         fontsize=14, 
         pad=20)
plt.xlabel('Year', fontsize=12)
plt.ylabel('Investment Value (Million EUR)', fontsize=12)

# Add legend with better positioning
plt.legend(loc='upper left', 
          bbox_to_anchor=(1, 1),
          frameon=True,
          fancybox=True,
          shadow=True)

# Customize grid
plt.grid(True, linestyle='--', alpha=0.7)

# Remove top and right spines
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)

# Adjust layout to prevent label cutoff
plt.tight_layout()

# Show plot
plt.show()

# Calculate and display CAGR
print("\nCompound Annual Growth Rate (CAGR) by Country:")
print("-" * 40)

for country in major_countries:
    country_data = major_country_data[major_country_data['geo_time_period'] == country]
    if len(country_data) >= 2:
        # Sort by year and get first and last values
        country_data = country_data.sort_values('year')
        first_year = country_data.iloc[0]
        last_year = country_data.iloc[-1]
        
        # Calculate CAGR
        years = last_year['year'] - first_year['year']
        if years > 0:
            cagr = (((last_year['value'] / first_year['value']) ** (1/years)) - 1) * 100
            print(f"{country_names[country]}: {cagr:.2f}%")
        else:
            print(f"Warning: Not enough years of data for {country_names[country]}")
    else:
        print(f"Warning: Insufficient data for {country_names[country]}")

print("\nAnalysis completed successfully!")
