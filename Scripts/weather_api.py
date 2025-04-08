import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
import requests
import os
import json
from datetime import datetime

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

# Define a function to get current weather data for the API server
def get_current_weather(city, api_key=None):
    """
    Get current weather for a given city using OpenWeatherMap API
    
    Parameters:
    city (str): City name
    api_key (str, optional): OpenWeatherMap API key, if None will use mock data
    
    Returns:
    dict: Weather data including temperature, condition, etc.
    """
    # If no API key is provided, return mock data
    if api_key is None:
        # Check if we have cached data in a file
        if os.path.exists('weather_data.json'):
            try:
                with open('weather_data.json', 'r') as f:
                    return json.load(f)
            except:
                pass

        # Otherwise return mock data
        mock_data = {
            "main": {
                "temp": 72,
                "feels_like": 70,
                "humidity": 65
            },
            "weather": [
                {
                    "description": "Partly cloudy",
                    "icon": "03d"
                }
            ],
            "wind": {
                "speed": 5.8,
                "deg": 220
            },
            "name": city,
            "dt": int(datetime.now().timestamp())
        }
        
        # Save mock data to file for future use
        with open('weather_data.json', 'w') as f:
            json.dump(mock_data, f)
            
        return mock_data
    
    # Use OpenWeatherMap API with provided key
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=imperial"
        response = requests.get(url)
        response.raise_for_status()
        
        weather_data = response.json()
        
        # Save to file for caching
        with open('weather_data.json', 'w') as f:
            json.dump(weather_data, f)
            
        return weather_data
    except Exception as e:
        print(f"Error fetching weather data: {e}")
        # Return mock data as fallback
        return get_current_weather(city, api_key=None)

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": 33.749,
    "longitude": -84.388,
    "daily": ["temperature_2m_max", "snowfall_sum"],
    "hourly": ["temperature_2m", "apparent_temperature", "precipitation", "weather_code", "relative_humidity_2m"],
    "current": "showers",
    "timezone": "America/New_York",
    "past_days": 92,
    "forecast_days": 16
}

# Only execute this code when run directly, not when imported
if __name__ == "__main__":
    responses = openmeteo.weather_api(url, params=params)

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]
    print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
    print(f"Elevation {response.Elevation()} m asl")
    print(f"Timezone {response.Timezone()}{response.TimezoneAbbreviation()}")
    print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

                                
    # Current values. The order of variables needs to be the same as requested.
    current = response.Current()
    current_showers = current.Variables(0).Value()

    print(f"Current time {current.Time()}")
    print(f"Current showers {current_showers}")
                                
    # Process hourly data. The order of variables needs to be the same as requested.
    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
    hourly_apparent_temperature = hourly.Variables(1).ValuesAsNumpy()
    hourly_precipitation = hourly.Variables(2).ValuesAsNumpy()
    hourly_weather_code = hourly.Variables(3).ValuesAsNumpy()
    hourly_relative_humidity_2m = hourly.Variables(4).ValuesAsNumpy()

    hourly_data = {
        "date": pd.date_range(
            start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
            end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left"
        ).strftime('%Y-%m-%d'),
        "time": pd.date_range(
            start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
            end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left"
        ).strftime('%H:%M')
    }

    hourly_data["hourly_temperature_2m"] = hourly_temperature_2m
    hourly_data["hourly_apparent_temperature"] = hourly_apparent_temperature
    hourly_data["hourly_precipitation"] = hourly_precipitation
    hourly_data["hourly_weather_code"] = hourly_weather_code
    hourly_data["hourly_relative_humidity_2m"] = hourly_relative_humidity_2m

    hourly_dataframe = pd.DataFrame(data = hourly_data)
    hourly_dataframe.to_csv("hourly_data_3months.csv", index=False)

    # Process daily data. The order of variables needs to be the same as requested.
    daily = response.Daily()
    daily_temperature_2m_max = daily.Variables(0).ValuesAsNumpy()
    daily_snowfall_sum = daily.Variables(1).ValuesAsNumpy()

    daily_data = {
        "date": pd.date_range(
            start=pd.to_datetime(daily.Time(), unit="s", utc=True),
            end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=daily.Interval()),
            inclusive="left"
        ).strftime('%Y-%m-%d'),
        "daily_temperature_2m_max": daily_temperature_2m_max,
        "daily_snowfall_sum": daily_snowfall_sum
    }

    daily_dataframe = pd.DataFrame(data = daily_data)
    daily_dataframe.to_csv("daily_data_3months.csv", index=False)

    # Create a combined dataset where daily values are added to midnight entries in the hourly data
    # First convert hourly_dataframe to include complete datetime for easier merging
    hourly_dataframe['datetime'] = pd.to_datetime(hourly_dataframe['date'] + ' ' + hourly_dataframe['time'])

    # Create a copy for the combined data
    combined_data = hourly_dataframe.copy()

    # Add empty columns for daily data
    combined_data['daily_temperature_2m_max'] = None
    combined_data['daily_snowfall_sum'] = None

    # Find midnight entries (00:00) and add daily data for the corresponding dates
    midnight_entries = combined_data['time'] == '00:00'

    # Create a dictionary to map dates to daily data for efficient lookup
    daily_data_dict = dict(zip(daily_dataframe['date'], 
                            zip(daily_dataframe['daily_temperature_2m_max'], 
                                daily_dataframe['daily_snowfall_sum'])))

    # Update only the midnight entries with daily data
    for idx in combined_data[midnight_entries].index:
        date = combined_data.loc[idx, 'date']
        if date in daily_data_dict:
            combined_data.loc[idx, 'daily_temperature_2m_max'] = daily_data_dict[date][0]
            combined_data.loc[idx, 'daily_snowfall_sum'] = daily_data_dict[date][1]

    # Drop the temporary datetime column as it's no longer needed
    combined_data = combined_data.drop(columns=['datetime'])

    # Save the combined DataFrame to a CSV file
    combined_data.to_csv("combined_data_3months.csv", index=False)

    print("Processing complete. Three CSV files have been generated:")
    print("1. hourly_data_3months.csv - Contains only hourly data")
    print("2. daily_data_3months.csv - Contains only daily data")
    print("3. combined_data_3months.csv - Contains hourly data with daily values at midnight entries")