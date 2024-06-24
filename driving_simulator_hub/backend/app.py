from flask import Flask, request, jsonify
from flask_cors import CORS
import threading
import socket
import json
import time
import sys
import signal
import os
from pathlib import Path
app = Flask(__name__)
CORS(app)

message = None
message_lock = threading.Lock()
received_message = None
received_message_lock = threading.Lock()
path = Path(__file__).parent
tcp_config = path / "tcp_config.json"


def tcp_connection():
    try:
        with open(tcp_config, "r") as config:
            config = json.load(config)
            tcp_host = config["tcp_host"]
            tcp_port = config["tcp_port"]

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(f"Connecting to server at {tcp_host}:{tcp_port}")
        client_socket.connect((tcp_host, tcp_port))
        print(f"Connected")

        return client_socket
    except Exception as e:
        sys.exit(f"Error connecting to server:, {str(e)}")

client_socket = tcp_connection()

def loop(run_event):
    global received_message

    global client_socket

    global message
    while run_event.is_set():
        with message_lock:
            if message is not None:
                print("sending message: ", message)
                client_socket.send(str(message).encode())
                received = client_socket.recv(1024).decode("utf-8")
                print("received: ", received)
                with received_message_lock:
                    received_message = received

                print("received_message: ", received_message)

                message = None

        time.sleep(1)


def web():
    app.run(debug=True, use_reloader=False, host="127.0.0.1", port=5000)


@app.route("/send-data", methods=["POST"])
def handle_data():
    global message
    global received_message
    data = request.json

    with message_lock:
        message = data

    print(data)
    while received_message is None:
        time.sleep(0.1)

    return jsonify(received_message)


if __name__ == "__main__":
    run_event = threading.Event()
    run_event.set()
    thread_loop = threading.Thread(target=loop, args=(run_event,))
    thread_loop.start()

    thread_flask = threading.Thread(target=web, daemon=True)
    thread_flask.start()

    def shutdown():
        global run_event
        run_event.clear()
        thread_loop.join()
        os.kill(os.getpid(), signal.SIGINT)
        thread_flask.join()
        

    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("KeyboardInterrupt received.")
        shutdown()
