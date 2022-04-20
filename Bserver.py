import socket
from _thread import *
import pickle
from Bgame import Game
import hashlib

from Bnetwork import HEADERSIZE


server = "192.168.1.15" # set ip as current on network, check each time router crashes
port = 5555 #gib port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
hashTable = {}

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Please wait for connection")

connected = set()
games = {}
idCount = 0
HEADERSIZE = 10

def receive_data(sock):
    full_msg = b''
    new_msg = True
    while True:
        msg = sock.recv(16)
        if new_msg:
            msglen = int(msg[:HEADERSIZE])
            new_msg = False
        
        full_msg += msg

        if len(full_msg)-HEADERSIZE == msglen:
            data = pickle.loads(full_msg[HEADERSIZE:])
            break

    return data

def send_data(clientsocket, data):
    data_to_send = pickle.dumps(data)
    data_size = bytes(f'{len(data_to_send):<{10}}', "utf-8")
    try:
        clientsocket.send(data_size + data_to_send)

    except socket.error as e:
        print(e)


def threaded_client(conn, p, gameId):
    global idCount
    conn.send(str.encode(str(p)))

    login =True
    while login: # start login sytem with client
        UsrName = ('Enter Username: ')#setting messages
        UsrPass = ('Enter Password: ')
        UsrReg = ('Registration Successful')
        UsrConn = ('Connection successful')
        UsrDeni = ('Login failed')

        print('sending username request')
        send_data(conn, UsrName) # send username request
        print('Sending username request complete')
        name = receive_data(conn) # read data 
        print('name read')
        print(name) # print out name taken
        print('sending Password Request')
        send_data(conn, UsrPass) #sending out password request
        print('Sending password request complete')
        password = receive_data(conn) #take password and
        password=hashlib.sha256(str.encode(password)).hexdigest() #hash with SHA256

        if name not in hashTable: # if user pass not in table, register them
            hashTable[name]=password
            send_data(conn, UsrReg)
            print('Registered: ',name)
            print("{:<8} {:<20}".format('USER', 'PASSWORD'))
            for k, v in hashTable.items():
                lable, num = k,v
                print("{:<8} {:<20}".format(lable, num))
            print("-------------------------------------------")

        else:
            if(hashTable[name] == password): #if contained in table, connect them and exit login system
                send_data(conn, UsrConn)
                print('connected: ' ,name)
                
                login = False
            else:
                send_data(conn, UsrDeni) # if password wrong, send message saying connection died and restart loop
                print('connection denied ',name)

    reply = ""
    while True:
        try:
            data = receive_data(conn)

            if gameId in games:
                game = games[gameId]

                if not data:
                    break
                else:
                    if data == "reset":
                        game.resetWent()
                    elif data != "get":
                        game.play(p, data)

                    

                    send_data(conn, game)
            else:
                break
        except Exception as e:
            print("Failed try")
            print(e)
            break

    print("Lost connection")

    try:
        del games[gameId]
        print("ClosingGame", gameId)
    except:
        pass
    idCount -= 1
    conn.close()
    
while True:
    conn, addr = s.accept()
    print("Connected to: ", addr)

    idCount += 1
    p = 0
    gameId = (idCount - 1)//2
    if idCount % 2 == 1:
        games[gameId] = Game(gameId)
        print("creating a new game...")
    else:
        games[gameId].ready = True
        p = 1


    start_new_thread(threaded_client, (conn, p, gameId))

