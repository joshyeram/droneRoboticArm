import sys
import socket
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('192.168.1.10', 59090))
print("connected")

while True:
    data = sock.recv(1024)
    print(data.decode('utf-8'))
    time.sleep(1)
    