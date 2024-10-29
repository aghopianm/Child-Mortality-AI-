import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file into a DataFrame
df = pd.read_csv('Infant nutrition data by country.csv')  # Replace with your file path

# Clean column names (remove leading/trailing spaces)
df.columns = df.columns.str.strip()

# Convert columns to numeric, handling errors
df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
df['Early initiation of breastfeeding (%)'] = pd.to_numeric(df['Early initiation of breastfeeding (%)'], errors='coerce')
df['Infants exclusively breastfed for the first six months of life (%)'] = pd.to_numeric(df['Infants exclusively breastfed for the first six months of life (%)'], errors='coerce')

# Print data types to confirm conversion
print(df.dtypes)

# Get a list of unique countries for plotting
countries = df['Countries, territories and areas'].unique()

# Plot Early initiation of breastfeeding (%)
plt.figure(figsize=(12, 8))

for country in countries:
    # Filter data for the current country
    country_data = df[df['Countries, territories and areas'] == country]
    
    # Plot Early initiation of breastfeeding vs. Year
    plt.plot(country_data['Year'], country_data['Early initiation of breastfeeding (%)'],
             marker='o', label=f'{country} - Early initiation of breastfeeding')

# Add labels and title
plt.xlabel('Year')
plt.ylabel('Percentage')
plt.title('Early Initiation of Breastfeeding by Country and Year')
plt.legend(loc='best')
plt.grid(True)

# Show the plot
plt.tight_layout()
plt.show()

# Plot Infants exclusively breastfed (%)
plt.figure(figsize=(12, 8))

for country in countries:
    # Filter data for the current country
    country_data = df[df['Countries, territories and areas'] == country]
    
    # Plot Infants exclusively breastfed vs. Year
    plt.plot(country_data['Year'], country_data['Infants exclusively breastfed for the first six months of life (%)'],
             marker='x', label=f'{country} - Infants exclusively breastfed')

# Add labels and title
plt.xlabel('Year')
plt.ylabel('Percentage')
plt.title('Infants Exclusively Breastfed for the First Six Months by Country and Year')
plt.legend(loc='best')
plt.grid(True)

# Show the plot
plt.tight_layout()
plt.show()