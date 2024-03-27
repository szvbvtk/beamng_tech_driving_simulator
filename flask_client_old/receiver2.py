import socket
from beamngpy import BeamNGpy, Scenario, Vehicle
import json
import ast
import threading
import queue

tcp_ip = "127.0.0.1"
tcp_port = 4917

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((tcp_ip, tcp_port))
s.listen(1)

print(f"Waiting for connection at {tcp_ip}:{tcp_port}")
try:
    conn, addr = s.accept()  # accept connection from client
except socket.timeout:
    print("Connection timeout")
    exit()

data_queue = queue.Queue()


def receive_data(exit_event, main_loop_thread):
    while not exit_event.is_set():
        try:
            data = conn.recv(1024).decode()
        except socket.timeout:
            print("Connection timeout")
            exit()

        conn.send("zwrot".encode())
        data = ast.literal_eval(data.decode("utf-8"))

        data_queue.put(data)


def main_loop(exit_event):
    while not exit_event.is_set():
        print("Main loop...")
        data = data_queue.get()
        command = command["command"]
        payload = command["payload"]

        if command == "exit":
            exit_event.set()
            break
        elif command == "start-scenario":
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


exit_event = threading.Event()

main_loop_thread = threading.Thread(target=main_loop, args=(exit_event,))
receiver_thread = threading.Thread(
    target=receive_data, args=(exit_event, main_loop_thread)
)
receiver_thread.start()
main_loop_thread.start()
