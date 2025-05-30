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
const busMap = L.map('busPositionsMap', {
    minZoom: 9,
    maxZoom: 14
}).setView([33.749, -84.388], 10);
let busMarkers = [];

// Add OpenStreetMap tile layer
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(busMap);

// Set bounds for Atlanta metro area
const atlantaBounds = L.latLngBounds(
    L.latLng(33.400, -84.950), // Southwest corner - expanded
    L.latLng(34.200, -83.900)  // Northeast corner - expanded
);
busMap.setMaxBounds(atlantaBounds.pad(0.1));

// Create train map using Leaflet
const trainMap = L.map('trainPositionsMap', {
    minZoom: 10,
    maxZoom: 14
}).setView([33.749, -84.388], 11);
let trainStationMarkers = {};
let trainMarkers = [];
let allTrainData = []; // Store all train data for filtering
let activeStationFilter = null; // Track active station filter

// Add OpenStreetMap tile layer to train map
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(trainMap);

// Train map also uses Atlanta bounds
trainMap.setMaxBounds(atlantaBounds.pad(0.1));

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

// MARTA train station coordinates (actual GPS coordinates)
const trainStations = {
    // Red Line stations (North-South)
    'NORTH SPRINGS': { lat: 33.9455, lng: -84.3561, lines: ['RED'] },
    'SANDY SPRINGS': { lat: 33.9321, lng: -84.3513, lines: ['RED'] },
    'DUNWOODY': { lat: 33.9212, lng: -84.3437, lines: ['RED'] },
    'MEDICAL CENTER': { lat: 33.9103, lng: -84.3515, lines: ['RED'] },
    'BUCKHEAD': { lat: 33.8465, lng: -84.3671, lines: ['RED'] },
    
    // Gold Line stations (North-South)
    'DORAVILLE': { lat: 33.9028, lng: -84.2799, lines: ['GOLD'] },
    'CHAMBLEE': { lat: 33.8879, lng: -84.3062, lines: ['GOLD'] },
    'BROOKHAVEN': { lat: 33.8600, lng: -84.3390, lines: ['GOLD'] },
    'LENOX': { lat: 33.8465, lng: -84.3566, lines: ['GOLD'] },
    
    // Shared stations for Red and Gold
    'LINDBERGH CENTER': { lat: 33.8231, lng: -84.3692, lines: ['RED', 'GOLD'] },
    'ARTS CENTER': { lat: 33.7893, lng: -84.3871, lines: ['RED', 'GOLD'] },
    'MIDTOWN': { lat: 33.7812, lng: -84.3862, lines: ['RED', 'GOLD'] },
    'NORTH AVENUE': { lat: 33.7712, lng: -84.3869, lines: ['RED', 'GOLD'] },
    'CIVIC CENTER': { lat: 33.7663, lng: -84.3872, lines: ['RED', 'GOLD'] },
    'PEACHTREE CENTER': { lat: 33.7590, lng: -84.3876, lines: ['RED', 'GOLD'] },
    'FIVE POINTS': { lat: 33.7542, lng: -84.3919, lines: ['RED', 'GOLD', 'GREEN', 'BLUE'] },
    'GARNETT': { lat: 33.7480, lng: -84.3952, lines: ['RED', 'GOLD'] },
    'WEST END': { lat: 33.7352, lng: -84.4132, lines: ['RED', 'GOLD'] },
    'OAKLAND CITY': { lat: 33.7163, lng: -84.4255, lines: ['RED', 'GOLD'] },
    'LAKEWOOD': { lat: 33.7002, lng: -84.4297, lines: ['RED', 'GOLD'] },
    'EAST POINT': { lat: 33.6768, lng: -84.4408, lines: ['RED', 'GOLD'] },
    'COLLEGE PARK': { lat: 33.6513, lng: -84.4488, lines: ['RED', 'GOLD'] },
    'AIRPORT': { lat: 33.6407, lng: -84.4444, lines: ['RED', 'GOLD'] },
    
    // Green Line stations (East-West)
    'BANKHEAD': { lat: 33.7723, lng: -84.4289, lines: ['GREEN'] },
    
    // Blue Line stations (East-West)
    'INDIAN CREEK': { lat: 33.7699, lng: -84.2291, lines: ['BLUE'] },
    'KENSINGTON': { lat: 33.7720, lng: -84.2499, lines: ['BLUE'] },
    'AVONDALE': { lat: 33.7753, lng: -84.2808, lines: ['BLUE'] },
    'DECATUR': { lat: 33.7748, lng: -84.2952, lines: ['BLUE'] },
    'EAST LAKE': { lat: 33.7650, lng: -84.3121, lines: ['BLUE'] },
    
    // Shared Green and Blue Line stations (East-West)
    'INMAN PARK': { lat: 33.7570, lng: -84.3524, lines: ['GREEN', 'BLUE'] },
    'KING MEMORIAL': { lat: 33.7501, lng: -84.3755, lines: ['GREEN', 'BLUE'] },
    'GEORGIA STATE': { lat: 33.7502, lng: -84.3863, lines: ['GREEN', 'BLUE'] },
    'OMNI': { lat: 33.7592, lng: -84.3977, lines: ['GREEN', 'BLUE'] },
    'VINE CITY': { lat: 33.7563, lng: -84.4044, lines: ['GREEN', 'BLUE'] },
    'ASHBY': { lat: 33.7562, lng: -84.4170, lines: ['GREEN', 'BLUE'] }
};

