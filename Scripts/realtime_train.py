import requests
import json
from datetime import datetime

def get_marta_train_data(api_key):
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
        print(f"Error fetching data: {e}")
        return None

def parse_train_data(data):
    if not data:
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