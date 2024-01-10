import socket
import json

with open("server_config.json", "r") as config:
    config_data = json.load(config)
    host = config_data["host"]
    port = config_data["port"]
    timeout = config_data["timeout"]

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP
server_socket.bind((host, port))  # bind socket to address and port
server_socket.listen(1)  # listen for incoming connections

if timeout > 0:
    server_socket.settimeout(timeout)  # set timeout
elif timeout == 0:
    server_socket.settimeout(None)  # infinite timeout
elif timeout < 0:
    print("Timeout cannot be negative")
    exit()

print(f"Waiting for connection at {host}:{port}")
try:
    client_socket, addr = server_socket.accept()  # accept connection from client
except socket.timeout:
    print("Connection timeout")
    exit()

print(f"Connected to client at {addr[0]}:{addr[1]}")

while True:
    data = client_socket.recv(1024).decode()
    if data == "exit":
        break
    print(f"data from client: {data}")

print("Closing connection...")

client_socket.close()
server_socket.close()
