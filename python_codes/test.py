import socket as s
import threading
import time

underline='\033[4m'
remove_underline='\033[24m'
color_block='\033[38;5;'
color_34=f'{color_block}34m'
color_75=f'{color_block}75m'
reset_colors='\033[0m'


def server_udp():
    server=s.socket(s.AF_INET,s.SOCK_DGRAM)
    ip,port='localhost',4444
    server.bind((ip,port))
    try:
        while True:
            msg,address=server.recvfrom(1024)
            print(f"{color_34}{msg.decode()}{reset_colors}",end='')
            if msg.decode()=="close":
                raise KeyboardInterrupt
            server.sendto(b"ACK",address)
    except KeyboardInterrupt:
        server.sendto(b"close",address)
        server.close()

def clinet_udp():
    clinet=s.socket(s.AF_INET,s.SOCK_DGRAM)
    ip,port='localhost',4444
    msg=b'hello'
    try:
        while True:
            time.sleep(0.2)
            clinet.sendto(msg,(ip,port))
            response,_=clinet.recvfrom(1024)
            print(f"    {color_75}{response.decode()}{reset_colors}")
            if response.decode()=="close":
                raise KeyboardInterrupt
    except KeyboardInterrupt:
        clinet.sendto(b"close",(ip,port))
        clinet.close()

def server_tcp():
    server=s.socket(s.AF_INET,s.SOCK_STREAM)
    ip,port='localhost',4445
    server.bind((ip,port))
    server.listen(1)
    client,_=server.accept()
    while True:
        msg=client.recv(1024)
        print(f"{color_34}{msg.decode()}{reset_colors}",end='')
        client.send(b"ACK")


def clinet_tcp():
    client=s.socket(s.AF_INET,s.SOCK_STREAM)
    ip,port='localhost',4445
    client.connect((ip,port))
    while True:
        time.sleep(0.2)
        msg=b'hello'
        client.send(msg)
        response=client.recv(1024)
        print('    ',response.decode(),sep='')

def port_scanner():
    scanner=s.socket(s.AF_INET,s.SOCK_STREAM)
    scanner.settimeout(1)
    scanner.connect_ex(())

def run_tcp():
    serv_tcp=threading.Thread(target=server_tcp,args=())
    cli_tcp=threading.Thread(target=clinet_tcp,args=())

    serv_tcp.start()
    cli_tcp.start()
def run_udp():
    serv_udp=threading.Thread(target=server_udp,args=())
    cli_udp=threading.Thread(target=clinet_udp,args=())

    serv_udp.start()
    cli_udp.start()

def main():
    port_scanner()


if __name__=='__main__':
    main()