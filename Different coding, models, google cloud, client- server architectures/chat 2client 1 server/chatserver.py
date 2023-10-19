import socket
import struct

def addr_to_bytes(addr):
    return socket.inet_aton(addr[0]) + struct.pack('H', addr[1])

def bytes_to_addr(addr):
    return (socket.inet_ntoa(addr[:4]), struct.unpack('H', addr[4:])[0])

def udp_server(addr):
    soc = socket.socket()
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    soc.bind(addr)
    soc.listen(5)
    print("listening")
    
    conn1, client_a = soc.accept()
    print(conn1,client_a)
    conn2, client_b = soc.accept()
    print(conn2,client_b)
    
    
    conn1.send(addr_to_bytes(client_a))
    conn2.send(addr_to_bytes(client_a))
    
    while 1:
      data=conn1.recv(1024)
      conn2.send(data)
      
      data=conn2.recv(1024)
      if data.decode('utf-8')!='':
        conn1.send(data)
      
    
    soc.shutdown(socket.SHUT_RDWR)
    soc.close()

addr = ('', 40004)
udp_server(addr)
