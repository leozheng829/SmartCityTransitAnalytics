from google.transit import gtfs_realtime_pb2
import requests
import json
from google.protobuf.json_format import MessageToJson

def get_vehicle_positions():
    try:
        feed = gtfs_realtime_pb2.FeedMessage()
        response = requests.get('https://gtfs-rt.itsmarta.com/TMGTFSRealTimeWebService/vehicle/vehiclepositions.pb')
        feed.ParseFromString(response.content)
        
        # Convert protobuf to JSON
        json_data = MessageToJson(feed)
        parsed_data = json.loads(json_data)
        
        # Save to file for reference
        with open('bus_positions.json', 'w') as f:
            json.dump(parsed_data, f, indent=4)
            
        return parsed_data
    except Exception as e:
        print(f"Error fetching vehicle positions: {e}")
        return None

if __name__ == "__main__":
    # When run directly, print the data
    positions = get_vehicle_positions()
    if positions:
        print(f"Retrieved {len(positions.get('entity', []))} vehicle positions")
    else:
        print("Failed to retrieve vehicle positions")