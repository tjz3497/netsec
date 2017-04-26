import requests
import re
from keys_local import *

IPINFO_START = "http://ipinfo.io/"
IPINFO_END = "/loc"
json = requests.get(IPINFO_START+'8.8.8.8'+IPINFO_END)
for i in json:
	loc = i.strip()
loc = str(loc)
loc = re.sub("[b']", '', loc)
latlon = loc.split(",")
print(latlon[0])
print(latlon[1], end='')
exit()