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
    client_socket.send("zwrot".encode())
    if data == "exit":
        break
    elif data == "play":
        from beamngpy import BeamNGpy, Scenario, Vehicle

        beamng = BeamNGpy(
            host="localhost",
            port=64256,
            home="D:\BeamNG.tech\BeamNG.tech.v0.31.2.0",
            user="D:\BeamNG.tech\BeamNG.tech.v0.31.2.0\Bin64",
        )
        beamng.open()

        scenario = Scenario("pejas_coast", "Mountain Race")
        vehicle = Vehicle("ego_vehicle", model="etk800", license="PEJAS")
        # Add it to our scenario at this position and rotation
        scenario.add_vehicle(
            vehicle, pos=(-717, 101, 118), rot_quat=(0, 0, 0.3826834, 0.9238795)
        )
        # Place files defining our scenario for the simulator to read
        scenario.make(beamng)
        # 010.734|I|GELua.tech_techCore.TechGE|Accepted new client: 127.0.0.1/64189

        # Load and start our scenario
        beamng.scenario.load(scenario)
        beamng.scenario.start()
        # Make the vehicle's AI span the map
        # vehicle.ai.set_mode("span")
        x = input("Hit enter when done...")
        if x is not None:
            beamng.close()

    print(f"data from client: {data}")

print("Closing connection...")

client_socket.close()
server_socket.close()
