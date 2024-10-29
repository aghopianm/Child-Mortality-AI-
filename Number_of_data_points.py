import pandas as pd

# Define the path to your CSV file
file_path = 'merged_data.csv'

# Load the dataset
data = pd.read_csv(file_path)

# Count the number of non-null data points
total_data_points = data.size  # The total number of cells in the DataFrame

print(f"Total number of data points: {total_data_points}")
