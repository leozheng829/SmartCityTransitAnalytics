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

The client layer consists of the user's web browser which renders the HTML, CSS, and JavaScript content served by the Flask application. Key components include:

- **HTML Structure**: Defined by `templates/base.html` and populated by partials like `_status_cards.html`, `_transit_map.html`, etc., rendered via Jinja2.
- **Styling**: Handled by `static/css/style.css`.
- **Client-Side Logic**: Contained within `static/js/dashboard.js`.
  - **Interactive Maps**: Implemented using Leaflet.js (loaded via CDN) to show bus and train positions.
  - **Data Fetching & Display**: Periodic AJAX calls (`fetchData` function) to the application's API endpoints to retrieve JSON data.
  - **UI Updates**: Dynamically updates HTML elements (status cards, maps, update lists) based on fetched data.

### 2. Application Layer

The application layer is built on the Flask framework (`app.py`, `routes.py`, `api/routes.py`) with the following components:

- **Web Routes (`routes.py`)**: Defines the main route (`/`) that renders the primary HTML page using Jinja2 templates (`base.html`, `index.html`, partials).
- **API Routes (`api/routes.py`)**: Provides JSON endpoints (e.g., `/api/weather`, `/api/trains`) accessed by the client-side JavaScript to fetch real-time data.
- **Template Engine (Jinja2)**: Renders HTML templates, enabling modular design with base layouts and partials.
- **Static Asset Serving**: Serves static files like CSS (`static/css/style.css`) and JavaScript (`static/js/dashboard.js`).
- **Configuration (`config/config.py`)**: Manages application settings like API URLs and cache paths.

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