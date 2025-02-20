from google.transit import gtfs_realtime_pb2
import requests
import json
from google.protobuf.json_format import MessageToJson

feed = gtfs_realtime_pb2.FeedMessage()
response = requests.get('https://gtfs-rt.itsmarta.com/TMGTFSRealTimeWebService/tripupdate/tripupdates.pb')
feed.ParseFromString(response.content)
print(feed)

json_data = MessageToJson(feed)
with open('bus_tripupdates.json', 'w') as f:
    json.dump(json.loads(json_data), f, indent=4)