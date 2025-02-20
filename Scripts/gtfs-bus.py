from google.transit import gtfs_realtime_pb2

import urllib
feed = gtfs_realtime_pb2.FeedMessage()
response = urllib.request.urlopen('https://gtfs-rt.itsmarta.com/TMGTFSRealTimeWebService/vehicle/vehiclepositions.pb')
feed.ParseFromString(response.read()) 
print(feed.entity)