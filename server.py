import socket
import threading

import json

HOST, PORT = "0.0.0.0", 8005
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
clients = []
sock.listen(1000)
print("[SERVER STARTED]")
def client_handler(client_socket, address):
    while True:
        got_msg = client_socket.recv(1024).decode()

        if not got_msg:
            break
        
        #client_socket.sendall(f"Server got: {got_msg}".encode())

        dmsg = json.loads(got_msg)

        if dmsg.get("type") == "send_chat_msg":
            if dmsg.get("msg"):
                respond = {
                    "type":"chat_msg",
                    "msg":dmsg.get("msg")
                }

                broadcast(client_socket, json.dumps(respond))


def broadcast(sender, msg):
    for cl in clients:
        if cl!= sender: 
            cl.sendall(msg.encode())
while True:
    client_socket, address = sock.accept()
    clients.append(client_socket)
    print(f"CLIENT CONNECTED {address}")
    thead = threading.Thread(target = client_handler, args=(client_socket, address), daemon=True)
    thead.start()
