from flask import Flask, render_template, jsonify
import json
import os
import requests
from datetime import datetime
import sys

# Add the Scripts directory to the path to import the weather_api module
sys.path.append('./Scripts')
try:
    import openmeteo_requests
    import requests_cache
    from retry_requests import retry
except ImportError:
    print("Warning: Some weather API dependencies are missing. Will use mock data.")

# Create weather client
try:
    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)
except Exception as e:
    print(f"Failed to setup Open-Meteo client: {e}")
    openmeteo = None

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Create templates directory if it doesn't exist
os.makedirs('templates', exist_ok=True)
os.makedirs('static', exist_ok=True)

# Get weather data using the open-meteo API
def get_weather_data():
    try:
        # If we can't use the API, fall back to cached data
        if openmeteo is None:
            return get_weather_fallback()
            
        # Atlanta coordinates
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": 33.749,
            "longitude": -84.388,
            "current": ["temperature_2m", "apparent_temperature", "precipitation", "weather_code", "relative_humidity_2m"],
            "temperature_unit": "fahrenheit",
            "timezone": "America/New_York"
        }
        
        # Make the API request
        responses = openmeteo.weather_api(url, params=params)
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
        
        return {
            'temperature': round(current_temperature),
            'condition': condition,
            'humidity': round(current_humidity),
            'feels_like': round(current_apparent_temp),
            'city': 'Atlanta'
        }
    except Exception as e:
        print(f"Error getting weather data: {e}")
        return get_weather_fallback()

def get_weather_description(weather_code):
    """Convert WMO weather code to human-readable description"""
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
    """Return mock weather data if the API is unavailable"""
    # Check if we have cached data in a file
    if os.path.exists('weather_data.json'):
        try:
            with open('weather_data.json', 'r') as f:
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
    with open('weather_data.json', 'w') as f:
        json.dump(mock_data, f)
        
    return mock_data

def get_marta_train_data():
    try:
        api_key = "3b78f59c-e96d-4085-a291-eefb29bc5ecf"  # MARTA API key
        url = f"https://developerservices.itsmarta.com:18096/itsmarta/railrealtimearrivals/developerservices/traindata"
        headers = {'accept': 'application/json'}
        params = {'apiKey': api_key}
        
        response = requests.get(url, headers=headers, params=params, verify=True)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to get train data: {response.status_code}")
            # If API call fails, try to use cached data
            if os.path.exists('train_data.json'):
                with open('train_data.json', 'r') as f:
                    return json.load(f)
    except Exception as e:
        print(f"Error fetching train data: {e}")
    
    # If all else fails, return empty array
    return []

def get_bus_positions():
    try:
        # If we have cached data, use it
        if os.path.exists('bus_positions.json'):
            with open('bus_positions.json', 'r') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error reading bus positions: {e}")
    
    # Return empty data structure if no data available
    return {"entity": []}

def get_transit_status():
    train_data = get_marta_train_data()
    
    # Default status
    train_status = {
        'status': 'On Time',
        'details': 'All lines operating normally',
        'affectedLines': []
    }
    
    # Count delays by line
    delays_by_line = {}
    for train in train_data:
        if 'DELAY' in train and train['DELAY'].startswith('T'):
            line = train['LINE']
            try:
                delay_seconds = train['DELAY'][1:-1]  # Remove 'T' prefix and 'S' suffix
                delay_value = int(delay_seconds)
                if abs(delay_value) > 300:  # More than 5 minutes
                    if line not in delays_by_line:
                        delays_by_line[line] = []
                    delays_by_line[line].append(abs(delay_value))
            except ValueError:
                pass
    
    # Check if any line has delays
    if delays_by_line:
        affected_lines = []
        details = []
        
        for line, delays in delays_by_line.items():
            avg_delay = sum(delays) / len(delays)
            minutes = round(avg_delay / 60)
            
            if minutes >= 5:
                affected_lines.append({
                    'line': line,
                    'delay': f'{minutes} minutes'
                })
                details.append(f"{line} Line: {minutes} minute delays")
        
        if affected_lines:
            if any(d['delay'].startswith(('10', '11', '12', '13', '14', '15')) for d in affected_lines):
                train_status['status'] = 'Major Delays'
            else:
                train_status['status'] = 'Minor Delays'
            
            train_status['details'] = ', '.join(details)
            train_status['affectedLines'] = affected_lines
    
    # Default bus status
    bus_status = {
        'status': 'On Time',
        'percentage': 95,
        'details': '95% of routes operating normally'
    }
    
    return {
        'busStatus': bus_status,
        'trainStatus': train_status
    }

