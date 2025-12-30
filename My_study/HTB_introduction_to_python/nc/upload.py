import socket
from os import path 

def upload(clinet_socket):
    fpath=input('Path:').strip()
    fname=fpath.split('/')[-1]
    fname_len=len(fname.encode())
    fsize=path.getsize(fpath)
    clinet_socket.sendall(fname_len.to_bytes(4,'big'))
    clinet_socket.sendall(fname.encode())
    clinet_socket.sendall(fsize.to_bytes(8,'big'))
    try:
        with open(fpath,'rb') as f:
            while True:
                chunk=f.read(4096)
                if not chunk:
                    break
                clinet_socket.sendall(chunk)
    except Exception as e:
        print(f"Error: {e}")


def main():
    sender=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sender.connect((('localhost',1337)))
    upload(sender)
    
if __name__=='__main__':
    main()







