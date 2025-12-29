import argparse
import textwrap
import sys
import socket
import threading
import subprocess
import shlex
from os import chdir,path
import errno 

def main():
    parser = argparse.ArgumentParser(
        description="My simple net tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(
            """Example:
        nc.py -t 192.168.1.108 -p 5555 -l -s\t#command shell               

        nc.py -t 192.168.1.108 -p 5555 -l -u=mytest.txt\t#upload to file

        nc.py -t 192.168.1.108 -p 5555 -l -e="cat /etc/passwd"\t# execute command 
        
        echo 'ABC' | ./nc.py -t 192.168.1.108 -p 135\t# echo text to server port 135
        
        nc.py -t 192.168.1.108 -p 5555\t# connect to server

        The default ip is 0.0.0.0 and the default port is 5555
        """
        ),
    )
    parser.add_argument("-s", "--shell", action="store_true", help="Starts a shell")
    parser.add_argument("-e", "--execute", help="execute specified command")
    parser.add_argument("-p", "--port", type=int, default=5555, help="specified port")
    parser.add_argument("-u", "--upload", action="store_true",help="upload file")
    parser.add_argument("-l", "--listen", action="store_true", help="listen")
    parser.add_argument("-t", "--target", default="0.0.0.0")

    args = parser.parse_args()
    if args.listen or sys.stdin.isatty():
        buffer = ""
    else:
        buffer = sys.stdin.raed()
    nc = Netcat(args, buffer.encode())
    nc.run()
    

def execute(command):
    command=command.strip()
    if command[0:2]=="cd":
        try:
            chdir(command[2::].strip())
            return ""
        except Exception as e:
                return str(e)+'\n'
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
            print(e)
            if e.errno == errno.EISCONN:
                pass
            else:
                raise 
        #if self.buffer:
        #    self.socket.send(self.buffer)
        if self.args.upload:
            client_thread=threading.Thread(target=self.handle,args=(self.socket,))
            client_thread.run()
        try:
            while True:
                buffer = input("> ")+"\n"
                self.socket.send(buffer.encode())
                recv_len = 1
                response = ""
                while recv_len:
                    data = self.socket.recv(4096)
                    recv_len = len(data)
                    response += data.decode()
                    if recv_len < 4096:
                        break
                if response:
                    print(response)

        except KeyboardInterrupt:
            print("user terminated.")
            self.socket.close()
            sys.exit() 

    def listen(self):
        self.socket.bind((self.args.target, self.args.port))
        self.socket.listen(5)
        while True:
            clinet_socket, client_address = self.socket.accept()
            del(client_address)
            client_thread = threading.Thread(target=self.handle, args=(clinet_socket,))
            client_thread.start()
    @staticmethod
    def recv_exact(clinet_socket,length):
        data=b''
        while len(data)<length:
            chunk=clinet_socket.recv(length-len(data))
            if not chunk:
                print("Connection currpted!")
                break
            data+=chunk
        return data
        

    def handle(self, clinet_socket):
        if self.args.execute:
            output = execute(self.args.execute)
            clinet_socket.send(output.encode())
        elif self.args.upload:
            # A way to receive file name and len as headers first then starting receiving the file 
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
                                raise ConnectionError("Connection corrupted: The sender closed early")
                            received+=len(chunk)
                            f.write(chunk)
                        del(received)
                except ConnectionError as e:
                    print("Upload failed: {e}")
                print("Done")

            else:
                fpath=input("path:").strip()
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
                            print(f"\rSent: {(sent/fsize)*100:.2f}",end='',flush=True)
                        print()
                except Exception as e:
                    print(f"Error: {e}")
                print("Done.")
                self.args.upload=False
                self.send()

        if self.args.shell:
            cmd_buffer = b""
            while True:
                try:
                    #clinet_socket.send(b"\n")
                    while "\n" not in cmd_buffer.decode():
                        cmd_buffer += clinet_socket.recv(64)
                    response = cmd_buffer.decode()
                    if response.strip()=='exit':
                        print(f"Connection closed.")
                        self.socket.close()
                        sys.exit()
                    response=execute(response)
                    if not response:
                        response+='\n'
                    if response:
                        clinet_socket.send(response.encode())
                    cmd_buffer = b""
                except Exception as e:
                    print(f"server killed {e}")
                    self.socket.close()
                    sys.exit()

class Arp_spoofing:
    def __init__(self,args):
        self.args=args
    
    def tt(self):
        print("arp spoofing tool.")
    def __str__(self):
        return self.args


if __name__ == "__main__":
    main()
