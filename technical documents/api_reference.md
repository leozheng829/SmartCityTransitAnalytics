# MARTA Transit Dashboard - API Reference

## Overview

The MARTA Transit Dashboard provides a set of RESTful API endpoints that return real-time transit data in JSON format. These endpoints can be used by developers to integrate MARTA transit data into their own applications.

## Base URL

All API endpoints are relative to the base URL of your application:

```
http://localhost:5001/api
```

## Authentication

Currently, the API does not require authentication as it serves public transit information.

## API Endpoints

### Weather Data

#### GET `/api/weather`

Returns current weather data for the Atlanta area.

**Example Request:**
```
GET /api/weather
```

**Example Response:**
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

### Train Data

#### GET `/api/trains`

Returns current MARTA train data including locations, destinations, and waiting times.

**Example Request:**
```
GET /api/trains
```

**Example Response:**
```json
[
  {
    "DESTINATION": "Airport",
    "DIRECTION": "S",
    "EVENT_TIME": "2025-03-28T14:22:32",
    "LINE": "RED",
    "NEXT_ARR": "14:23:32",
    "STATION": "MIDTOWN STATION",
    "TRAIN_ID": "408",
    "WAITING_SECONDS": 60,
    "WAITING_TIME": "1 min"
  },
  {
    "DESTINATION": "North Springs",
    "DIRECTION": "N",
    "EVENT_TIME": "2025-03-28T14:21:15",
    "LINE": "RED",
    "NEXT_ARR": "14:25:15",
    "STATION": "PEACHTREE CENTER STATION",
    "TRAIN_ID": "410",
    "WAITING_SECONDS": 180,
    "WAITING_TIME": "3 min"
  }
]
```

### Bus Position Data

#### GET `/api/buses/positions`

Returns current MARTA bus positions from the GTFS-RT feed.

**Example Request:**
```
GET /api/buses/positions
```

**Example Response:**
```json
{
  "header": {
    "gtfs_realtime_version": "2.0",
    "incrementality": "FULL_DATASET",
    "timestamp": 1648215960
  },
  "entity": [
    {
      "id": "1601",
      "vehicle": {
        "trip": {
          "tripId": "9898248",
          "routeId": "24490",
          "directionId": 0
        },
        "position": {
          "latitude": 33.8855,
          "longitude": -84.2474,
          "bearing": 180
        },
        "currentStopSequence": 12,
        "currentStatus": "IN_TRANSIT_TO",
        "timestamp": 1648215900,
        "vehicle": {
          "id": "1601",
          "label": "1601"
        }
      }
    }
  ]
}
```

### Bus Trip Updates

#### GET `/api/buses/trips`

Returns current MARTA bus trip updates and arrival predictions.

**Example Request:**
```
GET /api/buses/trips
```

**Example Response:**
```json
{
  "header": {
    "gtfs_realtime_version": "2.0",
    "incrementality": "FULL_DATASET",
    "timestamp": 1648215960
  },
  "entity": [
    {
      "id": "trip-9898248",
      "tripUpdate": {
        "trip": {
          "tripId": "9898248",
          "routeId": "24490"
        },
        "stopTimeUpdate": [
          {
            "stopSequence": 13,
            "arrival": {
              "time": 1648216200,
              "delay": 60
            },
            "departure": {
              "time": 1648216260,
              "delay": 60
            },
            "stopId": "48190"
          }
        ],
        "vehicle": {
          "id": "1601",
          "label": "1601"
        },
        "timestamp": 1648215900
      }
    }
  ]
}
```

### Transit System Status

#### GET `/api/status`

Returns the overall status of the MARTA transit system.

**Example Request:**
```
GET /api/status
```

**Example Response:**
```json
{
  "busStatus": {
    "status": "Minor Delays",
    "details": "Routes 24490, 24476 experiencing delays of 5-10 minutes",
    "affectedRoutes": [
      {
        "route": "24490",
        "delay": "8 minutes"
      },
      {
        "route": "24476",
        "delay": "6 minutes"
      }
    ]
  },
  "trainStatus": {
    "status": "On Time",
    "details": "All lines operating normally",
    "affectedLines": []
  }
}
```

### Service Updates

#### GET `/api/updates`

Returns recent service updates and alerts for the MARTA system.

**Example Request:**
```
GET /api/updates
```

**Example Response:**
```json
[
  {
    "id": "update-123",
    "title": "Blue Line Maintenance",
    "description": "Blue Line trains will operate on a single track between Decatur and Avondale stations due to scheduled track maintenance.",
    "timestamp": "2025-03-28T08:15:00",
    "affectedServices": ["BLUE"],
    "severity": "INFO"
  },
  {
    "id": "update-124",
    "title": "Bus Route 24476 Detour",
    "description": "Route 24476 is on detour due to construction on Peachtree Street. Expect delays of 10-15 minutes.",
    "timestamp": "2025-03-28T07:30:00",
    "affectedServices": ["BUS-24476"],
    "severity": "WARNING"
  }
]
```

## Error Responses

When an error occurs, the API will return a JSON response with an error message:

```json
{
  "error": "Resource not found",
  "status": 404
}
```

Common error status codes:

- `400` - Bad Request: The request was malformed or invalid
- `404` - Not Found: The requested resource was not found
- `500` - Internal Server Error: An unexpected error occurred on the server

## Rate Limiting

There are currently no rate limits on the API, but clients should implement reasonable caching to reduce load on the server. APIs might return cached data that is up to 60 seconds old.

## Caching Behavior

All endpoints may return cached data to improve performance. The maximum age of cached data is:

- Weather data: 10 minutes
- Train data: 60 seconds
- Bus position data: 30 seconds
- Bus trip data: 30 seconds
- System status: 2 minutes
- Service updates: 5 minutes