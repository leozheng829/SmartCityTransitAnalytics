# Smart City Transit Analytics

Real-time transit information with integrated weather data for smarter urban mobility.

![Smart City Transit Analytics](screenshot.png)

## Overview

This application provides real-time transit analytics by combining:
- Live bus and train position tracking
- Weather data integration
- Delay predictions and notifications
- Interactive maps
- Transit status dashboards

## Project Structure

- `/Scripts` - Backend Python scripts for data collection and API
- `/Collected Data` - Storage for historical transit and weather data
- `/sample-frontend` - React frontend application

## Setup and Running

### Backend Setup

1. Install Python dependencies:
   ```
   cd Scripts
   pip install -r requirements.txt
   ```

2. Start the API server:
   ```
   cd Scripts
   python api_server.py
   ```

The server will run on http://localhost:5000 and provide the following endpoints:
- `/api/weather` - Current weather data
- `/api/buses/positions` - Current bus positions
- `/api/buses/trips` - Bus trip updates
- `/api/trains` - Current train data
- `/api/status` - System-wide transit status
- `/api/updates` - Recent service updates

### Frontend Setup

1. Install Node.js dependencies:
   ```
   cd sample-frontend
   npm install
   ```

2. Start the development server:
   ```
   cd sample-frontend
   npm run dev
   ```

The frontend will be available at http://localhost:5173

## Features

- **Real-time Transit Map**: View live positions of buses and trains
- **Weather Integration**: Current weather conditions and their impact on transit
- **Status Cards**: At-a-glance system status for buses and trains
- **Delay Reporting**: Real-time delay information by route/line
- **Recent Updates**: Latest service updates and alerts

## Data Sources

- MARTA GTFS-RT feeds for bus positions and trip updates
- MARTA Rail API for train positions and statuses
- OpenWeatherMap API for current weather conditions

## Technologies Used

### Backend
- Python
- Flask
- GTFS Realtime
- Pandas/NumPy (for data processing)

### Frontend
- React
- TypeScript
- Tailwind CSS
- Mapbox GL
- Shadcn UI
- Vite

# Simple MARTA Transit Dashboard

A lightweight Flask application for displaying MARTA (Metropolitan Atlanta Rapid Transit Authority) bus and train data.

## Features

- Live display of MARTA train arrivals and bus positions
- Real-time Atlanta weather information via Open-Meteo API
- Interactive MARTA train map with train position indicators
- Visual status indicators for transit delays
- Transit system status updates
- No Mapbox dependency - uses a static map image

## Requirements

- Python 3.7+
- Flask
- Requests
- Open-Meteo weather API packages
- Pillow (for map image processing)

## Installation

1. Clone this repository or download the files

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Download sample data and the MARTA train map:
```bash
python download_sample_data.py
python download_marta_map.py
```

4. Run the application:
```bash
python simple_marta_app.py
```

5. Open your browser and navigate to:
```
http://localhost:5000
```

## How It Works

This application provides a simple interface for viewing MARTA transit data:

- **Weather Data**: Uses Open-Meteo API to fetch current Atlanta weather conditions
- **MARTA Train Map**: Displays a static MARTA rail map with interactive train position indicators
- **Train Data**: Shows real-time MARTA train positions, arrivals, and status information
- **Bus Data**: Displays MARTA bus positions and route information
- **Status Updates**: Provides system-wide status updates and service notifications

The application has both a bus view and train view, which can be toggled using the buttons in the interface.

## Data Sources

- **Weather**: Open-Meteo API for real-time Atlanta weather data
- **MARTA Train API**: Official MARTA API for real-time train data
- **Bus data**: Uses cached data or mock data when the real-time feed is not available
- **Map**: Static MARTA system map with dynamically positioned train indicators

## Features Added

- Dynamic train position indicators on the MARTA map
- Weather data now uses the Open-Meteo API for real-time conditions
- Interactive tooltips for train information
- Color-coded train lines matching MARTA's official colors
- Line-specific status indicators
- Responsive design that works on different screen sizes

## Notes

This application is designed for demonstration purposes to test frontend/backend integration. For production use, you would want to add error handling, authentication, and more robust data management.
