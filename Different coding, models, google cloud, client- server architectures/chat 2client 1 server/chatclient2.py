import socket
import struct

def addr_to_bytes(addr):
    return socket.inet_aton(addr[0]) + struct.pack('H', addr[1])

def bytes_to_addr(addr):
    return (socket.inet_ntoa(addr[:4]), struct.unpack('H', addr[4:])[0])

def udp_client(server):
    soc = socket.socket()
    soc.connect(server)
    print("connected")
    
    data = soc.recv(1024)
    peer = bytes_to_addr(data)
    print('peer:', *peer)
    
    while 1:
        data = soc.recv(1024)
        print(data.decode('utf-8'))

        print("Enter input:")
        mess=input()
        soc.send(bytes(mess,'utf-8'))
    
  

    
server_addr = ('34.125.102.191', 40004) # the server's  public address
udp_client(server_addr)