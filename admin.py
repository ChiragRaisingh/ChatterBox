import threading
import socket
import sys


host = "127.0.0.1"  # localhost
port = 55555



admin = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
admin.connect((host, port))    


exit_event = threading.Event()
nickname = input("Choose a nickname: ")

while True:

    if exit_event.is_set():
        break

    try:
        message = admin.recv(1024).decode('ascii')
    except Exception as e:
        print("Connection error:", e)
        exit_event.set()
        break

    if not message:
        print("Server closed the connection. Exiting...")
        exit_event.set()
        break

    if message == "ADMIN_DUP":
        print("Admin already exists. Exiting...")
        admin.send("ADMIN_DUP_CONF".encode('ascii'))
        exit_event.set()
        break

    elif message == "ADMIN":
        attempts = 3
        while attempts != 0:
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            if username == "admin" and password == "123":
                admin.send("ADMIN_CONF".encode('ascii'))
                break
            else:
                print("Invalid username or password")
                attempts -= 1
                if attempts == 0:
                    print("Too many attempts.")
                    exit_event.set()
                    break   

    elif message == 'NICK':
        admin.send(nickname.encode('ascii'))

    elif message == 'NICK_DUP':
        nickname = input("Duplicate nickname found, choose another nickname: ")
        admin.send(nickname.encode('ascii'))

    elif message == "Connected to the server!":
        print(message)
        break

    else:
        print(message)


if exit_event.is_set():
    admin.close()
    sys.exit()


def receive():
    while not exit_event.is_set():
        try:
            message = admin.recv(1024).decode('ascii')
            if not message:
                print("Server closed the connection.")
                exit_event.set()
                break
            print(message)
        except Exception as e:
            print("Error in receive thread:", e)
            exit_event.set()
            break

def write():
    while not exit_event.is_set():
        try:
            # Note: input() is blocking. This thread might not exit immediately
            # if it's waiting for input, but it will exit after input() returns.
            msg = input()
            if exit_event.is_set():
                break
            message = f"{nickname}(A): {msg}"
            admin.send(message.encode('ascii'))
        except Exception as e:
            print("Error in write thread:", e)
            exit_event.set()
            break

# Create threads for receiving and writing messages
receiveThread = threading.Thread(target=receive)
writeThread = threading.Thread(target=write)

receiveThread.start()
writeThread.start()

# Wait for both threads to finish before closing the program
receiveThread.join()
writeThread.join()

admin.close()
sys.exit()





# Kicks a client from the server
# nickname - nickname of client you want to kick

# def kick(nickname):
#     if nickname in nicknames_client_dict.keys():
#         client = nicknames_client_dict.get(nickname)
#         client.send("You were kicked from the chat! womp womp")
#         client.close()
#         clients.remove(client)
#         nicknames.remove(nickname)
#         nicknames_client_dict.pop(nickname)
#         broadcast("f{nickname} was kicked!")