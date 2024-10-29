import pandas as pd
import matplotlib.pyplot as plt

# Load data into frame
df = pd.read_csv('Infant nutrition data by country.csv')  

# strip
df.columns = df.columns.str.strip()

# Convert columns to numeric, handling errors
df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
df['Early initiation of breastfeeding (%)'] = pd.to_numeric(df['Early initiation of breastfeeding (%)'], errors='coerce')
df['Infants exclusively breastfed for the first six months of life (%)'] = pd.to_numeric(df['Infants exclusively breastfed for the first six months of life (%)'], errors='coerce')

# Define the economic tier mapping based on World Bank classifications for 2024-2025
economic_tier_mapping = {
    'High Income': [
        'United States of America', 'Russian Federation', 'Croatia', 'Uruguay', 'Panama', 'Malaysia',
        'Oman', 'Qatar', 'Saudi Arabia', 'United Arab Emirates', 'Trinidad and Tobago', 'Argentina',
        'Barbados'
    ],
    'Upper-Middle Income': [
        'China', 'Turkey', 'Belarus', 'Bosnia and Herzegovina', 'Montenegro', 'North Macedonia', 'Serbia',
        'Kazakhstan', 'Brazil', 'Colombia', 'Costa Rica', 'Cuba', 'Dominican Republic', 'Ecuador', 'Mexico',
        'Peru', 'Thailand', 'Fiji', 'Iran (Islamic Republic of)', 'Iraq', 'Jordan', 'Lebanon',
        'Albania', 'Armenia', 'Azerbaijan', 'Georgia'
    ],
    'Lower-Middle Income': [
        'Ukraine', 'Republic of Moldova', 'Belize', 'Bolivia (Plurinational State of)', 'El Salvador',
        'Guatemala', 'Honduras', 'Nicaragua', 'Paraguay', 'Jamaica', 'Egypt', 'Morocco', 'Tunisia',
        'Philippines', 'Vietnam', 'Indonesia', 'India', 'Bhutan', 'Sri Lanka', 'Djibouti', 'Pakistan',
        'Kyrgyzstan', 'Mongolia', 'Cambodia', 'Lao People\'s Democratic Republic'
    ],
    'Low Income': [
        'Afghanistan', 'Bangladesh', 'Myanmar', 'Nepal', 'Syrian Arab Republic', 'Yemen', 'Somalia', 'Sudan'
    ]
}

# Function to assign economic tier based on country
def get_economic_tier(country):
    for tier, countries in economic_tier_mapping.items():
        if country in countries:
            return tier
    return 'Other'  # If country doesn't fit in a defined tier

# Apply the economic tier assignment to the DataFrame
df['Economic Tier'] = df['Countries, territories and areas'].apply(get_economic_tier)

# Filter out the 'Other' tier if you don't want to include them in the plots
df = df[df['Economic Tier'] != 'Other']

# Set the consistent year range for all graphs
year_range = (1980, 2025)

# get the economic tier data 
tier_data = df.groupby(['Economic Tier', 'Year']).agg({
    'Early initiation of breastfeeding (%)': ['mean', 'std'],
    'Infants exclusively breastfed for the first six months of life (%)': ['mean', 'std']
}).reset_index()

# Flatten the multi-level columns
tier_data.columns = ['Economic Tier', 'Year', 'Early initiation mean', 'Early initiation std',
                     'Exclusive breastfeeding mean', 'Exclusive breastfeeding std']

# Get unique economic tiers for plotting
economic_tiers = df['Economic Tier'].unique()

# Loop through each economic tier and create two graphs for each (one for each indicator)
for tier in economic_tiers:
    tier_data_subset = tier_data[tier_data['Economic Tier'] == tier]
    
    # Filter valid year data to avoid issues
    tier_data_subset = tier_data_subset[(tier_data_subset['Year'] >= year_range[0]) & (tier_data_subset['Year'] <= year_range[1])]
    
    # Plot Early Initiation of Breastfeeding (%) with error bars
    plt.figure(figsize=(12, 8))
    
    if not tier_data_subset.empty:
        plt.errorbar(
            tier_data_subset['Year'], tier_data_subset['Early initiation mean'],
            yerr=tier_data_subset['Early initiation std'], fmt='o-', capsize=5,
            label=f'{tier} - Early initiation of breastfeeding'
        )
    
    # Add labels, title, consistent x-axis and y-axis range
    plt.xlabel('Year')
    plt.ylabel('Percentage')
    plt.title(f'Early Initiation of Breastfeeding in {tier} Countries (Average) by Year')
    plt.xlim(year_range)
    plt.ylim(0, 100)
    plt.legend(loc='best')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Plot Infants Exclusively Breastfed for the First Six Months (%) with error bars
    plt.figure(figsize=(12, 8))
    
    if not tier_data_subset.empty:
        plt.errorbar(
            tier_data_subset['Year'], tier_data_subset['Exclusive breastfeeding mean'],
            yerr=tier_data_subset['Exclusive breastfeeding std'], fmt='x-', capsize=5,
            label=f'{tier} - Infants exclusively breastfed'
        )
    
    # Add labels, title, consistent x-axis and y-axis range
    plt.xlabel('Year')
    plt.ylabel('Percentage')
    plt.title(f'Infants Exclusively Breastfed in {tier} Countries (Average) for the First Six Months by Year')
    plt.xlim(year_range)
    plt.ylim(0, 100)
    plt.legend(loc='best')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Print summary statistics
print(df.groupby('Economic Tier').agg({
    'Early initiation of breastfeeding (%)': ['mean', 'std', 'count'],
    'Infants exclusively breastfed for the first six months of life (%)': ['mean', 'std', 'count']
}))