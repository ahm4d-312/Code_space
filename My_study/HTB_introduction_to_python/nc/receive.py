import socket
def receive(clinet_socket):
    try:
        fname_len=int.from_bytes(recv_exact(clinet_socket,4),'big')
        fname=recv_exact(clinet_socket,fname_len).decode()
        f_len=int.from_bytes(recv_exact(clinet_socket,8),'big')
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
        print(f"Upload failed: {e}")

def recv_exact(clinet_socket,length):
        data=b''
        while len(data)<length:
            chunk=clinet_socket.recv(length-len(data))
            if not chunk:
                print("Connection currpted!")
                break
            data+=chunk
        return data

def main():
    server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    server.bind(('localhost',1337))
    server.listen(1)
    clinet,addr=server.accept()
    receive(clinet)

if __name__=='__main__':
    main()