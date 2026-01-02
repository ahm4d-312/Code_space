import scapy.all as scapy
import time
request=scapy.ARP()

request.pdst='172.20.10.1'
broadcast=scapy.Ether()

broadcast.dst="ff:ff:ff:ff:ff:ff"

request_broadcast=broadcast/request
clients=scapy.srp(request_broadcast,timeout=1)[0]
count=0
for i in clients:
    print(str(i[1].psrc)+'\t'+str(i[1].hwsrc))
    count+=1
print(len(clients),count)