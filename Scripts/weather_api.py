import openmeteo_requests
import requests
import pandas as pd
from datetime import datetime, timedelta

# Setup the Open-Meteo API client
openmeteo = openmeteo_requests.Client()

# API configuration
url = "https://archive-api.open-meteo.com/v1/archive"
params = {
    "latitude": 33.749,
    "longitude": -84.388,
    "start_date": "2025-02-04",
    "end_date": "2025-02-18",
    "hourly": "temperature_2m",
    "timezone": "America/New_York"
}

# Make API request
responses = openmeteo.weather_api(url, params=params)
response = responses[0]

# Process hourly data
hourly = response.Hourly()
hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()

# Create datetime range
hourly_data = {
    "date": pd.date_range(
        start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
        end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
        freq=pd.Timedelta(seconds=hourly.Interval()),
        inclusive="left"
    )
}
hourly_data["temperature_2m"] = hourly_temperature_2m

# Create and display dataframe
hourly_dataframe = pd.DataFrame(data=hourly_data)
print(f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E")
print(f"Timezone: {response.Timezone()} {response.TimezoneAbbreviation()}")
print("\nHourly Temperature Data:")
print(hourly_dataframe)