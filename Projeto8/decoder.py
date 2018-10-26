import numpy as np
import soundfile as sf
import sounddevice as sd
import matplotlib.pyplot as plt
import scipy.io.wavfile
from scipy import signal
from signalTeste import *


cutoff_hz = 4000.0
ripple_db = 60.0
freq_carrier = 14000.0
fs = 44100
signal_ = signalMeu()


def generateSin(freq, time):
        n = time*fs
        x = np.linspace(0.0, time, n)
        s = np.sin(freq*x*2*np.pi)
        return (x, s)

def filtra_sinal(data, samplerate):
    nyq_rate = samplerate/2
    width = 5.0/nyq_rate
    N , beta = signal.kaiserord(ripple_db, width)
    taps = signal.firwin(N, cutoff_hz/nyq_rate, window=('kaiser', beta))
    yFiltrado = signal.lfilter(taps, 1.0, data)
    return yFiltrado


def record():
    duration = 10
    audio = sd.rec(int(duration*fs),fs,channels=1)
    sd.wait()
    audio_ = audio[:,0]
    return audio_

audio = record()
scipy.io.wavfile.write('gracavaoteste.wav',fs,audio)
audio_time = len(audio)/fs
x = np.linspace(0, audio_time, len(audio))

t, carrier = generateSin(freq_carrier, audio_time)

demodulado = audio * carrier
scipy.io.wavfile.write('gravacaodemodulada.wav',fs,demodulado)
sinal = filtra_sinal(demodulado, fs)
sd.play(sinal, fs)

plt.plot(x, sinal)
plt.title("audio demodulado")
plt.show()

signal_.plotFFT(sinal, fs)
signal_.plotFFT(audio, fs)
 
