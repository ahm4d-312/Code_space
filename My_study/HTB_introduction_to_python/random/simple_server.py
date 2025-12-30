import socket


def wait():
    input()


ip, port = "127.0.0.1", 4444
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print(f"1. Created the server object: {server}.")
wait()

server.bind((ip, port))
print(f"2. Used bind method to assocaite the server with: {ip}:{port}")
wait()

print(f"Listening...")
response, address = server.recvfrom(1024)  # [msg , address]
print(f"3. Received the Msg: '{response.decode()}', from {address[0]}:{address[1]}")
wait()

msg = "Hello clinet"
print(f"4. Created the msg: '{msg}', of type:{type(msg)}")
wait()

print(
    f"Note: In order to send the msg, it must be converted to raw bytes since that the 'send' method only takes raw bytes parameters NOT str parmaeters"
)
wait()

msg_encoded = msg.encode("UTF-8")
print(f"5. encoded the msg to raw bytes: {msg_encoded}, of type: {type(msg_encoded)}")
wait()

server.sendto(msg_encoded, address)
print(f"6. sent the msg:{msg}, to: {address}")
wait()

server.close()
print("Finished")
