from signalTeste import *
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import sys
import keyboard


class Emiter:
    def __init__(self):
        self.sig = signalMeu()
        self.frequencia = 48000
        self.matrix_frequencias = {"1":(697,1209), "2":(697,1336), "3":(697,1209),
                                   "4":(770,1209), "5":(770,1336), "6":(770,1477),
                                   "7":(852,1209), "8":(852,1336), "9":(852,1477),
                                   "*":(941,1209), "0":(941,1336), "#":(941,1477)}
        self.time = 0
    
    def create_signal(self, tecla,amplitude=1,time=2):
        self.time, signal1 = self.sig.generateSin(self.matrix_frequencias[tecla][0], amplitude, time, self.frequencia)
        self.time, signal2 = self.sig.generateSin(self.matrix_frequencias[tecla][1], amplitude, time, self.frequencia)
        signal = np.add(signal1, signal2)
        return signal

    def play(self,signal):
        sd.play(signal , self.frequencia)
        plt.plot(self.time[:2000], signal[:2000])
        plt.show()



    
emiter = Emiter()

while True:
    if keyboard.is_pressed('1'):
        emiter.play(emiter.create_signal('1'))
    elif keyboard.is_pressed('2'):
        emiter.play(emiter.create_signal('2'))
    elif keyboard.is_pressed('3'):
        emiter.play(emiter.create_signal('3'))
    elif keyboard.is_pressed('4'):
        emiter.play(emiter.create_signal('4'))
    elif keyboard.is_pressed('5'):
        emiter.play(emiter.create_signal('5'))
    elif keyboard.is_pressed('6'):
        emiter.play(emiter.create_signal('6'))
    elif keyboard.is_pressed('7'):
        emiter.play(emiter.create_signal('7'))
    elif keyboard.is_pressed('8'):
        emiter.play(emiter.create_signal('8'))
    elif keyboard.is_pressed('9'):
        emiter.play(emiter.create_signal('9'))
    elif keyboard.is_pressed('0'):
        emiter.play(emiter.create_signal('0'))
    elif keyboard.is_pressed('shift+8'):
        emiter.play(emiter.create_signal('*'))
    elif keyboard.is_pressed('shift+#'):
        emiter.play(emiter.create_signal('#'))
