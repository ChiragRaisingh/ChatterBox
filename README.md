
#🗨️ Chatter Box

Chatter Box is a terminal-based chat room application that allows multiple users to connect to a locally hosted server and chat in real time. It runs entirely on the same host, with support for multiple terminals.

There are two types of users:

Admin: Has control over the chat room (via admin.py)

General User: Can join and chat (via client.py)

#🧪 What It Does
Real-time group chat across terminals

Admin can:

/kick [username] – remove a user from the chat

/quit – shut down the server and disconnect everyone

Users can send and receive messages freely

#🧰 Files Overview
server.py – Starts the chat server

admin.py – Run this to join as an admin

client.py – Run this to join as a regular user

#🚀 How to Run
Start the server:

bash
Copy
Edit
python server.py
Open separate terminals depending on the role:

For an admin:

bash
Copy
Edit
python admin.py
For a general user:

bash
Copy
Edit
python client.py
🛠️ Planned Improvements
🌐 Let it work across a local network or the internet

🖥️ Add a graphical user interface (GUI)
