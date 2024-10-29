import pandas as pd
import matplotlib.pyplot as plt

# Load the data into a dataframe
df = pd.read_csv('Infant nutrition data by country.csv')  

# strip colums 
df.columns = df.columns.str.strip()

# Convert columns to numeric, handling errors
df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
df['Early initiation of breastfeeding (%)'] = pd.to_numeric(df['Early initiation of breastfeeding (%)'], errors='coerce')
df['Infants exclusively breastfed for the first six months of life (%)'] = pd.to_numeric(df['Infants exclusively breastfed for the first six months of life (%)'], errors='coerce')

# Define sub-region mapping to split up the data a bit better
region_mapping = {
    # Europe divided into sub-regions
    'Western Europe': ['Austria', 'Belgium', 'France', 'Germany', 'Ireland', 'Luxembourg', 'Netherlands (Kingdom of the)', 'Switzerland', 'United Kingdom of Great Britain'],
    'Eastern Europe': ['Armenia', 'Azerbaijan', 'Belarus', 'Bulgaria', 'Georgia', 'Kazakhstan', 'Kyrgyzstan', 'Republic of Moldova', 'Russian Federation', 'Tajikistan', 'Turkmenistan', 'Ukraine', 'Uzbekistan'],
    'Northern Europe': ['Denmark', 'Estonia', 'Finland', 'Iceland', 'Latvia', 'Lithuania', 'Norway', 'Sweden'],
    'Southern Europe': ['Albania', 'Andorra', 'Bosnia and Herzegovina', 'Croatia', 'Cyprus', 'Greece', 'Italy', 'Malta', 'Monaco', 'Montenegro', 'North Macedonia', 'Portugal', 'San Marino', 'Serbia', 'Slovenia', 'Spain', 'Turkey'],

    # Americas divided into sub-regions
    'North America': ['Canada', 'United States of America'],
    'Central America and Caribbean': ['Bahamas', 'Barbados', 'Belize', 'Costa Rica', 'Cuba', 'Dominica', 'Dominican Republic', 'El Salvador', 'Grenada', 'Guatemala', 'Haiti', 'Honduras', 'Jamaica', 'Mexico', 'Nicaragua', 'Panama', 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Vincent and the Grenadines', 'Trinidad and Tobago'],
    'South America': ['Argentina', 'Bolivia (Plurinational State of)', 'Brazil', 'Chile', 'Colombia', 'Ecuador', 'Guyana', 'Paraguay', 'Peru', 'Suriname', 'Uruguay', 'Venezuela (Bolivarian Republic of)'],

    # Western-Pacific
    'Western-Pacific': ['Australia', 'Brunei Darussalam', 'Cambodia', 'China', 'Cook Islands', 
    'Fiji', 'Japan', 'Kiribati', "Lao People's Democratic Republic", 'Malaysia', 'Marshall Islands', 
    'Micronesia (Federated States of)', 'Mongolia', 'Nauru', 'New Zealand', 'Niue', 'Palau', 'Papua New Guinea', 'Philippines', 
    'Republic of Korea', 'Samoa', 'Singapore', 'Solomon Islands', 'Tonga', 'Tuvalu', 'Vanuatu', 'Viet Nam'],

    # Eastern Mediterranean
    'Eastern Mediterranean': ['Afghanistan', 'Bahrain', 'Djibouti', 'Egypt', 'Iran (Islamic Republic of)', 
    'Iraq', 'Jordan', 'Kuwait', 'Lebanon', 'Libya', 'Morocco', 'occupied Palestinian territory, including east Jerusalem', 
    'Oman', 'Pakistan', 'Qatar', 'Saudi Arabia', 'Somalia', 'Sudan', 'Syrian Arab Republic', 'Tunisia', 'United Arab Emirates', 
    'Yemen'],

    # South-East Asia
    'South-East Asia': ['Bangladesh', 'Bhutan', "Democratic People's Republic of Korea", 'India', 'Indonesia', 'Maldives',
    'Myanmar', 'Nepal', 'Sri Lanka', 'Thailand', 'Timor-Leste']
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

# Get unique regions for plotting
regions = df['Region'].unique()

# Loop through each region and create two graphs for each (one for each indicator)
for region in regions:
    region_data = df[df['Region'] == region]
    
    # Plot Early Initiation of Breastfeeding (%)
    plt.figure(figsize=(12, 8))
    for country in region_mapping[region]:
        country_data = region_data[region_data['Countries, territories and areas'] == country]
        
        # Filter valid year data to avoid issues
        country_data = country_data[(country_data['Year'] >= year_range[0]) & (country_data['Year'] <= year_range[1])]
        
        # Ensure theres going to be data tp plot
        if not country_data.empty:
            plt.plot(country_data['Year'], country_data['Early initiation of breastfeeding (%)'],
                     marker='o', label=f'{country} - Early initiation of breastfeeding')

    # Add labels, title, consistent x-axis and y-axis range
    plt.xlabel('Year')
    plt.ylabel('Percentage')
    plt.title(f'Early Initiation of Breastfeeding in {region} by Country and Year')
    plt.xlim(year_range)  # Set x-axis to 1990-2020
    plt.ylim(0, 100)      # Set y-axis to 0-100 for percentage
    plt.legend(loc='best')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Plot Infants Exclusively Breastfed for the First Six Months (%)
    plt.figure(figsize=(12, 8))
    for country in region_mapping[region]:
        country_data = region_data[region_data['Countries, territories and areas'] == country]
        
        # Filter valid year data to avoid issues
        country_data = country_data[(country_data['Year'] >= year_range[0]) & (country_data['Year'] <= year_range[1])]
        
        # Ensure theres data available to plot
        if not country_data.empty:
            plt.plot(country_data['Year'], country_data['Infants exclusively breastfed for the first six months of life (%)'],
                     marker='x', label=f'{country} - Infants exclusively breastfed')

    # Add labels, title, consistent x-axis and y-axis range
    plt.xlabel('Year')
    plt.ylabel('Percentage')
    plt.title(f'Infants Exclusively Breastfed in {region} for the First Six Months by Country and Year')
    plt.xlim(year_range)  # Set x-axis to 1990-2020
    plt.ylim(0, 100)      # Set y-axis to 0-100 for percentage
    plt.legend(loc='best')
    plt.grid(True)
    plt.tight_layout()
    plt.show()