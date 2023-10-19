import socket
from playsound import playsound
import pyaudio
from pocketsphinx import Decoder, get_model_path
import struct
import wave
import os

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
FORMAT=pyaudio.paInt16
CHUNK=val
CHANNELS=1
RATE=16000

audio=pyaudio.PyAudio()

#HOST="192.168.66.106"
#HOST = "192.168.0.247"  

HOST="34.125.102.191" 
PORT = 40002                     


if 1:
    soc = socket.socket()
    soc.connect((HOST, PORT))
    soc.send(b"client")
    print("connected")

    
    data = soc.recv(val)
    peer = bytes_to_addr(data)
    print('peer:', *peer)
    
    stream=audio.open(format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input= True,
        frames_per_buffer=CHUNK)
    decoder.start_utt()
    
    stream1=audio.open(format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        output= True,
        frames_per_buffer=CHUNK)
    
    
    print("Starting:")
    while 1:
        data=stream.read(val)
        stream1.write(data)
        print("sent data")
        if data:
            decoder.process_raw(data, False, False)
            
        if decoder.hyp() is not None:
            print([(seg.word, seg.prob, seg.start_frame, seg.end_frame) for seg in decoder.seg()])
            print("Detected %s" % (decoder.hyp().hypstr))
            decoder.end_utt()
            print("milind activated")
            playsound("sound.wav")
            
            frames = []
            data=stream.read(val)
            stream1.write(data)
            data=stream.read(val)
            stream1.write(data)

            for i in range(0, int(RATE / CHUNK * 2)):
                print("in for loop",i)
                data=stream.read(val)
                stream1.write(data)
                frames.append(data)
                
            
            wf = wave.open("test audio.wav", 'wb')
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(2)
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
            wf.close()
            
            
            filename="./test audio.wav"
                        
            with open(filename, "rb") as f:
                while True:
                    bytes_read = f.read(val)
                    if not bytes_read:
                        break
                    soc.sendall(bytes_read)
                    
                    
            
            soc.sendall(b"stop")
           # _=soc.recv(val)
            print("audio sent")     
            
            decoder.start_utt()
                        
      
# except Exception as e:
#     print("Error: ",e)