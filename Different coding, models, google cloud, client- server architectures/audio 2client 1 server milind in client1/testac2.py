import socket
import struct

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
                
#except Exception as e:
#        print("Error:",e)