#!/usr/bin/env python3

#David Hannan
#4/9/21
#Chat room client program using socket api for CS850


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
            #check for proper command usage
            if len(commandParts) == 3:
                #send login command to server
                s.send(bytes(command,'utf-8'))
                #receive response from server
                
                response = s.recv(1024)
                #decode header bytes
                result = response[:5]
                result = result.decode('utf-8')
                if result == "login":
                    #if header bytes match, get the user pickle
                    userObj = response[5:]
                    #unpickle User
                    userLogged = pickle.loads(userObj)
                    print("login confirmed")
                else:
                    #header bytes dont match, print error response
                    print(response.decode('utf-8'))
                
            else:
                print("Command usage: login <user> <pass>")
                s.send(bytes("retry",'utf-8'))
                response = s.recv(1024)
                response = response.decode('utf-8')
        elif commandParts[0] == "logout":
            #check for proper command usage
            if len(commandParts) == 1:
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
            else:
                print("Command usage: logout")
                command = "retry"
                s.send(bytes(command,'utf-8'))
                response = s.recv(1024)
                response = response.decode('utf-8')
        elif commandParts[0] == "send":
            #make sure a user is logged in
            if userLogged and userLogged.logStatus == True:
                #split the send command to keep the message content together
                sendMsg = command.split(" ", 1)
                #check for proper send usage
                if len(sendMsg) == 2 and sendMsg[0] == "send":
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
                    print("Command usage: send <message>")
                    command = "retry"
                    s.send(bytes(command,'utf-8'))
                    response = s.recv(1024)
                    response = response.decode('utf-8')
            else:
                #handle if no user is logged in
                print("Denied. Please login first.")
                command = "retry"
                s.send(bytes(command,'utf-8'))
                response = s.recv(1024)
                response = response.decode('utf-8')
        elif commandParts[0] == "newuser":
            #check for proper newuser usage
            if len(commandParts) == 3:
                s.send(bytes(command,'utf-8'))
                response = s.recv(1024)
                response = response.decode('utf-8')
                print(response)
            else:
                print("Command usage: newuser <username> <password>")
                command = "retry"
                s.send(bytes(command,'utf-8'))
                response = s.recv(1024)
                response = response.decode('utf-8')
        else:
            #catch invalid commands
            print("Invalid Command. Potential commands are:")
            if userLogged.logStatus == True:
                print("send <message>\nlogout")
            elif userLogged.logStatus == False:
                print("newuser <username> <password>\nlogin <username> <password>")
            command = "retry"
            s.send(bytes(command,'utf-8'))
            response = s.recv(1024)
            response = response.decode('utf-8')
            
        