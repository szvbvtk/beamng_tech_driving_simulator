import threading
import socket
import time
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

def receive_data(exit_event, main_loop_thread):
    while not exit_event.is_set():
        try:
            data = client_socket.recv(1024).decode()
        except socket.timeout:
            print("Connection timeout")
            exit()
            
        client_socket.send("zwrot".encode())
        if data == "exit":
            exit_event.set()
            break
        elif data == "play":
            main_loop_thread.start()

        print(f"data from client: {data}")
    
    main_loop_thread.join()

def main_loop(exit_event):
    while not exit_event.is_set():
        print("Main loop...")
        time.sleep(1)

# if __name__ == "__main__":
exit_event = threading.Event()
main_loop_thread = threading.Thread(target=main_loop, args=(exit_event,))
receive_data_thread = threading.Thread(target=receive_data, args=(exit_event, main_loop_thread))
receive_data_thread.start()
# main_loop_thread.start()

receive_data_thread.join()
# main_loop_thread.join()

print("Closing connection...")