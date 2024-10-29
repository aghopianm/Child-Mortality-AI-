# First region mapping (Selected Countries)
mortality_rates = set([
    'Afghanistan', 'Albania', 'Algeria', 'Argentina', 'Armenia', 'Azerbaijan', 'Bangladesh', 'Barbados', 'Belarus', 
    'Belize', 'Benin', 'Bhutan', 'Bolivia (Plurinational State of)', 'Bosnia and Herzegovina', 'Botswana', 'Brazil', 
    'Burkina Faso', 'Burundi', "Cote d'Ivoire", 'Cabo Verde', 'Cambodia', 'Cameroon', 'Central African Republic', 'Chad', 
    'Colombia', 'Comoros', 'Congo', 'Costa Rica', 'Croatia', 'Cuba', "Democratic People's Republic of Korea", 'Djibouti', 
    'Dominican Republic', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Eswatini', 'Ethiopia', 'Fiji', 
    'Gabon', 'Gambia', 'Georgia', 'Ghana', 'Guatemala', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Honduras', 'India', 
    'Indonesia', 'Iran (Islamic Republic of)', 'Iraq', 'Jamaica', 'Jordan', 'Kazakhstan', 'Kenya', 'Kyrgyzstan', 
    "Lao People's Democratic Republic", 'Lebanon', 'Lesotho', 'Liberia', 'Madagascar', 'Maldives', 'Malawi', 'Malaysia', 
    'Mali', 'Marshall Islands', 'Mauritania', 'Mexico', 'Mongolia', 'Montenegro', 'Morocco', 'Mozambique', 'Myanmar', 
    'Namibia', 'Nauru', 'Nepal', 'Nicaragua', 'Niger', 'Nigeria', 'North Macedonia', 'occupied Palestinian territory, including east Jerusalem', 
    'Oman', 'Pakistan', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Qatar', 'Republic of Moldova', 
    'Romania', 'Russian Federation', 'Rwanda', 'Saint Lucia', 'Samoa', 'Sao Tome and Principe', 'Senegal', 'Serbia', 
    'Sierra Leone', 'Solomon Islands', 'Somalia', 'South Africa', 'South Sudan', 'Sri Lanka', 'Sudan', 'Suriname', 
    'Syrian Arab Republic', 'Turkiye', 'Tajikistan', 'Thailand', 'Timor-Leste', 'Togo', 'Trinidad and Tobago', 'Tunisia', 
    'Turkmenistan', 'Tuvalu', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Republic of Tanzania', 'United States of America', 
    'Uruguay', 'Uzbekistan', 'Vanuatu', 'Venezuela (Bolivarian Republic of)', 'Viet Nam', 'Yemen', 'Zambia', 'Zimbabwe'
])

# Second region mapping (Sub-regions)
nutritional_data = set([
    'Austria', 'Belgium', 'France', 'Germany', 'Ireland', 'Luxembourg', 'Netherlands (Kingdom of the)', 'Switzerland', 
    'United Kingdom of Great Britain', 'Armenia', 'Azerbaijan', 'Belarus', 'Bulgaria', 'Georgia', 'Kazakhstan', 'Kyrgyzstan', 
    'Republic of Moldova', 'Russian Federation', 'Tajikistan', 'Turkmenistan', 'Ukraine', 'Uzbekistan', 'Denmark', 
    'Estonia', 'Finland', 'Iceland', 'Latvia', 'Lithuania', 'Norway', 'Sweden', 'Albania', 'Andorra', 'Bosnia and Herzegovina', 
    'Croatia', 'Cyprus', 'Greece', 'Italy', 'Malta', 'Monaco', 'Montenegro', 'North Macedonia', 'Portugal', 'San Marino', 
    'Serbia', 'Slovenia', 'Spain', 'Turkey', 'Canada', 'United States of America', 'Bahamas', 'Barbados', 'Belize', 
    'Costa Rica', 'Cuba', 'Dominica', 'Dominican Republic', 'El Salvador', 'Grenada', 'Guatemala', 'Haiti', 'Honduras', 
    'Jamaica', 'Mexico', 'Nicaragua', 'Panama', 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Vincent and the Grenadines', 
    'Trinidad and Tobago', 'Argentina', 'Bolivia (Plurinational State of)', 'Brazil', 'Chile', 'Colombia', 'Ecuador', 'Guyana', 
    'Paraguay', 'Peru', 'Suriname', 'Uruguay', 'Venezuela (Bolivarian Republic of)', 'Australia', 'Brunei Darussalam', 
    'Cambodia', 'China', 'Cook Islands', 'Fiji', 'Japan', 'Kiribati', "Lao People's Democratic Republic", 'Malaysia', 
    'Marshall Islands', 'Micronesia (Federated States of)', 'Mongolia', 'Nauru', 'New Zealand', 'Niue', 'Palau', 'Papua New Guinea', 
    'Philippines', 'Republic of Korea', 'Samoa', 'Singapore', 'Solomon Islands', 'Tonga', 'Tuvalu', 'Vanuatu', 'Viet Nam', 
    'Afghanistan', 'Bahrain', 'Djibouti', 'Egypt', 'Iran (Islamic Republic of)', 'Iraq', 'Jordan', 'Kuwait', 'Lebanon', 
    'Libya', 'Morocco', 'occupied Palestinian territory, including east Jerusalem', 'Oman', 'Pakistan', 'Qatar', 'Saudi Arabia', 
    'Somalia', 'Sudan', 'Syrian Arab Republic', 'Tunisia', 'United Arab Emirates', 'Yemen', 'Bangladesh', 'Bhutan', 
    "Democratic People's Republic of Korea", 'India', 'Indonesia', 'Maldives', 'Myanmar', 'Nepal', 'Sri Lanka', 'Thailand', 'Timor-Leste'
])

# Find countries in the mortality rates that dont exist in the nutritonal data
missing_in_second = mortality_rates - nutritional_data

# Find countries in the nutritional data that dont exist in the mortality rate data
missing_in_first = nutritional_data - mortality_rates

# Output the differences
print("Countries in the Infant Nutrition data that are not in the mortality rate datasets (by continent):", missing_in_second)
print("\n\n\n\nCountries in the mortality data sets (By continent) that are not in the  Infant Nutrition Dataset", missing_in_first)
