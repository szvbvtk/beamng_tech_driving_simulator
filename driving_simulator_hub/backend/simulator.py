import socket
from beamngpy import BeamNGpy, Scenario, Vehicle
from beamngpy.sensors import Electrics
from collections import defaultdict
import json
import ast
import threading
import queue
import time
import sys
import os
from pathlib import Path

isGameRunning = False
isGameRunning_lock = threading.Lock()
vehicle_data = defaultdict(lambda: 0)
vehicle_data_lock = threading.Lock()
vehicle = None

path = Path(__file__).parent
tcp_config = path / "tcp_config.json"

def tcp_connection():
    try:
        with open(tcp_config, "r") as config:
            config = json.load(config)
            tcp_host = config["tcp_host"]
            tcp_port = config["tcp_port"]

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((tcp_host, tcp_port))
        s.listen(1)

        print(f"Waiting for connection at {tcp_host}:{tcp_port}")
        try:
            conn, addr = s.accept()  # accept connection from client
        except socket.timeout:
            sys.exit("Connection timeout")
        print("Connected")

        return conn
    except Exception as e:
        sys.exit(f"Error connecting to server:, {str(e)}")


data_queue = queue.Queue()

beamng = BeamNGpy(
    host="localhost",
    port=64256,
    home="D:\BeamNG.tech\BeamNG.tech.v0.31.2.0",
    user="D:\BeamNG.tech\BeamNG.tech.v0.31.2.0\Bin64",
)
beamng.open()

conn = tcp_connection()


def receive_data(exit_event, main_loop_thread):
    while not exit_event.is_set():
        try:
            data = conn.recv(1024).decode("utf-8")
        except socket.timeout:
            sys.exit("Connection timeout")
        except ConnectionResetError:
            sys.exit("Connection disconnected")

        data = ast.literal_eval(data)

        data_queue.put(data)


def parse_current_data(current_data):
    # current_data["speed"] = str(round(current_data["speed"] * 1.60934, 2)) + " km/h"
    current_data_json = json.dumps(current_data)
    # print(current_data_json)
    return current_data_json


def main_loop(exit_event):
    global isGameRunning
    global vehicle
    while not exit_event.is_set():
        print("Main loop...")
        data = data_queue.get()

        command = data["command"]
        payload = data["payload"]

        if command == "exit":
            conn.send("zwrot".encode())
            exit_event.set()
            break
        elif command == "start-scenario":
            if payload['scenarioId'] == 1:
                scenario_thread = threading.Thread(target=scenario_1_loop)
            elif payload['scenarioId'] == 2:
                scenario_thread = threading.Thread(target=scenario_2_loop)

            scenario_thread.start()
 

            while not isGameRunning:
                print("Waiting for game to start...")
                time.sleep(0.5)

            conn.send("zwrot".encode())
        elif command == "get-current-data":
            print("Get current data")
            # print(vehicle_data)
            current_data = vehicle_data.copy()
            print("current_data: ")
            print(current_data)
            current_data["speed"] = (
                str(round(current_data["speed"] * 1.60934, 2)) + " km/h"
            )
            # current_data["speed"] = 10
            current_data_json = parse_current_data(current_data)
            conn.send(current_data_json.encode())
        elif command == "stop-scenario":
            vehicle.logging.stop()
            beamng.close()
            conn.send("zwrot".encode())
            break

def scenario_2_loop():
    pass

def scenario_1_loop():
    global vehicle_data
    global vehicle
    global isGameRunning
    print("Scenario 1 loop...")
    scenario = Scenario("west_coast_usa", "example")
    # Create an ETK800 with the licence plate 'PYTHON'
    vehicle = Vehicle(vid="kkk", model="etk800", license="PYTHON")
    vehicle.sensors.attach("electrics", Electrics())
    # Add it to our scenario at this position and rotation
    scenario.add_vehicle(
        vehicle, pos=(-717, 101, 118), rot_quat=(0, 0, 0.3826834, 0.9238795)
    )

    scenario.make(beamng)

    # Load and start our scenario
    beamng.scenario.load(scenario)
    beamng.scenario.start()

    with isGameRunning_lock:
        isGameRunning = True
    print(isGameRunning)

    vehicle.logging.start("data")

    while True:
        # print("Scenario 1 loop...")
        time.sleep(1)
        with vehicle_data_lock:
            vehicle.sensors.poll()
            vehicle_data["speed"] = (
                vehicle.sensors["electrics"]["wheelspeed"] * 3.6 * 0.621371
            )

            vehicle_data["left_signal"] = vehicle.sensors["electrics"]["left_signal"]
            vehicle_data["right_signal"] = vehicle.sensors["electrics"]["right_signal"]
            vehicle_data["gear"] = vehicle.sensors["electrics"]["gear"]

            print(vehicle_data  )


if __name__ == "__main__":
    exit_event = threading.Event()

    main_loop_thread = threading.Thread(target=main_loop, args=(exit_event,))
    receiver_thread = threading.Thread(
        target=receive_data, args=(exit_event, main_loop_thread)
    )
    receiver_thread.start()
    main_loop_thread.start()

    def shutdown():
        exit_event.set()
        receiver_thread.join()
        main_loop_thread.join()
        conn.close()
        beamng.close()
        os.kill(os.getpid(), 9)

    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("KeyboardInterrupt received.")
        shutdown()
