import socket

class Network():
    def __init__(self):
        self.client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server = "192.168.86.47"
        self.port = 5555
        self.addr = (self.server,self.port)
        self.pos = self.connect()

    def get_pos(self):
        return self.pos


    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(e)
    def send(self,data):
        try:
            self.client.send(str.encode(data))
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(e)


n = Network()
response = n.send("100,200")  # Send valid position data
if response:
    print(f"Server response: {response}")
response = n.send("")  # Send invalid data (empty string) for testing
if response:
    print(f"Server response: {response}")
