from signalTeste import *
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import time
import pickle
import peakutils
import keyboard


class Decoder:
    def __init__(self):
        self.sig = signalMeu()
        self.frequencia = 48000
        self.matrix_frequencias =  {"1":[697,1209], "2":[697,1336], "3":[697,1209], "4":[770,1209], "5":[770,1336], "6":[770,1477], "7":[852,1209], "8":[852,1336], "9":[852,1477], "*":[941,1209], "0":[941,1336], "#":[941,1477]}
        self.time = 0

    def record(self):
        duration = 2
        recording = sd.rec(int(duration * self.frequencia), samplerate = self.frequencia, channels=1)
        sd.wait()
        return recording[:,0]

    def findPeaks(self):
        recording_fft = self.sig.calcFFT(self.record(), self.frequencia)

        indexes = peakutils.indexes(recording_fft[1], thres=0.5, min_dist=10)
        return recording_fft[0][indexes]

    def plotFFT2(self):
        recording_fft = self.sig.calcFFT(self.record(), self.frequencia)
        plt.figure()
        plt.plot(recording_fft[0], np.abs(recording_fft[1]))
        plt.title("Fourier")
        plt.show()

    def findKeys(self):
        peaks = self.findPeaks()
        possible_frequency = [697, 1209, 1336, 770, 852, 1477, 941]

        received_frequency = []
        for peak in peaks:
            for frequency in possible_frequency:
                if abs(peak - frequency) < 30:
                    received_frequency.append(frequency)

        print(received_frequency)


        for key in self.matrix_frequencias.keys():
            print(self.matrix_frequencias[key])
            if received_frequency == self.matrix_frequencias[key]:
                print(key)
                break



    def plotHarmonics(self):
        frequencies = self.findPeaks()
        for frequency in frequencies:
            senoid = self.sig.generateSin(frequency, 1, 2, self.frequencia)
            plt.figure()
            plt.title("Gráfico para o harmonico de {} Hz".format(frequency))
            plt.plot(senoid[0][:2000], senoid[1][:2000])
        plt.show()

decoder = Decoder()

#decoder.plotFFT2()
#decoder.plotHarmonics()
print(decoder.findPeaks())
decoder.plotHarmonics()
#decoder.plotFFT2()
decoder.findKeys()
