import socket
import threading
import random

def handle_client(clientSocket, peers):
    # Receive data from the client
    clientSocket.recv(1024)
    clientSocket.close()

def Server():
    # Get the number of peers from user input
    n = int(input("Enter the number of peers: "))
    
    # Create a list to store peer addresses
    peers = []
    
    # Set up the server socket
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind(('0.0.0.0', 9999))
    serverSocket.listen(n)
    
    print(f"Server listening on port 9999, waiting for {n} peers to connect...")
    
    # Accept connections from n peers
    for _ in range(n):
        client_socket, addr = serverSocket.accept()
        print(f"Accepted connection from {addr}")
        peers.append((client_socket, addr))
        client_handler = threading.Thread(target=handle_client, args=(client_socket, peers))
        client_handler.start()
    
    # Send a message to 1/4 of the peers with the IP address and port of a random peer. This means half of the peers will be assigned another human to talk to.
    humanConversations = n // 4
    msgdPeers = set()
    for _ in range(humanConversations):
        peerTwo = random.choice(peers)
        peerOne = random.choice(peers)
        msgdPeers.add(peerOne)
        msgdPeers.add(peerOne)
        outSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        outSocket.connect(peerOne[1])
        msg = f"{peerTwo[1][0]}:{peerTwo[1][1]},1"
        outSocket.send(msg.encode())
        outSocket.close()
        outSocket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        outSocket2.connect(peerOne[1])
        msg = f"{peerOne[1][0]}:{peerOne[1][1]},2"
        outSocket2.send(msg.encode())
        outSocket2.close()
    
    # Close communication with the messaged peers and the peers whose IP addresses were given
    for peer in msgdPeers:
        peer[0].close()
    
    serverSocket.close()


class Client:
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.peer_ip = None
        self.peer_port = None
        self.priority = None
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def connect_to_server(self):
        self.client_socket.connect((self.server_ip, self.server_port))
        print(f"Connected to server at {self.server_ip}:{self.server_port}")
    
    def receive_message(self):
        while(not message):
            message = self.client_socket.recv(1024).decode()
            peer_info, self.priority = message.split(',')
            self.peer_ip, self.peer_port = peer_info.split(':')
            self.peer_port = int(self.peer_port)
            self.priority = int(self.priority)
            print(f"Received message: {message}")
            print(f"Peer IP: {self.peer_ip}, Peer Port: {self.peer_port}, Priority: {self.priority}")
    
    def communicate_with_peer(self):
        peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        peer_socket.connect((self.peer_ip, self.peer_port))
        
        if self.priority == 1:
            self.send_message(peer_socket)
            self.receive_message_from_peer(peer_socket)
        else:
            self.receive_message_from_peer(peer_socket)
            self.send_message(peer_socket)
        
        peer_socket.close()
    
    def send_message(self, peer_socket):
        message = "Hello from client!"
        peer_socket.send(message.encode())
        print(f"Sent message: {message}")
    
    def receive_message_from_peer(self, peer_socket):
        message = peer_socket.recv(1024).decode()
        print(f"Received message: {message}")
    
    def start(self):
        self.connect_to_server()
        self.receive_message()
        self.communicate_with_peer()
        self.client_socket.close()