The steps to effectively run the project are as follows:

(Optional) Data visualisation step to get acclimated with the nutritional data, this uses matplotlib to display the data:

1. all_countries_plotted_nutrition.py - all countries nutritonal data plotted
2. Countries_clustered_with_subsections.py - nutritonal data clustered by continent, 
with some subsections within continents for visual clarity. As you can see the graphs
are clearer than individual countries plotted.
3. error_bar_data_plotted.py - continents clustered with error bars 
to show the range in the data. 
4. economic_and_nutritional_plotted.py - this shows countries's nutritonal data, who are grouped
by their GDP into four different groups.

(Optional) Simple analytics to show discrepencies in the data & total datapoints

1. Number_of_data_points.py - this file displays the total number of datapoints in the merged file: 125,890
to note, this is BEFORE KNN imputation is implemented to fill the file, this is JUST on the merged file.
2. Country_discrepancy_calculator.py - this file shows the discrepancy between the countries that exist in 
the nutritonal data file and the mortality data file. This is important to understand as many countries do not exist
in both datasets.

Step by step in how to run this project if you want to follow along
- these are the order I ran the files to preprocess the data, 
align year ranges and then train and test my neural network model

1. merge_mortality_rates.py - this file merges all mortality rate csv files together
2. merge_mortality_and_nutrition.py - this file merges the above merged mortality files
with the nutritional data to form one file. merged_data.csv is the uncleaned, but merged, file that is saved.
3. hill_climbing.py - this file removes error bar data and takes the mean value, and handles year-range data
with interpolation. Hill climbing optimises the exponent used in interpolation to ensure a smooth transition in the data.
cleaned_data.csv is the fully clean file with year-range values handled and no error bar data.
4. NN_with_features.py - Uses KNN imputation to impute missing values, then trains and tests a neural network model.
imputed_knn_data.csv is the final full file that is a complete and clean dataset. It is worth noting that 
I don't think that imputed_knn_data.csv is a neccessary step to save the file, however I thought it was interesting
to open the file to see how the imputation has effected the values. 
5. (Optional) NN_no_features.py - Uses KNN imputation to impute missing values, and then evaluates model performance
WITHOUT feature selection. This proved to be more innaccurate than the feature selection model (see report for more details)