import socket
 
s = socket.socket()
host = socket.gethostname()
port = 1234
s.bind((host, port))
s.listen(5)

while True:
    c, addr = s.accept()
    print('Connection obtained from ... ', addr)
    c.send(b'Grace for connecting')
    c.close ()