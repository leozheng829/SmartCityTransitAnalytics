"""
Service updates utilities for the Simple MARTA App
"""

import sys
import os

# Add parent directory to import path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import necessary modules
from utils.train_data import get_marta_train_data

def get_recent_updates():
    """
    Generate recent service updates based on transit data
    
    Returns:
        list: Service updates with type and message
    """
    # Generate updates based on train data
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