# MARTA Transit Dashboard - Map Implementation

## Overview

The MARTA Transit Dashboard features interactive maps for visualizing bus and train locations using Leaflet.js, a leading open-source JavaScript library for mobile-friendly interactive maps. This document details the implementation of these maps, their features, and how they can be extended.

## Technology Stack

- **Leaflet.js**: Core mapping library
- **OpenStreetMap**: Tile provider for map backgrounds
- **JavaScript**: Client-side implementation
- **MARTA APIs**: Data sources for transit information

## Map Components

The application includes two primary map components:

1. **Bus Map**: Displays real-time bus positions across the Atlanta metropolitan area
2. **Train Map**: Shows train stations and real-time train positions with interactive features

## Bus Map Implementation

### Key Features

- Real-time bus markers with information popups
- Automatic map bounds adjustment based on active buses
- Configurable geographic constraints to focus on Atlanta area
- Clickable bus markers showing route, bus ID, and position information

### Implementation Details

The bus map is initialized in `index.html` with these key components:

```javascript
// Create the bus map using Leaflet
const busMap = L.map('busPositionsMap', {
    minZoom: 9,
    maxZoom: 14
}).setView([33.749, -84.388], 10);

// Add OpenStreetMap tile layer
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(busMap);

// Set bounds for Atlanta metro area
const atlantaBounds = L.latLngBounds(
    L.latLng(33.400, -84.950), // Southwest corner
    L.latLng(34.200, -83.900)  // Northeast corner
);
busMap.setMaxBounds(atlantaBounds.pad(0.1));
```

### Bus Marker Creation

Bus markers are created dynamically from API data:

```javascript
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
```

### Automatic View Adjustment

The map automatically adjusts to show all active buses:

```javascript
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
```

## Train Map Implementation

### Key Features

- Interactive station markers with tooltips
- Color-coded train lines (Red, Gold, Blue, Green)
- Station filtering to show trains arriving at selected stations
- Automatic map initialization when the train view is selected
- Train icons color-coded by line

### Station Data Model

The train map uses a comprehensive station data model with accurate GPS coordinates:

```javascript
// MARTA train station coordinates
const trainStations = {
    // Red Line stations (North-South)
    'NORTH SPRINGS': { lat: 33.9455, lng: -84.3561, lines: ['RED'] },
    'SANDY SPRINGS': { lat: 33.9321, lng: -84.3513, lines: ['RED'] },
    // ... additional stations ...
    'FIVE POINTS': { lat: 33.7542, lng: -84.3919, lines: ['RED', 'GOLD', 'GREEN', 'BLUE'] },
    // ... additional stations ...
};
```

### Train Line Rendering

Train lines are rendered as polylines connecting station coordinates:

```javascript
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
```

### Station Filtering

The train map includes a filtering feature that shows trains arriving at a selected station:

```javascript
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
            // Reset other stations to default style
            // ...
        }
    }
    
    // Update train list to only show trains with this station as next stop
    updateTrainList(stationName);
    
    // Show filter indicator
    // ...
}
```

### Train Icons

Train icons are dynamically created based on line color:

```javascript
function createTrainIcon(line) {
    const color = lineColors[line] || '#999999';
    
    return L.divIcon({
        className: 'train-icon',
        html: `<div style="background-color: ${color}; width: 14px; height: 14px; border-radius: 50%; border: 2px solid white;"></div>`,
        iconSize: [14, 14],
        iconAnchor: [7, 7]
    });
}
```

## Performance Considerations

### Map Initialization

Maps are only initialized when they become visible to save resources:

```javascript
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
```

### Marker Management

Markers are efficiently managed to prevent memory leaks:

```javascript
// Clear previous train markers
trainMarkers.forEach(marker => trainMap.removeLayer(marker));
trainMarkers = [];
```

### Geographic Filtering

Data is filtered geographically to avoid overloading the map:

```javascript
// Only show buses within Atlanta bounds
const busLatLng = L.latLng(bus.position.latitude, bus.position.longitude);
if (atlantaBounds.contains(busLatLng)) {
    // Create marker...
}
```

## Design Decisions

### Use of Circle Markers for Stations

Train stations are represented as circle markers rather than standard markers for better visual integration with the train lines:

```javascript
const marker = L.circleMarker([stationData.lat, stationData.lng], {
    radius: 6,
    fillColor: '#FFFFFF',
    color: '#000000',
    weight: 2,
    opacity: 1,
    fillOpacity: 1
});
```

### Custom Div Icons for Trains

Trains use custom div icons rather than standard markers to maintain a consistent look and feel:

```javascript
const trainIcon = createTrainIcon(train.LINE);
const marker = L.marker(stationCoords, { icon: trainIcon });
```

### Map Bounds Restriction

Maps are restricted to the Atlanta metropolitan area to prevent users from panning too far away from relevant data:

```javascript
busMap.setMaxBounds(atlantaBounds.pad(0.1));
```

## Extending the Map

### Adding New Map Features

To add new features to the map:

1. Add initialization code to the appropriate map creation section
2. Ensure new features are properly cleaned up when views change
3. Document any new configuration options

### Custom Markers

To create custom markers:

```javascript
const customIcon = L.icon({
    iconUrl: 'path/to/icon.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34]
});

L.marker([latitude, longitude], { icon: customIcon }).addTo(map);
```

### Additional Map Layers

To add additional map layers:

```javascript
// Create a new layer
const newLayer = L.layerGroup();

// Add features to the layer
L.marker([33.749, -84.388]).addTo(newLayer);

// Add the layer to the map
newLayer.addTo(map);

// Create layer controls
const baseMaps = {
    "OpenStreetMap": osmLayer
};

const overlayMaps = {
    "New Feature": newLayer
};

L.control.layers(baseMaps, overlayMaps).addTo(map);
```
