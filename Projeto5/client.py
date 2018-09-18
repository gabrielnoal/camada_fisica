
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

serialName = "/dev/ttyACM1"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
#serialName = "COM5"                  # Windows(variacao de)



print("porta COM aberta com sucesso")



def main(fileName):
    # Inicializa enlace ... variavel com possui todos os metodos e propriedades do enlace, que funciona em threading
    com = enlace(serialName)

    # Ativa comunicacao
    com.enable()
    com.rx.clearBuffer()

    #verificar que a comunicação foi aberta
    print("comunicação aberta")

    # Faz a etapa Synch do client
    print("-------------------------------")
    print("-----Começou o client Synch----")
    com.clientSynch()
    print("----Terminou o client Synch----")
    print("-------------------------------")
    img = open(imgName, "rb").read()
    #print(img)
    imgLen    = len(img)
    sub_pack= com.splitPack(img)

    # Transmite dado
    print("tentado transmitir .... {} bytes".format(imgLen))
    time.sleep(0.3)
    com.clientSendPackages(sub_pack)
    print("----Terminou a transmissão----")
    print("-------------------------------")
    

    

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    imgName = "emoji.jpg"
    main(imgName)