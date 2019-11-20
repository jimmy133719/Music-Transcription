# Music-Transcription

### Description
Create sheet music from a recording.

### Environment 
* Matlab: 2019a  
* Python: 3.6.0  
* Python library: numpy 1.13.1, librosa 0.6.2, matplotlib 2.0.0, abjad 3.0.0  


### Method1
1. Apply short-time Fourier transform to input recording. 
2. Establish the chart between piano keys and frequency.
3. Find the closest piano key of every time index.
4. Find median from fixed amount of keys of time indeces to generate key.
#### Execution
Change line 18 in sheetmusic_method1.py to your own recording and execute.

### Method2
Since method1 can only generate fixed-length key, method2 uses power density to determine note length.
#### Execution
1. Change line 3 in method2.m to your own recording and execute. This procedure will generate a csv file that contains information about the key's location and frequency.
2. Use csv file generated from 1. as input and run method2_note.py

