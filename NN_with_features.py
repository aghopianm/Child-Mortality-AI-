"""This file first imputes missing values with KNN imputation, then trains and tests
a neural network 
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.impute import KNNImputer

""" Function to load and preprocess data from our data file
'features' are the input columns, 'target' is the column we want to predict"""

def load_and_prepare_data(file_path, features, target):
    df = pd.read_csv(file_path)  # Load data from CSV file
    # Convert categorical 'Countries, territories and areas' column using one-hot encoding
    df_encoded = pd.get_dummies(df, columns=['Countries, territories and areas'])  
    # Extract input features (X) and target variable (y)
    X = df_encoded[features + [col for col in df_encoded.columns if col.startswith('Countries, territories and areas_')]]
    y = df_encoded[target]
    return X, y

""" Function to handle missing values using KNN imputation
The KNNImputer will fill missing values by averaging the values of the 10 nearest neighbour data points"""

def impute_missing_values(X, y, n_neighbors=10):
    knn_imputer = KNNImputer(n_neighbors=n_neighbors)  # Initialize KNN imputer with 10 neighbours as best results
    # Fit and transform the input feature matrix (X) and target (y) to fill missing values
    X_imputed = pd.DataFrame(knn_imputer.fit_transform(X), columns=X.columns)
    # Impute target values (y) separately and return it as a Series
    y_imputed = pd.Series(knn_imputer.fit_transform(y.values.reshape(-1, 1)).flatten(), name=y.name)
    return X_imputed, y_imputed

""" Function to define and train the neural network model
'hidden_layers' specifies the number of neurons in each hidden layer
'max_iter' is the maximum number of training iterations"""

def train_neural_network(X_train, y_train, hidden_layers=(100, 50), max_iter=1000):
    # Create MLPRegressor model with specified hidden layers and max iterations
    nn_model = MLPRegressor(hidden_layer_sizes=hidden_layers, max_iter=max_iter, random_state=50)
    nn_model.fit(X_train, y_train)  # Train the neural network model on the training data
    return nn_model

""" Function to evaluate the trained neural network model on test data
It uses Mean Squared Error and R^2 as evaluation metrics"""

def evaluate_model(model, X_test, y_test):
    predictions = model.predict(X_test)  # Predict target values for the test set
    mse = mean_squared_error(y_test, predictions)  # Calculate MSE to measure average prediction error
    r2 = r2_score(y_test, predictions)  # Calculate R^2 to measure goodness-of-fit
    return mse, r2

""" Function to predict under-five mortality rate for a specific country and year
Uses the trained neural network model and the now fully imputed data for prediction"""

def predict_country_mortality_rate(country, year, default_breastfeeding_early, default_breastfeeding_exclusive, model, scaler, X_columns, imputed_data):
    # Construct the one-hot encoded column name for the specified country
    country_col = f'Countries, territories and areas_{country}'
    
    # Search for data corresponding to the given country and year in the imputed data
    country_data = imputed_data[(imputed_data['Year'] == year) & (imputed_data[country_col] == 1)]
    
    # If breastfeeding data for the country and year exists, use it; otherwise, use default breastfeeding values
    if not country_data.empty:
        breastfeeding_early = country_data['Early initiation of breastfeeding (%)'].values[0]
        breastfeeding_exclusive = country_data['Infants exclusively breastfed for the first six months of life (%)'].values[0]
    else:
        breastfeeding_early = default_breastfeeding_early
        breastfeeding_exclusive = default_breastfeeding_exclusive
    
    # Create a dictionary of input features for prediction
    input_data = {
        'Year': [year],
        'Early initiation of breastfeeding (%)': [breastfeeding_early],
        'Infants exclusively breastfed for the first six months of life (%)': [breastfeeding_exclusive]
    }
    
    # Add country one-hot encoded columns (set the specified country column to 1, and others to 0)
    for col in X_columns:
        if col.startswith('Countries, territories and areas_'):
            input_data[col] = [1 if col == country_col else 0]
    
    # Convert the input data dictionary to a DataFrame and reorder columns to match the training data
    input_df = pd.DataFrame(input_data)
    input_df = input_df.reindex(columns=X_columns, fill_value=0)
    
    # Scale the input data using the same scaler used for training
    input_data_scaled = scaler.transform(input_df)
    # Predict the mortality rate using the neural network model
    prediction = model.predict(input_data_scaled)
    
    return prediction[0]  # Return the predicted value

"""Main execution of the file is here, I have used functions throughout this programme although
that is not necessary, given the fact that this code is unlikely to be reused.."""
if __name__ == "__main__":
    features = ['Year', 'Early initiation of breastfeeding (%)', 
                'Infants exclusively breastfed for the first six months of life (%)']
    target = 'Under-five mortality rate (per 1000 live births) (SDG 3.2.1) Both sexes'

    X, y = load_and_prepare_data('cleaned_data.csv', features, target)

    X_imputed, y_imputed = impute_missing_values(X, y)

    """Save the imputed dataset to a CSV file for future use and inspection
    this is not really needed but good for me to see how the imputation affects the data"""

    imputed_data = pd.concat([X_imputed, y_imputed], axis=1)
    imputed_data.to_csv('imputed_knn_data.csv', index=False)

    # Split the dataset into training and testing sets 
    X_train, X_test, y_train, y_test = train_test_split(X_imputed, y_imputed, test_size=0.2, random_state=50)

    # Normalise the features using StandardScaler 
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    nn_model = train_neural_network(X_train_scaled, y_train)

    """ Evaluate the trained model on the test data and print performance metrics
    Print the values for me to see in the terminal to check it worked"""
    mse, r2 = evaluate_model(nn_model, X_test_scaled, y_test)
    print("\nNeural Network Results (with KNN Imputation):")
    print(f"MSE: {mse:.4f}")
    print(f"R^2: {r2:.4f}")
    
    # Example prediction for a specific country and year for further testing
    country = "Afghanistan"
    year = 2015
    breastfeeding_early = 60  # Default value if early initiation breastfeeidng data is not available
    breastfeeding_exclusive = 50  # Default value if infants exclusively breastfeeding data is not available

    # Predict under-five mortality rate for the specified country and year
    prediction = predict_country_mortality_rate(country, year, breastfeeding_early, breastfeeding_exclusive, nn_model, scaler, X.columns, imputed_data)
    
    #Print the predicted mortality rate for me to see in terminal
    print(f"\nPredicted mortality rate for {country} in {year}:")
    print(f"Neural Network (KNN Imputation): {prediction:.2f}")
