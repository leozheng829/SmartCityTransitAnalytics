# MARTA Transit Dashboard - Configuration Guide

## Overview

This document details how to configure the MARTA Transit Dashboard application for different environments and use cases. The configuration system allows customization of API endpoints, credentials, caching behavior, and visual elements.

## Configuration Files

The main configuration files are located in the `config/` directory:

- `config.py` - Main configuration file (created by copying `config.example.py`)
- `config.example.py` - Example configuration with documented options

## Basic Configuration

### Required Configuration

At minimum, you need to set up the following configuration options:

1. **MARTA API Key**: Required for accessing train data
2. **Cache Directory**: Location to store cached API responses
3. **Server Settings**: Host, port, and debug mode

### Example Basic Configuration

```python
# MARTA API settings
MARTA_TRAIN_API_KEY = "your-api-key-here"
MARTA_TRAIN_API_URL = "http://developer.itsmarta.com/RealtimeTrain/RestServiceNextTrain/GetRealtimeArrivals"

# Cache settings
CACHE_DIR = "cache"
TRAIN_CACHE_FILE = "cache/train_data.json"
BUS_POSITIONS_CACHE_FILE = "cache/bus_positions.json"
BUS_TRIPS_CACHE_FILE = "cache/bus_trips.json"
WEATHER_CACHE_FILE = "cache/weather_data.json"

# Server settings
DEBUG = True
PORT = 5000
HOST = "0.0.0.0"
```

## Advanced Configuration Options

### API Endpoints and Keys

```python
# MARTA API settings
MARTA_TRAIN_API_KEY = "your-api-key-here"
MARTA_TRAIN_API_URL = "http://developer.itsmarta.com/RealtimeTrain/RestServiceNextTrain/GetRealtimeArrivals"
MARTA_BUS_POSITIONS_URL = "http://developer.itsmarta.com/gtfs_realtime/VehiclePositions.pb"
MARTA_BUS_TRIPS_URL = "http://developer.itsmarta.com/gtfs_realtime/TripUpdate.pb"

# Weather API settings
WEATHER_API_BASE_URL = "https://api.open-meteo.com/v1/forecast"
ATLANTA_LAT = 33.749
ATLANTA_LON = -84.388
```

### Caching Configuration

Control how data is cached to balance performance and freshness:

```python
# Caching settings
CACHE_DIR = "cache"
TRAIN_CACHE_FILE = "cache/train_data.json"
BUS_POSITIONS_CACHE_FILE = "cache/bus_positions.json"
BUS_TRIPS_CACHE_FILE = "cache/bus_trips.json"
WEATHER_CACHE_FILE = "cache/weather_data.json"

# Cache expiration (in seconds)
TRAIN_CACHE_EXPIRY = 60  # 1 minute
BUS_CACHE_EXPIRY = 30    # 30 seconds
WEATHER_CACHE_EXPIRY = 600  # 10 minutes
```

### Map Configuration

Configure the map display and boundaries:

```python
# Map display settings
MAP_DEFAULT_CENTER = [33.749, -84.388]  # Atlanta coordinates
MAP_DEFAULT_ZOOM = 11
MAP_MIN_ZOOM = 9
MAP_MAX_ZOOM = 14

# Atlanta bounds (for constraining the map view)
MAP_BOUNDS_SW = [33.400, -84.950]  # Southwest corner
MAP_BOUNDS_NE = [34.200, -83.900]  # Northeast corner
```

### User Interface Settings

Customize the user interface:

```python
# UI settings
APP_NAME = "MARTA Transit Dashboard"
REFRESH_INTERVAL = 30  # seconds
MAX_TRAINS_DISPLAY = 6
MAX_BUSES_DISPLAY = 6
ENABLE_ANIMATIONS = True
THEME_COLOR = "#CE0E2D"  # MARTA red
```

### Logging Configuration

Configure application logging:

```python
# Logging configuration
LOG_LEVEL = "INFO"  # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FILE = "app.log"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
ENABLE_CONSOLE_LOGGING = True
```

## Environment Variables

The application also supports configuration via environment variables, which override values in the config file:

| Environment Variable | Description | Example |
|----------------------|-------------|---------|
| `MARTA_API_KEY` | MARTA Train API key | `your-api-key` |
| `DEBUG` | Enable debug mode | `True` or `False` |
| `PORT` | Server port | `5000` |
| `HOST` | Server host | `0.0.0.0` |
| `CACHE_DIR` | Directory for cached data | `cache` |

### Using Environment Variables

```bash
# Linux/macOS
export MARTA_API_KEY=your-api-key
export PORT=8080

# Windows
set MARTA_API_KEY=your-api-key
set PORT=8080
```

## Setting Up API Keys

### MARTA API Key

1. Visit [MARTA Developer Resources](http://www.itsmarta.com/app-developer-resources.aspx)
2. Register for an API key
3. Add the key to your `config.py` file:
   ```python
   MARTA_TRAIN_API_KEY = "your-marta-api-key"
   ```

## Troubleshooting Configuration Issues

### Common Configuration Problems

1. **Missing API Key**: Ensure your MARTA API key is set correctly
   - Error: "Authentication failed" in logs
   - Solution: Check your API key is correct and properly formatted

2. **Incorrect Cache Directory**: Ensure cache directory exists and is writable
   - Error: "Permission denied" or "No such file or directory"
   - Solution: Create the cache directory: `mkdir -p cache`

3. **Port Already in Use**: Server fails to start because the port is in use
   - Error: "Address already in use"
   - Solution: Change the port in configuration

## Configuration Validation

The application validates your configuration at startup. Watch the console output for any warning or error messages about the configuration. 