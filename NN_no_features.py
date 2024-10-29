""" This file imputes the data with KNN imputation like the model with feature selection,
but this file does NOT use any features.
The reason for this is to compare the model with features results vs. this one without"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.impute import KNNImputer

df = pd.read_csv('cleaned_data.csv')

# Create dummy variables for categorical features, in this case coutnires territories and areas
df_encoded = pd.get_dummies(df, columns=['Countries, territories and areas'])

"""Prepare X and Y, we use .drop here to drop the target in the X variable as this is the 
simplest and most effective method for using a no feature selection model. This means that all
variables will be included except for the target variable """
target = 'Under-five mortality rate (per 1000 live births) (SDG 3.2.1) Both sexes'
X = df_encoded.drop(columns=[target])
y = df_encoded[target]

# Handle missing values using KNN Imputation
knn_imputer = KNNImputer(n_neighbors=10)
X_imputed = pd.DataFrame(knn_imputer.fit_transform(X), columns=X.columns)
y_imputed = pd.Series(knn_imputer.fit_transform(y.values.reshape(-1, 1)).flatten(), name=y.name)

# Save the imputed dataset to a CSV file for inspection, not neccessary but I was interested in how it changes
imputed_data = pd.concat([X_imputed, y_imputed], axis=1)
imputed_data.to_csv('imputed_knn_data.csv', index=False)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_imputed, y_imputed, test_size=0.2, random_state=50)

# Scale the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Neural Network Model
nn_model = MLPRegressor(hidden_layer_sizes=(100, 50), max_iter=1000, random_state=50)
nn_model.fit(X_train_scaled, y_train)
nn_predictions = nn_model.predict(X_test_scaled)

#print results in the terminal for evaluation
print("\nNeural Network Results (with KNN Imputation):")
print(f"MSE: {mean_squared_error(y_test, nn_predictions):.4f}")
print(f"R^2: {r2_score(y_test, nn_predictions):.4f}")

# Function to predict mortality rate for a specific country and year
def predict_mortality_rate(country, year, model, imputed_data):
    country_col = f'Countries, territories and areas_{country}'
    
    # Select the country data
    country_data = imputed_data[(imputed_data['Year'] == year) & (imputed_data[country_col] == 1)]
    
    # Prepare the input dictionary with just the year and country
    input_data = {'Year': [year]}
    
    # Create one-hot encoded country columns
    for col in X.columns:
        if col.startswith('Countries, territories and areas_'):
            input_data[col] = [1 if col == country_col else 0]
    
    # Create DataFrame and reindex
    input_df = pd.DataFrame(input_data)
    input_df = input_df.reindex(columns=X.columns, fill_value=0)
    
    # Scale the input data
    input_data_scaled = scaler.transform(input_df)
    
    # Make prediction
    prediction = model.predict(input_data_scaled)
    
    return prediction[0]

# Example usage with fully imputed data for further testing
country = "Afghanistan"
year = 2015

nn_prediction = predict_mortality_rate(country, year, nn_model, imputed_data)

#Print results for specific country in specific year for evaluation
print(f"\nPredicted mortality rate for {country} in {year}:")
print(f"Neural Network (KNN Imputation): {nn_prediction:.2f}")