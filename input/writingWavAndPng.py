#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import numpy as np
import sys, os

from scipy import arange, ceil, complex128, dot, exp, float64, hamming, log2, zeros
from scipy import pi as mpi
from scipy.fftpack import fft
from scipy.sparse import lil_matrix, csr_matrix
from scipy.io.wavfile import read

from matplotlib import pylab as pl
from constant_q_trans import *

from datetime import datetime

import pyaudio
import wave

import cPickle as pickle

import soundDetector

import scipy.fftpack
from pylab import *

import ConfigParser
inifile = ConfigParser.SafeConfigParser()
inifile.read("../conf/config.ini")

varfile = ConfigParser.SafeConfigParser()
varfile.read("../conf/var.ini")


sys.path.append(os.pardir)
import output.outmod as outmod

parser = argparse.ArgumentParser(description='Predict Waveform')
parser.add_argument('--savename', '-s', default='sample',
                    help='file name to save')
parser.add_argument('--recordingtime', '-r', type=float, default=5,
                    help='Recording time')
args = parser.parse_args()

CHUNK=varfile.getint("input","chunk")
RATE=varfile.getint("input","rate")
CHANNELS=varfile.getint("input","channels")

p=pyaudio.PyAudio()

def data2fft(data):
    data = np.frombuffer(data, dtype= "int16") / 32768.0
    hammingWindow = np.hamming(data.shape[0])
    data = data * hammingWindow
    X = np.fft.fft(data)  # FFT                                                                    
    return [np.sqrt(c.real ** 2 + c.imag ** 2) for c in X]  # 振幅スペクトル 

def get_dir_name(data_dir="../clustering/"+inifile.get("config","sound_dir")+"/"):
    count = 0
    for dirName, subdirList, fileList in os.walk(data_dir):
        for dname in subdirList:
            if dname.isdigit() is True:
                count+=1
    count+=1
    return data_dir + "{0:03d}".format(count)

#ROOT = "../data"
ROOT = get_dir_name()
if not os.path.exists(ROOT):
    os.mkdir(ROOT)
PATH = ROOT    
# PATH = os.path.join(ROOT, args.savename)
# if not os.path.exists(PATH):
#     os.mkdir(PATH)

WAVE_OUTPUT_FILENAME = PATH + "/"+inifile.get("config","sound_file")
IMAGE_OUTPUT_FILENAME = PATH + "/img.png"
RAW_OUTPUT_FILENAME = PATH + "/data.pkl"

def recordingAndWriting():
    # stream=p.open(format = pyaudio.paInt16,
    #               channels = CHANNELS,
    #               rate = RATE,
    #               frames_per_buffer = CHUNK,
    #               input = True)
    
    # frames = []
    # print "start"
    # for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    #     input = stream.read(CHUNK)
    #     frames.append(input)
    
    # print "stop"
    # stream.stop_stream()
    # stream.close()
    # p.terminate()

    #音声取得、wav書込
    data, starttime = soundDetector.record_wrap()

    #print WAVE_OUTPUT_FILENAME
    #data = b''.join(frames)
    wf = wave.open(WAVE_OUTPUT_FILENAME, "wb")
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(RATE)
    wf.writeframes(data)
    wf.close()
    start = 0

    #outputの関数を呼ぶ
    ap = outmod.AudioPlayer()
    ap.setAudioFile(WAVE_OUTPUT_FILENAME)
    outmod.playLoop(ap)

    ap1 = outmod.AudioPlayer()
    ap1.setAudioFile(WAVE_OUTPUT_FILENAME)
    ap1.setAudioWaitTime(0.3)
    outmod.playLoop(ap1)

    ap2 = outmod.AudioPlayer()
    ap2.setAudioFile(WAVE_OUTPUT_FILENAME)
    ap2.setAudioWaitTime(0.6)
    outmod.playLoop(ap2)
    
    #starttime = datetime.now()

    # print 'start fft'
    # fft_data = data2fft(data)
    # print 'finish fft'

    # FFT結果を保存
    # file_fft = open(IMAGE_OUTPUT_FILENAME, 'w')
    # pickle.dump(fft_data[0:1000], file_fft)
    # file_fft.close()

    # 画像生成
    # fs, data = read(WAVE_OUTPUT_FILENAME)
    # cq_spec, freqs = cq_fft(data, fs)
    # w, h = cq_spec.shape
    # fig = pl.figure()
    # fig.add_subplot(111)
    # pl.imshow(abs(cq_spec).T, aspect = "auto", origin = "lower")
    # pl.tick_params(labelbottom='off')
    # pl.tick_params(labelleft='off')
    # pl.savefig(IMAGE_OUTPUT_FILENAME, bbox_inches='tight')

    # dumpを保存
    # f = open(RAW_OUTPUT_FILENAME, 'w')
    # pickle.dump(cq_spec, f)
    # f.close()

    #return IMAGE_OUTPUT_FILENAME
    return WAVE_OUTPUT_FILENAME, starttime

if __name__ == "__main__":
    recordingAndWriting()
