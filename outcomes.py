import requests
import pandas as pd
import json
import os

# List of indicator codes
indicators = [
    "WHOSIS_000001",  # Life Expectancy at Birth
    "WHOSIS_000015",  # Healthy Life Expectancy (HALE)
    "WHOSIS_000004",  # Adult Mortality Rate (15-60 years)
    "MDG_0000000011", # HIV Prevalence among Adults (15-49 years)
    "NCD_BMI_30A",    # Obesity Prevalence (age-standardized)
    "NCD_HYP_PREVALENCE_A", # Hypertension Prevalence (age-standardized)
    "MDG_0000000001", # Contraceptive Prevalence (any method)
    "SDG_0000000028", # Cardiovascular Disease Mortality
    "SDG_0000000030", # Mental Health Disorder Prevalence
    "NCD_BMI_25A"     # Diabetes Prevalence (age-standardized)
]

# Initialize a dictionary to store all data
all_data = {}

# Function to get data for each indicator and store it in the JSON structure
def fetch_data(indicator):
    url = f"https://ghoapi.azureedge.net/api/{indicator}?$filter=TimeDim ge 2000 and TimeDim le 2020"
    
    # Send request
    response = requests.get(url)
    
    # Check if request was successful
    if response.status_code == 200:
        data = response.json()
        
        # Add indicator data to the dictionary
        all_data[indicator] = data['value']
        print(f"Data for {indicator} successfully fetched!")
    else:
        print(f"Failed to retrieve data for {indicator} - Status code: {response.status_code}")

# Loop through the indicators and fetch data for each
for indicator in indicators:
    fetch_data(indicator)

# Define the path to the data folder
output_directory = os.path.join('global-healthcare', 'data')
os.makedirs(output_directory, exist_ok=True)  # Ensure the directory exists

# Save the combined data as a JSON file in the data folder
output_file_path = os.path.join(output_directory, 'health_data_2000_2020.json')
with open(output_file_path, 'w') as json_file:
    json.dump(all_data, json_file, indent=4)

print(f"All data saved to {output_file_path}")
