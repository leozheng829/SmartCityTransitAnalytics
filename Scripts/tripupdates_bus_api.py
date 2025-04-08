from google.transit import gtfs_realtime_pb2
import requests
import json
from google.protobuf.json_format import MessageToJson

def get_trip_updates():
    try:
        feed = gtfs_realtime_pb2.FeedMessage()
        response = requests.get('https://gtfs-rt.itsmarta.com/TMGTFSRealTimeWebService/tripupdate/tripupdates.pb')
        feed.ParseFromString(response.content)
        
        # Convert protobuf to JSON
        json_data = MessageToJson(feed)
        parsed_data = json.loads(json_data)
        
        # Save to file for reference
        with open('bus_tripupdates.json', 'w') as f:
            json.dump(parsed_data, f, indent=4)
            
        return parsed_data
    except Exception as e:
        print(f"Error fetching trip updates: {e}")
        return None

if __name__ == "__main__":
    # When run directly, print the data
    trip_updates = get_trip_updates()
    if trip_updates:
        print(f"Retrieved {len(trip_updates.get('entity', []))} trip updates")
    else:
        print("Failed to retrieve trip updates")