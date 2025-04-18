# MARTA Transit Dashboard

A modular Flask application for displaying MARTA (Metropolitan Atlanta Rapid Transit Authority) bus and train data.

## Features

- Live display of MARTA train arrivals and bus positions
- Real-time Atlanta weather information
- Interactive maps for trains and buses using Leaflet
- Station-based filtering and status indicators
- Reliable fallback mechanism using cached data

## Requirements

- Python 3.7+
- Flask
- Requests

## Installation

1. Clone this repository or download the files

2. Install required packages:
```bash
cd simple_marta_app
pip install -r requirements.txt
```

3. Run the application:
```bash
python ../run.py
```

4. Open your browser and navigate to:
```
http://localhost:5000
```

## Documentation

For detailed information about the application, please refer to the `Technical Documents` folder which contains:

- **System Architecture** - Overview of the system components and layers
- **API Reference** - Complete list of available endpoints
- **Map Implementation** - Details on the interactive maps
- **Data Flow Diagram** - How data moves through the system
- **Installation Guide** - Comprehensive setup instructions
- **Configuration Guide** - Available configuration options
- **External APIs** - Information about integrated third-party services
- **Real-Time Data Processing** - How data is acquired and processed

## Data Sources

The application uses MARTA's Train API, Bus GTFS-RT feeds, and Open-Meteo for weather data, with automatic fallback to cached data when needed.

## Extending the Application

This modular design makes it easy to extend. See the `Technical Documents` for guidance on adding new features or modifying existing ones. 