import socket
import time


class clientSocket:
    def __init__(self,port):
        self.HOST = '127.0.0.1'     # Endereco IP do Servidor
        self.PORT = port            # Porta que o Servidor esta
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.settimeout(0.5)
        

        self.isConnected = False

        
    def connect(self):
        if self.isConnected != True:
            while self.isConnected != True:
                try:
                    self.socket.connect((self.HOST, self.PORT))
                    self.isConnected = True
                    print("Conectou cliente na porta {}".format(self.PORT))
                except:
                    self.socket.close()
                    print("Tentou Conectar")
                    time.sleep(0.2)

    def sendData(self,data):
        data = str(data)
        self.socket.sendall(data.encode())

class serverSocket:
    def __init__(self,port):
        self.HOST = '127.0.0.1'
        self.PORT = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.orig = (self.HOST, self.PORT)
        self.socket.bind(self.orig)
        self.socket.listen(5)
        self.isConnected = False


        

    def getData(self,NData=1024*2):
        self.con.settimeout(0.5)
        try:
            return self.con.recv(NData).decode('utf-8')
        except:
            print(self.con)
    
    def openServer(self):
        if self.isConnected != True:
            while self.isConnected != True:
                try:
                    self.con, self.cliente = self.socket.accept()
                    self.isConnected = True
                    print("Conectou server na porta {}".format(self.PORT))
                except:
                    print("Tentou Conectar")
                    time.sleep(0.2)
