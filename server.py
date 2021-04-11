#!/usr/bin/env python3


#David Hannan
#4/9/21
#Chat room server program using socket api for CS850


import socket
import csv
from User import User
import pickle

HOST = '127.0.0.1'  
PORT = 18737        



def checkFunction(conn, data):
    #decode byte data and split the string into parts
    data = data.decode('utf-8')
    command = data.split()
    if command[0] == "newuser":
        #call funct to check if user already exists
        result = checkUserExists(command[1])
        if result == True:
            #if user does not exist call funct to create the new user
            newUser(conn,command[1], command[2])
        elif result == False:
            error = "Denied. User account already exists."
            conn.send(bytes(error,'utf-8'))
    elif command[0] == "login":
        #call login funct
        result = login(conn, command[1], command[2])
        if result == True:
            updateUserState(command[1], True)
            #get User obj and put in pickle to send to client
            logged = getUser(command[1])
            logged = pickle.dumps(logged)
            #header string to indicate login success to client
            header = bytes("login",'utf-8')
            #send header and userObj pickle to client
            conn.send(header + logged)
        elif result == False:
            conn.send(bytes("Denied. Username or password incorrect",'utf-8'))
    elif command[0] == "send":
        #split send command into 3 parts (2 spaces) (send,username,message content)
        command = data.split(" ", 2)
        #msg create and print to server
        msg = command[1] + ": " + command[2]
        print(msg)
        #send msg to client
        conn.send(bytes(msg,'utf-8'))
    elif command[0] == "logout":
        #make sure user can be logged out
        updateUserState(command[1], True)
        result = getUserState(command[1])
        if result == True:
            #make user logged in state false
            updateUserState(command[1], False)
            #msg and print to server
            msg = command[1] + " logout"
            print(msg)
            #send logout msg to client
            conn.send(bytes(command[1] + " left",'utf-8'))
        elif result == False:
            error = "Denied. Please login first"
    elif command[0] == "retry":
        #response for if no user is logged in
        conn.send(bytes("retrying",'utf-8'))


def checkUserExists(user):
    #iterate over users in array to check if the user exists
    for name in users:
        username = name.username
        if username == user:
            #user already exists
            return False
    
    return True
        

#func to put a new user into the users.txt file
def newUser(conn,username,passw):
    #open the file and format the new user entry
    File = open("users.txt", "a")
    entry = "\n(" + username + ", " + passw + ")"
    #add the new entry to the User list
    users.append(User(username, False))
    #add the entry on a newline to the file
    File.write(entry)
    File.close()
    #report success
    success = "New user account created. Please login."
    print("New user account created.")
    conn.send(bytes(success,'utf-8'))


#func to login a user
def login(conn,user,passw):
    #open the users file
    File = open("users.txt", "r")
    #iterate over users in the file, use csv to access parts of the entries
    reader = csv.reader(File, delimiter=',')
    for row in reader:
        #get a username entry
        username = row[0]
        #remove parenthesis
        username = username[1:]
        #compare user entered username with username in file
        if username == user:
            #if matched, get the password for the user
            recordPass = row[1]
            #remove parenthesis
            recordPass = recordPass[:-1]
            #remove leading space
            recordPass = recordPass[1:]
            #compare passwords
            if recordPass == passw:
                print(username, "login.")
                return True
    File.close()
    return False


#func to change user logged in status
def updateUserState(user, state):
    for name in users:
        username = name.username
        if username == user:
            name.logStatus = state


#func to get logged in state of user
def getUserState(user):
    for name in users:
        username = name.username
        if username == user:
            return name.logStatus


#get a specific User obj
def getUser(user):
    for name in users:
        username = name.username
        if username == user:
            return name


#create the User obj list
def usersInit():
    users = []
    #open users file
    File = open("users.txt", "r")
    reader = csv.reader(File, delimiter=',')
    #read in usernames
    for row in reader:
        username = row[0]
        username = username[1:]
        #create new Users with the usernames in the file
        users.append(User(username,False))
    File.close()
    return users


print("My chat room server. Version one.")

while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            data = conn.recv(1024)
            #initiate a list of all users
            users = usersInit()
            #send data from client to function to figure out what to do
            checkFunction(conn,data)
            conn.sendall(data)