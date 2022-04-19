import pyaudio
import numpy as np
from numpy import interp
from scipy.fftpack import fft
from scipy.signal import windows
import math
import soundfile
import matplotlib.pyplot as plt
from scipy.signal import medfilt, butter, lfilter, freqz
from pyACA import computePitch
from scipy.io.wavfile import read as wavread
from scipy.io.wavfile import write
import util

# Current problems
## Audio concatenation
## Min and max f0

# Initializations
silence_flag = False
pyaudio_format = pyaudio.paFloat32
n_channels = 1
silenceThresholdindB = -40
fs = 44100
iBlockLength=2048
iHopLength=iBlockLength
thres_dB = -40 # Voicing mask threshold for silence detection

record_time = iBlockLength/fs


"""
Main Part Of Code
"""

# initialise pyaudio
p = pyaudio.PyAudio()

# open stream
stream = p.open(format=pyaudio_format,
                channels=n_channels,
                rate=fs,
                input=True,
                frames_per_buffer=iHopLength)

print("*** starting recording")
audio_block = np.array([], dtype=np.float32)
audio = np.array([], dtype=np.float32)
f0 = np.array([], dtype=np.float32)

# low pass filter initializations:
order = 3
cutOff = 1200  # Hz
while True:
    try:
        # record a short phrase
        for i in range(0, int(fs / iHopLength * record_time)):
            audiobuffer = stream.read(iBlockLength, exception_on_overflow=False)
            signal = np.frombuffer(audiobuffer, dtype=np.float32)
            audio_block = np.append(audio_block, signal)
            audio = np.append(audio, audio_block)

        audio_block = util.butter_lowpass_filter(audio_block, cutOff, fs, order)
        f0_block, t = computePitch('SpectralHps', audio_block, fs, afWindow=None, iBlockLength=2048, iHopLength=1024)
        f0_block = util.detect_silence(audio_block, f0_block, thres_dB)
        f0 = np.append(f0, f0_block)
        print (f0_block)

        # reinitiate audio_block
        audio_block = np.array([])

    except KeyboardInterrupt:
        print("***Ending Stream")
        break

stream.stop_stream()
stream.close()
p.terminate()

print("exporting audio...")
write("output.wav", fs, audio)
np.savetxt('f0.txt', f0)
print("done exporting!")
