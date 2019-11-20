# -*- coding: utf-8 -*-
"""
Created on Tue Jun 25 14:32:32 2019

@author: Jimmykoh
"""
import csv
import numpy as np
import math
from collections import Counter
import abjad

filename = 'star_v2.csv'

with open(filename,newline='') as csvfile:
    rows = csv.reader(csvfile)
    cnt = 0
    for row in rows:
        if cnt == 0:
            duration_list = row
        else:
            note_list = row
        cnt += 1    


## corresponding notation
note_notation = []
container = abjad.Container()
voice = abjad.Voice("")
for i in range(len(note_list)):
    note_frequency = float(note_list[i])
    numbered_pitch = abjad.NumberedPitch.from_hertz(note_frequency)
    print(note_frequency)
    named_pitch = numbered_pitch.get_name()
    if note_frequency>100:
        if int(duration_list[i])<16 or abs(int(duration_list[i])-16)<abs(int(duration_list[i])-32):
            duration = 8
        else:
            duration = 4
        voice.append(abjad.Note(named_pitch + str(duration)))

abjad.show(voice)    
