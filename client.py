#!/usr/bin/env python3


import socket


HOST = '127.0.0.1'
PORT = 18737        # The port used by the server

print("My chat room client. Version One.\n")

input = input()
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(input.encode())
    data = s.recv(1024)

print('Received', repr(data))