import os
import random
import matplotlib.pyplot as plt
import numpy as np

import librosa as lr
from librosa.display import specshow
from librosa.core import stft, amplitude_to_db


dir = '2020-11-14/'

def audio(dir):
    return lr.load(dir + random.choice(os.listdir(dir)))
     

acoustic_audio, freq = audio(dir)

# Time against Amplitude
def time_domain():
    ixs = np.arange(acoustic_audio.shape[-1])
    time = ixs/freq
    fig, ax  = plt.subplots()
    ax.plot(time, acoustic_audio)
    plt.show()

# Spectrogram visuals
def spectrogram():
    HOP_LENGTH = 2**4
    SIZE_WINDOW = 2**7
    audio_spec = stft(acoustic_audio, hop_length=HOP_LENGTH, n_fft=SIZE_WINDOW)
    # Convert into decibels for visualization
    spec_db = amplitude_to_db(audio_spec)# Visualize
    fig, ax = plt.subplots()
    specshow(spec_db, sr=freq, x_axis='time', y_axis='Hz', hop_length=HOP_LENGTH,  ax=ax)
    plt.show()

# Combined visuals
def audio_visual(audiofile):
    plt.figure(figsize=(12,7))
    audiofile, freq = lr.load(audiofile)
    ixs = np.arange(audiofile.shape[-1])
    time = ixs/freq
    HOP_LENGTH = 2**4
    SIZE_WINDOW = 2**7
    audio_spec = stft(audiofile, hop_length=HOP_LENGTH, n_fft=SIZE_WINDOW)
    # Convert into decibels for visualization
    spec_db = amplitude_to_db(audio_spec)# Visualize
    plt.subplot(2,1,1)
    plt.plot(time, audiofile)
    # fig, ax = plt.subplots()
    plt.subplot(2,1,2)

    specshow(spec_db, sr=freq, x_axis='time', y_axis='hz', hop_length=HOP_LENGTH)
    plt.show()

audio_visual('audio_files_harvard.wav')



