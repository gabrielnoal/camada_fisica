# -*- coding: utf-8 -*-
"""
Created on Fri Sep 14 14:57:54 2018

@author: rcararrto
"""
#exemplos de manipulacao de bits
def main():
    
    q= 0b10011
    data = 0b101101010000
    shifitado = data >> 7
    XorResultado = shifitado ^ q
    for b in range(1):
        print(" resultado em binario {}" .format(bin(XorResultado)))
        print(" numero de casas {}" .format(-2 + len(bin(XorResultado))))
        print(" teste xor {}" .format(bin(XorResultado)[0]))
        print(" teste xor {}" .format(bin(XorResultado)[1]))
        print(" resultado em int {}" .format(XorResultado))
        
    teste  =bin(int.from_bytes(b"hello world", byteorder="big")).strip('0b')
    print ("Como sequencia de bits {}"  .format(teste) )
    
    teste  =bin(int.from_bytes(bytes([0xFA]), byteorder="big")).strip('0b')
    print ("Como sequencia de bits {}"  .format(teste) )
    print(len(teste))
    print(teste[5])
    
    
        #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
 