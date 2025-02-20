import openmeteo_requests
import requests
import pandas as pd
import json
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

# Create dataframe
hourly_dataframe = pd.DataFrame(data=hourly_data)

# Save as CSV
start_date = params['start_date'].replace('-', '')
end_date = params['end_date'].replace('-', '')
csv_filename = f'weather_data_{start_date}_{end_date}.csv'
hourly_dataframe.to_csv(csv_filename, index=False)

# Convert to JSON and save
# weather_data = {
#     "coordinates": {
#         "latitude": response.Latitude(),
#         "longitude": response.Longitude()
#     },
#     "timezone": {
#         "name": response.Timezone(),
#         "abbreviation": response.TimezoneAbbreviation()
#     },
#     "hourly_data": hourly_dataframe.to_dict(orient='records')
# }

# # Save JSON
# with open('weather_data.json', 'w') as f:
#     json.dump(weather_data, f, indent=4)

print(f"File saved: weather_data.csv")
print(f"\nCoordinates: {response.Latitude()}°N {response.Longitude()}°E")
print(f"Timezone: {response.Timezone()} {response.TimezoneAbbreviation()}")
print("\nHourly Temperature Data:")
print(hourly_dataframe)