import openmeteo_requests

import requests_cache
import pandas as pd
from retry_requests import retry

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

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
	"time": pd.Series(["00:00"] * len(daily_temperature_2m_max))  # Assuming daily data is at midnight
}

daily_data["daily_temperature_2m_max"] = daily_temperature_2m_max
daily_data["daily_snowfall_sum"] = daily_snowfall_sum

daily_dataframe = pd.DataFrame(data = daily_data)
daily_dataframe.to_csv("daily_data_3months.csv", index=False)

# Create a new DataFrame for combined data where the hourly and daily data are combined
combined_data = pd.DataFrame()

# Add hourly data to combined DataFrame
combined_data = pd.concat([combined_data, hourly_dataframe], ignore_index=True)

# Add daily data to combined DataFrame
combined_data = pd.concat([combined_data, daily_dataframe], ignore_index=True)

# Save the combined DataFrame to a CSV file
combined_data.to_csv("combined_data_3months.csv", index=False)