// Map of alternative names for each station (common variations)
const stationAliases = {
    'AIRPORT': ['AIRPORT STATION', 'HARTSFIELD', 'HARTSFIELD-JACKSON', 'HARTSFIELD JACKSON', 'ATL AIRPORT'],
    'ARTS CENTER': ['ARTS CENTER STATION', 'WOODRUFF ARTS CENTER'],
    'BROOKHAVEN': ['BROOKHAVEN STATION', 'BROOKHAVEN/OGLETHORPE', 'OGLETHORPE'],
    'CIVIC CENTER': ['CIVIC CENTER STATION'],
    'COLLEGE PARK': ['COLLEGE PARK STATION'],
    'DECATUR': ['DECATUR STATION'],
    'DORAVILLE': ['DORAVILLE STATION'],
    'EAST LAKE': ['EAST LAKE STATION'],
    'EAST POINT': ['EAST POINT STATION'],
    'FIVE POINTS': ['FIVE POINTS STATION'],
    'GARNETT': ['GARNETT STATION'],
    'GEORGIA STATE': ['GEORGIA STATE STATION', 'GSU'],
    'INDIAN CREEK': ['INDIAN CREEK STATION'],
    'INMAN PARK': ['INMAN PARK STATION', 'INMAN PARK/REYNOLDSTOWN', 'REYNOLDSTOWN'],
    'KENSINGTON': ['KENSINGTON STATION'],
    'KING MEMORIAL': ['KING MEMORIAL STATION', 'MLK'],
    'LAKEWOOD': ['LAKEWOOD STATION', 'LAKEWOOD/FT. MCPHERSON', 'FORT MCPHERSON'],
    'LENOX': ['LENOX STATION', 'LENOX SQUARE'],
    'LINDBERGH CENTER': ['LINDBERGH STATION', 'LINDBERGH CENTER STATION'],
    'MEDICAL CENTER': ['MEDICAL CENTER STATION'],
    'MIDTOWN': ['MIDTOWN STATION'],
    'NORTH AVENUE': ['NORTH AVENUE STATION', 'NORTH AVE'],
    'NORTH SPRINGS': ['NORTH SPRINGS STATION'],
    'OAKLAND CITY': ['OAKLAND CITY STATION'],
    'OMNI': ['OMNI STATION', 'CNN', 'CNN CENTER', 'STATE FARM ARENA', 'MERCEDES-BENZ STADIUM'],
    'PEACHTREE CENTER': ['PEACHTREE CENTER STATION', 'PEACHTREE CTR'],
    'SANDY SPRINGS': ['SANDY SPRINGS STATION'],
    'VINE CITY': ['VINE CITY STATION'],
    'WEST END': ['WEST END STATION']
};

