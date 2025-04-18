"""
Bus data utilities for the Simple MARTA App
"""

import json
import os
import sys

# Add parent directory to import path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.config import (
    MARTA_BUS_POSITIONS_URL,
    MARTA_BUS_TRIPS_URL,
    BUS_POSITIONS_CACHE_FILE,
    BUS_TRIPS_CACHE_FILE
)

# Try to import the bus API modules
try:
    from google.transit import gtfs_realtime_pb2
    import requests
    from google.protobuf.json_format import MessageToJson
    
    # Flag indicating that required modules are available
    HAS_GTFS_MODULES = True
except ImportError:
    print("Warning: GTFS-RT modules not found. Will use cached data for buses.")
    HAS_GTFS_MODULES = False

def get_bus_positions():
    """
    Get real-time bus position data from MARTA GTFS-RT API
    
    Returns:
        dict: Bus position data
    """
    try:
        # Try to use the real API if available
        if HAS_GTFS_MODULES:
            print("Fetching live bus position data...")
            feed = gtfs_realtime_pb2.FeedMessage()
            response = requests.get(MARTA_BUS_POSITIONS_URL)
            feed.ParseFromString(response.content)
            
            # Convert protobuf to JSON
            json_data = MessageToJson(feed)
            bus_data = json.loads(json_data)
            
            if bus_data:
                # Cache the data for future use
                os.makedirs(os.path.dirname(BUS_POSITIONS_CACHE_FILE), exist_ok=True)
                with open(BUS_POSITIONS_CACHE_FILE, 'w') as f:
                    json.dump(bus_data, f)
                    
                return bus_data
            else:
                print("Failed to get live bus data, falling back to cache")
        else:
            print("Bus API modules not available, using cached data")
            
        # Fall back to cached data
        return get_bus_positions_fallback()
    except Exception as e:
        print(f"Error getting bus positions: {e}")
        return get_bus_positions_fallback()

def get_bus_positions_fallback():
    """
    Return cached bus position data if the API is unavailable
    
    Returns:
        dict: Bus position data from cache, or empty dict if no cache
    """
    try:
        if os.path.exists(BUS_POSITIONS_CACHE_FILE):
            with open(BUS_POSITIONS_CACHE_FILE, 'r') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error reading bus positions cache: {e}")
    
    # Return empty data structure if no data available
    return {"entity": []}

def get_bus_trips():
    """
    Get real-time bus trip updates from MARTA GTFS-RT API
    
    Returns:
        dict: Bus trip update data
    """
    try:
        # Try to use the real API if available
        if HAS_GTFS_MODULES:
            print("Fetching live bus trip data...")
            feed = gtfs_realtime_pb2.FeedMessage()
            response = requests.get(MARTA_BUS_TRIPS_URL)
            feed.ParseFromString(response.content)
            
            # Convert protobuf to JSON
            json_data = MessageToJson(feed)
            trip_data = json.loads(json_data)
            
            if trip_data:
                # Cache the data for future use
                os.makedirs(os.path.dirname(BUS_TRIPS_CACHE_FILE), exist_ok=True)
                with open(BUS_TRIPS_CACHE_FILE, 'w') as f:
                    json.dump(trip_data, f)
                    
                return trip_data
            else:
                print("Failed to get live trip data, falling back to cache")
        else:
            print("Trip updates API modules not available, using cached data")
            
        # Fall back to cached data
        return get_bus_trips_fallback()
    except Exception as e:
        print(f"Error getting bus trip updates: {e}")
        return get_bus_trips_fallback()

def get_bus_trips_fallback():
    """
    Return cached bus trip data if the API is unavailable
    
    Returns:
        dict: Bus trip data from cache, or empty dict if no cache
    """
    try:
        if os.path.exists(BUS_TRIPS_CACHE_FILE):
            with open(BUS_TRIPS_CACHE_FILE, 'r') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error reading bus trips cache: {e}")
    
    # Return empty data structure if no data available
    return {"entity": []}

def get_bus_status():
    """
    Calculate the status of MARTA bus system
    
    Returns:
        dict: Status information for buses
    """
    # For now, return a simple static status
    # In a more complete implementation, we would analyze trip data
    # to calculate actual on-time percentages
    
    return {
        'status': 'On Time',
        'percentage': 95,
        'details': '95% of routes operating normally'
    } 