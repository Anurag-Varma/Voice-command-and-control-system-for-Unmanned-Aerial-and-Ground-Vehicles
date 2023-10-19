import socket               # Import socket module

s = socket.socket()         # Create a socket object
host = "172.23.89.226"  # Get local machine name
port = 40003          # Reserve a port for your service.

s.connect((host, port))
print(s.recv(1024))
s.send(b'Hello server!')
s.close()
