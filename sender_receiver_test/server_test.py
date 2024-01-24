import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("127.0.0.1", 4917))
server.listen()

conn, addr = server.accept()
print(f"Połączono z {addr}")

# data = conn.recv(1024)

# print(f"Otrzymano dane: {data.decode('utf-8')}")
while True:
    data = conn.recv(1024)
    if not data:
        break
    print(f"Otrzymano dane: {data.decode('utf-8')}")

conn.close()
