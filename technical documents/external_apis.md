# MARTA Transit Dashboard - External APIs

## Overview

The MARTA Transit Dashboard integrates with several external APIs to provide real-time transit and weather information. This document details these APIs, how they are integrated, and fallback mechanisms when they are unavailable.

## MARTA Train API

### API Details

- **Provider**: Metropolitan Atlanta Rapid Transit Authority (MARTA)
- **Documentation**: [MARTA Developer Resources](http://www.itsmarta.com/app-developer-resources.aspx)
- **Base URL**: `http://developer.itsmarta.com/RealtimeTrain/RestServiceNextTrain/GetRealtimeArrivals`
- **Format**: JSON
- **Authentication**: API Key required (query parameter `apiKey`)
- **Rate Limits**: None specified by provider, but application implements reasonable limits
- **Update Frequency**: ~20 seconds

### Integration Details

The application interacts with the MARTA Train API via the `train_data.py` module, which handles:

- API requests with proper authentication
- Error handling and retries
- Response parsing and data transformation
- Caching responses to disk

### Example Response

```json
[
  {
    "DESTINATION": "Hamilton E Holmes Station",
    "DIRECTION": "W",
    "EVENT_TIME": "2025-03-28T14:22:32",
    "LINE": "BLUE",
    "NEXT_ARR": "14:23:32",
    "STATION": "FIVE POINTS STATION",
    "TRAIN_ID": "104",
    "WAITING_SECONDS": "60",
    "WAITING_TIME": "1 min"
  }
]
```

### Fallback Mechanism

When the MARTA Train API is unavailable, the application:

1. Returns cached data from `TRAIN_CACHE_FILE` if available
2. Logs the failure and error details
3. Displays a user-friendly message if no data is available

## MARTA Bus GTFS-RT Feeds

### API Details

- **Provider**: MARTA
- **Documentation**: [MARTA GTFS Information](http://www.itsmarta.com/developers/data-sources/general-transit-feed-specification-gtfs.aspx)
- **Vehicle Positions URL**: `http://developer.itsmarta.com/gtfs_realtime/VehiclePositions.pb`
- **Trip Updates URL**: `http://developer.itsmarta.com/gtfs_realtime/TripUpdate.pb`
- **Format**: Protocol Buffers (GTFS-RT)
- **Authentication**: None required
- **Update Frequency**: ~30 seconds

### Integration Details

The application processes GTFS-RT data via the `bus_data.py` module, which:

- Fetches the Protocol Buffer data
- Parses it using the `gtfs-realtime-bindings` library
- Converts it to JSON for internal use
- Caches the processed data
- Extracts route and timing information

### Example Processed Data

```json
{
  "entity": [
    {
      "id": "1601",
      "vehicle": {
        "trip": {
          "tripId": "9898248",
          "routeId": "24490"
        },
        "position": {
          "latitude": 33.8855,
          "longitude": -84.2474
        },
        "vehicle": {
          "id": "1601"
        }
      }
    }
  ]
}
```

### Fallback Mechanism

When GTFS-RT feeds are unavailable:

1. The application attempts to use cached data
2. If no cache is available, it displays an appropriate message
3. The system continues to function with other available data sources

## Open-Meteo Weather API

### API Details

- **Provider**: Open-Meteo
- **Documentation**: [Open-Meteo API Docs](https://open-meteo.com/en/docs)
- **Base URL**: `https://api.open-meteo.com/v1/forecast`
- **Format**: JSON
- **Authentication**: None required (free tier)
- **Rate Limits**: 10,000 requests per day
- **Update Frequency**: Data updated hourly

### Integration Details

Weather data is handled by the `weather.py` module, which:

- Constructs appropriate queries for Atlanta weather
- Uses the `openmeteo-requests` package for optimized requests
- Processes and transforms the response into a simplified format
- Implements caching with the `requests-cache` library

### Example Response

```json
{
  "temperature": 72.5,
  "condition": "Partly Cloudy",
  "humidity": 65,
  "windSpeed": 8.3,
  "windDirection": "NE",
  "precipitationChance": 10,
  "icon": "partly-cloudy"
}
```

### Fallback Mechanism

When the weather API is unavailable:

1. The system uses cached weather data if available
2. If cached data is older than 24 hours, a generic weather message is displayed
3. Weather functionality degrades gracefully while transit data continues to function

## OpenStreetMap (Leaflet Tiles)

### API Details

- **Provider**: OpenStreetMap
- **Documentation**: [OpenStreetMap Tile Usage Policy](https://operations.osmfoundation.org/policies/tiles/)
- **Tile URL Format**: `https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png`
- **Format**: PNG tiles
- **Authentication**: None required
- **Rate Limits**: [Usage policy](https://operations.osmfoundation.org/policies/tiles/) requires reasonable use

### Integration Details

Map tiles are loaded directly by Leaflet.js in the browser:

- No server-side processing is required
- Tiles are requested directly by the client browser
- Caching is handled by the browser

### Usage Considerations

- The application follows OpenStreetMap's [Tile Usage Policy](https://operations.osmfoundation.org/policies/tiles/)
- For heavy usage, consider using a commercial tile provider
- Attribution is properly displayed on the map

## Integration Challenges and Solutions

### Challenge: API Reliability

**Solution:**
- Implement robust error handling
- Cache all API responses
- Create fallback data sources
- Use exponential backoff for retries

### Challenge: Data Format Differences

**Solution:**
- Create consistent internal data models
- Transform API responses to match expected formats
- Sanitize and validate all external data

### Challenge: Rate Limiting

**Solution:**
- Implement client-side caching
- Batch requests when possible
- Set reasonable refresh intervals
- Monitor API usage

## Monitoring and Maintenance

The application includes the following to ensure API integrations remain functional:

1. Logging of all API request successes and failures
2. Monitoring of response times
3. Validation of response formats
4. Alerts for persistent API failures