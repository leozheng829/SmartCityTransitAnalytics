# Weather Machine Learning Model

This script analyzes weather data and builds a machine learning model to predict temperature based on various weather features.

## Features

- Loads and preprocesses weather data from CSV files
- Trains a Random Forest regression model to predict hourly temperature
- Evaluates model performance using metrics like RMSE and R²
- Analyzes feature importance to understand what factors most affect temperature
- Makes predictions for future temperature based on the trained model
- Saves the trained model for future use

## Requirements

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

1. Ensure your weather data is in the correct format in `../Collected Data/combined_data_3months.csv`
2. Run the script:

```bash
python weather_ml_model.py
```

3. The script will:
   - Train a model on your data
   - Output performance metrics to the console
   - Save the trained model to `weather_model.joblib`
   - Generate predictions for the next week to `../Collected Data/prediction_results.csv`
   - Create a feature importance plot as `feature_importance.png`

## Customization

You can modify the following aspects of the script:

- `DATA_PATH`: Path to your input data
- `MODEL_OUTPUT_PATH`: Where to save the trained model
- `RESULTS_PATH`: Where to save prediction results
- In the `predict_future()` function, change the `days` parameter to predict for a different time period

## Model Details

The script uses a Random Forest Regressor to predict hourly temperature based on:

- Time features (hour, day of week, month, day)
- Weather conditions (apparent temperature, precipitation, humidity)
- Weather categories (clear, cloudy, rain, etc.)

Feature importance analysis will show which of these factors most strongly influence temperature predictions. 