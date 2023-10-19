import socket
import struct


import sys
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

import SpeechModels
import tensorflow as tf
import librosa
import numpy as np

from tensorflow.keras.models import Model, load_model
from kapre.time_frequency import Melspectrogram, Spectrogram
from kapre.utils import Normalization2D



commands=["unknown/silence","nine","yes","no","up","down","left","right","on","off","stop",
          "go","zero","one","two","three","four","five","six","seven","eight","backward",
          "bed","bird","cat","dog","follow","forward","happy","house","learn","marvin",
          "sheila","tree","visual","wow"]


#commands=["yes","no","up","down","left","right","on","off","stop","go","backward","forward"]


model = load_model('./model-attRNN-35words.h5', custom_objects={'Melspectrogram': Melspectrogram, 'Normalization2D': Normalization2D })






def addr_to_bytes(addr):
    return socket.inet_aton(addr[0]) + struct.pack('H', addr[1])

def bytes_to_addr(addr):
    return (socket.inet_ntoa(addr[:4]), struct.unpack('H', addr[4:])[0])


val=1024*4
CHUNK = val
CHANNELS = 1
RATE = 16000


HOST = '34.125.102.191'        
PORT = 40002            

if 1:
    soc = socket.socket()
    soc.connect((HOST, PORT))
    soc.send(b"drone")
    print("connected")
    
    data = soc.recv(val)
    peer = bytes_to_addr(data)
    print('peer:', *peer)
    
    if 1:
        print("started receiving")
        while 1:
            
            filename = "test audio.wav"
            print("receiving file")
            bytes_read = soc.recv(val)
            soc.send(b"read")
            with open(filename, "wb") as f:
                print("inside while")
                i=0
                while True:
                    print(i)
                    if bytes_read[-4:]==bytes("stop",'utf-8'):
                        f.write(bytes_read[:-4])
                        break
                    f.write(bytes_read)
                    bytes_read = soc.recv(val)
                    #soc.send(b"read")
                    i=i+1
            f.close()
            print("audio received")
            
            
            fileName = "test audio.wav" 
    
            
            y, sr = librosa.load(fileName, sr=None)
            np.save(fileName + '.npy', y)
            
            X = np.empty((1, 16000))
            curX = np.load(fileName+".npy")
            if curX.shape[0] == 16000:
                    X[0] = curX
            elif curX.shape[0] > 16000:
                    randPos = np.random.randint(curX.shape[0]-16000)
                    X[0] = curX[randPos:randPos+16000]
            else:
                    randPos = np.random.randint(16000-curX.shape[0])
                    X[0, randPos:randPos + curX.shape[0]] = curX

            
            y_predict = model.predict(X[:1])
            
            print("\n")
            print(np.argmax(y_predict,axis=1))
            print(commands[np.argmax(y_predict,axis=1)[0]]+"\n")
                
#except Exception as e:
#        print("Error:",e)