import sys
import random
import socket
import threading
import PyQt5
import math
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit, QPushButton, QInputDialog
from PyQt5.QtGui import QPalette, QColor, QFont, QIcon
from PyQt5.QtCore import Qt

class TuringTest(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.peerColor = random.choice(['red', 'blue', 'yellow', 'magenta', 'orange', 'cyan'])
        self.msgCount = 0  # Initialize message count
        self.maxMsgCount = 20
        self.testMode = 0;
        self.myTurn = 1
        # get server IP and port
        server_ip, checkOutput = QInputDialog.getText(self, 'Server IP', 'Enter Server IP Address:')
        if not checkOutput: sys.exit()
        server_port, checkOutput = QInputDialog.getInt(self, 'Server Port', 'Enter Server Port Number:')
        if not checkOutput: sys.exit()
        if server_ip == "test" or server_ip == "Test":
            self.testMode = 1;
        if not self.testMode:
            # Connect to the server
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.connect((server_ip, server_port))
            # Receive peer's IP and port from the server
            peerInfo = self.server_socket.recv(1024).decode().split(':')
            if peerInfo[2] == "0":      #listen first
                self.myTurn = 0
                self.server_socket.close()
                # Start thread to listen for incoming messages
                self.listen_thread = threading.Thread(target=self.listen_for_messages)
                self.listen_thread.start()
                # Set connection to peer
                self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.client_socket.connect((peerInfo[0], int(peerInfo[1])))
            else:                       #talk first
                # Set connection to peer
                self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.client_socket.connect((peerInfo[0], int(peerInfo[1])))
                # Start thread to listen for incoming messages
                self.listen_thread = threading.Thread(target=self.listen_for_messages)
                self.listen_thread.start()
        if self.myTurn == 1: self.chat_display.append(f'<span style="color: {self.peerColor};">PEER </span>CONNECTED & <span style="color: green;">YOU </span> TYPE FIRST')
        else: self.chat_display.append(f'<span style="color: green;">YOU </span>CONNECTED & <span style="color: {self.peerColor};">PEER </span> TYPES FIRST')


    def initUI(self):
        self.setWindowTitle('Turing Test')
        self.setWindowIcon(QIcon('icon.png'))# Set icon
        QApplication.setWindowIcon(QIcon('icon.png'))
        self.resize(800, 600)  # Set the window size
        self.setMinimumSize(800, 600)
        # Set dark theme
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(10, 10, 10))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor(10, 10, 10))
        palette.setColor(QPalette.AlternateBase, QColor(10, 10, 10))
        palette.setColor(QPalette.ToolTipBase, Qt.white)
        palette.setColor(QPalette.ToolTipText, Qt.white)
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor(10, 10, 10))
        palette.setColor(QPalette.ButtonText, Qt.white)
        palette.setColor(QPalette.BrightText, Qt.red)
        palette.setColor(QPalette.Link, QColor(42, 42, 42))
        palette.setColor(QPalette.Highlight, QColor(42, 42, 42))
        palette.setColor(QPalette.HighlightedText, Qt.black)
        self.setPalette(palette)
        # Layouts & Widgets
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setStyleSheet("background-color: #262626; color: white; border: 1px solid white;")
        self.chat_display.setFont(QFont('Arial', 16))  # Set font size for chat display
        self.message_input = QLineEdit()
        self.message_input.setFont(QFont('Arial', 15))  # Set font size for input area
        self.message_input.setStyleSheet("background-color: #262626; color: white; border: 1px solid white;")
        self.send_button = QPushButton(' Send ')
        self.send_button.setFont(QFont('Arial', 15))  # Set font size for send button
        self.send_button.setStyleSheet("background-color: #262626; color: white; border: 1px solid white;")
        vbox.addWidget(self.chat_display)
        hbox.addWidget(self.message_input)
        hbox.addWidget(self.send_button)
        vbox.addLayout(hbox)
        self.setLayout(vbox)
        # Connect the send button and enter key.
        self.send_button.clicked.connect(self.send_message)
        self.message_input.returnPressed.connect(self.send_message)  # Use Enter to send message

    def send_message(self):
        if self.msgCount < self.maxMsgCount and self.myTurn:
            message = self.message_input.text()
            if message:
                self.chat_display.append(f'<span style="color: green;">YOU:</span> {message} <span style="color: gray;">[{math.floor(self.msgCount/2)+1}/10]</span>')
                self.message_input.clear()
                self.msgCount += 1
                self.myTurn = 0  # Switch turns
                if not self.testMode:
                    self.client_socket.send(message.encode())  # Send message
                else:
                    # What does recieving look like?
                    self.recv_message(f'Test response to: {message}')

    def recv_message(self, writeMessage):
        if self.msgCount < self.maxMsgCount:
            self.chat_display.append(f'<span style="color: {self.peerColor};">PEER:</span> {writeMessage} <span style="color: gray;">[{math.floor(self.msgCount/2)+1}/10]</span>')
            self.msgCount += 1
            self.myTurn = 1

    def listen_for_messages(self):
        while True:
            recvMessage = self.client_socket.recv(1024).decode()
            if recvMessage:
                self.recv_message(recvMessage)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    Turing_Test = TuringTest()
    Turing_Test.show()
    sys.exit(app.exec_())
