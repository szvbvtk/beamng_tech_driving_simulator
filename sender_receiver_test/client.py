import socket
import json

try:
    with open("server_config.json", "r") as config:
        config_data = json.load(config)
        host = config_data["host"]
        port = int(config_data["port"])
except FileNotFoundError:
    print("server_config.json not found")
    exit()


try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP
    client_socket.connect((host, port))  # connect to server
except ConnectionRefusedError:
    print("Server is not running")
    exit()

print(f"Connected to server at {host}:{port}")

while True:
    data = input("Enter data: ")
    client_socket.send(data.encode())
    if data == "exit":
        break

print("Closing connection...")
client_socket.close()
