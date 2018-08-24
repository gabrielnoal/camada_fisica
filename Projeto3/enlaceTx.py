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
        self.EOP         = self.createEOP()
        self.headSize    = 16

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

    def calcOverHead(self):
        overHead = (self.headSize + len(self.payload) + len(self.EOP)/len(self.payload))
        print("Overhead: {}%".format(round(overHead,2)/10))
        return overHead
        
        
    def createHEAD(self, payloadSize, EOPSize):
        head_bytes = None
        overHead = (self.headSize + payloadSize + EOPSize)/payloadSize
        overHead = self.calcOverHead()
        head_bytes = round(overHead).to_bytes(self.headSize, byteorder="big")
        head_bytes = payloadSize.to_bytes(self.headSize, byteorder="big")
        
        return head_bytes


    def createEOP(self):
        EOPbytes = bytes("WARLEN","utf-8")
        print(EOPbytes)
        return EOPbytes

    def createPACKAGE(self, head, payload):
        self.package = head + payload + self.EOP

    def addByteStuff(self,payload):
        pass


    def sendBuffer(self, data):
        """ Write a new data to the transmission buffer.
            This function is non blocked.

        This function must be called only after the end
        of transmission, this erase all content of the buffer
        in order to save the new value.
        """
        #print(data)
        self.payload = data
        HEAD = self.createHEAD(len(self.payload), len(self.EOP))
        self.createPACKAGE(HEAD, self.payload)
        
        self.transLen   = 0
        self.buffer = self.package
        #print(self.buffer)
        #tempoteorico = (self.getBufferLen*2)/
        
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
