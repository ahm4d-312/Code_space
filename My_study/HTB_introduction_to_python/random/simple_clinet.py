import socket


def wait():
    input()


ip, port = "127.0.0.1", 4444
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print(f"1. Created the clinet object: {client}.")
wait()

msg = "Hello server"
print(f"2. Created the msg: '{msg}', of type:{type(msg)}")
wait()

print(
    f"Note: In order to send the msg, it must be converted to raw bytes since that the 'send' method only takes raw bytes parameters NOT str parmaeters"
)
wait()

msg_encoded = msg.encode("UTF-8")
print(f"3. encoded the msg to raw bytes: {msg_encoded}, of type: {type(msg_encoded)}")
wait()

client.sendto(msg_encoded, (ip, port))
print(f"4. sent the msg: '{msg}',to {ip}:{port}")
wait()

print("Listening")
response, address = client.recvfrom(1024)
print(f"5. Received: {response.decode("UTF-8")},from {address}")
wait()

client.close()
print("Finished")
