# Simple MARTA Transit Dashboard

A modular Flask application for displaying MARTA (Metropolitan Atlanta Rapid Transit Authority) bus and train data.

## Features

- Live display of MARTA train arrivals and bus positions via official MARTA APIs
- Real-time bus trip updates and arrival predictions
- Real-time Atlanta weather information via Open-Meteo API
- **Interactive MARTA train and bus maps using Leaflet**
- **Station-based filtering to show trains arriving at selected stations**
- **Train lines displayed with proper colors and real GPS coordinates**
- Visual status indicators for transit delays
- Transit system status updates

## Project Structure

```
simple_marta_app/
├── api/                # API route definitions
│   └── routes.py       # API endpoints
├── config/             # Configuration settings
│   └── config.py       # App configuration
├── static/             # Static files (CSS, images)
│   └── style.css       # Application styles
├── templates/          # HTML templates
│   └── index.html      # Main application template
├── utils/              # Utility modules
│   ├── bus_data.py     # Bus data functions
│   ├── map.py          # Map utility functions
│   ├── templates.py    # Template generators
│   ├── train_data.py   # Train data functions
│   ├── updates.py      # Service updates functions
│   └── weather.py      # Weather data functions
├── app.py              # Main application setup
├── routes.py           # Web route definitions
├── requirements.txt    # Package dependencies
└── README.md           # This file
```

## Requirements

- Python 3.7+
- Flask
- Requests
- Open-Meteo weather API packages
- Google Protobuf (for GTFS-RT bus data)
- Leaflet.js (for interactive maps)

## Installation

1. Clone this repository or download the files

2. Install required packages:
```bash
cd marta_transit_dashboard
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

## API Endpoints

- `/api/weather` - Current Atlanta weather data
- `/api/trains` - Current MARTA train data
- `/api/buses/positions` - Current MARTA bus positions
- `/api/buses/trips` - Current MARTA bus trip updates and predictions
- `/api/status` - System-wide transit status
- `/api/updates` - Recent service updates

## Interactive Maps

### Bus Map
- Shows real-time positions of MARTA buses within the Atlanta metropolitan area
- Bus markers are clickable and display route, bus ID, and position information
- Map automatically adjusts to show all currently operating buses
- Configurable bounds to focus on the greater Atlanta area

### Train Map
- Interactive map showing all MARTA train stations with their actual GPS coordinates
- Color-coded train lines (Red, Gold, Blue, Green)
- Trains appear as colored circles at their current station
- Click on stations to filter and show only trains arriving at that station
- "Show All Trains" button to clear station filters

## Data Sources

- **Weather**: Open-Meteo API for real-time Atlanta weather data
- **MARTA Train API**: Official MARTA API for real-time train data
- **Bus Positions**: MARTA GTFS-RT vehicle positions feed
- **Bus Trip Updates**: MARTA GTFS-RT trip updates feed
- **Map**: Leaflet.js with OpenStreetMap tiles for interactive mapping

## Fallback Mechanism

If the live APIs are unavailable for any reason, the application will automatically fall back to cached data. This ensures that the application can still function even when network connectivity is limited or the MARTA APIs are experiencing issues.

## Extending the Application

This modular design makes it easy to extend the application:

1. Add new API endpoints in `api/routes.py`
2. Add new utility modules in the `utils/` directory
3. Update the templates in `templates/` directory
4. Add new static assets to the `static/` directory 