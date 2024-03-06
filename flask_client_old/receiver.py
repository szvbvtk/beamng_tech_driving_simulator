import socket

tcp_ip = '127.0.0.1'
tcp_port = 4917

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((tcp_ip, tcp_port))

s.listen(1)

conn, addr = s.accept()

while True:
    data = conn.recv(1024)
    if not data:
        break
    print("received data:", data)
    conn.send(data) 