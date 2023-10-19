import socket
import struct

val=1024*2


PORT=40002
addr = ('', PORT)
print("Available on port "+str(PORT))


def addr_to_bytes(addr):
    return socket.inet_aton(addr[0]) + struct.pack('H', addr[1])

def bytes_to_addr(addr):
    return (socket.inet_ntoa(addr[:4]), struct.unpack('H', addr[4:])[0])

def server(addr):
    soc = socket.socket()
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    soc.bind(addr)
    soc.listen(5)
    print("listening")
    
    conn1, client_a = soc.accept()
    connection=conn1.recv(val)
    print(conn1,client_a)
    
    if(connection==b"client"):
        conn2, client_b = soc.accept()
        connection=conn2.recv(val)
        print(conn2,client_b)
    else:
        conn2=conn1
        client_b=client_a
        conn1, client_a = soc.accept()
        connection=conn1.recv(val)
        print(conn1,client_a)
        
    
    
    conn1.send(addr_to_bytes(client_b))
    conn2.send(addr_to_bytes(client_a))
    
    while 1:
      data=conn1.recv(val)
      conn2.send(data)
    
    soc.shutdown(socket.SHUT_RDWR)
    soc.close()


server(addr)
