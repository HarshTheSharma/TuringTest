import Turing

if __name__ == "__main__":
    server_ip = input("Enter server IP: ")
    server_port = int(input("Enter server port: "))
    client = Turing.Client(server_ip, server_port)
    client.start()
