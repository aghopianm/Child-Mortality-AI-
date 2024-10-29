#This file merges all mortality rates together

import pandas as pd
import glob
import os

# Use a generic path that expands to my home directory to remain anonymous
home_dir = os.path.expanduser('~')

# Path to the folder containing your CSV files
path = os.path.join(home_dir, 'Desktop/AAI_2024_Datasets/Child mortality rates_*.csv')

# List all CSV files matching the pattern
all_files = glob.glob(path)

# Read and concatenate all CSV files
df_list = [pd.read_csv(file) for file in all_files]
merged_df = pd.concat(df_list, ignore_index=True)

# Save the merged CSV to a generic path
output_path = os.path.join(home_dir, 'Desktop/AAI_2024_Datasets/all_mortality_rates.csv')
merged_df.to_csv(output_path, index=False)

# Print statement to show that the script has been successful
print("All mortality rates saved.")
