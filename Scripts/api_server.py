import json
import os
import time
import threading
import datetime
from flask import Flask, jsonify
from flask_cors import CORS

# Import the transit and weather modules
from weather_api import get_current_weather
from realtime_train import get_marta_train_data
from vehicleposition_bus_api import get_vehicle_positions
from tripupdates_bus_api import get_trip_updates

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Cache for storing data to reduce API calls
data_cache = {
    'weather': {
        'data': None,
        'timestamp': 0,
        'ttl': 900  # 15 minutes
    },
    'bus_positions': {
        'data': None,
        'timestamp': 0,
        'ttl': 30  # 30 seconds
    },
    'bus_trips': {
        'data': None,
        'timestamp': 0,
        'ttl': 60  # 1 minute
    },
    'train_data': {
        'data': None,
        'timestamp': 0,
        'ttl': 30  # 30 seconds
    }
}

# Background thread for data fetching
def data_fetcher():
    while True:
        try:
            # Update weather data if needed
            if data_cache['weather']['data'] is None or (time.time() - data_cache['weather']['timestamp']) > data_cache['weather']['ttl']:
                weather_data = get_current_weather("Atlanta")
                if weather_data:
                    data_cache['weather']['data'] = {
                        'temperature': weather_data['main']['temp'],
                        'condition': weather_data['weather'][0]['description']
                    }
                    data_cache['weather']['timestamp'] = time.time()
            
            # Update bus positions if needed
            if data_cache['bus_positions']['data'] is None or (time.time() - data_cache['bus_positions']['timestamp']) > data_cache['bus_positions']['ttl']:
                bus_data = get_vehicle_positions()
                if bus_data:
                    data_cache['bus_positions']['data'] = bus_data
                    data_cache['bus_positions']['timestamp'] = time.time()
            
            # Update bus trip updates if needed
            if data_cache['bus_trips']['data'] is None or (time.time() - data_cache['bus_trips']['timestamp']) > data_cache['bus_trips']['ttl']:
                trip_data = get_trip_updates()
                if trip_data:
                    data_cache['bus_trips']['data'] = trip_data
                    data_cache['bus_trips']['timestamp'] = time.time()
            
            # Update train data if needed
            if data_cache['train_data']['data'] is None or (time.time() - data_cache['train_data']['timestamp']) > data_cache['train_data']['ttl']:
                # Replace with your actual API key
                api_key = "3b78f59c-e96d-4085-a291-eefb29bc5ecf"
                train_data = get_marta_train_data(api_key)
                if train_data:
                    data_cache['train_data']['data'] = train_data
                    data_cache['train_data']['timestamp'] = time.time()
            
            # Sleep for 10 seconds before checking again
            time.sleep(10)
        except Exception as e:
            print(f"Error in data fetcher: {e}")
            time.sleep(30)  # Wait longer if there's an error

# Start the background thread
fetcher_thread = threading.Thread(target=data_fetcher, daemon=True)
fetcher_thread.start()

# API Endpoints
@app.route('/api/weather', methods=['GET'])
def get_weather():
    if data_cache['weather']['data'] is None:
        return jsonify({
            'temperature': 72,
            'condition': 'Partly Cloudy'
        })
    return jsonify(data_cache['weather']['data'])

@app.route('/api/buses/positions', methods=['GET'])
def get_buses():
    if data_cache['bus_positions']['data'] is None:
        return jsonify({ 'entity': [] })
    return jsonify(data_cache['bus_positions']['data'])

@app.route('/api/buses/trips', methods=['GET'])
def get_bus_trips():
    if data_cache['bus_trips']['data'] is None:
        return jsonify({ 'entity': [] })
    return jsonify(data_cache['bus_trips']['data'])

@app.route('/api/trains', methods=['GET'])
def get_trains():
    if data_cache['train_data']['data'] is None:
        return jsonify([])
    return jsonify(data_cache['train_data']['data'])

@app.route('/api/status', methods=['GET'])
def get_status():
    try:
        # Determine bus status
        bus_status = {
            'status': 'On Time',
            'percentage': 95,
            'details': '95% of routes operating normally'
        }
        
        # Determine train status based on actual data
        train_status = {
            'status': 'On Time',
            'details': 'All lines operating normally',
            'affectedLines': []
        }
        
        if data_cache['train_data']['data']:
            # Count delays by line
            delays_by_line = {}
            for train in data_cache['train_data']['data']:
                if 'DELAY' in train and train['DELAY'].startswith('T'):
                    line = train['LINE']
                    delay_seconds = train['DELAY'][1:-1]  # Remove 'T' prefix and 'S' suffix
                    
                    try:
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
        
        return jsonify({
            'busStatus': bus_status,
            'trainStatus': train_status
        })
    except Exception as e:
        print(f"Error generating status: {e}")
        return jsonify({
            'busStatus': {
                'status': 'On Time',
                'percentage': 95,
                'details': '95% of routes operating normally'
            },
            'trainStatus': {
                'status': 'Minor Delays',
                'details': 'Red Line: 5-10 minute delays',
                'affectedLines': [
                    {
                        'line': 'RED',
                        'delay': '5-10 minutes'
                    }
                ]
            }
        })

@app.route('/api/updates', methods=['GET'])
def get_updates():
    try:
        updates = []
        
        # Add bus updates
        updates.append({
            'type': 'on-time',
            'message': 'Route 110 operating on schedule'
        })
        
        # Add weather-related update
        if data_cache['weather']['data']:
            condition = data_cache['weather']['data']['condition'].lower()
            if 'rain' in condition or 'storm' in condition:
                updates.append({
                    'type': 'delayed',
                    'message': 'Weather advisory: Expect delays on north-bound routes due to rain'
                })
            elif 'snow' in condition:
                updates.append({
                    'type': 'disrupted',
                    'message': 'Weather advisory: Service disruptions possible due to snow'
                })
        
        # Add train delay updates from actual data
        if data_cache['train_data']['data']:
            # Find significant delays
            for train in data_cache['train_data']['data']:
                if 'DELAY' in train and train['DELAY'].startswith('T'):
                    try:
                        delay_seconds = int(train['DELAY'][1:-1])  # Remove 'T' prefix and 'S' suffix
                        
                        if delay_seconds > 600:  # More than 10 minutes delay
                            updates.append({
                                'type': 'disrupted',
                                'message': f"Service disruption on {train['LINE']} Line between {train['STATION']} and {train['DESTINATION']}"
                            })
                            break  # Just add one significant disruption
                    except ValueError:
                        pass
        
        # If no disruptions found, add a general delay notice
        if not any(u['type'] == 'disrupted' for u in updates):
            updates.append({
                'type': 'delayed',
                'message': 'Minor delays expected during rush hour'
            })
        
        return jsonify(updates)
    except Exception as e:
        print(f"Error generating updates: {e}")
        return jsonify([
            { 'type': 'on-time', 'message': 'Route 110 operating on schedule' },
            { 'type': 'delayed', 'message': 'Weather advisory: Expect delays on north-bound routes' },
            { 'type': 'disrupted', 'message': 'Service disruption on Blue Line between Stations A and B' }
        ])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)