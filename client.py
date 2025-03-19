import socket
import threading
import sys

# Create an event to signal threads to exit
exit_event = threading.Event()
nickname = input("Choose a nickname: ")

host = "127.0.0.1"  # localhost
port = 55555

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

# --- Handshake Section ---
while True:

    if exit_event.is_set():
            break

    try:
        message = client.recv(1024).decode('ascii')
    except Exception as e:
        print("Connection error:", e)
        exit_event.set()
        break

    if not message:
        print("Server closed the connection. Exiting...")
        exit_event.set()
        break
    
    if message == "ADMIN":
        client.send("CLIENT".encode('ascii'))

    elif message == "ADMIN_DUP":   
        client.send("CLIENT".encode('ascii'))

    elif message == 'NICK':
        client.send(nickname.encode('ascii'))

    elif message == 'NICK_DUP':         
        nickname = input("Duplicate nickname found, choose another nickname: ")
        client.send(nickname.encode('ascii'))

    elif message == "Connected to the server!":
        print(message)
        break
    
    else:
        print(message)

# If handshake failed, close the client and exit
if exit_event.is_set():
    client.close()
    sys.exit()

def receive():
    while not exit_event.is_set():
        try:
            message = client.recv(1024).decode('ascii')
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
            message = f"{nickname}: {msg}"
            client.send(message.encode('ascii'))
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

client.close()
sys.exit()