// Function to check if a destination matches a station name
function matchesStationName(destination, stationName) {
    if (!destination || !stationName) return false;
    
    destination = destination.toUpperCase().trim();
    stationName = stationName.toUpperCase().trim();
    
    // Direct match
    if (destination.includes(stationName)) return true;
    
    // Remove "STATION" suffix for comparison
    if (destination.includes(stationName.replace(' STATION', ''))) return true;
    
    // Check aliases
    const aliases = stationAliases[stationName] || [];
    return aliases.some(alias => destination.includes(alias));
}

// Line colors
const lineColors = {
    'RED': '#CE0E2D',
    'GOLD': '#FFA500',
    'BLUE': '#0000FF',
    'GREEN': '#008000'
};

// Initialize the train map with stations and route lines
function initializeTrainMap() {
    // First add route lines
    addTrainRouteLines();
    
    // Then add station markers
    for (const [stationName, stationData] of Object.entries(trainStations)) {
        // Create marker for the station
        const marker = L.circleMarker([stationData.lat, stationData.lng], {
            radius: 6,
            fillColor: '#FFFFFF',
            color: '#000000',
            weight: 2,
            opacity: 1,
            fillOpacity: 1
        });
        
        // Add tooltip with station name
        marker.bindTooltip(stationName, {
            permanent: false,
            direction: 'top'
        });
        
        // Add click handler to filter trains by destination
        marker.on('click', function() {
            filterTrainsByDestination(stationName);
        });
        
        marker.addTo(trainMap);
        trainStationMarkers[stationName] = marker;
    }
    
    // Add reset filter button to the map
    const resetFilterControl = L.control({ position: 'topright' });
    resetFilterControl.onAdd = function() {
        const div = L.DomUtil.create('div', 'reset-filter-control');
        div.innerHTML = '<button class="btn btn-sm btn-secondary" id="resetTrainFilter">Show All Trains</button>';
        return div;
    };
    resetFilterControl.addTo(trainMap);
    
    // Add event listener to the reset button
    setTimeout(() => {
        document.getElementById('resetTrainFilter')?.addEventListener('click', function(e) {
            e.stopPropagation(); // Prevent the map from receiving the click
            resetTrainFilter();
        });
    }, 100);
}

// Add train route lines to the map
function addTrainRouteLines() {
    // Red Line (North Springs to Airport)
    const redLineStations = [
        'NORTH SPRINGS', 'SANDY SPRINGS', 'DUNWOODY', 'MEDICAL CENTER', 'BUCKHEAD', 
        'LINDBERGH CENTER', 'ARTS CENTER', 'MIDTOWN', 'NORTH AVENUE', 'CIVIC CENTER', 
        'PEACHTREE CENTER', 'FIVE POINTS', 'GARNETT', 'WEST END', 'OAKLAND CITY', 
        'LAKEWOOD', 'EAST POINT', 'COLLEGE PARK', 'AIRPORT'
    ];
    
    // Gold Line (Doraville to Airport)
    const goldLineStations = [
        'DORAVILLE', 'CHAMBLEE', 'BROOKHAVEN', 'LENOX', 'LINDBERGH CENTER', 
        'ARTS CENTER', 'MIDTOWN', 'NORTH AVENUE', 'CIVIC CENTER', 'PEACHTREE CENTER', 
        'FIVE POINTS', 'GARNETT', 'WEST END', 'OAKLAND CITY', 'LAKEWOOD', 'EAST POINT', 
        'COLLEGE PARK', 'AIRPORT'
    ];
    
    // Green Line (Bankhead to Edgewood-Candler Park)
    const greenLineStations = [
        'BANKHEAD', 'ASHBY', 'VINE CITY', 'OMNI', 'FIVE POINTS', 'GEORGIA STATE', 
        'KING MEMORIAL', 'INMAN PARK'
    ];
    
    // Blue Line (Indian Creek to Hamilton E. Holmes)
    const blueLineStations = [
        'INDIAN CREEK', 'KENSINGTON', 'AVONDALE', 'DECATUR', 'EAST LAKE', 'INMAN PARK', 
        'KING MEMORIAL', 'GEORGIA STATE', 'FIVE POINTS', 'OMNI', 'VINE CITY', 'ASHBY'
    ];
    
    drawRouteLine(redLineStations, lineColors.RED, 5);
    drawRouteLine(goldLineStations, lineColors.GOLD, 5);
    drawRouteLine(greenLineStations, lineColors.GREEN, 5);
    drawRouteLine(blueLineStations, lineColors.BLUE, 5);
}

