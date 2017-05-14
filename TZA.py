#IMPORT BLOCK
import requests
import re
import time
import json
import pycountry

from keys_local import *
from pcap_in import *


#VARIABLE BLOCK for ip to lat
IPINFO_START = "http://ipinfo.io/"
IPINFO_SL = "/loc"
IPINFO_END = "loc"
IPINFO_state = "/region"
IPINFO_country = "/country'"

#VARIABLE BLOCK for timezone api call
TZ_START = "https://maps.googleapis.com/maps/api/timezone/json?location="
TZ_STAMP = "&timestamp="
TZ_KEY = "&key="

def the_goods(file):

	#GET THE PCAP STUFF
	PCAP_DICT = cutter(file_name = file)

	#get local timestamp for maps timezone api call
	timestamp = time.time()
	timestamp = str(timestamp).split(".")
	timestamp = timestamp[0]
	#make it an int for math later
	timeInt = int(timestamp)
	#account for local  time offset of 4 hours
	timeInt = timeInt + (3600 * 4)

	#make a dictionary to hold the count of different timezones
	#IDC = id counter
	timeZone_IDC = {}
	local_counts = {}
	country_ids = []

	#get some big time info for all the IPs
	for ipper, j in PCAP_DICT.items():
		#get the break down of time info aka raw offset, dst offset, and time zone id
		time_break = get_time_info(islocal = 0, ip = ipper, stamp = timestamp)
		#get the timestamp from the capture for the given ip
		from_cap = int(PCAP_DICT[ipper])
		#calculate the local time of connection based on the above two value sets
		time_of_connection = int(time_break[0]) + int(time_break[1]) + from_cap

		#get the local time (just hour/minute/second) in seconds for math later
		#note to self: index 3 is hour, 4 is minute, 5 is second
		time_attribs = time.localtime(time_of_connection)
		local_count = (time_attribs[3] * 3600) + (time_attribs[4] * 60) + time_attribs[5]
		local_counts[ipper] = local_count

		#add the current timezone id to the dictionary counting timezone ids
		timeZone_IDC = timeZone_ID_Counter(tzIDC = timeZone_IDC, tzID = time_break[2])

		#add the country ID to the list for worldmap
		country = time_break[3]
		if(country != ''):
			country = (pycountry.countries.get(alpha_2 = country)).alpha_3
			country_ids.append(country)

	#do the maths
	average_connection_time = big_mather(local_counts)

	#turn the seconds into hours, minutes, seconds
	hms = seconds_to_hms(average_connection_time)

	#calculate how far from the average time each connection is
	dist_from_avg = get_dist(loc = local_counts, avg = average_connection_time)
	avg_data = []
	for i,j in dist_from_avg.items():
		temp = {'ip': i, 'distance from average': j}
		avg_data.append(temp)

	#determine if the connection time is weird
	avg_var = get_avg_var(dist_from_avg)
	bads = get_bads(dist_from_avg, avg_var)

	susps = []
	for i,j in bads.items():
		temp = {'ip': i, 'distance from average': j}
		susps.append(temp)

	return(avg_data, country_ids, average_connection_time, susps)

def get_bads(distAvg, avgVar):
	bads = {}
	distAver = distAvg
	
	for ip, dist in distAvg.items():
		distAver[ip] = distAver[ip] / avgVar
		if(distAver[ip] > 1.6 or distAver[ip] < .4):
			bads[ip] = distAver[ip]

	return(bads)

def get_avg_var(distAvg):
	avg_var = 0;
	count = 0;
	for i,j in distAvg.items():
		count += 1
		avg_var = int(avg_var + j)
	avg_var = int(avg_var / count)

	return(avg_var)

def get_dist(loc, avg):
	dist = {}
	for i,j in loc.items():
		dist[i] = abs(avg - j)
	return dist

def seconds_to_hms(secs):
	m, s = divmod(secs, 60)
	h, m = divmod(m, 60)
	result = (h, m, s)
	return result

def big_mather(counts):
	average_time = 0
	how_many = 0
	for i,j in counts.items():
		average_time += j
		how_many += 1
	return int(average_time / how_many)

def timeZone_ID_Counter(tzIDC, tzID):
	for key in tzIDC.keys():
		if tzID == key:
			tzIDC[key] = tzIDC[key] + 1
			return tzIDC
	tzIDC[tzID] = 1
	return tzIDC


def get_time_info(islocal, ip, stamp):
	isLoc = islocal
	#if its not local we need to supply an IP address in the request
	#IP
	if isLoc == 0:
		req = IPINFO_START + ip
		datas = (requests.get(req)).json()
		country = datas["country"]
		state = datas["region"]
		if('loc' in datas):
			loc = datas["loc"]
			loc = str(loc)
			latlon = re.sub("[b']",'',loc)
		else:
			isLoc = 1
		if(country == "US" and state != ''):
			place = ''
		else:
			place = country
	#noIP
	if isLoc == 1:
		req = IPINFO_START + IPINFO_END
		#send the request for the latitude and longitude
		json = requests.get(req)
		#make the answer pretty
		for i in json:
			loc = i.strip()
		loc = str(loc)
		latlon = re.sub("[b']",'',loc)
		place = ''

	#get the timezone for the given latitude and longitude
	TZ_CALL = TZ_START+latlon+TZ_STAMP+stamp+TZ_KEY+MAPS_TZ_API
	tz_out = requests.get(TZ_CALL)
	data = tz_out.json()

	#get the raw offset and DST offset values
	raw = data["rawOffset"]
	dst = data["dstOffset"]
	tzid = data["timeZoneId"]
	#add em up for the actual time
	results = (raw, dst, tzid, place)
	return results