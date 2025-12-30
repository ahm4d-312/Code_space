import scapy.all as scapy
import time
request=scapy.ARP()

request.pdst='192.168.1.1/24'
broadcast=scapy.Ether()

broadcast.dst="ff:ff:ff:ff:ff:ff"

request_broadcast=broadcast/request
clients=scapy.srp(request_broadcast,timeout=1)
s=clients[0]
print(clients[1])
print(len(s))
#print(s[0],'\n\n\n',s[2])
count=0
for i in s:
    print(i[1].psrc+'\t'+i[1].hwsrc)
    count+=1
print(count,'\n--------')
count=0
for i in clients[1]:
    print(f'\r{i[1].pdst},\t{count}',end='',flush=True)
    count+=1
    time.sleep(0.05)
print()
print(count)