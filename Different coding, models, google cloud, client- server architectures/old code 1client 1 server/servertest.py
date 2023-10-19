import socket               # Import socket module

s = socket.socket()         # Create a socket object
host = "0.0.0.0"  # Get local machine name
port = 40003              # Reserve a port for your service.
print(host)

try:
    s.bind((socket.gethostname(), port))        # Bind to the port

    s.listen(5)                 # Now wait for client connection.
    while True:
        c, addr = s.accept()     # Establish connection with client.
        print('Got connection from', addr)
        mess=b'Thank you for connecting'
        c.send(mess)
        test=c.recv(1024)
        print(test)
        c.close()                # Close the connection
except:
    s.close()