#This file merges the merged mortality data with nutritional data

import pandas as pd
import os

# Use a generic path that expands to my home directory to remain anonymous
home_dir = os.path.expanduser('~')

#  Load the datasets
nutrition_data = pd.read_csv(os.path.join(home_dir, 'Desktop/AAI_2024_Datasets/Infant nutrition data by country.csv'))
mortality_data = pd.read_csv(os.path.join(home_dir, 'Desktop/AAI_2024_Datasets/all_mortality_rates.csv'))

# Rename 'Unnamed: 0' to 'Countries, territories and areas' and 'Unnamed: 1' to 'Year' in mortality data
mortality_data.rename(columns={'Unnamed: 0': 'Countries, territories and areas', 
                               'Unnamed: 1': 'Year'}, inplace=True)

# Perform a full outer merge on 'Countries, territories and areas' and 'Year'
merged_data = pd.merge(mortality_data, nutrition_data, 
                       on=['Countries, territories and areas', 'Year'], 
                       how='outer')

# Define new column names directly
new_column_names = [
    'Countries, territories and areas', 
    'Year', 
    'Under-five mortality rate (per 1000 live births) (SDG 3.2.1) Both sexes', 
    'Under-five mortality rate (per 1000 live births) (SDG 3.2.1) Male', 
    'Under-five mortality rate (per 1000 live births) (SDG 3.2.1) Female', 
    'Number of deaths among children under-five Both sexes', 
    'Number of deaths among children under-five Male', 
    'Number of deaths among children under-five Female', 
    'Early initiation of breastfeeding (%)', 
    'Infants exclusively breastfed for the first six months of life (%)'
]

# Assign new column names to the merged DataFrame
merged_data.columns = new_column_names

# Save this to a new file using a generic path
intermediate_output_path = os.path.join(home_dir, 'Desktop/AAI_2024_Datasets/merged_data.csv')
merged_data.to_csv(intermediate_output_path, index=False)

# Print statement to show that the script has been successful
print("All merged data saved.")  # To note, this is NOT fully cleaned data, error bars and year-ranges are not handled yet
