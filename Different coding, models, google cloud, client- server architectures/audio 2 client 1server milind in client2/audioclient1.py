import socket
from playsound import playsound
import pyaudio
import struct

def addr_to_bytes(addr):
    return socket.inet_aton(addr[0]) + struct.pack('H', addr[1])

def bytes_to_addr(addr):
    return (socket.inet_ntoa(addr[:4]), struct.unpack('H', addr[4:])[0])



val=1024*2
FORMAT=pyaudio.paInt16
CHUNK=val
CHANNELS=1
RATE=16000

audio=pyaudio.PyAudio()

#HOST="192.168.66.106"
#HOST = "192.168.0.247"  

HOST="34.125.102.191" 
PORT = 40003                        


if 1:
    soc = socket.socket()
    soc.connect((HOST, PORT))
    print("connected")
    
    data = soc.recv(1024)
    peer = bytes_to_addr(data)
    print('peer:', *peer)
    
    stream=audio.open(format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input= True,
        frames_per_buffer=CHUNK)

    print("Sending audio to " + HOST + ":" + str(PORT))
    while 1:
        print("sending...")
        data=stream.read(val)
        soc.send(data)
        print("sent...")  
        message=soc.recv(val)
        if message==b"success":
            playsound("C:/Users/panud/OneDrive/Desktop/sound.wav")
            print("success")
            message=""
# except Exception as e:
#     print("Error: ",e)