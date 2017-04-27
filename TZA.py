#IMPORT BLOCK
import requests
import re
import time
import json

from keys_local import *
from pcap_in import *


#VARIABLE BLOCK for ip to lat
IPINFO_START = "http://ipinfo.io/"
IPINFO_SL = "/loc"
IPINFO_END = "loc"

#VARIABLE BLOCK for timezone api call
TZ_START = "https://maps.googleapis.com/maps/api/timezone/json?location="
TZ_STAMP = "&timestamp="
TZ_KEY = "&key="

def the_goods():

	#GET THE PCAP STUFF
	PCAP_DICT = cutter()
	#for i, j in PCAP_DICT.items():
	#	print(i + " , ", end='')
	#	print(j)

	#get local timestamp for maps timezone api call
	timestamp = time.time()
	timestamp = str(timestamp).split(".")
	timestamp = timestamp[0]
	#make it an int for math later
	timeInt = int(timestamp)
	#print(time.ctime(timeInt))
	#account for local  time offset of 4 hours
	timeInt = timeInt + (3600 * 4)

	#localTot = get_time_info(islocal = 1, ip = 0, stamp = timestamp, tint = timeInt)
	#print(time.ctime(localTot))
	tester = 0
	for i, j in PCAP_DICT.items():
		if tester == 1:
			ipper = i
		tester = tester + 1
	print(ipper)
	destTot = get_time_info(islocal = 0, ip = ipper, stamp = timestamp, tint = timeInt)
	print(time.ctime(destTot[2]))
	exit()

def get_time_info(islocal, ip, stamp, tint):
	req = ""
	#if its not local we need to supply an IP address in the request
	#noIP
	if islocal == 1:
		req = IPINFO_START + IPINFO_END
	#IP
	else:
		req = IPINFO_START + ip + IPINFO_SL
	#send the request for the latitude and longitude
	json = requests.get(req)
	#make the answer pretty
	for i in json:
		loc = i.strip()
	loc = str(loc)
	latlon = re.sub("[b']",'',loc)

	#get the timezone for the given latitude and longitude
	TZ_CALL = TZ_START+latlon+TZ_STAMP+stamp+TZ_KEY+MAPS_TZ_API
	tz_out = requests.get(TZ_CALL)
	data = tz_out.json()

	#get the raw offset and DST offset values
	raw = data["rawOffset"]
	dst = data["dstOffset"]
	#add em up for the actual time
	timeTot = raw+dst+tint
	results = (raw, dst, timeTot)
	return results

the_goods()