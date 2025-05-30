"""
Template utilities for the Simple MARTA App
"""

import os
import sys

# Add parent directory to import path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.config import TEMPLATES_DIR, STATIC_DIR

def create_index_template():
    """
    Create the index.html template file
    """
    template_path = os.path.join(TEMPLATES_DIR, 'index.html')
    
    # If the template already exists, don't overwrite it
    if os.path.exists(template_path):
        print(f"Template already exists at {template_path}")
        return
        
    os.makedirs(TEMPLATES_DIR, exist_ok=True)
    
    with open(template_path, 'w') as f:
        f.write("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Simple MARTA Transit Dashboard</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
    <!-- Leaflet CSS for maps -->
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
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
                                    
                                    <!-- Bus Map Container -->
                                    <div class="marta-map-container mb-4">
                                        <div id="busPositionsMap" class="map-container"></div>
                                    </div>
                                    
                                    <h4 class="mt-4">Bus Details</h4>
                                    <div id="busPositions" class="row"></div>
                                    
                                    <h4 class="mt-4">Recent Trip Updates</h4>
                                    <div id="busTripUpdates" class="row"></div>
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

    <!-- Leaflet JS for maps -->
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    
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

        // Create the bus map using Leaflet
        const busMap = L.map('busPositionsMap').setView([33.749, -84.388], 11);
        let busMarkers = [];
        
        // Add OpenStreetMap tile layer
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(busMap);

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
            
            // Clear previous bus markers from the map
            busMarkers.forEach(marker => busMap.removeLayer(marker));
            busMarkers = [];
            
            if (busData && busData.entity && busData.entity.length > 0) {
                // Show all buses on the map
                busData.entity.forEach(entity => {
                    const bus = entity.vehicle;
                    if (bus && bus.position) {
                        // Create a marker for the bus
                        const routeId = bus.trip?.routeId || 'Unknown';
                        const busLabel = bus.vehicle?.label || 'Unknown';
                        
                        const marker = L.marker([bus.position.latitude, bus.position.longitude]);
                        marker.bindPopup(`
                            <strong>Bus ${busLabel}</strong><br>
                            Route: ${routeId}<br>
                            Position: ${bus.position.latitude.toFixed(4)}, ${bus.position.longitude.toFixed(4)}
                        `);
                        marker.addTo(busMap);
                        busMarkers.push(marker);
                    }
                });
                
                // If we have buses on the map, adjust the view to show all of them
                if (busMarkers.length > 0) {
                    const group = new L.featureGroup(busMarkers);
                    busMap.fitBounds(group.getBounds().pad(0.1));
                }
                
                // Show up to 6 buses in detail cards
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
            
            // Add bus trip updates
            const tripData = await fetchData('buses/trips');
            const busTripUpdatesDiv = document.getElementById('busTripUpdates');
            busTripUpdatesDiv.innerHTML = '';
            
            if (tripData && tripData.entity && tripData.entity.length > 0) {
                // Show up to 6 trip updates
                const maxTrips = Math.min(6, tripData.entity.length);
                for (let i = 0; i < maxTrips; i++) {
                    const trip = tripData.entity[i].tripUpdate;
                    if (trip) {
                        const tripCard = document.createElement('div');
                        tripCard.className = 'col-md-4 mb-3';
                        
                        // Get the next stop if available
                        let nextStopInfo = 'No stop information';
                        if (trip.stopTimeUpdate && trip.stopTimeUpdate.length > 0) {
                            const nextStop = trip.stopTimeUpdate[0];
                            const delay = nextStop.departure?.delay || nextStop.arrival?.delay || 0;
                            const delayMinutes = Math.abs(Math.round(delay / 60));
                            const delayText = delay > 0 
                                ? `<span class="badge bg-warning">${delayMinutes}m late</span>` 
                                : delay < 0 
                                    ? `<span class="badge bg-info">${delayMinutes}m early</span>`
                                    : `<span class="badge bg-success">On time</span>`;
                            
                            nextStopInfo = `
                                <p>Next stop: ${nextStop.stopId || 'Unknown'}</p>
                                <p>Status: ${delayText}</p>
                            `;
                        }
                        
                        tripCard.innerHTML = `
                            <div class="card">
                                <div class="card-body">
                                    <h5 class="card-title">Route ${trip.trip?.routeId || 'Unknown'}</h5>
                                    <p>Trip ID: ${trip.trip?.tripId || 'Unknown'}</p>
                                    ${nextStopInfo}
                                </div>
                            </div>
                        `;
                        busTripUpdatesDiv.appendChild(tripCard);
                    }
                }
            } else {
                busTripUpdatesDiv.innerHTML = '<p class="col-12 text-center">No trip update data available</p>';
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
            // Resize map after showing it (needed for proper rendering)
            busMap.invalidateSize();
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
    
    print(f"Created index.html template at {template_path}")

def create_css_template():
    """
    Create the CSS template file
    """
    css_path = os.path.join(STATIC_DIR, 'style.css')
    os.makedirs(STATIC_DIR, exist_ok=True)
    
    with open(css_path, 'w') as f:
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

/* Bus map styles */
.map-container {
    height: 400px;
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
    
    print(f"Created style.css template at {css_path}") 