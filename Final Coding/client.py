import socket
#from playsound import playsound
import pyaudio
from pocketsphinx import Decoder, get_model_path
import struct
import wave
import os
import signal, sys

def signal_handler(signal, frame):
    print("Program exiting ")
    soc.shutdown(socket.SHUT_RDWR)
    soc.close() 
    print("stopped")
    sys.exit(0)
    

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



HOST="10.242.222.142" 
PORT = 40002                     

soc = socket.socket()
try:
    soc.connect((HOST, PORT))
    _=soc.recv(val)
    print(HOST,PORT)
    print("connected")
    
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
        print("Waiting for activation command:")
        if data:
            decoder.process_raw(data, False, False)
            
        if decoder.hyp() is not None:
            print([(seg.word, seg.prob, seg.start_frame, seg.end_frame) for seg in decoder.seg()])
            print("Detected %s" % (decoder.hyp().hypstr))
            decoder.end_utt()
            print("milind activated")
            #playsound("sound.wav")
            
            frames = []
            data=stream.read(val)
            stream1.write(data)
            data=stream.read(val)
            stream1.write(data)
            
            print("Sending audio")
            for i in range(0, int(RATE / CHUNK * 1.5)):
                print("In for loop",i)
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
            print("audio sent")     
            
            decoder.start_utt()
            
            mess=soc.recv(val)
            print("Command is:"+mess.decode('utf-8'))
            if mess==b"stop":
                break   
        signal.signal(signal.SIGINT, signal_handler)
      
    soc.shutdown(socket.SHUT_RDWR)
    soc.close()   

except KeyboardInterrupt:
    print("keyboard error")
    
except Exception as e:
     print("Error: ",e)
     soc.shutdown(socket.SHUT_RDWR)
     soc.close() 
     print("stopped")