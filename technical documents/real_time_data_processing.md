# MARTA Transit Dashboard - Real-Time Data Processing

## Overview

The MARTA Transit Dashboard processes and displays real-time transit data from multiple sources. This document explains how the application fetches, processes, transforms, and visualizes real-time data to provide up-to-date transit information.

## Data Sources

The application integrates with the following real-time data sources:

1. **MARTA Train API**: JSON-based API providing real-time train arrival information
2. **MARTA Bus GTFS-RT Feeds**: Protocol Buffer feeds for bus positions and trip updates
3. **Open-Meteo Weather API**: Real-time weather conditions for the Atlanta area

## Data Processing Pipeline

### 1. Data Acquisition

The data acquisition process is handled by utility modules in the `utils/` directory:

#### Train Data (`train_data.py`)

```python
def get_marta_train_data():
    """
    Get real-time MARTA train data
    
    Returns:
        list: Train data with position, status, etc.
    """
    try:
        headers = {'accept': 'application/json'}
        params = {'apiKey': MARTA_TRAIN_API_KEY}
        
        response = requests.get(
            MARTA_TRAIN_API_URL, 
            headers=headers, 
            params=params, 
            verify=True
        )
        
        if response.status_code == 200:
            data = response.json()
            
            # Cache the data for future use
            os.makedirs(os.path.dirname(TRAIN_CACHE_FILE), exist_ok=True)
            with open(TRAIN_CACHE_FILE, 'w') as f:
                json.dump(data, f)
                
            return data
        else:
            print(f"Failed to get train data: {response.status_code}")
            return get_train_data_fallback()
    except Exception as e:
        print(f"Error fetching train data: {e}")
        return get_train_data_fallback()
```

#### Bus Data (`bus_data.py`)

```python
def get_bus_positions():
    """
    Get real-time MARTA bus position data from GTFS-RT feed
    
    Returns:
        dict: Bus position data in JSON format
    """
    try:
        response = requests.get(MARTA_BUS_POSITIONS_URL)
        
        if response.status_code == 200:
            # Parse the Protocol Buffer message
            feed = gtfs_realtime_pb2.FeedMessage()
            feed.ParseFromString(response.content)
            
            # Convert to JSON-serializable format
            data = protobuf_to_dict(feed)
            
            # Cache the data
            with open(BUS_POSITIONS_CACHE_FILE, 'w') as f:
                json.dump(data, f)
                
            return data
        else:
            return get_bus_positions_fallback()
    except Exception as e:
        print(f"Error fetching bus positions: {e}")
        return get_bus_positions_fallback()
```

### 2. Data Transformation

Raw data from APIs is transformed into formats suitable for the application:

#### Status Calculation

The application calculates system status based on delay patterns:

```python
def get_train_status(train_data=None):
    """
    Calculate the status of MARTA train lines based on delays
    
    Args:
        train_data (list, optional): Train data to analyze
        
    Returns:
        dict: Status information for train lines
    """
    if train_data is None:
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
    
    # Analyze delays and update status
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
    
    return train_status
```

### 3. Data Caching

All data is cached to ensure the application remains functional even when APIs are unavailable:

```python
def get_train_data_fallback():
    """
    Return cached train data if the API is unavailable
    
    Returns:
        list: Train data from cache, or empty list if no cache
    """
    try:
        if os.path.exists(TRAIN_CACHE_FILE):
            with open(TRAIN_CACHE_FILE, 'r') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error reading train cache: {e}")
    
    # If all else fails, return empty array
    return []
```

### 4. API Endpoints

The application provides RESTful API endpoints that serve processed data:

```python
@api_bp.route('/trains')
def trains():
    """
    Get current train data
    
    Returns:
        JSON: Train data with position, status, etc.
    """
    data = get_marta_train_data()
    return jsonify(data)

@api_bp.route('/status')
def status():
    """
    Get transit system status
    
    Returns:
        JSON: Status information for buses and trains
    """
    train_status = get_train_status()
    bus_status = get_bus_status()
    
    return jsonify({
        'busStatus': bus_status,
        'trainStatus': train_status
    })
```

### 5. Client-Side Processing

The frontend performs additional processing using JavaScript:

```javascript
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
    } else {
        // Show train cards (up to 6)
        updateTrainList();
    }
} else {
    allTrainData = [];
    trainPositionsDiv.innerHTML = '<p class="col-12 text-center">No train data available</p>';
}
```

## Real-Time Data Challenges and Solutions

### Challenge: Data Reliability

**Solution:**
- Implement robust error handling in all API calls
- Create fallback mechanisms to use cached data
- Log all API failures for monitoring
- Add user-friendly messages when data is unavailable

### Challenge: Data Freshness

**Solution:**
- Implement appropriate cache expiration times for different data types
- Provide automatic refresh of data at regular intervals
- Allow manual refresh via the UI
- Display timestamps showing when data was last updated

### Challenge: Data Format Inconsistencies

**Solution:**
- Create normalized internal data models
- Implement data validation and sanitization
- Handle edge cases and missing fields
- Use type coercion where appropriate

## Data Refresh Strategy

### Server-Side Refresh

- Weather data: Cached for 10 minutes
- Train data: Cached for 60 seconds
- Bus positions: Cached for 30 seconds
- Bus trip updates: Cached for 30 seconds

### Client-Side Refresh

- Automatic refresh every 30 seconds via JavaScript
- Manual refresh button triggering immediate data update
- Selective refreshing (only update visible components)

## Performance Optimizations

### Data Transfer Optimizations

- Only send necessary data fields to the client
- Use compression for API responses
- Buffer API requests to prevent overwhelming external APIs

### Processing Optimizations

- Process data on the server when possible
- Perform client-side filtering rather than requesting filtered data
- Cache computed values (e.g., status calculations)

### Visualization Optimizations

- Only update UI elements when data has changed
- Lazy-load components that aren't immediately visible
- Use efficient DOM updates to minimize repaints

## Monitoring and Logging

The application includes monitoring of real-time data processing:

```python
def log_api_request(endpoint, success, status_code=None, error=None):
    """
    Log API request details
    
    Args:
        endpoint (str): API endpoint 
        success (bool): Whether request was successful
        status_code (int, optional): HTTP status code
        error (str, optional): Error message if any
    """
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    if success:
        log_message = f"{timestamp} - API Request - {endpoint} - Success - {status_code}"
    else:
        log_message = f"{timestamp} - API Request - {endpoint} - Failed - {error}"
    
    print(log_message)  # For console output
    
    # Append to log file
    with open(LOG_FILE, 'a') as f:
        f.write(log_message + '\n')
```
