# MARTA Transit Dashboard - System Architecture

## Overview

The MARTA Transit Dashboard is a Flask-based web application that provides real-time information about the Metropolitan Atlanta Rapid Transit Authority (MARTA) bus and train services. The application integrates with MARTA's public APIs and other third-party services to display transit information in an accessible and user-friendly interface.

## System Components

```
┌───────────────────┐     ┌───────────────────┐     ┌───────────────────┐
│                   │     │                   │     │                   │
│  Client Browser   │◄────┤  Flask Web App    │◄────┤  Data Services    │
│                   │     │                   │     │                   │
└───────────────────┘     └───────────────────┘     └───────────────────┘
```

### 1. Client Layer

The client layer consists of the user's web browser which renders the HTML, CSS, and JavaScript content. Key components include:

- **Interactive Maps**: Implemented using Leaflet.js to show bus and train positions
- **Status Cards**: Display bus and train system status
- **Weather Information**: Shows current Atlanta weather
- **Data Refresh**: Periodic AJAX calls to update data without page reloads

### 2. Application Layer

The application layer is built on the Flask framework with the following components:

- **Web Routes**: Serve HTML templates and handle user requests
- **API Routes**: Provide JSON endpoints for real-time data
- **Template Engine**: Renders HTML templates with dynamic data
- **Static Assets**: Serves CSS, JavaScript, and other static resources

### 3. Data Service Layer

The data service layer handles data acquisition, processing, and caching:

- **External API Integration**: Communicates with MARTA's APIs and other services
- **Data Processing**: Transforms raw API data into usable formats
- **Caching System**: Stores API responses for reliability and performance
- **Fallback Mechanisms**: Provides cached data when live APIs are unavailable

## Data Flow

1. **Data Acquisition**:
   - Application periodically fetches data from MARTA APIs and weather services
   - Raw data is processed and stored in the cache

2. **Data Serving**:
   - Client requests are handled by Flask routes
   - Application retrieves processed data from cache or live APIs
   - Data is formatted as JSON and sent to the client

3. **Client Rendering**:
   - JavaScript code parses JSON responses
   - Maps, cards, and status indicators are updated with new data
   - UI is refreshed without reloading the page

## Integration Points

- **MARTA Train API**: Real-time train arrival information
- **MARTA GTFS-RT Feeds**: Real-time bus positions and trip updates
- **Weather API**: Current weather conditions for Atlanta
- **OpenStreetMap**: Map tiles for Leaflet.js

## Reliability Features

- **Caching**: All API responses are cached to disk
- **Fallback Data**: System falls back to cached data when APIs are unavailable
- **Error Handling**: Graceful handling of API failures

## Performance Considerations

- **Client-Side Rendering**: Minimizes server load for UI updates
- **Selective Map Loading**: Maps are only initialized when viewed
- **Filtered Data**: Only relevant data is sent to the client