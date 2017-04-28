# netsec
TimeZoneAnalyzer -  tool which focuses on the location data of connections which take place.  The tool takes geolocation data from connection IPs and then matches the connection time to the IPs local timezone.  This data will be visualized as  a 'top source location' graph in addition to analysis of what (local) times most users frequently connect.   This will be represented both as raw numbers and statistical data analyzed from the larger data set.  Additionally, I will provide a determination, based on the connection time of the IP, whether or not a connection actually originates from the IP being reported, or if a proxy of some type is being utilized.  This information can be as a metric to attempt to mark suspicious connections, as well as for marketing and demographic purposes.

How to Install:
Simply download and run the presented files from the command line.

Dependencies:
Python3
scapy3k (pip install scapy-python3)

APIs:
Must have a google maps timezone (https://developers.google.com/maps/documentation/timezone/intro#Responses) API key placed in a keys_local.py file in the local directory with the variable
name 'MAPS_TZ_API'

Contributors - Tyler Zimmermann tjz3497@rit.edu

License - MIT