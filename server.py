# Future Functionality:
# - remove repeating msgs when sending
# - be able to kick members only as admin
# - quit session
# - over the internet

# cd "C:\Users\chira\Personal Projects\ChatterBox"

# TODO:
# Add Function Specs and comments
# Organize my folders 
# implement write thread for server/or keep server as listen only and implement perms and roles for clients
# image/video sharing
# GUI using ttkinter

import threading
import socket

host = "127.0.0.1" #localhost
port = 55555

data_lock = threading.Lock()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host,port))
server.listen()

nicknames_client_dict = {}
HasAdmin = False
adminNickname = ""



def getClientByNickname(nickname):
    return nicknames_client_dict.get(nickname)

def getNicknameByClient(client):
    for nick in nicknames_client_dict.keys():
        if nicknames_client_dict.get(nick) == client:
            return nick
    return None 

# Sends a broadcast message to all of clients in the server
# message - the message you want to be broadcast to all of the clients (should be string)
def broadcast(message):
    with data_lock:
        for nick in nicknames_client_dict.keys():
            getClientByNickname(nick).send(message)

# Receives a message sent by a client and broadcasts it to all the other clients
# If there is an error receiving the message from a client (e.g. if the client incorrectly disconnects from the server)
# it disconnects the client and removes them and their nickname from their respectictive lists
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            messagechars = list(message.decode('ascii'))

            if HasAdmin and getNicknameByClient(client) == adminNickname:
                cmndid_idx = len(adminNickname) + 5
                if messagechars[cmndid_idx] == "/":
                    start_idx = cmndid_idx + 1
                    end_idx = start_idx
                    while end_idx < len(messagechars) and messagechars[end_idx] != " ":
                        end_idx += 1

                    cmnd = str(''.join(messagechars[start_idx:end_idx]))
                    nickname = str(''.join(messagechars[end_idx+1:len(messagechars)-1]))
                    adminPerms(cmnd, nickname)
                else:
                    broadcast(message)
            else:
                broadcast(message)
                
        except:

            with data_lock:
                nickname = getNicknameByClient(client)
                nicknames_client_dict.pop(nickname)
            client.close()
            broadcast(f"{nickname} left the chat...".encode('ascii'))
            break
        
def adminPerms(cmnd, nickname):
    if cmnd == "kick":
        kick(nickname)
    elif cmnd == "quit":
        quit()
    else:
        print("Invalid Command")

def kick(nickname):
    pass

def quit():
    pass

def receive():
    while True:
        client, address = server.accept()
        print(f"Connected established: {str(address)}")
        global adminNickname, HasAdmin
        isAdmin = False
        
        if HasAdmin:
            client.send("ADMIN_DUP".encode('ascii'))
            if (client.recv(1024).decode('ascii')) == "ADMIN_DUP_CONF":
                client.close()
                continue
        else:
            client.send("ADMIN".encode('ascii'))
            if (client.recv(1024).decode('ascii')) == "ADMIN_CONF":
                isAdmin = True
                HasAdmin = True

        client.send("NICK".encode('ascii'))  
        nickname = client.recv(1024).decode('ascii')
        print(f"Nickname of the client is {nickname}")
        if isAdmin:   
            adminNickname = nickname  

        attempts = 3
        while nickname in nicknames_client_dict.keys() and attempts != 0:
            client.send("NICK_DUP".encode('ascii'))   
            nickname = client.recv(1024).decode('ascii')       
            print(f"Nickname of the client is {nickname}")   
            if isAdmin:   
                adminNickname = nickname  
            attempts -= 1

        if attempts == 0:
            print("Too Many Attempts, Client Disconnected")
            client.close()
            continue

        nicknames_client_dict.update({nickname:client})

        broadcast(f"{nickname} joined the chat...".encode('ascii'))
        if isAdmin:
            print(f"{nickname} is the admin!")
        client.send("Connected to the server!".encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()            

              
print("Server is listening...")
receive()




