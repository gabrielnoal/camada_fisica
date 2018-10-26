import numpy as np
import soundfile as sf
import sounddevice as sd
import matplotlib.pyplot as plt
import scipy.io.wavfile
from scipy import signal
from signalTeste import *


cutoff_hz = 4000.0
ripple_db = 60.0
f_carrier = 14000.0
fs = 44100


def generateSin(freq, time):
        n = time*fs
        x = np.linspace(0.0, time, n)
        s = np.sin(freq*x*2*np.pi)
        return (x, s)

def normaliza(data):
    amp_max = max(abs(data))
    normalizada = []
    for i in range(len(data)):
        norma = data[i] / amp_max
        normalizada.append(norma)
    return normalizada

def filtra_sinal(data, samplerate):
    nyq_rate = samplerate/2
    width = 5.0/nyq_rate
    N , beta = signal.kaiserord(ripple_db, width)
    taps = signal.firwin(N, cutoff_hz/nyq_rate, window=('kaiser', beta))
    yFiltrado = signal.lfilter(taps, 1.0, data)
    return yFiltrado

signal_ = signalMeu()
audio, samplerate = sf.read('gravacao.wav')
audio = audio[:,0]
audio_time = len(audio)/fs
x = np.linspace(0, audio_time, len(audio))

audio_normalizado = normaliza(audio)

audio_filtrado = filtra_sinal(audio_normalizado, samplerate)

t, carrier = generateSin(f_carrier, audio_time)
audio_modulado = carrier * audio_filtrado

sd.play(audio_modulado * 2, fs)
sd.wait()


#
plt.plot(x, audio)
plt.title("audio")
plt.show()
signal_.plotFFT(audio, fs)

plt.plot(x, audio_normalizado)
plt.title("audio normalizado")
plt.show()
signal_.plotFFT(audio_normalizado, fs)

plt.plot(x, audio_filtrado)
plt.title("aduio filtrado")
plt.show()
signal_.plotFFT(audio_filtrado, fs)


plt.plot(x, audio_modulado)
plt.title("audio modulado")
#plt.xlim(1.0, 1.25)
plt.show()
signal_.plotFFT(audio_modulado, fs)
