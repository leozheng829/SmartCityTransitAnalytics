import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import os

# Define paths
DATA_PATH = "../Collected Data/combined_data_3months.csv"
MODEL_OUTPUT_PATH = "weather_model.joblib"
RESULTS_PATH = "../Collected Data/prediction_results.csv"

def load_data():
    """Load and preprocess the weather data."""
    print("Loading and preprocessing data...")
    # Load the data
    df = pd.read_csv(DATA_PATH)
    
    # Filter out rows with missing values in our target or key features
    df = df.dropna(subset=['hourly_temperature_2m'])
    
    # Create datetime column
    df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'])
    
    # Extract additional features from date and time
    df['hour'] = df['datetime'].dt.hour
    df['day_of_week'] = df['datetime'].dt.dayofweek
    df['month'] = df['datetime'].dt.month
    df['day'] = df['datetime'].dt.day
    
    # Convert weather codes to categories (simplified)
    # Weather codes: 0=Clear, 1=Mainly Clear, 2=Partly Cloudy, 3=Overcast
    # 45,48=Fog, 51,53,55=Drizzle, 61,63,65=Rain, 71,73,75=Snow, etc.
    def classify_weather(code):
        if code == 0:
            return 'clear'
        elif code in [1, 2]:
            return 'partly_cloudy'
        elif code == 3:
            return 'overcast'
        elif code in [45, 48]:
            return 'fog'
        elif code in [51, 53, 55]:
            return 'drizzle'
        elif code in [61, 63, 65]:
            return 'rain'
        elif code in [71, 73, 75]:
            return 'snow'
        else:
            return 'other'
    
    # Apply the classification
    df['weather_category'] = df['hourly_weather_code'].apply(classify_weather)
    
    # One-hot encode the weather category
    df = pd.get_dummies(df, columns=['weather_category'], drop_first=True)
    
    return df

def prepare_features(df):
    """Prepare features and target variables for the model."""
    print("Preparing features and target variables...")
    
    # Define features and target
    # We'll predict temperature based on other weather conditions and time features
    features = ['hour', 'day_of_week', 'month', 'day', 
                'hourly_apparent_temperature', 'hourly_precipitation', 
                'hourly_relative_humidity_2m']
    
    # Add weather category columns if they exist
    weather_cols = [col for col in df.columns if 'weather_category' in col]
    features.extend(weather_cols)
    
    # Some features might be missing in some rows, so we'll drop those rows
    df = df.dropna(subset=features)
    
    # Define target
    target = 'hourly_temperature_2m'
    
    # Create feature matrix and target vector
    X = df[features]
    y = df[target]
    
    return X, y, features

def train_model(X, y):
    """Train a RandomForest model on the data."""
    print("Training model...")
    
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Scale the features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train a Random Forest model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train_scaled, y_train)
    
    # Save the model and scaler
    joblib.dump((model, scaler, X_train.columns.tolist()), MODEL_OUTPUT_PATH)
    
    return model, scaler, X_train, X_test, y_train, y_test

def evaluate_model(model, scaler, X_test, y_test):
    """Evaluate the model's performance."""
    print("Evaluating model...")
    
    # Make predictions
    X_test_scaled = scaler.transform(X_test)
    y_pred = model.predict(X_test_scaled)
    
    # Calculate metrics
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)
    
    print(f"Mean Squared Error: {mse:.2f}")
    print(f"Root Mean Squared Error: {rmse:.2f}")
    print(f"R² Score: {r2:.2f}")
    
    return y_pred, mse, rmse, r2

def analyze_feature_importance(model, features):
    """Analyze and plot feature importance."""
    print("Analyzing feature importance...")
    
    # Get feature importances
    importances = model.feature_importances_
    indices = np.argsort(importances)[::-1]
    
    # Print feature ranking
    print("Feature ranking:")
    for i in range(len(features)):
        print(f"{i+1}. {features[indices[i]]} ({importances[indices[i]]:.4f})")
    
    # Plot feature importances
    plt.figure(figsize=(10, 6))
    plt.title("Feature Importances")
    plt.bar(range(len(features)), importances[indices], align="center")
    plt.xticks(range(len(features)), [features[i] for i in indices], rotation=90)
    plt.tight_layout()
    plt.savefig("feature_importance.png")
    
def predict_future(model, scaler, features, days=7):
    """Make predictions for future days."""
    print(f"Predicting temperature for the next {days} days...")
    
    # Get the latest data
    df = pd.read_csv(DATA_PATH)
    latest_date = pd.to_datetime(df['date'].iloc[-1])
    
    # Create future dates
    future_dates = [latest_date + pd.Timedelta(days=i) for i in range(1, days+1)]
    
    # Create a DataFrame for future predictions
    future_df = pd.DataFrame()
    future_df['date'] = [d.strftime('%Y-%m-%d') for d in future_dates]
    
    # For simplicity, we'll create entries for every 3 hours
    hours = [0, 3, 6, 9, 12, 15, 18, 21]
    future_predictions = []
    
    for date in future_dates:
        for hour in hours:
            # Create a feature row
            # This is simplified and would need real features in a production environment
            # Here we're using average values from the training data
            
            feature_row = {
                'hour': hour,
                'day_of_week': date.dayofweek,
                'month': date.month,
                'day': date.day,
                # Use median values from our dataset for other features
                'hourly_apparent_temperature': df['hourly_apparent_temperature'].median(),
                'hourly_precipitation': df['hourly_precipitation'].median(),
                'hourly_relative_humidity_2m': df['hourly_relative_humidity_2m'].median()
            }
            
            # Add weather category columns
            for col in features:
                if 'weather_category' in col and col not in feature_row:
                    feature_row[col] = 0
            
            # Set the most common weather category to 1 
            # (this is very simplified and would need improvement)
            common_weather = 'weather_category_clear'
            if common_weather in features:
                feature_row[common_weather] = 1
                
            # Convert to DataFrame
            feature_df = pd.DataFrame([feature_row])
            feature_df = feature_df[features]
            
            # Scale and predict
            feature_scaled = scaler.transform(feature_df)
            temp_prediction = model.predict(feature_scaled)[0]
            
            # Add to results
            future_predictions.append({
                'date': date.strftime('%Y-%m-%d'),
                'time': f"{hour:02d}:00",
                'predicted_temperature': temp_prediction
            })
    
    # Convert to DataFrame and save
    predictions_df = pd.DataFrame(future_predictions)
    predictions_df.to_csv(RESULTS_PATH, index=False)
    
    return predictions_df

def main():
    """Main function to run the entire pipeline."""
    print("Starting weather prediction model training and evaluation...")
    
    # Load and preprocess data
    df = load_data()
    
    # Prepare features
    X, y, features = prepare_features(df)
    
    # Train model
    model, scaler, X_train, X_test, y_train, y_test = train_model(X, y)
    
    # Evaluate model
    y_pred, mse, rmse, r2 = evaluate_model(model, scaler, X_test, y_test)
    
    # Analyze feature importance
    analyze_feature_importance(model, features)
    
    # Make future predictions
    future_predictions = predict_future(model, scaler, features)
    
    print("Model training and evaluation complete!")
    print(f"Model saved to: {MODEL_OUTPUT_PATH}")
    print(f"Future predictions saved to: {RESULTS_PATH}")

if __name__ == "__main__":
    main() 