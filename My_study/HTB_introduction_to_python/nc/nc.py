import argparse
import textwrap
import sys
import socket
import threading
import subprocess
from os import chdir,path
import errno 
from colorama import init,Fore
init(autoreset=True)

def netcat_parser(sub_parser):
    netcat_parser=sub_parser.add_parser(
        'nc',
        description=Fore.LIGHTWHITE_EX+"My simple net tool"+Fore.MAGENTA,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(
            Fore.YELLOW+"""Example:
        nc.py -t 192.168.1.108 -p 5555 -lc\t#start a command shell (listener side)              
        nc.py -t 192.168.1.108 -p 5555 -c\t#start a command shell (sender side)

        nc.py -t 192.168.1.108 -p 5555 -lu\t#upload a file (listener side)
        nc.py -t 192.168.1.108 -p 5555 -u\t#upload a file (sender side)
        
        nc.py -t 192.168.1.108 -p 5555 -luc\t#upload a file and then start a shell (listener side)
        nc.py -t 192.168.1.108 -p 5555 -uc\t#upload a file and then start a shell (sender side)
        
        
        nc.py -t 192.168.1.108 -p 5555\t# connect to server

        The default ip is 0.0.0.0 and the default port is 5555
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
        description="Simple ARP spoofing tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(
        """Example:
        Will be added later
        """
        )
        )
    arp_parser.add_argument('-s','--sss',help="test")    

def execute(command):
    command=command.strip()
    if command[0:2]=="cd":
        try:
            chdir(command[2::].strip())
            return ""
        except FileNotFoundError as e:
                return str(e)+'\n'
        except:
            raise
    output = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    if output.stderr.decode():
        return output.stderr.decode()
    return output.stdout.decode()


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
        try:
            self.socket.connect((self.args.target, self.args.port))
        except OSError as e:
            if e.errno == errno.EISCONN:
                print(Fore.GREEN+str(e).split(maxsplit=2)[-1])
                pass
            else:
                raise

        if self.args.upload:
            client_thread=threading.Thread(target=self.handle,args=(self.socket,))
            client_thread.run()
        try:
            while True:
                buffer = input(Fore.LIGHTWHITE_EX+"> ")+"\n"
                self.socket.send(buffer.encode())
                if buffer=='exit\n':
                    print(Fore.RED+f"Connection Closed")
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
                    print(Fore.LIGHTBLUE_EX+response)

        except KeyboardInterrupt:
            print(Fore.RED+"user terminated.")
            self.exit()
        except BrokenPipeError:
            print(Fore.RED+f"The server is down")
            self.exit()
        except:
            raise

    def listen(self):
        self.socket.bind((self.args.target, self.args.port))
        self.socket.listen(1)
        
        clinet_socket = self.socket.accept()[0]
        client_thread = threading.Thread(target=self.handle, args=(clinet_socket,))
        client_thread.start()

    def handle(self, clinet_socket):
        if self.args.upload:
            if self.args.listen:
                try:
                    fname_len=int.from_bytes(Netcat.recv_exact(clinet_socket,4),'big')
                    fname=Netcat.recv_exact(clinet_socket,fname_len).decode()
                    f_len=int.from_bytes(Netcat.recv_exact(clinet_socket,8),'big')
                    with open(fname,'wb') as f:
                        received=0
                        while received<f_len:
                            chunk=clinet_socket.recv(min(4096,f_len-received))
                            if not chunk:
                                raise ConnectionError(Fore.RED+"Connection corrupted: The sender closed early")
                            received+=len(chunk)
                            f.write(chunk)
                        del(received)
                except ConnectionError as e:
                    print(Fore.RED+f"Upload failed: {e}")
                    if self.args.command:
                        return
                    self.exit()
                print(Fore.GREEN+"Done")
                if not self.args.command:
                    self.exit()

            else:
                fpath=input(Fore.MAGENTA+"path:").strip()
                fname=fpath.split('/')[-1]
                fname_len=len(fname.encode())
                fsize=path.getsize(fpath)
                clinet_socket.sendall(fname_len.to_bytes(4,'big'))
                clinet_socket.sendall(fname.encode())
                clinet_socket.sendall(fsize.to_bytes(8,'big'))
                try:
                    with open(fpath,'rb') as f:
                        sent=0
                        while True:
                            chunk=f.read(4096)
                            if not chunk:
                                break
                            clinet_socket.sendall(chunk)
                            sent+=len(chunk)
                            print(Fore.MAGENTA+f"\rSent: {(sent/fsize)*100:.2f}",end='',flush=True)
                        print()
                except Exception as e:
                    print(Fore.RED+f"Error: {e}")
                print(Fore.GREEN+"Done.")
                self.args.upload=False
                if self.args.command:
                    self.send()
                sys.exit()

        if self.args.command:
            cmd_buffer = b""
            while True:
                try:
                    while "\n" not in cmd_buffer.decode():
                        cmd_buffer += clinet_socket.recv(64)
                    response = cmd_buffer.decode()
                    if response.strip()=='exit':
                        print(Fore.RED+f"Connection closed.")
                        self.exit()
                    response=execute(response)
                    if not response:
                        response+='\n'
                    if response:
                        clinet_socket.send(response.encode())
                    cmd_buffer = b""
                except Exception as e:
                    print(Fore.RED+f"server killed {e}")
                    self.exit()
    @staticmethod                    
    def recv_exact(clinet_socket,length):
        data=b''
        while len(data)<length:
            chunk=clinet_socket.recv(length-len(data))
            if not chunk:
                print(Fore.RED+"Connection currpted!")
                break
            data+=chunk
        return data
    
    def exit(self):
        self.socket.close()
        sys.exit()

class Arp_spoofing:
    def __init__(self,args):
        self.args=args
    
    def tt(self):
        print("arp spoofing tool.")
    def __str__(self):
        return self.args


def main():

    parser = argparse.ArgumentParser(description="Choose what mode you wanna use:")
    sub_parsers=parser.add_subparsers(dest='mode',required=True)
    
    netcat_parser(sub_parsers)
    arp_parser(sub_parsers)

    args = parser.parse_args()

    if args.mode=='nc':
        buffer=''
        nc = Netcat(args, buffer.encode())
        nc.run()

if __name__ == "__main__":
    main()
