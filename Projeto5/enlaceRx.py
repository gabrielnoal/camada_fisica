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

# Threads
import threading

# Class
class RX(object):
    """ This class implements methods to handle the reception
        data over the p2p fox protocol
    """
    
    def __init__(self, fisica):
        """ Initializes the TX class
        """
        self.fisica      = fisica
        self.buffer      = bytes(bytearray())
        self.threadStop  = False
        self.threadMutex = True
        self.READLEN     = 1024
        self.EOP         =  fisica.EOP
        self.packageFound = True
        self.timeout     = False

    def thread(self): 
        """ RX thread, to send data in parallel with the code
        essa é a funcao executada quando o thread é chamado. 
        """
        while not self.threadStop:
            if(self.threadMutex == True):
                #print(len(self.buffer))
                rxTemp, nRx = self.fisica.read(self.READLEN)
                if (nRx > 0):
                    self.buffer += rxTemp
                time.sleep(0.01)

    def threadStart(self):
        """ Starts RX thread (generate and run)
        """
        self.thread = threading.Thread(target=self.thread, args=())
        self.thread.start()

    def threadKill(self):
        """ Kill RX thread
        """
        self.threadStop = True

    def threadPause(self):
        """ Stops the RX thread to run

        This must be used when manipulating the Rx buffer
        """
        self.threadMutex = False

    def threadResume(self):
        """ Resume the RX thread (after suspended)
        """
        self.threadMutex = True

    def getIsEmpty(self):
        """ Return if the reception buffer is empty
        """
        if(self.getBufferLen() == 0):
            return(True)
        else:
            return(False)

    def getBufferLen(self):
        """ Return the total number of bytes in the reception buffer
        """
        return(len(self.buffer))

    def getAllBuffer(self, len):
        """ Read ALL reception buffer and clears it
        """
        self.threadPause()
        b = self.buffer[:]
        self.clearBuffer()
        self.threadResume()
        return(b)

    def getBuffer(self, nData):
        """ Remove n data from buffer
        """
        self.threadPause()
        b           = self.buffer[0:nData]
        self.buffer = self.buffer[nData:]
        self.threadResume()
        
        return(b)

    def isBufferFull(self):
        start_time = time.time()
        isFull = False
        bufferLen = self.getBufferLen() 
        while isFull == False:
            final_time = time.time() - start_time
            if final_time >= 5:
                self.timeout = True
                return isFull
            time.sleep(0.1)
            if bufferLen == self.getBufferLen() and bufferLen > 0:
                isFull = True 
            else:
                bufferLen = self.getBufferLen() 
        
        return isFull

    def getNData(self):
        """ Read N bytes of data from the reception buffer

        This function blocks until the number of bytes is received
        """
#        temPraLer = self.getBufferLen()
#        print('leu %s ' + str(temPraLer) )
        
        #if self.getBufferLen() < size:
            #print("ERROS!!! TERIA DE LER %s E LEU APENAS %s", (size,temPraLer))
        bufferFull = self.isBufferFull()
        
        #while(self.isBufferFull() == False):
            #time.sleep(0.05)
            
        #self.findEOP(self.getBuffer(size))
        if bufferFull == True:
            size = self.getBufferLen()
            return self.getBuffer(size)
        else:
            return 0

    def findEOP(self, dados):
        eop = bytes("WARLEN","utf-8")
        achou = False
        for byte in dados:
            if byte == eop:
                achou = True
                print("EOP encontrado no index {}".format(dados.index(byte)))
        
        if not achou:
            print("[ERRO] - EOP NOT ENCONTRADO")
        print("Tamanho dos dados: {}".format(len(dados)))
        pass

    def clearBuffer(self):
        """ Clear the reception buffer
        """
        self.buffer = b""

    def unpackage(self,package):
        eop = package.find(self.EOP)
        if eop != -1: #se eop existe
            #self.packageFound = True
            header = package[:16]
            payload = package[16:(len(package)-len(self.EOP))]
            #print(payload)
            print("-----------------")
            print("------HEADER-----")
            print(header)
            
            packageNumber_bytes = header[5:6]
            packageNumber_int = header[5]
            print("-----------------")
            print("NUMERO DO PACOTE")
            print(packageNumber_bytes)
            print(packageNumber_int)

            packageTotal_bytes = header[6:7]
            packageTotal_int = header[6]
            print("-----------------")
            print("NUMERO TOTAL DE PACOTES")
            print(packageTotal_bytes)
            print(packageTotal_int)

            erro8_bytes = header[7:8]
            erro8_int = header[7]
            print("-----------------")
            print("---ERRO TIPO 8---")
            print(erro8_bytes)
            print(erro8_int)
    

            packageExpected_bytes = header[8:9]
            packageExpected_int   = header[8]
            print("-----------------")
            print("PACOTE ESPERADO")
            print(packageExpected_bytes)
            print(packageExpected_int)
    

            msg_type_bytes = header[9:10]
            msg_type_int = header[9]
            print("-----------------")
            print("TIPO DE MENSAGEM")
            print(msg_type_bytes)
            print(msg_type_int)


            overHead_bytes = header[10:12]
            overHead_int = int.from_bytes(overHead_bytes, byteorder='big')
            print("-----------------")
            print("----OVER HEAD----")
            print(overHead_bytes)
            print("{}%".format(overHead_int))

            payloadSize_bytes = header[12:]
            payloadSize_int = int.from_bytes(payloadSize_bytes, byteorder='big')
            print("-----------------")
            print("--PAYLOAD SIZE--")
            print(payloadSize_bytes)
            print(payloadSize_int)

            print("-----------------")

            return packageNumber_int, packageTotal_int, erro8_int, packageExpected_int, payloadSize_int , payload
            