def get_recent_updates():
    # Generate updates based on weather and train data
    updates = [
        {'type': 'on-time', 'message': 'Route 110 operating on schedule'}
    ]
    
    # Check train data for delays
    train_data = get_marta_train_data()
    for train in train_data:
        if 'DELAY' in train and train['DELAY'].startswith('T'):
            try:
                delay_seconds = int(train['DELAY'][1:-1])
                if delay_seconds > 600:  # More than 10 minutes delay
                    updates.append({
                        'type': 'disrupted',
                        'message': f"Service disruption on {train['LINE']} Line between {train['STATION']} and {train['DESTINATION']}"
                    })
                    break
            except ValueError:
                pass
    
    # Add a general delay notice if no specific disruptions found
    if not any(u['type'] == 'disrupted' for u in updates):
        updates.append({
            'type': 'delayed',
            'message': 'Minor delays expected during rush hour'
        })
    
    return updates

# Routes
@app.route('/')
def index():
    return render_template('index.html')

# API routes
@app.route('/api/weather')
def weather():
    return jsonify(get_weather_data())

@app.route('/api/trains')
def trains():
    data = get_marta_train_data()
    # Save a copy for caching
    with open('train_data.json', 'w') as f:
        json.dump(data, f)
    return jsonify(data)

@app.route('/api/buses/positions')
def buses():
    return jsonify(get_bus_positions())

@app.route('/api/status')
def status():
    return jsonify(get_transit_status())

@app.route('/api/updates')
def updates():
    return jsonify(get_recent_updates())

