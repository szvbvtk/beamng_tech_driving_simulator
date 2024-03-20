import socket
from beamngpy import BeamNGpy, Scenario, Vehicle
import json
import ast

tcp_ip = "127.0.0.1"
tcp_port = 4917

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((tcp_ip, tcp_port))

s.listen(1)

conn, addr = s.accept()

while True:
    data = conn.recv(1024)
    if data:
        print(data)
    if not data:
        break
    # print("received data:", data)
    py_obj = ast.literal_eval(data.decode("utf-8"))
    command = py_obj['command']

    # print(field_value)
    if command == "start-scenario":
        beamng = BeamNGpy(
            host="localhost",
            port=64256,
            home="D:\BeamNG.tech\BeamNG.tech.v0.31.2.0",
            user="D:\BeamNG.tech\BeamNG.tech.v0.31.2.0\Bin64",
        )
        beamng.open()

        scenario = Scenario("west_coast_usa", "example")
        # Create an ETK800 with the licence plate 'PYTHON'
        vehicle = Vehicle("ego_vehicle", model="etk800", license="PYTHON")
        # Add it to our scenario at this position and rotation
        scenario.add_vehicle(
            vehicle, pos=(-717, 101, 118), rot_quat=(0, 0, 0.3826834, 0.9238795)
        )

        scenario.make(beamng)

        # Load and start our scenario
        beamng.scenario.load(scenario)
        beamng.scenario.start()
    conn.send(data)
