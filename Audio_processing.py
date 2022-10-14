import os
import random
import matplotlib.pyplot as plt
import numpy as np

import librosa as lr
from librosa.display import specshow
from librosa.core import stft, amplitude_to_db


dir = '2020-11-14/'

def audio(dir):
    return random.choice(os.listdir(dir))

acoustic_audio, freq = lr.load(dir+audio(dir))

def time_domain():
    ixs = np.arange(acoustic_audio.shape[-1])
    time = ixs/freq
    fig, ax  = plt.subplots()
    ax.plot(time, acoustic_audio)
    plt.show()

def spectogram():
    HOP_LENGTH = 2**4
    SIZE_WINDOW = 2**7
    audio_spec = stft(acoustic_audio, hop_length=HOP_LENGTH, n_fft=SIZE_WINDOW)
    # Convert into decibels for visualization
    spec_db = amplitude_to_db(audio_spec)# Visualize
    fig, ax = plt.subplots()
    specshow(spec_db, sr=freq, x_axis='time', y_axis='hz', hop_length=HOP_LENGTH,  ax=ax)
    plt.show()

print(spectogram())


