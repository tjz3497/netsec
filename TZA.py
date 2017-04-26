#IMPORT BLOCK
import requests
import re
import time
from keys_local import *

#VARIABLE BLOCK for ip to lat
IPINFO_START = "http://ipinfo.io/"
IPINFO_END = "/loc"

#get ip lat/long
json = requests.get(IPINFO_START+'8.8.8.8'+IPINFO_END)
for i in json:
	loc = i.strip()
loc = str(loc)
latlon = re.sub("[b']", '', loc)

#get timestamp for map timezone api call
timestamp = time.time()
timestamp = str(timestamp).split(".")
timestamp = timestamp[0]

#VARIABLE BLOCK for map timezone api
TZ_CALL = "https://maps.googleapis.com/maps/api/timezone/json?location="+latlon+"&timestamp="+timestamp+"&key="+MAPS_TZ_API
tz_out = requests.get(TZ_CALL)
for i in tz_out:
	print(i)

exit()