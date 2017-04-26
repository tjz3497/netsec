#IMPORT BLOCK
import requests
import re
import time
from keys_local import *
import json

#VARIABLE BLOCK for ip to lat
IPINFO_START = "http://ipinfo.io/"
IPINFO_END = "/loc"

#get timestamp for map timezone api call
timestamp = time.time()
timestamp = str(timestamp).split(".")
timestamp = timestamp[0]
timeInt = int(timestamp)

#TEST
print(time.ctime(timeInt))

#######LOCAL######################
#get local info
json = requests.get(IPINFO_START + "loc")
for i in json:
	loc = i.strip()
loc = str(loc)
latlon = re.sub("[b']", '', loc)

#VARIABLE BLOCK for map timezone api
TZ_CALL = "https://maps.googleapis.com/maps/api/timezone/json?location="+latlon+"&timestamp="+timestamp+"&key="+MAPS_TZ_API

#get timezone from the goog
tz_out = requests.get(TZ_CALL)
data = tz_out.json()

#combine raw offset with DST
raw = data["rawOffset"]
dst = data["dstOffset"]

localTot = raw+dst+timeInt
print(time.ctime(localTot))
print("Local Timezone is: "+data["timeZoneName"])
#######END LOCAL######################

#######DEST######################
#get ip lat/long
json = requests.get(IPINFO_START+'8.8.8.8'+IPINFO_END)
for i in json:
	loc = i.strip()
loc = str(loc)
latlon = re.sub("[b']", '', loc)

#VARIABLE BLOCK for map timezone api
TZ_CALL = "https://maps.googleapis.com/maps/api/timezone/json?location="+latlon+"&timestamp="+timestamp+"&key="+MAPS_TZ_API

#get timezone from the goog
tz_out = requests.get(TZ_CALL)
data = tz_out.json()

#combine raw offset with DST
raw = data["rawOffset"]
dst = data["dstOffset"]

destTot = raw+dst+timeInt
print(time.ctime(destTot))
print("Destination Timezone is: "+data["timeZoneName"])
#######END DEST######################

exit()