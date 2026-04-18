import socket
import threading
HOST, PORT = "0.0.0.0", 8005
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
clients = []
sock.listen(1000)
print("[SERVER STARTED]")
def client_handler(client_socket, address):
    while True:
        got_msg = client_socket.recv(1024).decode()
        client_socket.sendall(f"Server got: {got_msg}".encode())
        broadcast(client_socket, got_msg)
def broadcast(sender, msg):
    for cl in clients:
        if cl!= sender: 
            cl.sandall(msg.encode())
while True:
    client_socket, address = sock.accept()
    clients.append(client_socket)
    print(f"CLIENT CONNECTED {address}")
    thead = threading.Thread(target = client_handler, args=(client_socket, address), daemon=True)
    thead.start()