if __name__ == '__main__':
    # Create HTML template
    with open('templates/index.html', 'w') as f:
        f.write("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Simple MARTA Transit Dashboard</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <div class="container mt-5">
        <header class="text-center mb-5">
            <h1 class="display-4">MARTA Transit Dashboard</h1>
            <p class="lead">Real-time transit information for Atlanta</p>
            <button id="refreshBtn" class="btn btn-primary">Refresh Data</button>
        </header>

        <div class="row mb-5">
            <div class="col-md-4">
                <div class="card h-100">
                    <div class="card-body">
                        <h5 class="card-title">Weather in <span id="city">Atlanta</span></h5>
                        <h2 id="temperature">--°F</h2>
                        <p id="conditions">Loading weather data...</p>
                        <p>Feels like: <span id="feelsLike">--</span>°F</p>
                        <p>Humidity: <span id="humidity">--</span>%</p>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card h-100">
                    <div class="card-body">
                        <h5 class="card-title">Bus Status</h5>
                        <h2 id="busStatus">--</h2>
                        <p id="busDetails">Loading bus status...</p>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card h-100">
                    <div class="card-body">
                        <h5 class="card-title">Train Status</h5>
                        <h2 id="trainStatus">--</h2>
                        <p id="trainDetails">Loading train status...</p>
                    </div>
                </div>
            </div>
        </div>

        <div class="row mb-5">
            <div class="col-12">
                <div class="card">
                    <div class="card-header">
                        <h5 class="mb-0">Transit Map</h5>
                        <div class="btn-group mt-2">
                            <button class="btn btn-sm btn-outline-primary active" id="showBuses">Bus View</button>
                            <button class="btn btn-sm btn-outline-primary" id="showTrains">Train View</button>
                        </div>
                    </div>
                    <div class="card-body">
                        <div id="transitMap">
                            <div id="busView" class="simple-map">
                                <div id="busMapContent" class="text-center p-3">
                                    <h3>Bus Positions</h3>
                                    <p>Showing latest bus positions</p>
                                    <div id="busPositions" class="row"></div>
                                </div>
                            </div>
                            
                            <div id="trainView" class="simple-map" style="display:none;">
                                <div id="trainMapContent" class="text-center p-3">
                                    <h3>MARTA Train Map</h3>
                                    <p>Showing latest train positions</p>
                                    <div class="marta-map-container">
                                        <img src="{{ url_for('static', filename='marta_train_map.jpg') }}" alt="MARTA Train Map" class="img-fluid marta-map">
                                        <div id="train-indicators"></div>
                                    </div>
                                    <div id="trainPositions" class="row mt-4"></div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="row">
            <div class="col-12">
                <div class="card">
                    <div class="card-header d-flex justify-content-between align-items-center">
                        <h5 class="mb-0">Recent Updates</h5>
                        <button id="refreshUpdates" class="btn btn-sm btn-outline-primary">Refresh</button>
                    </div>
                    <div class="card-body">
                        <ul id="recentUpdates" class="list-group list-group-flush">
                            <li class="list-group-item">Loading updates...</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Map of MARTA train stations and their coordinates on the map image
        // These are estimated positions based on the map image proportion
        const stationPositions = {
            // Red Line stations (North-South)
            'NORTH SPRINGS': { top: 0, left: 48, line: 'RED' },
            'SANDY SPRINGS': { top: 8, left: 48, line: 'RED' },
            'DUNWOODY': { top: 16, left: 48, line: 'RED' },
            'MEDICAL CENTER': { top: 24, left: 48, line: 'RED' },
            'BUCKHEAD': { top: 31, left: 48, line: 'RED' },
            'LINDBERGH CENTER': { top: 39, left: 48, line: 'RED' },
            
            // Gold Line stations (North-South)
            'DORAVILLE': { top: 0, left: 62, line: 'GOLD' },
            'CHAMBLEE': { top: 8, left: 62, line: 'GOLD' },
            'BROOKHAVEN': { top: 16, left: 62, line: 'GOLD' },
            'LENOX': { top: 31, left: 58, line: 'GOLD' },
            
            // Shared Red/Gold Line stations
            'ARTS CENTER': { top: 46, left: 48, line: 'RED_GOLD' },
            'MIDTOWN': { top: 51, left: 48, line: 'RED_GOLD' },
            'NORTH AVENUE': { top: 56, left: 48, line: 'RED_GOLD' },
            'CIVIC CENTER': { top: 61, left: 48, line: 'RED_GOLD' },
            'PEACHTREE CENTER': { top: 66, left: 48, line: 'RED_GOLD' },
            'FIVE POINTS': { top: 72, left: 48, line: 'RED_GOLD_GREEN_BLUE' },
            'GARNETT': { top: 78, left: 48, line: 'RED_GOLD' },
            'WEST END': { top: 85, left: 42, line: 'RED_GOLD' },
            'OAKLAND CITY': { top: 90, left: 42, line: 'RED_GOLD' },
            'LAKEWOOD': { top: 95, left: 42, line: 'RED_GOLD' },
            'EAST POINT': { top: 100, left: 42, line: 'RED_GOLD' },
            'COLLEGE PARK': { top: 105, left: 42, line: 'RED_GOLD' },
            'AIRPORT': { top: 110, left: 42, line: 'RED_GOLD' },
            
            // Green Line stations (East-West)
            'BANKHEAD': { top: 72, left: 25, line: 'GREEN' },
            
            // Shared Green/Blue Line stations
            'ASHBY': { top: 72, left: 32, line: 'GREEN_BLUE' },
            'VINE CITY': { top: 72, left: 36, line: 'GREEN_BLUE' },
            'OMNI': { top: 72, left: 41, line: 'GREEN_BLUE' },
            'GEORGIA STATE': { top: 72, left: 55, line: 'GREEN_BLUE' },
            'KING MEMORIAL': { top: 72, left: 62, line: 'GREEN_BLUE' },
            'INMAN PARK': { top: 72, left: 69, line: 'GREEN_BLUE' },
            'EDGEWOOD': { top: 72, left: 76, line: 'GREEN_BLUE' },
            
            // Blue Line stations (East-West)
            'EAST LAKE': { top: 72, left: 83, line: 'BLUE' },
            'DECATUR': { top: 72, left: 90, line: 'BLUE' },
            'AVONDALE': { top: 72, left: 97, line: 'BLUE' },
            'KENSINGTON': { top: 72, left: 104, line: 'BLUE' },
            'INDIAN CREEK': { top: 72, left: 111, line: 'BLUE' }
        };

        // Simplified data fetching without complex libraries
        async function fetchData(endpoint) {
            try {
                const response = await fetch(`/api/${endpoint}`);
                if (!response.ok) {
                    throw new Error(`Network response was not ok: ${response.status}`);
                }
                return await response.json();
            } catch (error) {
                console.error(`Error fetching ${endpoint}:`, error);
                return null;
            }
        }

        // Update the UI with fetched data
        async function updateUI() {
            // Update weather
            const weather = await fetchData('weather');
            if (weather) {
                document.getElementById('temperature').textContent = `${weather.temperature}°F`;
                document.getElementById('conditions').textContent = weather.condition;
                document.getElementById('feelsLike').textContent = weather.feels_like;
                document.getElementById('humidity').textContent = weather.humidity;
                document.getElementById('city').textContent = weather.city;
            }

            // Update transit status
            const status = await fetchData('status');
            if (status) {
                // Bus status
                document.getElementById('busStatus').textContent = status.busStatus.status;
                document.getElementById('busDetails').textContent = status.busStatus.details;
                
                // Train status
                document.getElementById('trainStatus').textContent = status.trainStatus.status;
                document.getElementById('trainDetails').textContent = status.trainStatus.details;
                
                // Set status colors
                const busStatusEl = document.getElementById('busStatus');
                const trainStatusEl = document.getElementById('trainStatus');
                
                busStatusEl.className = '';
                trainStatusEl.className = '';
                
                if (status.busStatus.status === 'On Time') {
                    busStatusEl.classList.add('text-success');
                } else if (status.busStatus.status === 'Minor Delays') {
                    busStatusEl.classList.add('text-warning');
                } else {
                    busStatusEl.classList.add('text-danger');
                }
                
                if (status.trainStatus.status === 'On Time') {
                    trainStatusEl.classList.add('text-success');
                } else if (status.trainStatus.status === 'Minor Delays') {
                    trainStatusEl.classList.add('text-warning');
                } else {
                    trainStatusEl.classList.add('text-danger');
                }
            }

            // Update recent updates
            const updates = await fetchData('updates');
            if (updates && updates.length > 0) {
                const updatesList = document.getElementById('recentUpdates');
                updatesList.innerHTML = '';
                
                updates.forEach(update => {
                    const listItem = document.createElement('li');
                    listItem.className = 'list-group-item';
                    
                    const dot = document.createElement('span');
                    dot.className = 'status-dot';
                    
                    if (update.type === 'on-time') {
                        dot.classList.add('status-on-time');
                    } else if (update.type === 'delayed') {
                        dot.classList.add('status-delayed');
                    } else {
                        dot.classList.add('status-disrupted');
                    }
                    
                    listItem.appendChild(dot);
                    listItem.appendChild(document.createTextNode(' ' + update.message));
                    updatesList.appendChild(listItem);
                });
            }

            // Update simple transit views
            updateTransitViews();
        }

        async function updateTransitViews() {
            // Update bus positions view
            const busData = await fetchData('buses/positions');
            const busPositionsDiv = document.getElementById('busPositions');
            busPositionsDiv.innerHTML = '';
            
            if (busData && busData.entity && busData.entity.length > 0) {
                // Show up to 6 buses
                const maxBuses = Math.min(6, busData.entity.length);
                for (let i = 0; i < maxBuses; i++) {
                    const bus = busData.entity[i].vehicle;
                    if (bus && bus.position) {
                        const busCard = document.createElement('div');
                        busCard.className = 'col-md-4 mb-3';
                        busCard.innerHTML = `
                            <div class="card">
                                <div class="card-body">
                                    <h5 class="card-title">Bus ${bus.vehicle?.label || 'Unknown'}</h5>
                                    <p>Route: ${bus.trip?.routeId || 'Unknown'}</p>
                                    <p>Position: ${bus.position.latitude.toFixed(4)}, ${bus.position.longitude.toFixed(4)}</p>
                                </div>
                            </div>
                        `;
                        busPositionsDiv.appendChild(busCard);
                    }
                }
            } else {
                busPositionsDiv.innerHTML = '<p class="col-12 text-center">No bus position data available</p>';
            }

            // Update train positions view
            const trainData = await fetchData('trains');
            const trainPositionsDiv = document.getElementById('trainPositions');
            const trainIndicatorsDiv = document.getElementById('train-indicators');
            
            trainPositionsDiv.innerHTML = '';
            trainIndicatorsDiv.innerHTML = '';
            
            if (trainData && trainData.length > 0) {
                // Clear previous train indicators
                trainIndicatorsDiv.innerHTML = '';
                
                // Create train indicators on the map
                trainData.forEach(train => {
                    const station = train.STATION;
                    if (station && stationPositions[station]) {
                        // Create train indicator
                        const indicator = document.createElement('div');
                        indicator.className = 'train-indicator';
                        
                        // Set position based on the station
                        indicator.style.top = `${stationPositions[station].top}%`;
                        indicator.style.left = `${stationPositions[station].left}%`;
                        
                        // Set color based on train line
                        let colorClass = '';
                        if (train.LINE === 'RED') colorClass = 'train-red';
                        else if (train.LINE === 'GOLD') colorClass = 'train-gold';
                        else if (train.LINE === 'BLUE') colorClass = 'train-blue';
                        else if (train.LINE === 'GREEN') colorClass = 'train-green';
                        
                        indicator.classList.add(colorClass);
                        
                        // Add tooltip with train info
                        const tooltip = document.createElement('div');
                        tooltip.className = 'train-tooltip';
                        tooltip.innerHTML = `
                            <strong>Train ${train.TRAIN_ID}</strong><br>
                            ${train.LINE} Line<br>
                            Next: ${train.STATION}<br>
                            To: ${train.DESTINATION}<br>
                            Arriving: ${train.WAITING_TIME}
                        `;
                        
                        indicator.appendChild(tooltip);
                        trainIndicatorsDiv.appendChild(indicator);
                    }
                });
                
                // Show up to 6 trains in the cards below the map
                const maxTrains = Math.min(6, trainData.length);
                for (let i = 0; i < maxTrains; i++) {
                    const train = trainData[i];
                    if (train) {
                        const trainCard = document.createElement('div');
                        trainCard.className = 'col-md-4 mb-3';
                        
                        // Determine line color class
                        let colorClass = 'bg-secondary';
                        if (train.LINE === 'RED') colorClass = 'bg-danger';
                        if (train.LINE === 'GOLD') colorClass = 'bg-warning';
                        if (train.LINE === 'BLUE') colorClass = 'bg-primary';
                        if (train.LINE === 'GREEN') colorClass = 'bg-success';
                        
                        trainCard.innerHTML = `
                            <div class="card">
                                <div class="card-header ${colorClass} text-white">
                                    ${train.LINE} Line
                                </div>
                                <div class="card-body">
                                    <h5 class="card-title">Train ${train.TRAIN_ID}</h5>
                                    <p>Next station: ${train.STATION}</p>
                                    <p>Arrival: ${train.WAITING_TIME}</p>
                                    <p>Destination: ${train.DESTINATION}</p>
                                </div>
                            </div>
                        `;
                        trainPositionsDiv.appendChild(trainCard);
                    }
                }
            } else {
                trainPositionsDiv.innerHTML = '<p class="col-12 text-center">No train data available</p>';
            }
        }

        // Toggle between bus and train views
        document.getElementById('showBuses').addEventListener('click', function() {
            document.getElementById('busView').style.display = 'block';
            document.getElementById('trainView').style.display = 'none';
            document.getElementById('showBuses').classList.add('active');
            document.getElementById('showTrains').classList.remove('active');
        });

        document.getElementById('showTrains').addEventListener('click', function() {
            document.getElementById('busView').style.display = 'none';
            document.getElementById('trainView').style.display = 'block';
            document.getElementById('showBuses').classList.remove('active');
            document.getElementById('showTrains').classList.add('active');
        });

        // Handle refresh buttons
        document.getElementById('refreshBtn').addEventListener('click', updateUI);
        document.getElementById('refreshUpdates').addEventListener('click', async function() {
            const updates = await fetchData('updates');
            if (updates && updates.length > 0) {
                const updatesList = document.getElementById('recentUpdates');
                updatesList.innerHTML = '';
                
                updates.forEach(update => {
                    const listItem = document.createElement('li');
                    listItem.className = 'list-group-item';
                    
                    const dot = document.createElement('span');
                    dot.className = 'status-dot';
                    
                    if (update.type === 'on-time') {
                        dot.classList.add('status-on-time');
                    } else if (update.type === 'delayed') {
                        dot.classList.add('status-delayed');
                    } else {
                        dot.classList.add('status-disrupted');
                    }
                    
                    listItem.appendChild(dot);
                    listItem.appendChild(document.createTextNode(' ' + update.message));
                    updatesList.appendChild(listItem);
                });
            }
        });

        // Initial data load
        updateUI();
        
        // Refresh data every 30 seconds
        setInterval(updateUI, 30000);
    </script>
</body>
</html>
        """)

    # Create CSS file
    with open('static/style.css', 'w') as f:
        f.write("""
body {
    background-color: #f8f9fa;
}

.card {
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    transition: transform 0.2s;
}

.card:hover {
    transform: translateY(-5px);
}

.simple-map {
    background-color: #eee;
    border-radius: 8px;
    overflow: hidden;
    padding: 15px;
}

.marta-map-container {
    position: relative;
    width: 100%;
    max-width: 800px;
    margin: 0 auto;
}

.marta-map {
    width: 100%;
    border-radius: 8px;
    border: 1px solid #ddd;
}

.train-indicator {
    position: absolute;
    width: 15px;
    height: 15px;
    border-radius: 50%;
    background-color: #333;
    transform: translate(-50%, -50%);
    z-index: 10;
    cursor: pointer;
}

.train-indicator:hover .train-tooltip {
    display: block;
}

.train-tooltip {
    display: none;
    position: absolute;
    bottom: 100%;
    left: 50%;
    transform: translateX(-50%);
    background-color: rgba(0, 0, 0, 0.8);
    color: white;
    padding: 5px 10px;
    border-radius: 4px;
    font-size: 12px;
    white-space: nowrap;
    z-index: 100;
    min-width: 150px;
}

.train-red {
    background-color: #e51636;
    box-shadow: 0 0 5px #e51636;
}

.train-gold {
    background-color: #f9a825;
    box-shadow: 0 0 5px #f9a825;
}

.train-blue {
    background-color: #0d47a1;
    box-shadow: 0 0 5px #0d47a1;
}

.train-green {
    background-color: #388e3c;
    box-shadow: 0 0 5px #388e3c;
}

.status-dot {
    display: inline-block;
    width: 10px;
    height: 10px;
    border-radius: 50%;
    margin-right: 5px;
}

.status-on-time {
    background-color: #28a745;
}

.status-delayed {
    background-color: #ffc107;
}

.status-disrupted {
    background-color: #dc3545;
}

#temperature, #busStatus, #trainStatus {
    font-size: 2rem;
    font-weight: bold;
}

.text-success {
    color: #28a745 !important;
}

.text-warning {
    color: #ffc107 !important;
}

.text-danger {
    color: #dc3545 !important;
}
        """)

    # Download the MARTA map image
    import urllib.request
    os.makedirs('static', exist_ok=True)
    try:
        print("Downloading MARTA train map...")
        # Using a URL for the MARTA map from the internet
        urllib.request.urlretrieve("https://www.itsmarta.com/images/train-stations-map.jpg", "static/marta_train_map.jpg")
        print("MARTA train map downloaded successfully.")
    except Exception as e:
        print(f"Error downloading MARTA map: {e}")
        # If download fails, create a placeholder image
        with open("static/marta_train_map.jpg", "wb") as f:
            f.write(b"")
        print("Created placeholder for MARTA map. Please add a map image manually.")

    print("Starting the simple MARTA transit app...")
    app.run(debug=True, port=5000) 