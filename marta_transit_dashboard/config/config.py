"""
Configuration settings for the Simple MARTA App
"""

import os

# API configuration
MARTA_TRAIN_API_KEY = "3b78f59c-e96d-4085-a291-eefb29bc5ecf"
MARTA_TRAIN_API_URL = "https://developerservices.itsmarta.com:18096/itsmarta/railrealtimearrivals/developerservices/traindata"
MARTA_BUS_POSITIONS_URL = "https://gtfs-rt.itsmarta.com/TMGTFSRealTimeWebService/vehicle/vehiclepositions.pb"
MARTA_BUS_TRIPS_URL = "https://gtfs-rt.itsmarta.com/TMGTFSRealTimeWebService/tripupdate/tripupdates.pb"

# Weather API configuration
WEATHER_API_URL = "https://api.open-meteo.com/v1/forecast"
ATLANTA_LATITUDE = 33.749
ATLANTA_LONGITUDE = -84.388

# File paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR, 'static')
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
CACHE_DIR = os.path.join(BASE_DIR, 'cache')
MAP_FILE_PATH = os.path.join(STATIC_DIR, 'marta_train_map.jpg')

# Ensure directories exist
for directory in [STATIC_DIR, TEMPLATES_DIR, CACHE_DIR]:
    os.makedirs(directory, exist_ok=True)

# Cache files
WEATHER_CACHE_FILE = os.path.join(CACHE_DIR, 'weather_data.json')
TRAIN_CACHE_FILE = os.path.join(CACHE_DIR, 'train_data.json')
BUS_POSITIONS_CACHE_FILE = os.path.join(CACHE_DIR, 'bus_positions.json')
BUS_TRIPS_CACHE_FILE = os.path.join(CACHE_DIR, 'bus_tripupdates.json')

# Map configuration
MARTA_MAP_URL = "https://www.itsmarta.com/images/train-stations-map.jpg"
MAP_BACKUP_URL = "https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/MARTA_Rail_Map.svg/1200px-MARTA_Rail_Map.svg.png"

# Application settings
DEBUG = True
PORT = 5001
HOST = '0.0.0.0'
TEMPLATES_AUTO_RELOAD = True
CACHE_EXPIRATION = 3600  # 1 hour 