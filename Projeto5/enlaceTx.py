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
import numpy as np
import binascii
import struct

# Threads
import threading

# Class
class TX(object):
    """ This class implements methods to handle the transmission
        data over the p2p fox protocol
    """

    def __init__(self, fisica):
        """ Initializes the TX class
        """
        self.fisica      = fisica
        self.buffer      = bytes(bytearray())
        self.transLen    = 0
        self.empty       = True
        self.threadMutex = False
        self.threadStop  = False
        self.package     = None
        self.EOP         =  fisica.EOP
        self.headSize    = 16
        self.payload     = b'\x00'

    def thread(self):
        """ TX thread, to send data in parallel with the code
        """
        while not self.threadStop:
            if(self.threadMutex):
                self.transLen    = self.fisica.write(self.buffer)
                #print("O tamanho transmitido. IMpressao dentro do thread {}" .format(self.transLen))
                self.threadMutex = False

    def threadStart(self):
        """ Starts TX thread (generate and run)
        """
        self.thread = threading.Thread(target=self.thread, args=())
        self.thread.start()

    def threadKill(self):
        """ Kill TX thread
        """
        self.threadStop = True

    def threadPause(self):
        """ Stops the TX thread to run

        This must be used when manipulating the tx buffer
        """
        self.threadMutex = False

    def threadResume(self):
        """ Resume the TX thread (after suspended)
        """
        self.threadMutex = True

    def calcOverHead(self, payload):
        overHead = (self.headSize + len(payload) + len(self.EOP)/len(payload))
        print("Overhead: {}%".format(overHead))
        return overHead
        
        
    def createHEAD(self, msg_type, payload, packageNum, packageTotal , error8, packageExpected):
        packageNum = (packageNum).to_bytes(1, byteorder="big") #Numero do pacote em bytes
        packageTotal = (packageTotal).to_bytes(1, byteorder="big") #Numero total do pacote em bytes
        error8 = (error8).to_bytes(1, byteorder="big") #Erro tipo 8. False se 0, True se 1.
        packageExpected = (packageExpected).to_bytes(1, byteorder="big") #Numero do pacote que era pra chegar em bytes
        msg_type = (msg_type).to_bytes(1, byteorder="big") #Tipo de mensagem em 1 bytes         
        overHead = self.calcOverHead(payload) # Calcula o overhead
        overHead_bytes = round(overHead).to_bytes(2, byteorder="big") #Transforma o overhead em 2 bytes
        payloadSize = len(payload) # Tamanho do dado a ser transmitido
        payloadSize_bytes = payloadSize.to_bytes(4, byteorder="big") #Transforma o payloadSize em 4 bytes
        headSize = (self.headSize - (len(packageNum) + len(packageTotal) + len(error8) + len(packageExpected) + len(msg_type) + len(payloadSize_bytes) + len(overHead_bytes))) #É o tamanho complementar do head
        head_bytes = (0).to_bytes(headSize, byteorder="big")
        head_bytes += packageNum + packageTotal + error8 + packageExpected + msg_type + overHead_bytes + payloadSize_bytes
        #print("seu head: ",head_bytes)
        return head_bytes



    def createPACKAGE(self, msg_type = 0, payload = (b'\x00'), packageNum=1, packageTotal=1 ,error8=0, packageExpected=0):
        head = self.createHEAD(msg_type,payload, packageNum, packageTotal , error8, packageExpected)
        self.package = head + payload + self.EOP
        return self.package


    def sendBuffer(self, data):
        """ Write a new data to the transmission buffer.
            This function is non blocked.

        This function must be called only after the end
        of transmission, this erase all content of the buffer
        in order to save the new value.
        """
        #print(data)
        self.transLen   = 0
        self.buffer = data
        #print(self.buffer)
        self.threadMutex  = True


    def getBufferLen(self):
        """ Return the total Size of bytes in the TX buffer
        """
        return(len(self.buffer))

    def getStatus(self):
        """ Return the last transmission Size
        """
        #print("O tamanho transmitido. Impressao fora do thread {}" .format(self.transLen))
        return(self.transLen)


    def getIsBussy(self):
        """ Return true if a transmission is ongoing
        """
        return(self.threadMutex)
