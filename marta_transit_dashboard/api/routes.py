"""
API routes for the Simple MARTA App
"""

from flask import Blueprint, jsonify
import sys
import os

# Add parent directory to import path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the necessary modules
from utils.weather import get_weather_data
from utils.train_data import get_marta_train_data, get_train_status
from utils.bus_data import get_bus_positions, get_bus_trips, get_bus_status
from utils.updates import get_recent_updates

# Create a Blueprint for API routes
api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/weather')
def weather():
    """
    Get current weather data
    
    Returns:
        JSON: Weather data including temperature, condition, etc.
    """
    return jsonify(get_weather_data())

@api_bp.route('/trains')
def trains():
    """
    Get current train data
    
    Returns:
        JSON: Train data with position, status, etc.
    """
    data = get_marta_train_data()
    return jsonify(data)

@api_bp.route('/buses/positions')
def buses():
    """
    Get current bus position data
    
    Returns:
        JSON: Bus position data
    """
    return jsonify(get_bus_positions())

@api_bp.route('/buses/trips')
def bus_trips():
    """
    Get current bus trip update data
    
    Returns:
        JSON: Bus trip update data
    """
    return jsonify(get_bus_trips())

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

@api_bp.route('/updates')
def updates():
    """
    Get service updates
    
    Returns:
        JSON: Recent service updates
    """
    return jsonify(get_recent_updates()) 