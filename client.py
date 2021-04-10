#!/usr/bin/env python3

#David Hannan
#4/9/21
#Chat room client program for CS850


import socket
import pickle
from User import User


HOST = '127.0.0.1'
PORT = 18737        # The port used by the server

print("My chat room client. Version One.\n")

userLogged = User("init",False)

while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        #get user input
        command = input()
        #split user input into parts on spaces
        commandParts = command.split()

        #if statement to check for login, logout, and send commands
        if commandParts[0] == "login":
            #send login command to server
            s.send(bytes(command,'utf-8'))
            #receive user object in a pickle for later use
            userLogged = s.recv(1024)
            #unpickle User
            userLogged = pickle.loads(userLogged)
            print("login confirmed")
        elif commandParts[0] == "logout":
            #make sure a user is logged in
            if userLogged and userLogged.logStatus == True:
                #use User object to tell the server which user to logout
                msg = commandParts[0] + " " + userLogged.username
                s.send(bytes(msg,'utf-8'))
                response = s.recv(1024)
                #get logout response and close socket connection
                response = response.decode('utf-8')
                print(response)
                s.close
                break
            else:
                #handle if no user is logged in
                print("Denied. Please login first.")
                command = "retry"
                s.send(bytes(command,'utf-8'))
                response = s.recv(1024)
                response = response.decode('utf-8')
        elif commandParts[0] == "send":
            #make sure a user is logged in
            if userLogged and userLogged.logStatus == True:
                #split the send command to keep the message content together
                sendMsg = command.split(" ", 1)
                #insert the username into the command to send to the server
                sendMsg.insert(1,userLogged.username)
                sendStr = ""
                #put the send command together and send to server
                for ele in sendMsg:
                    sendStr += ele + " "
                s.send(bytes(sendStr,'utf-8'))
                response = s.recv(1024)
                response = response.decode('utf-8')
                print(response)
            else:
                #handle if no user is logged in
                print("Denied. Please login first.")
                command = "retry"
                s.send(bytes(command,'utf-8'))
                response = s.recv(1024)
                response = response.decode('utf-8')
        else:
            #handle for newuser command since it doesnt need anything special
            s.send(bytes(command,'utf-8'))
            response = s.recv(1024)
            response = response.decode('utf-8')
            print(response)
            
        