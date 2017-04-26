import scapy

pkts = rdpcap("data.pcap")

test = ""
for pkt in pkts:
	temp = pkt.sprintf("%IP.src%,%IP.dst%,")
	test = test + temp

print(test)