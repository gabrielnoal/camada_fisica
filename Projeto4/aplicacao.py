#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#####################################################
# Camada Física da Computação
# Gabriel Noal e Warlen Rodrigues
#16/08/2018
#  Aplicação
####################################################

import aplicacao_receive
import aplicacao_send
import time
from tkinter import filedialog
from tkinter import*

#Método Seleciona arquivo


class Application:
    def __init__(self, app, master=None):
        self.app = app
        self.filePath = ""
        self.filename = ""
        self.fontePadrao = ("Arial", "10")

    
        

        if app == "send":
            """Inicia o primeiro container"""
            self.primeiroContainer = Frame(master)
            self.primeiroContainer["pady"] = 5
            self.primeiroContainer.pack()

            self.titulo = Label(self.primeiroContainer, text="Aplicação Envia")
            self.titulo["font"] = ("Arial", "10", "bold")
            self.titulo.pack()
            """Finaliza o primeiro container"""
            
            """Inicia o segundo container"""
            self.segundoContainer = Frame(master)
            self.segundoContainer["padx"] = 20
            self.segundoContainer.pack()

            self.arquivoLabel = Label(self.segundoContainer,text="Arquivo selecionado", font=self.fontePadrao)
            self.arquivoLabel.pack()
            """Finaliza o segundo container"""
    

            """Inicia o terceiro container"""
            self.terceiroContainer = Frame(master)
            self.terceiroContainer["padx"] = 20
            self.terceiroContainer.pack()


            self.campoTexto = Entry(self.terceiroContainer)
            self.campoTexto.insert(END,"Nenhum arquivo selecionado")
            self.campoTexto["state"] = DISABLED
            self.campoTexto["width"] = 30
            self.campoTexto["font"] = self.fontePadrao
            self.campoTexto.pack(side=LEFT)

            self.buttonSelecFile = Button(self.terceiroContainer, command=self.selectFile)
            self.buttonSelecFile["text"] = "Selecionar arquivo"
            self.buttonSelecFile["font"] = ("Calibri", "8")
            self.buttonSelecFile["width"] = 12
            self.buttonSelecFile.pack(side=RIGHT)
            """Finaliza o terceiro container"""
    
            """Inicia o quarto container"""
            self.quartoContainer = Frame(master)
            self.quartoContainer["pady"] = 10
            self.quartoContainer.pack()

            self.buttonSend = Button(self.quartoContainer,command=self.sendFile)
            self.buttonSend["text"] = "Enviar Arquivo"
            self.buttonSend["font"] = ("Calibri", "8")
            self.buttonSend["width"] = 12
            self.buttonSend.pack()
            """Finaliza o quarto container"""
          
  
        else:
            self.recieveFile()

    def selectFile(self):
        self.campoTexto["state"] = NORMAL
        self.filePath = filedialog.askopenfilename(initialdir = "./",title = "Select file",filetypes = (("all files","*"),("all files","*.*")))
        self.campoTexto.delete(0,'end')
        filename = self.filePath.split("/")
        self.filename = filename[-1]
        self.campoTexto.insert(END,self.filename)
        self.campoTexto["state"] = DISABLED
        pass

    def sendFile(self):
        #print(self.filePath)
        file_emoji = "/home/gabrielnoal/Documentos/INSPER/4o semestre/Camada Fisica/camada_fisica/Projeto4/emoji.jpg"
        aplicacao_send.main(self.filePath)
        pass
    
    def recieveFile(self):
        aplicacao_receive.main()
        pass



while True:
    send_or_receive = input("Precione S abrir a aplicação do send e R para abrir a aplicação do receive (S/r): ")
    if send_or_receive == "" or send_or_receive == "s":
        app = "send"
        break
    if send_or_receive == "r":
        app = "receive"
        break
    else:
        print("Input invalido")
        print("Digite S ou R")


root = Tk()
Application(app,root)
root.mainloop()