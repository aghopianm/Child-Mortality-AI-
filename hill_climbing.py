"""File to handle year ranges and error bar data, then apply hill climbing 
to optimise the interpolation process, room for improvement in the code
but overrall the functionality is there."""

import pandas as pd
import numpy as np
import re
from typing import Dict, List, Union

# Parse year into a list of integers for ranges like 2008-2009, these are split
def parse_year(year_str: Union[str, float]) -> Union[List[int], None]:
    if pd.isna(year_str) or year_str == 'Year':
        return None
    if '-' in str(year_str):  # Check for ranges like "2008-2009"
        return [int(y) for y in year_str.split('-')]
    return [int(year_str)]  # Single year, just return it in a list

#Extract mean value, if this is a string then I will just extract the number
def get_mean_val(value: Union[str, float, int]) -> Union[float, str]:
    if pd.isna(value):
        return value  # If value is NaN/null just return it.
    if isinstance(value, (int, float)):
        return value  # If there's already a number then nothing to do so return it.
    if isinstance(value, str):
        match = re.match(r'^(\d+(?:\.\d+)?)', value)
        if match:
            return float(match.group(1))  # Convert string to float.
    return value  # Return as-is if nothing matches.

# Interpolate between two years based on exponent that tweaks the curve
def interpolate_value(start_year: int, end_year: int, start_value: float, 
                      end_value: float, target_year: int, exponent: float) -> float:
    if start_year == end_year:
        return start_value  # Return value if no range. e.g: 2008 by itself.
    progress = (target_year - start_year) / (end_year - start_year)
    adjusted_progress = progress ** exponent  # Raise progress to exponent for curve tweaking
    return start_value + adjusted_progress * (end_value - start_value)

# Calculate smoothness of data: less extreme values and differences = better
def calc_smoothness(df: pd.DataFrame) -> float:
    numeric_cols = df.select_dtypes(include=[np.number])
    diff = numeric_cols.diff().abs().mean().mean()  # Average of absolute differences
    # Check for extreme values (upper/lower 1% of data)
    extremes = ((numeric_cols > numeric_cols.quantile(0.99)) | 
                (numeric_cols < numeric_cols.quantile(0.01))).sum().sum()
    # Balance between "smooth" (less diff) and extremes (less count)
    return -diff - 0.1 * extremes

# Hill-climbing optimization to fine-tune exponent parameter for smoother iterations.
def hill_climbing(df: pd.DataFrame, initial_exponent: float = 1.0, iterations: int = 100) -> float:
    current_exponent = initial_exponent
    current_score = calc_smoothness(df)  # Initial score

    for _ in range(iterations):
        new_exponent = current_exponent * np.random.uniform(0.9, 1.1)  # Randomly tweak exponent
        new_score = calc_smoothness(df)

        # If new score is better/higher, update the exponent
        if new_score > current_score:
            current_exponent = new_exponent
            current_score = new_score

    return current_exponent  # Return the best exponent we found

# Process country data year by year (handles ranges, single years, etc.)
def process_country(group: pd.DataFrame) -> Dict[int, Dict[str, float]]:
    country_data = {}  # Store processed data here

    for _, row in group.iterrows():
        years = parse_year(row['Year'])  # Parse the year/years
        if years is None:
            continue  # Continue if no valid year

        if len(years) == 1:
            # If single year like 2008 then just add it
            year = years[0]
            if year not in country_data:
                country_data[year] = {}
            
            # Store each column's value for the year
            for col in group.columns:
                if col != 'Year' and pd.notna(row[col]):
                    country_data[year][col] = get_mean_val(row[col])  # Get value
        else:
            # Range of years, interpolation is needed.
            start_year, end_year = years
            optimized_exponent = hill_climbing(group)  # Optimise the exponent
            
            for year in range(start_year, end_year + 1):
                if year not in country_data:
                    country_data[year] = {}
                
                for col in group.columns:
                    if col != 'Year' and pd.notna(row[col]):
                        # Find valid values before and after for interpolation
                        before = next((y for y in range(year, start_year - 1, -1) if y in country_data and col in country_data[y] and pd.notna(country_data[y][col])), None)
                        after = next((y for y in range(year, end_year + 1) if y in country_data and col in country_data[y] and pd.notna(country_data[y][col])), None)
                        
                        if before is not None and after is not None:
                            # Interpolate between the two
                            country_data[year][col] = interpolate_value(before, after, country_data[before][col], country_data[after][col], year, optimized_exponent)
                        elif before is None and after is None:
                            # No valid values to interpolate, use value
                            country_data[year][col] = get_mean_val(row[col])
                        elif before is None:
                            country_data[year][col] = country_data[after][col]  # No before value so we use after
                        else:
                            country_data[year][col] = country_data[before][col]  # No after value so we use before
    
    return country_data  # Done with this country

# Align data across all countries and years
def align_data(df: pd.DataFrame) -> pd.DataFrame:
    grouped = df.groupby('Countries, territories and areas')  # Group by country
    aligned_data = []

    for country, group in grouped:
        group = group.sort_values('Year')  # Sort by year
        country_data = process_country(group)  # Process data for this country
        
        for year, data in country_data.items():
            row_data = {'Countries, territories and areas': country, 'Year': year}
            row_data.update(data)
            aligned_data.append(row_data)  # Add to final result
    
    result_df = pd.DataFrame(aligned_data)
    result_df = result_df.sort_values(['Countries, territories and areas', 'Year'])  # Sort
    
    # Reorder columns, moving breastfeeding-related ones to the end
    cols = list(result_df.columns)
    breastfeeding_cols = ['Early initiation of breastfeeding (%)', 'Infants exclusively breastfed for the first six months of life (%)']
    for col in breastfeeding_cols:
        cols.remove(col)
    result_df = result_df[cols + breastfeeding_cols]  # Put breastfeeding columns at the end
    
    return result_df  

def main():
    input_file = 'merged_data.csv'  
    output_file = 'cleaned_data.csv'  

    df = pd.read_csv(input_file) 
    aligned_df = align_data(df)  
    aligned_df.to_csv(output_file, index=False)  # Save to file for future reference

    # Let me know the script worked
    print(f"Data alignment with hill climbing complete. Results saved to '{output_file}'.")

"""I've implemented a main function here and other functions defined earlier in the programme, not 
sure if this was necessary as I won't be repeating this code elsewhere but I thought it was good
practice"""
if __name__ == "__main__":
    main()