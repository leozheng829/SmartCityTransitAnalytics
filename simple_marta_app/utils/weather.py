"""
Weather data utilities for the Simple MARTA App
"""

import json
import os
import sys

# Add parent directory to import path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.config import (
    WEATHER_API_URL,
    ATLANTA_LATITUDE,
    ATLANTA_LONGITUDE,
    WEATHER_CACHE_FILE
)

# Try to import OpenMeteo
try:
    import openmeteo_requests
    import requests_cache
    from retry_requests import retry
    
    # Create OpenMeteo client
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)
except ImportError:
    print("Warning: Weather API dependencies missing. Will use fallback data.")
    openmeteo = None

def get_weather_data():
    """
    Get current Atlanta weather data from Open-Meteo API
    
    Returns:
        dict: Weather data including temperature, condition, etc.
    """
    try:
        # If we can't use the API, fall back to cached data
        if openmeteo is None:
            return get_weather_fallback()
            
        # Set up API request parameters
        params = {
            "latitude": ATLANTA_LATITUDE,
            "longitude": ATLANTA_LONGITUDE,
            "current": [
                "temperature_2m", 
                "apparent_temperature", 
                "precipitation", 
                "weather_code", 
                "relative_humidity_2m"
            ],
            "temperature_unit": "fahrenheit",
            "timezone": "America/New_York"
        }
        
        # Make the API request
        responses = openmeteo.weather_api(WEATHER_API_URL, params=params)
        response = responses[0]
        
        # Process current values
        current = response.Current()
        current_temperature = current.Variables(0).Value()
        current_apparent_temp = current.Variables(1).Value()
        current_precipitation = current.Variables(2).Value()
        current_weather_code = current.Variables(3).Value()
        current_humidity = current.Variables(4).Value()
        
        # Get weather condition description based on WMO code
        condition = get_weather_description(current_weather_code)
        
        # Prepare the result
        result = {
            'temperature': round(current_temperature),
            'condition': condition,
            'humidity': round(current_humidity),
            'feels_like': round(current_apparent_temp),
            'city': 'Atlanta'
        }
        
        # Cache the data for future use
        with open(WEATHER_CACHE_FILE, 'w') as f:
            json.dump(result, f)
            
        return result
    except Exception as e:
        print(f"Error getting weather data: {e}")
        return get_weather_fallback()

def get_weather_description(weather_code):
    """
    Convert WMO weather code to human-readable description
    
    Args:
        weather_code (int): WMO weather code
        
    Returns:
        str: Human-readable weather description
    """
    weather_codes = {
        0: "Clear sky",
        1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
        45: "Fog", 48: "Depositing rime fog",
        51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
        56: "Light freezing drizzle", 57: "Dense freezing drizzle",
        61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
        66: "Light freezing rain", 67: "Heavy freezing rain",
        71: "Slight snow fall", 73: "Moderate snow fall", 75: "Heavy snow fall",
        77: "Snow grains",
        80: "Slight rain showers", 81: "Moderate rain showers", 82: "Violent rain showers",
        85: "Slight snow showers", 86: "Heavy snow showers",
        95: "Thunderstorm", 96: "Thunderstorm with hail", 99: "Thunderstorm with heavy hail"
    }
    return weather_codes.get(weather_code, "Unknown")

def get_weather_fallback():
    """
    Return mock weather data if the API is unavailable
    
    Returns:
        dict: Mock weather data
    """
    # Check if we have cached data in a file
    if os.path.exists(WEATHER_CACHE_FILE):
        try:
            with open(WEATHER_CACHE_FILE, 'r') as f:
                data = json.load(f)
                return {
                    'temperature': data.get('temperature', 72),
                    'condition': data.get('condition', 'Partly cloudy'),
                    'humidity': data.get('humidity', 65),
                    'feels_like': data.get('feels_like', 70),
                    'city': data.get('city', 'Atlanta')
                }
        except:
            pass
    
    # Return hardcoded data as a last resort
    mock_data = {
        'temperature': 72,
        'condition': 'Partly cloudy',
        'humidity': 65,
        'feels_like': 70,
        'city': 'Atlanta'
    }
    
    # Cache this data for future use
    os.makedirs(os.path.dirname(WEATHER_CACHE_FILE), exist_ok=True)
    with open(WEATHER_CACHE_FILE, 'w') as f:
        json.dump(mock_data, f)
        
    return mock_data 