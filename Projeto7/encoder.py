from signalTeste import *
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import sys
import keyboard
import time


class Emiter:
    def __init__(self):
        self.sig = signalMeu()
        self.frequencia = 48000
        self.matrix_frequencias = {"1":[697,1209], "2":[697,1336], "3":[697,1209],
                                   "4":[770,1209], "5":[770,1336], "6":[770,1477],
                                   "7":[852,1209], "8":[852,1336], "9":[852,1477],
                                   "*":[941,1209], "0":[941,1336], "#":[941,1477]}
        self.time = 0
        self.graf_line = 1
        self.graf_column = 4
        self.graf_number = 1

    
    def create_signal(self, tecla,amplitude=1,time=1):
        #print("Signal 1:{}".format(self.matrix_frequencias[tecla][0]))
        #print("Signal 2:{}".format(self.matrix_frequencias[tecla][1]))
        self.time, signal1 = self.sig.generateSin(self.matrix_frequencias[tecla][0], amplitude, time, self.frequencia)
        self.time, signal2 = self.sig.generateSin(self.matrix_frequencias[tecla][1], amplitude, time, self.frequencia)
        signal = np.add(signal1, signal2)
        signals = [signal1, signal2, signal]
        names = [("Frequencia {}".format(self.matrix_frequencias[tecla][0])), ("Frequencia {}".format(self.matrix_frequencias[tecla][1])),("Somatoria das Frequencias {}x{}".format(self.matrix_frequencias[tecla][0],self.matrix_frequencias[tecla][1])),tecla]
        return names, signals

    def play(self, names, signals):
        sd.stop()
        sd.play(signals[2] , self.frequencia)
        self.plota(signals,names)
        
    
    def plota(self, signals, names):
        tecla = names[3]
        if self.graf_number >=3:
            self.graf_number =1
        fig = plt.figure(figsize=(15,3))
        fig.canvas.set_window_title("Tecla: "+tecla)
        plt.subplot(self.graf_line, self.graf_column, self.graf_number)
        plt.plot(self.time[:1000], signals[0][:1000])
        plt.xlabel("Tempo")
        plt.ylabel("Amplitude")
        plt.title(names[0] +"hz")

        self.graf_number += 1
        plt.subplot(self.graf_line, self.graf_column, self.graf_number)
        plt.plot(self.time[:1000], signals[1][:1000])
        plt.xlabel("Tempo")
        plt.ylabel("Amplitude")
        plt.title(names[1] +"hz")

        self.graf_number += 1
        plt.subplot(self.graf_line, self.graf_column, self.graf_number)
        plt.plot(self.time[:1000], signals[2][:1000])
        plt.xlabel("Tempo")
        plt.ylabel("Amplitude")
        plt.title(names[2] +"hz")

        self.graf_number += 1
        x,y = self.sig.calcFFT(signals[2][:1000], self.frequencia)
        plt.subplot(self.graf_line, self.graf_column, self.graf_number)
        plt.plot(x[:1000], np.abs(y))
        plt.xlabel("Tempo")
        plt.ylabel("Amplitude")
        plt.title('Fourier')

        plt.tight_layout()
        plt.show()

        
emiter = Emiter()

while True:
    if keyboard.is_pressed('1'):
        names, signals = emiter.create_signal('1')
        emiter.play(names, signals)
    elif keyboard.is_pressed('2'):
        names, signals = emiter.create_signal('2')
        emiter.play(names, signals)
    elif keyboard.is_pressed('3'):
        names, signals = emiter.create_signal('3')
        emiter.play(names, signals)
    elif keyboard.is_pressed('4'):
        names, signals = emiter.create_signal('4')
        emiter.play(names, signals)
    elif keyboard.is_pressed('5'):
        names, signals = emiter.create_signal('5')
        emiter.play(names, signals)
    elif keyboard.is_pressed('6'):
        names, signals = emiter.create_signal('6')
        emiter.play(names, signals)
    elif keyboard.is_pressed('7'):
        names, signals = emiter.create_signal('7')
        emiter.play(names, signals)
    elif keyboard.is_pressed('8'):
        names, signals = emiter.create_signal('8')
        emiter.play(names, signals)
    elif keyboard.is_pressed('9'):
        names, signals = emiter.create_signal('9')
        emiter.play(names, signals)
    elif keyboard.is_pressed('0'):
        names, signals = emiter.create_signal('0')
        emiter.play(names, signals)
    elif keyboard.is_pressed('shift+8'):
        names, signals = emiter.create_signal('*')
        emiter.play(names, signals)
    elif keyboard.is_pressed('shift+3'):
        names, signals = emiter.create_signal('#')
        emiter.play(names, signals)
