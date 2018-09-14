#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#####################################################
# Camada Física da Computação
#Carareto
#17/02/2018
#  Camada de Enlace
####################################################

# Importa pacote de tempo
import time

# Construct Struct
#from construct import *

# Interface Física
from interfaceFisica import fisica

# enlace Tx e Rx
from enlaceRx import RX
from enlaceTx import TX

class enlace(object):
    """ This class implements methods to the interface between Enlace and Application
    """

    def __init__(self, name):
        """ Initializes the enlace class
        """
        self.fisica      = fisica(name)
        self.rx          = RX(self.fisica)
        self.tx          = TX(self.fisica)
        self.connected   = False
        self.payload     = b'\x00'
        self.package     = None
        self.dataSize    = 0    
        self.headSize    = 16
        self.clientSynchComplete = False
        self.serverSynchComplete = False

        self.mensagemTipo1 = {'enviada': False , 'recebida': False}
        self.mensagemTipo2 = {'enviada': False , 'recebida': False}
        self.mensagemTipo3 = {'enviada': False , 'recebida': False}
        self.mensagemTipo4 = {'enviada': False , 'recebida': False}
        self.mensagemTipo5 = {'enviada': False , 'recebida': False}
        self.mensagemTipo6 = {'enviada': False , 'recebida': False}
        self.mensagemTipo7 = {'enviada': False , 'recebida': False}



    def enable(self):
        """ Enable reception and transmission
        """
        self.fisica.open()
        self.rx.threadStart()
        self.tx.threadStart()

    def disable(self):
        """ Disable reception and transmission
        """
        self.rx.threadKill()
        self.tx.threadKill()
        time.sleep(1)
        self.fisica.close()

        

    ################################
    # Application  interface       #
    ################################
    def sendData(self, data):
        """ Send data over the enlace interface
        """
        self.tx.sendBuffer(data)


    def getData(self, last_message=0):
        """ Get n data over the enlace interface
        Return the byte array and the size of the buffer
        """
        # print('entrou na leitura e tentara ler ' + str(size) )
        
        data = self.rx.getNData()
        if data == 0:
            data = self.tx.createPACKAGE(0)
            messageType = self.checkMessageType(data,last_message)
        else:
            messageType = self.checkMessageType(data) #Verifica o tipo da mensagem no buffer
        payloadSize = 1
        if messageType == 4:
            #print(data)
            recievePack = data
            self.packageNumber, self.packageTotal, self.erro8, self.packageExpected, self.dataSize, self.data = self.rx.unpackage(recievePack)
            self.checkAcknoledgement(self.data, self.dataSize)
            return self.data, len(self.data), self.dataSize

        

        return data, len(data), payloadSize
    
    def findEOP(self, dados):
        EOPbytes = 129
        EOPbytes = EOPbytes.to_bytes(4, byteorder="big")
        print("EOP: {}".format(EOPbytes))
        achou = False
        for byte in dados:
            #print(byte)
            if byte == EOPbytes:
                achou = True
                print("EOPbytes encontrado no index {}".format(dados.index(byte)))
        
        if not achou:
            print("[ERRO] - EOPbytes NOT ENCONTRADO")
        print("Tamanho dos dados: {}".format(len(dados)))
        pass

    def clientSynch(self):
        # Cria pacote vazio com mensagem tipo 1
        pack1 = self.tx.createPACKAGE(1)
        while self.mensagemTipo2['recebida'] == False:
            
            # Envia mensagem tipo 1
            self.sendData(pack1)
            print("Mensagem tipo 1: Enviada")
            time.sleep(0.1)

    

            self.getData(1) # Le o Buffer de recebimento
            timeout = self.rx.timeout
            if timeout >= 5:
                print("[ERRO] - Não recebimento da mensagem tipo 2")
                return
        #Cria pacote vazio com mensagem tipo 3    
        pack3 = self.tx.createPACKAGE(3)
        # Envia mensagem tipo 3
        self.sendData(pack3)
        print("Mensagem tipo 3: Enviada")
        self.mensagemTipo3['enviada'] == True
        self.clientSynchComplete = True

    def serverSynch(self):
        while self.mensagemTipo1['recebida'] == False:
            time.sleep(0.1)
            self.getData()
        
        # Cria pacote vazio com mensagem tipo 2
        pack2 = self.tx.createPACKAGE(2)
        self.sendData(pack2)
        print("Mensagem tipo 2: Enviada") # Envia mensagem tipo 2

        time.sleep(0.1)
        while self.mensagemTipo3['recebida'] == False:
            self.getData(2)
            timeout = self.rx.timeout
            if timeout >= 5:
                print("[ERRO] - Não recebimento da mensagem tipo 3")
                return
        self.serverSynchComplete = True


    def clientSendFile(self, file):
        time.sleep(0.2)
        pack = self.tx.createPACKAGE(4, file)
        #print(pack)
        self.rx.unpackage(pack)
        self.sendData(pack)
        self.mensagemTipo4['enviada'] = True

        time.sleep(0.2)
        while self.mensagemTipo5['recebida'] == False:
            data , size, payloadSize = self.getData(4)
            timeout = self.rx.timeout
            if timeout >= 5:
                print("[ERRO] - Não recebimento da mensagem tipo 5 ou 6")
                return
            if self.mensagemTipo6["recebida"] == True:
                self.sendData(pack)
                print("Mensagem tipo 4 enviada novamente")


    def checkAcknoledgement(self, data, payloadSize):
        print("Len data: {}  PayloadSize: {}".format(len(data), payloadSize))
        if len(data) == payloadSize:
            mensagemTipo5 = self.tx.createPACKAGE(5)
            self.sendData(mensagemTipo5)
            self.mensagemTipo5['enviada'] = True
            print("Mensagem tipo 5 enviada")
            
        else:
            mensagemTipo6 = self.tx.createPACKAGE(6)
            self.sendData(mensagemTipo6)
            self.mensagemTipo5['enviada'] = True
            print("Mensagem tipo 6 enviada")


    def checkMessageType(self,message,last_message=0):
        messageType = 0
        try:
            messageType = message[9]
        except:
            print("DEU RUIM AQUI")
        print(messageType)
        
        if messageType == 0 and last_message != 0:
            if last_message == 4:
                print("[ERRO] - Não recebimento da mensagem tipo 5 ou 6")
            else:
                print("[ERRO] - Não recebimento da mensagem tipo {}".format(last_message+1))


        if messageType == 1:
            print("Mensagem tipo 1: Recebida")
            self.mensagemTipo1['recebida'] = True

        elif messageType == 2:
            print("Mensagem tipo 2: Recebida")
            self.mensagemTipo2['recebida'] = True

        elif messageType == 3:
            print("Mensagem tipo 3: Recebida")
            self.mensagemTipo3['recebida'] = True
        
        elif messageType == 4:
            print("Mensagem tipo 4: Recebida")
            self.mensagemTipo4['recebida'] = True
            return 4
        elif messageType == 5:
            print("Mensagem tipo 5: Recebida")
            self.mensagemTipo5['recebida'] = True
            self.sendEndingMassage()
            return 5
            
        elif messageType == 6:
            print("Mensagem tipo 6: Recebida")
            self.mensagemTipo6['recebida'] = True
            return 6

        elif messageType == 7:
            # Encerra comunicação
            print("Mensagem tipo 7: Recebida")
            print("-------------------------")
            print("Comunicação encerrada")
            print("-------------------------")
            self.mensagemTipo7['recebida'] = True
            self.disable()    
        else:
            pass
            #print("ERROR: Mensagem tipo {}".format(messageType))
            #print("ERROR: Ultima Mensagem {}".format(last_message))

    def sendEndingMassage(self):
        pack7 = self.tx.createPACKAGE(7)
        self.sendData(pack7)
        self.mensagemTipo7['enviada'] = True
        print("Mensagem tipo 7: Enviada")
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        self.disable()

    