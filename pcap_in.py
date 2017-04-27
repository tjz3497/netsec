from scapy.all import *
import time

def cutter():
#pkts = rdpcap("SkypeIRC.cap")
	pkts = rdpcap("data.pcap")

	bad = ['0.0.0.0', '??']
	cut = {}
	for pkt in pkts:
		key = (pkt.sprintf("%IP.src%")).strip()
		for k in bad:
			if not (key == k):
				cut[key] = pkt.time
	#	temp = pkt.sprintf("%IP.src%,%IP.dst%,")
	#	cut = cut + temp

	return cut;