import requests
import json
from datetime import datetime

def get_marta_train_data(api_key):
    """
    Get real-time MARTA train data
    
    Parameters:
    api_key (str): MARTA API key
    
    Returns:
    list: List of train data objects
    """
    url = f"https://developerservices.itsmarta.com:18096/itsmarta/railrealtimearrivals/developerservices/traindata"
    headers = {
        'accept': 'application/json'
    }
    params = {
        'apiKey': api_key
    }

    try:
        response = requests.get(url, headers=headers, params=params, verify=True)
        response.raise_for_status()
        
        data = response.json()
        # Save the raw data to a JSON file with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        with open(f'train_data_{timestamp}.json', 'w') as f:
            json.dump(data, f, indent=4)
        return data

    except requests.exceptions.RequestException as e:
        print(f"Error fetching train data: {e}")
        
        # If we can't get live data, try to use cached data
        try:
            with open('train_data.json', 'r') as f:
                return json.load(f)
        except:
            # If no cached data, return an empty list
            return []

def parse_train_data(data):
    """
    Parse train data for display
    
    Parameters:
    data (list): List of train data objects
    
    Returns:
    None: Prints formatted train data
    """
    if not data:
        print("No train data available")
        return
    
    for train in data:
        print(f"""
Train ID: {train.get('TRAIN_ID')}
Line: {train.get('LINE')}
Station: {train.get('STATION')}
Direction: {train.get('DIRECTION')}
Next Arrival: {train.get('NEXT_ARR')}
""")

if __name__ == "__main__":
    api_key = "3b78f59c-e96d-4085-a291-eefb29bc5ecf"
    train_data = get_marta_train_data(api_key)
    parse_train_data(train_data)
    
    # Save a copy with a generic name for caching
    if train_data:
        with open('train_data.json', 'w') as f:
            json.dump(train_data, f, indent=4)