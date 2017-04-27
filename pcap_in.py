from scapy.all import *
import time
import ipaddress

def cutter():
	#pkts = rdpcap("SkypeIRC.cap")
	pkts = rdpcap("data.pcap")

	cut = {}
	for pkt in pkts:
		key = (pkt.sprintf("%IP.src%")).strip()

		addr = ipaddress.ip_address(key)
		if not (addr.is_private):
			time = str(pkt.time).split(".")
			time = time[0]
			#cut[key] = int(time)
			cut[key] = time

	return cut;