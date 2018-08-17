
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

serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
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
    print ("Recebendo dados .... ")
    parte_buffer=[]
    buffer_completo=[]
    while True:
        bytesSeremLidos=com.rx.getBufferLen()
        if bytesSeremLidos>0:
            start = time.time()
            passrxBuffer, nRx = com.getData(1)
            parte_buffer.append(passrxBuffer)
        else:
            if len(parte_buffer)>0:
                if len(parte_buffer)==512:
                    buffer_completo += parte_buffer
                    parte_buffer=[]
                else:
                    buffer_completo+=parte_buffer
                    if len(buffer_completo)>0:
                        tempoRecebimento = time.time() - start
                        print(b''.join(buffer_completo),len(buffer_completo),"Tempo de recebimento da informação em segundos:{}".format(tempoRecebimento))
                        img = b''.join(buffer_completo)
                        buffer_completo=[]
                        parte_buffer=[]
    #print(bytesSeremLidos)

    # log
    print ("Lido              {} bytes ".format(nRx))
    newFile = open("novoarquivo.jpg", "wb")
    newFile.write(img)
    newFile.close()

    # Encerra comunicação
    print("-------------------------")
    print("Comunicação encerrada")
    print("-------------------------")
    com.disable()
    return tempoRecebimento


    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
#if __name__ == "__main__":
#    main()
