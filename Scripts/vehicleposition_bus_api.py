from google.transit import gtfs_realtime_pb2
import requests

feed = gtfs_realtime_pb2.FeedMessage()
response = requests.get('https://gtfs-rt.itsmarta.com/TMGTFSRealTimeWebService/vehicle/vehiclepositions.pb')
feed.ParseFromString(response.content)
print(feed)
# for entity in feed.entity:
#   if entity.HasField('vehicle'):
#     print(entity.vehicle)