import socket
from _thread import *
import sys

server = "192.168.86.47"
port = 5555

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

try:
    s.bind((server,port))
except socket.error as e:
    str(e)
    sys.exit()


s.listen(2)
print(f"Waiting for a connection. Server Started on : {server}:{port}")

def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1])

def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])

pos = [(0,0),(100,100)]

def threaded_client(conn,player):
    conn.send(str.encode(make_pos(pos[player])))
    
    reply = ""

    while True:
        try:
            data = read_pos(conn.recv(2048).decode())
            pos[player] = data


            if not data:
                print("Disconnected")
                break
            else:
                if player == 1:
                    reply = pos[0]
                else:
                    reply = pos[1]
                print(f"received: {data}")
                print(f"sending: {reply}")
            conn.sendall(str.encode(make_pos(reply)))
        except socket.error as e:
            print(e)
    print("Lost connection")
    conn.close()

currentplayer = 0



while True:
    conn,address = s.accept()
    print(f"Connected to:{address}")

    start_new_thread(threaded_client,(conn,currentplayer))
    currentplayer += 1