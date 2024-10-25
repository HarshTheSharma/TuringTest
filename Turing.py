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
        clientSocket, clientAddr = serverSocket.accept()
        print(f"Accepted connection from {clientAddr}")
        peers.append((clientSocket, clientAddr))
        client_handler = threading.Thread(target=handle_client, args=(clientSocket, peers))
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
    def __init__(self, serverIP, serverPort):
        self.serverIP = serverIP
        self.serverPort = serverPort
        self.peerIP = None
        self.peerPort = None
        self.priority = None
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def connect_to_server(self):
        self.clientSocket.connect((self.serverIP, self.serverPort))
        print(f"Connected to server at {self.serverIP}:{self.serverPort}")
    
    def receive_message(self):
        while(not message):
            message = self.clientSocket.recv(1024).decode()
            peerInfo, self.priority = message.split(',')
            self.peerIP, self.peerPort = peerInfo.split(':')
            self.peerPort = int(self.peerPort)
            self.priority = int(self.priority)
            print(f"Received message: {message}")
            print(f"Peer IP: {self.peerIP}, Peer Port: {self.peerPort}, Priority: {self.priority}")
    
    def communicate_with_peer(self):
        peerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        peerSocket.connect((self.peerIP, self.peerPort))
        
        if self.priority == 1:
            self.send_message(peerSocket)
            self.receive_message_from_peer(peerSocket)
        else:
            self.receive_message_from_peer(peerSocket)
            self.send_message(peerSocket)
        
        peerSocket.close()
    
    def send_message(self, peerSocket):
        message = "Hello from client!"
        peerSocket.send(message.encode())
        print(f"Sent message: {message}")
    
    def receive_message_from_peer(self, peerSocket):
        message = peerSocket.recv(1024).decode()
        print(f"Received message: {message}")
    
    def start(self):
        self.connect_to_server()
        self.receive_message()
        self.communicate_with_peer()
        self.clientSocket.close()
