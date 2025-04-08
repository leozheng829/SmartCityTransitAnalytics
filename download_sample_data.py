import requests
import json
import os

def download_train_data():
    """Download and save MARTA train data"""
    try:
        # MARTA Train API endpoint
        api_key = "3b78f59c-e96d-4085-a291-eefb29bc5ecf"  # MARTA API key
        url = f"https://developerservices.itsmarta.com:18096/itsmarta/railrealtimearrivals/developerservices/traindata"
        headers = {'accept': 'application/json'}
        params = {'apiKey': api_key}
        
        print("Downloading MARTA train data...")
        response = requests.get(url, headers=headers, params=params, verify=True)
        
        if response.status_code == 200:
            data = response.json()
            
            # Save the data to a file
            with open('train_data.json', 'w') as f:
                json.dump(data, f, indent=2)
            
            print(f"✅ Successfully downloaded train data: {len(data)} entries")
            
            # Also create a sample version with a few records
            if len(data) > 6:
                sample_data = data[:6]  # Take first 6 entries
                
                with open('sample_train_data.json', 'w') as f:
                    json.dump(sample_data, f, indent=2)
                
                print(f"✅ Created sample train data with {len(sample_data)} entries")
            
        else:
            print(f"❌ Failed to download train data. Status code: {response.status_code}")
            print(f"Response: {response.text}")
    
    except Exception as e:
        print(f"❌ Error downloading train data: {str(e)}")

def create_sample_bus_data():
    """Create sample bus position data in GTFS format"""
    print("Creating sample bus position data...")
    
    # Sample bus data in GTFS-RT format (simplified)
    sample_data = {
        "entity": [
            {
                "id": "1",
                "vehicle": {
                    "vehicle": {"id": "1101", "label": "1101"},
                    "trip": {"routeId": "110"},
                    "position": {"latitude": 33.7565, "longitude": -84.3880},
                    "timestamp": 1633027200,
                    "occupancyStatus": "MANY_SEATS_AVAILABLE"
                }
            },
            {
                "id": "2",
                "vehicle": {
                    "vehicle": {"id": "2202", "label": "2202"},
                    "trip": {"routeId": "120"},
                    "position": {"latitude": 33.7629, "longitude": -84.3920},
                    "timestamp": 1633027260,
                    "occupancyStatus": "FEW_SEATS_AVAILABLE"
                }
            },
            {
                "id": "3",
                "vehicle": {
                    "vehicle": {"id": "3303", "label": "3303"},
                    "trip": {"routeId": "130"},
                    "position": {"latitude": 33.7689, "longitude": -84.3963},
                    "timestamp": 1633027320,
                    "occupancyStatus": "MANY_SEATS_AVAILABLE"
                }
            },
            {
                "id": "4",
                "vehicle": {
                    "vehicle": {"id": "4404", "label": "4404"},
                    "trip": {"routeId": "140"},
                    "position": {"latitude": 33.7754, "longitude": -84.4010},
                    "timestamp": 1633027380,
                    "occupancyStatus": "STANDING_ROOM_ONLY"
                }
            },
            {
                "id": "5",
                "vehicle": {
                    "vehicle": {"id": "5505", "label": "5505"},
                    "trip": {"routeId": "150"},
                    "position": {"latitude": 33.7830, "longitude": -84.4060},
                    "timestamp": 1633027440,
                    "occupancyStatus": "MANY_SEATS_AVAILABLE"
                }
            },
            {
                "id": "6",
                "vehicle": {
                    "vehicle": {"id": "6606", "label": "6606"},
                    "trip": {"routeId": "160"},
                    "position": {"latitude": 33.7912, "longitude": -84.4112},
                    "timestamp": 1633027500,
                    "occupancyStatus": "FEW_SEATS_AVAILABLE"
                }
            }
        ]
    }
    
    # Save the generated data
    with open('bus_positions.json', 'w') as f:
        json.dump(sample_data, f, indent=2)
    
    print(f"✅ Created sample bus position data with {len(sample_data['entity'])} entries")

if __name__ == "__main__":
    print("Starting data download process...")
    
    # Download train data
    download_train_data()
    
    # Create sample bus data
    create_sample_bus_data()
    
    # Check if files exist
    train_file = os.path.exists('train_data.json')
    sample_train_file = os.path.exists('sample_train_data.json')
    bus_file = os.path.exists('bus_positions.json')
    
    print("\nData files status:")
    print(f"train_data.json: {'✅ Created' if train_file else '❌ Not created'}")
    print(f"sample_train_data.json: {'✅ Created' if sample_train_file else '❌ Not created'}")
    print(f"bus_positions.json: {'✅ Created' if bus_file else '❌ Not created'}")
    
    print("\nSetup complete! You can now run 'python simple_marta_app.py' to start the application.") 