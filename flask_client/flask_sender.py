from flask import Flask, render_template, request, jsonify
import json
import threading
import time
import socket
import os
import signal


with open("./server_config.json", "r") as server_config_file:
    server_config = json.load(server_config_file)
    tcp_host = server_config["host"]
    tcp_port = server_config["port"]


app = Flask(__name__)
message = None
message_lock = threading.Lock()


def loop(run_event):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP
    client_socket.connect((tcp_host, tcp_port))  # connect to server
    print(f"Connected to server at {tcp_host}:{tcp_port}")
    global message
    while run_event.is_set():
        with message_lock:
            if message is not None:
                print("sending message: ", message)
                client_socket.send(str(message).encode())
                message = None

        time.sleep(1)


@app.route("/")
def index():
    return render_template("index.html")


# @app.route("/shutdown", defaults={"shutdown_delay": 5}, methods=["POST"])
# @app.route("/shutdown/<int:shutdown_delay>", methods=["POST"])
@app.route("/shutdown", methods=["POST"])
def shutdown():
    shutdown_delay = (
        int(request.form.get("shutdown_delay"))
        if request.form.get("shutdown_delay")
        else 5
    )
    threading.Thread(target=shutdown, args=(shutdown_delay,)).start()

    return render_template("shutdown.html", delay=shutdown_delay)


@app.route("/send", methods=["POST"])
def send():
    global message

    if request.method == "POST":
        data_from_input = request.form.get("data")

        with message_lock:
            message = data_from_input

        return jsonify({"message": message})


def web():
    app.run(debug=True, use_reloader=False, host="127.0.0.1", port=5000)


def shutdown(delay=0):
    global run_event
    run_event.clear()
    thread_loop.join()
    os.kill(os.getpid(), signal.SIGINT)
    thread_flask.join()


if __name__ == "__main__":
    run_event = threading.Event()
    run_event.set()
    thread_loop = threading.Thread(target=loop, args=(run_event,))
    thread_loop.start()

    thread_flask = threading.Thread(target=web, daemon=True)
    thread_flask.start()

    # wait for ctrl+c
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("KeyboardInterrupt received.")
        shutdown()
