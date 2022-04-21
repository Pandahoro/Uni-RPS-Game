from importlib.resources import Package
import socket
import pickle
HEADERSIZE = 10
hostName = socket.gethostname()
localIp = socket.gethostbyname(hostName)

class Network: #creating network class
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = localIp
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect()
       

    def getP(self):
        return self.p

    def connect(self):
        #try to connect, pass if cant
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except:
            pass
    # original network code caused following error "EOFerror: Ran out of input" so new solution was found
    #def send(self, data):
        #send validation
        #try:
            #self.client.send(str.encode(data))
            #return pickle.loads(self.client.recv(2048*2))
        #except socket.error as e:
            #print(e)

    def send_data(self, data):
        
        data_to_send = pickle.dumps(data)
        data_size = bytes(f'{len(data_to_send):<{10}}', "utf-8")
        try:
            self.client.send(data_size + data_to_send)
            package = self.receive_data()
            
            return package
        except socket.error as e:
            print(e)

    def Check_msg(self): # function to get what was sent for checking
        
        return Packagemsg
    


    def receive_data(self):
        full_msg = b''
        new_msg = True
        global Packagemsg
        while True:
            msg = self.client.recv(16)
            
            if new_msg:
                msglen = int(msg[:HEADERSIZE])
                new_msg = False
            
            full_msg += msg

            if len(full_msg)-HEADERSIZE == msglen:
                data = pickle.loads(full_msg[HEADERSIZE:])
                break
        Packagemsg = data      
        return data