// Draw a train route line on the map
function drawRouteLine(stationNames, color, weight) {
    const coordinates = stationNames.map(name => {
        if (trainStations[name]) {
            return [trainStations[name].lat, trainStations[name].lng];
        }
        return null;
    }).filter(coord => coord !== null);
    
    if (coordinates.length >= 2) {
        const polyline = L.polyline(coordinates, {
            color: color,
            weight: weight,
            opacity: 0.7
        });
        
        polyline.addTo(trainMap);
    }
}

// Custom icon for trains based on line color
function createTrainIcon(line) {
    const color = lineColors[line] || '#999999';
    
    return L.divIcon({
        className: 'train-icon',
        html: `<div style="background-color: ${color}; width: 14px; height: 14px; border-radius: 50%; border: 2px solid white;"></div>`,
        iconSize: [14, 14],
        iconAnchor: [7, 7]
    });
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
                // Only create markers for buses within Atlanta bounds
                const busLatLng = L.latLng(bus.position.latitude, bus.position.longitude);
                if (atlantaBounds.contains(busLatLng)) {
                    // Create a marker for the bus
                    const routeId = bus.trip?.routeId || 'Unknown';
                    const busLabel = bus.vehicle?.label || 'Unknown';
                    
                    const marker = L.marker(busLatLng);
                    marker.bindPopup(`
                        <strong>Bus ${busLabel}</strong><br>
                        Route: ${routeId}<br>
                        Position: ${bus.position.latitude.toFixed(4)}, ${bus.position.longitude.toFixed(4)}
                    `);
                    marker.addTo(busMap);
                    busMarkers.push(marker);
                }
            }
        });
        
        // If we have buses on the map, adjust the view to show all of them
        if (busMarkers.length > 0) {
            // Create a feature group for buses within Atlanta bounds
            const validMarkers = busMarkers.filter(marker => {
                const latlng = marker.getLatLng();
                return atlantaBounds.contains(latlng);
            });
            
            if (validMarkers.length > 0) {
                const group = new L.featureGroup(validMarkers);
                busMap.fitBounds(group.getBounds().pad(0.1));
            } else {
                // If no valid markers, reset to Atlanta center
                busMap.setView([33.749, -84.388], 10);
            }
        }
        
        // Show up to 6 buses in detail cards
        const maxBuses = Math.min(6, busData.entity.length);
        let busesShown = 0;
        
        for (let i = 0; i < busData.entity.length && busesShown < maxBuses; i++) {
            const bus = busData.entity[i].vehicle;
            if (bus && bus.position) {
                // Only show buses within Atlanta bounds
                const busLatLng = L.latLng(bus.position.latitude, bus.position.longitude);
                if (atlantaBounds.contains(busLatLng)) {
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
                    busesShown++;
                }
            }
        }
        
        if (busesShown === 0) {
            busPositionsDiv.innerHTML = '<p class="col-12 text-center">No bus position data available within Atlanta area</p>';
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
    
    trainPositionsDiv.innerHTML = '';
    
    // Clear previous train markers
    trainMarkers.forEach(marker => trainMap.removeLayer(marker));
    trainMarkers = [];
    
    if (trainData && trainData.length > 0) {
        // Store the train data globally for filtering
        allTrainData = trainData;
        
        // Create train markers on the map
        trainData.forEach(train => {
            const station = train.STATION;
            if (station && trainStations[station]) {
                // Get station coordinates
                const stationCoords = [trainStations[station].lat, trainStations[station].lng];
                
                // Create a marker for the train
                const trainIcon = createTrainIcon(train.LINE);
                const marker = L.marker(stationCoords, { icon: trainIcon });
                
                // Add popup with train info
                marker.bindPopup(`
                    <strong>Train ${train.TRAIN_ID}</strong><br>
                    ${train.LINE} Line<br>
                    Next Station: ${train.STATION}<br>
                    Arriving: ${train.WAITING_TIME}<br>
                    Destination: ${train.DESTINATION}
                `);
                
                marker.addTo(trainMap);
                trainMarkers.push(marker);
                
                // Highlight station with train
                if (trainStationMarkers[station]) {
                    trainStationMarkers[station].setStyle({
                        fillColor: lineColors[train.LINE] || '#FFFFFF'
                    });
                }
            }
        });
        
        // If we have an active filter, apply it, otherwise show all trains
        if (activeStationFilter) {
            updateTrainList(activeStationFilter);
            
            // Re-add the filter notice
            const filterInfo = document.createElement('div');
            filterInfo.className = 'col-12 mb-2 text-center filter-notice';
            filterInfo.innerHTML = `
                <div class="alert alert-info">
                    Showing trains arriving at: <strong>${activeStationFilter}</strong>
                    <button class="btn btn-sm btn-outline-dark ms-2" onclick="resetTrainFilter()">
                        Clear Filter
                    </button>
                </div>
            `;
            trainPositionsDiv.insertBefore(filterInfo, trainPositionsDiv.firstChild);
        } else {
            // Show train cards (up to 6)
            updateTrainList();
        }
    } else {
        allTrainData = [];
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
    // Initialize train map if first time viewing
    if (Object.keys(trainStationMarkers).length === 0) {
        initializeTrainMap();
    }
    // Resize map after showing it (needed for proper rendering)
    trainMap.invalidateSize();
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

// Filter trains by station
function filterTrainsByDestination(stationName) {
    activeStationFilter = stationName;
    
    // Highlight the selected station
    for (const [name, marker] of Object.entries(trainStationMarkers)) {
        if (name === stationName) {
            marker.setStyle({
                fillColor: '#FFFF00',
                fillOpacity: 1,
                radius: 8
            });
        } else {
            // Reset other stations to default style if they don't have a train
            const hasTrainAtStation = allTrainData.some(train => train.STATION === name);
            
            marker.setStyle({
                fillColor: hasTrainAtStation ? 
                    lineColors[allTrainData.find(t => t.STATION === name)?.LINE] || '#FFFFFF' : 
                    '#FFFFFF',
                fillOpacity: 1,
                radius: 6
            });
        }
    }
    
    // Update train list to only show trains with this next station
    updateTrainList(stationName);
    
    // Show filter indicator
    const trainPositionsDiv = document.getElementById('trainPositions');
    const filterInfo = document.createElement('div');
    filterInfo.className = 'col-12 mb-2 text-center filter-notice';
    filterInfo.innerHTML = `
        <div class="alert alert-info">
            Showing trains arriving at: <strong>${stationName}</strong>
            <button class="btn btn-sm btn-outline-dark ms-2" onclick="resetTrainFilter()">
                Clear Filter
            </button>
        </div>
    `;
    
    // Remove any existing filter notice
    document.querySelectorAll('.filter-notice').forEach(el => el.remove());
    
    // Add the new filter notice at the top
    if (trainPositionsDiv.firstChild) {
        trainPositionsDiv.insertBefore(filterInfo, trainPositionsDiv.firstChild);
    } else {
        trainPositionsDiv.appendChild(filterInfo);
    }
}

// Reset train filter
function resetTrainFilter() {
    activeStationFilter = null;
    
    // Reset all station markers to default style
    for (const [name, marker] of Object.entries(trainStationMarkers)) {
        const hasTrainAtStation = allTrainData.some(train => train.STATION === name);
        
        marker.setStyle({
            fillColor: hasTrainAtStation ? 
                lineColors[allTrainData.find(t => t.STATION === name)?.LINE] || '#FFFFFF' : 
                '#FFFFFF',
            fillOpacity: 1,
            radius: 6
        });
    }
    
    // Show all trains
    updateTrainList();
    
    // Remove filter notice
    document.querySelectorAll('.filter-notice').forEach(el => el.remove());
}

// Update train list with filtered or unfiltered data
function updateTrainList(destinationFilter = null) {
    const trainPositionsDiv = document.getElementById('trainPositions');
    
    // Remove existing train cards but keep filter notice if present
    Array.from(trainPositionsDiv.children)
        .filter(el => !el.classList.contains('filter-notice'))
        .forEach(el => el.remove());
    
    // Filter trains if a station is specified
    const filteredTrains = destinationFilter 
        ? allTrainData.filter(train => matchesStationName(train.STATION, destinationFilter))
        : allTrainData;
        
    // For debugging - log the mismatch to console
    if (destinationFilter && filteredTrains.length === 0) {
        console.log('Filter mismatch. Looking for:', destinationFilter);
        console.log('Available next stations:', allTrainData.map(t => t.STATION));
    }

    if (filteredTrains.length > 0) {
        // Show filtered trains
        const maxTrains = Math.min(6, filteredTrains.length);
        for (let i = 0; i < maxTrains; i++) {
            const train = filteredTrains[i];
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
        
        // Add note if results were filtered
        if (destinationFilter && filteredTrains.length > maxTrains) {
            const moreInfo = document.createElement('div');
            moreInfo.className = 'col-12 text-center mt-2';
            moreInfo.innerHTML = `<p>Showing ${maxTrains} of ${filteredTrains.length} trains to ${destinationFilter}</p>`;
            trainPositionsDiv.appendChild(moreInfo);
        }
    } else if (destinationFilter) {
        // No trains with the specified station
        const noTrains = document.createElement('div');
        noTrains.className = 'col-12 text-center';
        noTrains.innerHTML = `<p>No trains currently arriving at ${destinationFilter}</p>`;
        trainPositionsDiv.appendChild(noTrains);
    } else {
        // No train data at all
        trainPositionsDiv.innerHTML += '<p class="col-12 text-center">No train data available</p>';
    }
}

// Initial data load
updateUI();

// Debug function to log train destinations
function debugTrainDestinations() {
    console.log("=== Train Destination Debugging ===");
    console.log("Station names defined in the map:", Object.keys(trainStations));
    
    if (allTrainData && allTrainData.length > 0) {
        console.log("Current train destinations:", allTrainData.map(t => t.DESTINATION));
        
        // Show mapping between stations and trains
        const destinationMap = {};
        allTrainData.forEach(train => {
            if (!destinationMap[train.DESTINATION]) {
                destinationMap[train.DESTINATION] = [];
            }
            destinationMap[train.DESTINATION].push(train.TRAIN_ID);
        });
        
        console.log("Destination to Train mapping:", destinationMap);
    } else {
        console.log("No train data available");
    }
}

// Call debug function after data is loaded
setTimeout(debugTrainDestinations, 2000);

// Refresh data every 30 seconds
setInterval(updateUI, 30000);
