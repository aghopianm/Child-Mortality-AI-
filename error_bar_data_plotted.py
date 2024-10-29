import pandas as pd
import matplotlib.pyplot as plt

# Load the data into a frame
df = pd.read_csv('Infant nutrition data by country.csv')  

# strip
df.columns = df.columns.str.strip()

# Convert columns to numeric, handling errors
df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
df['Early initiation of breastfeeding (%)'] = pd.to_numeric(df['Early initiation of breastfeeding (%)'], errors='coerce')
df['Infants exclusively breastfed for the first six months of life (%)'] = pd.to_numeric(df['Infants exclusively breastfed for the first six months of life (%)'], errors='coerce')

# Define the region mapping for continents
region_mapping = {
    'Europe': [
        'Albania', 'Armenia', 'Azerbaijan', 'Belarus', 'Bosnia and Herzegovina', 'Croatia', 'Georgia', 'Kazakhstan', 
        'Kyrgyzstan', 'Montenegro', 'North Macedonia', 'Republic of Moldova', 'Russian Federation', 'Serbia', 
        'Turkiye', 'Ukraine'
    ],
    'Americas': [
        'Argentina', 'Barbados', 'Belize', 'Bolivia (Plurinational State of)', 'Brazil', 'Colombia', 'Costa Rica', 
        'Cuba', 'Dominican Republic', 'Ecuador', 'El Salvador', 'Guatemala', 'Honduras', 'Jamaica', 'Mexico', 
        'Nicaragua', 'Panama', 'Paraguay', 'Peru', 'Trinidad and Tobago', 'United States of America', 'Uruguay', 
        'Venezuela (Bolivarian Republic of)'
    ],
    'Western-Pacific': [
        'Cambodia', 'China', 'Fiji', 'Lao People\'s Democratic Republic', 'Malaysia', 'Mongolia', 'Papua New Guinea', 
        'Philippines', 'Viet Nam'
    ],
    'Eastern Mediterranean': [
        'Afghanistan', 'Djibouti', 'Egypt', 'Iran (Islamic Republic of)', 'Iraq', 'Jordan', 'Lebanon', 'Morocco', 
        'Oman', 'Pakistan', 'Qatar', 'Saudi Arabia', 'Somalia', 'Sudan', 'Syrian Arab Republic', 'Tunisia', 
        'United Arab Emirates', 'Yemen'
    ],
    'South-East Asia': [
        'Bangladesh', 'Bhutan', 'India', 'Indonesia', 'Maldives', 'Myanmar', 'Nepal', 'Sri Lanka', 'Thailand'
    ]
}

# Function to assign region based on country
def get_region(country):
    for region, countries in region_mapping.items():
        if country in countries:
            return region
    return 'Other'  # If country doesn't fit in a defined region

# Apply the region assignment to the DataFrame
df['Region'] = df['Countries, territories and areas'].apply(get_region)

# Filter out the 'Other' region if you don't want to include them in the plots
df = df[df['Region'] != 'Other']

# Set the consistent year range for all graphs
year_range = (1980, 2025)

# Aggregate data by region and year (calculate both mean and standard deviation)
regional_data = df.groupby(['Region', 'Year']).agg({
    'Early initiation of breastfeeding (%)': ['mean', 'std'],
    'Infants exclusively breastfed for the first six months of life (%)': ['mean', 'std']
}).reset_index()

# Flatten the multi-level columns
regional_data.columns = ['Region', 'Year', 'Early initiation mean', 'Early initiation std',
                         'Exclusive breastfeeding mean', 'Exclusive breastfeeding std']

# Get unique regions for plotting
regions = df['Region'].unique()

# Loop through each region and create two graphs for each (one for each indicator)
for region in regions:
    region_data = regional_data[regional_data['Region'] == region]
    
    # Filter valid year data to avoid issues
    region_data = region_data[(region_data['Year'] >= year_range[0]) & (region_data['Year'] <= year_range[1])]
    
    # Plot Early Initiation of Breastfeeding (%) with error bars
    plt.figure(figsize=(12, 8))
    
    if not region_data.empty:
        plt.errorbar(
            region_data['Year'], region_data['Early initiation mean'],
            yerr=region_data['Early initiation std'], fmt='o-', capsize=5,
            label=f'{region} - Early initiation of breastfeeding'
        )
    
    # Add labels, title, consistent x-axis and y-axis range
    plt.xlabel('Year')
    plt.ylabel('Percentage')
    plt.title(f'Early Initiation of Breastfeeding in {region} (Regional Average) by Year')
    plt.xlim(year_range)  # Set x-axis to 1990-2020
    plt.ylim(0, 100)      # Set y-axis to 0-100 for percentage
    plt.legend(loc='best')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Plot Infants Exclusively Breastfed for the First Six Months (%) with error bars
    plt.figure(figsize=(12, 8))
    
    if not region_data.empty:
        plt.errorbar(
            region_data['Year'], region_data['Exclusive breastfeeding mean'],
            yerr=region_data['Exclusive breastfeeding std'], fmt='x-', capsize=5,
            label=f'{region} - Infants exclusively breastfed'
        )
    
    # Add labels, title, consistent x-axis and y-axis range
    plt.xlabel('Year')
    plt.ylabel('Percentage')
    plt.title(f'Infants Exclusively Breastfed in {region} (Regional Average) for the First Six Months by Year')
    plt.xlim(year_range)  # Set x-axis to 1990-2020
    plt.ylim(0, 100)      # Set y-axis to 0-100 for percentage
    plt.legend(loc='best')
    plt.grid(True)
    plt.tight_layout()
    plt.show()
