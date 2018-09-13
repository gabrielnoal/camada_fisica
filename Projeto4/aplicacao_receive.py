
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#####################################################
# Camada Física da Computação
#Carareto
#17/02/2018
#  Aplicação
####################################################

print("comecou")

from enlace import *
import time

# voce deverá descomentar e configurar a porta com através da qual ira fazer a
# comunicaçao
# Serial Com Port
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

serialName = "/dev/ttyACM2"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
#serialName = "COM5"                  # Windows(variacao de)



print("porta COM aberta com sucesso")

    

def main():
    # Inicializa enlace ... variavel com possui todos os metodos e propriedades do enlace, que funciona em threading
    com = enlace(serialName)

    # Ativa comunicacao
    com.enable()
    
    #verificar que a comunicação foi aberta
    print("comunicação aberta")



    # Atualiza dados da transmissão
    # txSize = com.tx.getStatus()

    # Faz a recepção dos dados
    print("-------------------------------")
    print("-----Começou o server Synch----")
    while com.serverSynchComplete == False:
        com.serverSynch()
    print("----Terminou o server Synch----")
    print("-------------------------------")

    # Faz a recepção dos dados
    print ("Recebendo dados... ")
    payloadSize = 0
    while payloadSize < 1:
        time.sleep(0.1)    
        data, size , payloadSize = com.getData()

    print("-------------------------------")

    print ("Lido              {} bytes ".format(size))
    newFile = open("novoarquivo.jpg", "wb")
    newFile.write(data)
    newFile.close()


    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()