"""
Train data utilities for the Simple MARTA App
"""

import json
import os
import requests
import sys

# Add parent directory to import path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.config import (
    MARTA_TRAIN_API_URL,
    MARTA_TRAIN_API_KEY,
    TRAIN_CACHE_FILE
)

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

def get_train_status(train_data=None):
    """
    Calculate the status of MARTA train lines based on delays
    
    Args:
        train_data (list, optional): Train data to analyze. If None, fetches new data.
        
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
    
    return train_status 