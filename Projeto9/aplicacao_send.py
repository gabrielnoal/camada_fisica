import socket
from tkinter import*
import time
from my_socket import *
class Application:
    def __init__(self,master=None):
        self.fontePadrao = ("Arial", "10")
        self.PORT = 1234            # Porta que o Servidor esta

        self.client = clientSocket(5000)
        self.client.connect()

#        self.server = serverSocket(1234)
#        self.server.openServer()


        """Inicia o primeiro container"""
        self.primeiroContainer = Frame(master)
        self.primeiroContainer["pady"] = 5
        self.primeiroContainer.pack()

        self.titulo = Label(self.primeiroContainer, text="Aplicação Envia")
        self.titulo["font"] = ("Arial", "10", "bold")
        self.titulo.pack()

        self.texto = Text(self.primeiroContainer)
        #self.texto.insert(END, "Server conectado na porta {} \n".format(self.server.PORT))
        self.texto.insert(END, "Cliente conectado na porta {} \n".format(self.client.PORT))
        
        self.texto["font"] = ("Arial", "10", "bold")
        self.texto["state"] = DISABLED
        self.texto.pack()
        """Finaliza o primeiro container"""

        

        """Inicia o segundo container"""
        self.segundoContainer = Frame(master)
        self.segundoContainer["padx"] = 20
        self.segundoContainer.pack()

        self.arquivoLabel = Label(self.segundoContainer, font=self.fontePadrao)
        self.arquivoLabel.pack()
        """Finaliza o segundo container"""


        """Inicia o terceiro container"""
        self.terceiroContainer = Frame(master)
        self.terceiroContainer["padx"] = 20
        self.terceiroContainer.pack()

        self.campoTexto = Entry(self.terceiroContainer)
        self.campoTexto.insert(END,"")
        self.campoTexto["width"] = 30
        self.campoTexto["font"] = self.fontePadrao
        self.campoTexto.pack()
        
        """Finaliza o terceiro container"""

        """Inicia o quarto container"""
        self.quartoContainer = Frame(master)
        self.quartoContainer["pady"] = 10
        self.quartoContainer.pack()

        self.buttonGet = Button(self.quartoContainer,command=self.getText)
        self.buttonGet["text"] = "Recebe Mensagem"
        self.buttonGet["font"] = ("Calibri", "8")
        self.buttonGet["width"] = 12
        self.buttonGet.pack(side=LEFT)
        

        self.buttonSend = Button(self.quartoContainer,command=self.sendText)
        self.buttonSend["text"] = "Envia Mensagem"
        self.buttonSend["font"] = ("Calibri", "8")
        self.buttonSend["width"] = 12
        self.buttonSend.pack(side=RIGHT)
        """Finaliza o quarto container"""


    def getText(self):
        try:
            self.texto["state"] = NORMAL
            #msg = self.server.getData()
            self.texto.insert(END,'Ele: ' + msg + '\n')
            self.texto["state"] = DISABLED
            
        except socket.timeout as e:
            print(e)

    def sendText(self):
        msg = self.campoTexto.get()
        self.campoTexto.delete(0,END)
        try:
            self.client.sendData(msg)
            print("enviou")
        except:
            pass
        self.texto["state"] = NORMAL
        self.texto.insert(END,"Eu: "+ msg +'\n')
        self.texto["state"] = DISABLED




root = Tk()
root.title("Send")
Application = Application(root)
root.mainloop()


          