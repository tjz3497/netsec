from scapy.all import *
import time
import ipaddress

def cutter(file_name):
	pkts = rdpcap(file_name)

	cut = {}
	for pkt in pkts:
		key = (pkt.sprintf("%IP.src%")).strip()

		if not (key=='??'):
			addr = ipaddress.ip_address(key)
			if not (addr.is_private):
				time = str(pkt.time).split(".")
				time = time[0]
				cut[key] = time

	return cut;