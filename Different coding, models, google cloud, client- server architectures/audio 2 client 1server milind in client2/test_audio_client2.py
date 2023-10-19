import socket
import pyaudio
from pocketsphinx import Decoder, get_model_path
import os
import wave
import time
import struct

def addr_to_bytes(addr):
    return socket.inet_aton(addr[0]) + struct.pack('H', addr[1])

def bytes_to_addr(addr):
    return (socket.inet_ntoa(addr[:4]), struct.unpack('H', addr[4:])[0])


model_dir = get_model_path()
ps_config = Decoder.default_config()
ps_config.set_string('-logfn','nul')
ps_config.set_string('-hmm', os.path.join(model_dir, 'en-us'))       
ps_config.set_string('-dict', 'hotword.dict')
ps_config.set_string('-keyphrase', 'milind')
ps_config.set_float('-kws_threshold', 1e-30)
decoder = Decoder(ps_config)


val=1024*4
CHUNK = val
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000

audio = pyaudio.PyAudio()

HOST = '34.125.102.191'        
PORT = 40003            

if 1:
    soc = socket.socket()
    soc.connect((HOST, PORT))
    print("connected")
    
    data = soc.recv(val)
    peer = bytes_to_addr(data)
    print('peer:', *peer)
    
    if 1:
        #data=soc.recv(val)
        stream = audio.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                output=True,
                frames_per_buffer=CHUNK)
        decoder.start_utt()
        i=0
        flag=0
        print("started receiving")
        while 1:
                print("test0")
                data = soc.recv(val)
                print("received")
                if data:
                    print("test1")
                    decoder.process_raw(data, False, False)
                if decoder.hyp() is not None:
                    print("test2")
                    time.sleep(3)
                    message=b"success"
                    soc.send(message)
                    flag=1
                    
                    print([(seg.word, seg.prob, seg.start_frame, seg.end_frame) for seg in decoder.seg()])
                    print("Detected %s" % (decoder.hyp().hypstr))
                    decoder.end_utt()
                    decoder.start_utt()
                    print("milind activated")
                
                if 1:
                    message=b"success"
                    soc.send(message)
                    frames = []

                    for i in range(0, int(RATE / CHUNK * 6)):
                        print("in for loop",i)
                        data = soc.recv(val)
                        stream.write(data)
                        frames.append(data)
                        soc.send(bytes("hi",'utf-8'))
                        
                    
                    wf = wave.open("test audio.wav", 'wb')
                    wf.setnchannels(CHANNELS)
                    wf.setsampwidth(2)
                    wf.setframerate(RATE)
                    wf.writeframes(b''.join(frames))
                    wf.close()
                    
                    frames=[]
                
                if flag!=1:
                    print("test3")
                    soc.send(bytes("hi",'utf-8'))
                    
                print("test4")
                flag=0
                i=i+1
                
#except Exception as e:
#        print("Error:",e)