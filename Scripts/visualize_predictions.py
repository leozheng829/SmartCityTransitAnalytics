import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from datetime import datetime

def load_data():
    """Load prediction results and actual data for comparison."""
    # Load predictions
    predictions_path = "../Collected Data/prediction_results.csv"
    predictions_df = pd.read_csv(predictions_path)
    
    # Load actual data for comparison (if available)
    actual_data_path = "../Collected Data/combined_data_3months.csv"
    if os.path.exists(actual_data_path):
        actual_df = pd.read_csv(actual_data_path)
        # Keep only rows with valid temperature data
        actual_df = actual_df.dropna(subset=['hourly_temperature_2m'])
    else:
        actual_df = None
    
    return predictions_df, actual_df

def plot_temperature_predictions(predictions_df):
    """Plot temperature predictions for each day."""
    # Create a directory for the plots if it doesn't exist
    output_dir = "../Collected Data/Visualizations"
    os.makedirs(output_dir, exist_ok=True)
    
    # Convert date strings to datetime
    predictions_df['datetime'] = pd.to_datetime(predictions_df['date'] + ' ' + predictions_df['time'])
    
    # Sort by datetime
    predictions_df = predictions_df.sort_values('datetime')
    
    # Get unique dates
    unique_dates = predictions_df['date'].unique()
    
    # Plot temperatures for each date
    plt.figure(figsize=(12, 8))
    
    # Plot each day with a different color
    for i, date in enumerate(unique_dates):
        day_data = predictions_df[predictions_df['date'] == date]
        plt.plot(day_data['time'], 
                 day_data['predicted_temperature'], 
                 'o-', 
                 label=date,
                 color=plt.cm.tab10(i % 10))
    
    plt.title('Predicted Hourly Temperatures')
    plt.xlabel('Time')
    plt.ylabel('Temperature (°C)')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(title='Date')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Save the plot
    plt.savefig(f"{output_dir}/temperature_predictions.png")
    plt.close()
    
    # Create a combined plot showing the trend across all days
    plt.figure(figsize=(12, 6))
    plt.plot(predictions_df['datetime'], predictions_df['predicted_temperature'], 'o-')
    plt.title('Temperature Prediction Trend')
    plt.xlabel('Date and Time')
    plt.ylabel('Temperature (°C)')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Save the trend plot
    plt.savefig(f"{output_dir}/temperature_trend.png")
    plt.close()

def compare_with_actual(predictions_df, actual_df):
    """If actual data is available for the prediction period, compare predictions with actual values."""
    if actual_df is None:
        print("No actual data available for comparison.")
        return
    
    # Create datetime columns for comparison
    predictions_df['datetime'] = pd.to_datetime(predictions_df['date'] + ' ' + predictions_df['time'])
    actual_df['datetime'] = pd.to_datetime(actual_df['date'] + ' ' + actual_df['time'])
    
    # Find overlapping dates (if any)
    prediction_dates = set(predictions_df['date'])
    actual_dates = set(actual_df['date'])
    overlapping_dates = prediction_dates.intersection(actual_dates)
    
    if not overlapping_dates:
        print("No overlapping dates between predictions and actual data for comparison.")
        return
    
    # Create output directory if it doesn't exist
    output_dir = "../Collected Data/Visualizations"
    os.makedirs(output_dir, exist_ok=True)
    
    # Filter data for overlapping dates
    overlap_predictions = predictions_df[predictions_df['date'].isin(overlapping_dates)]
    overlap_actual = actual_df[actual_df['date'].isin(overlapping_dates)]
    
    # Now we need to match the exact timestamps
    # This is a simplified approach - we'll match based on date and time
    merged_data = pd.merge(
        overlap_predictions, 
        overlap_actual[['date', 'time', 'hourly_temperature_2m']], 
        on=['date', 'time'], 
        how='inner',
        suffixes=('_pred', '')
    )
    
    if merged_data.empty:
        print("No exact time matches between predictions and actual data.")
        return
    
    # Plot comparison
    plt.figure(figsize=(12, 6))
    plt.plot(merged_data['datetime'], merged_data['predicted_temperature'], 'o-', label='Predicted')
    plt.plot(merged_data['datetime'], merged_data['hourly_temperature_2m'], 'o-', label='Actual')
    plt.title('Predicted vs Actual Temperatures')
    plt.xlabel('Date and Time')
    plt.ylabel('Temperature (°C)')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Save the comparison plot
    plt.savefig(f"{output_dir}/prediction_vs_actual.png")
    plt.close()
    
    # Calculate error metrics
    mae = np.mean(np.abs(merged_data['predicted_temperature'] - merged_data['hourly_temperature_2m']))
    rmse = np.sqrt(np.mean(np.square(merged_data['predicted_temperature'] - merged_data['hourly_temperature_2m'])))
    
    print(f"Mean Absolute Error: {mae:.2f}°C")
    print(f"Root Mean Squared Error: {rmse:.2f}°C")
    
    # Save error metrics to file
    with open(f"{output_dir}/error_metrics.txt", 'w') as f:
        f.write(f"Comparison performed on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Number of comparison points: {len(merged_data)}\n")
        f.write(f"Mean Absolute Error: {mae:.2f}°C\n")
        f.write(f"Root Mean Squared Error: {rmse:.2f}°C\n")

def main():
    """Main function to run visualization."""
    print("Starting prediction visualization...")
    
    # Load data
    predictions_df, actual_df = load_data()
    
    # Visualize predictions
    plot_temperature_predictions(predictions_df)
    
    # Compare with actual data if available
    compare_with_actual(predictions_df, actual_df)
    
    print("Visualization complete! Check the 'Visualizations' folder for results.")

if __name__ == "__main__":
    main() 