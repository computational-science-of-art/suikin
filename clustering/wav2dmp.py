# -*- coding: utf-8 -*-
from scipy.io.wavfile import read
import numpy as np
import sys, os
import cPickle as pickle

def wav2dmp(wavpath, dumppath):
    fs, data = read(wavpath)
    data = np.frombuffer(data, dtype= "int16") / 32768.0
    hammingWindow = np.hamming(data.shape[0])
    data = data * hammingWindow
    X = np.fft.fft(data)  # FFT    
    fft_data = [np.sqrt(c.real ** 2 + c.imag ** 2) for c in X]
    file_fft = open(dumppath, 'w')
    pickle.dump(fft_data[0:1000], file_fft)
    file_fft.close()

if __name__ == "__main__":
    # for dirName, subdirList, fileList in os.walk('hayakuti_data'):
    #     for dname in subdirList:
    #         print dname
    wav2dmp('sound.wav', 'fft.pkl')
    # f = open( 'test.dump' , 'r' )
    # print pickle.load( f )
    # f.close()
