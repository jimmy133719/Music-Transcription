# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 17:54:16 2019

@author: Jimmykoh
"""
import numpy as np
import librosa
import librosa.display
import math
import matplotlib.pyplot as plt
from collections import Counter
import abjad


  
dir = './'
filename = 'star.wav'
y, fs1 = librosa.load(filename)
fs = 16000
y = librosa.resample(y, fs1, fs)

## get stft of signal
N_fft = 1024
Hop_length = 256
Win_length = 512
S = librosa.stft(y,n_fft=N_fft,hop_length=Hop_length,win_length=Win_length, window='hann')
w = np.linspace(0,fs/2,num=S.shape[0])
# D = 20*math.log10(abs(S))
D = np.abs(S)
D_norm = D - D.min(axis=0)
D_norm = D_norm/np.abs(D_norm).max(axis=0)


## show spectrogram
librosa.display.specshow(librosa.power_to_db(D,ref=np.max),sr=fs,y_axis='log',x_axis='time')
plt.title('Power spectrogram')
plt.colorbar(format='%+2.0f dB')
plt.tight_layout()

## get piano frequency
keys= []
level = 2**(1/12)
for n in range(1,89):
    key = (level**(n-49))*440
    keys.append(key)

## frame segment and find corresponding piano frequency
tempo = 120 # bpm
tempo = tempo/60 # bps
framelen = 1/tempo*fs
framelen = math.floor(framelen/Hop_length)-1 # number of time bins per beat
framelen = int(framelen/2) # use quater beat as framelen

## find peak frequency of each time bin
max_freq = []
for i in range(D.shape[1]):
    index = np.where(D[:,i]==max(D[:,i]))
#    if len(index)>1:
#        index = min(index)
    max_freq.append(w[index][0])

## find the nearest pinao frequency of each peak frequency
key_num = []
for i in range(D.shape[1]):
    min_error = np.abs(max_freq[i]-max(keys))
    key_num.append(0)
    for j in range(0,len(keys)):
        if np.abs(max_freq[i]-keys[j])<min_error:
            min_error = np.abs(max_freq[i]-keys[j])
            key_num[i] = j+1

beat_total = math.floor(len(key_num)/framelen)
note = []
for i in range(beat_total):
    counter = Counter(key_num[framelen*i:framelen*(i+1)-1])
    most_common_note = counter.most_common(1)
    note.append(most_common_note[0][0])

## corresponding notation
note_notation = []
container = abjad.Container()
numbered_pitch = abjad.NumberedPitch.from_hertz(keys[note[0]-1])
named_pitch = numbered_pitch.get_name()
temp = named_pitch
cnt = 1
for i in range(len(note)):
    note_frequency = keys[note[i]-1]
    numbered_pitch = abjad.NumberedPitch.from_hertz(note_frequency)
    print(note_frequency)
    named_pitch = numbered_pitch.get_name()

    if note_frequency>100:
        container.append(abjad.Note(named_pitch + '8'))
abjad.show(container)                        


  