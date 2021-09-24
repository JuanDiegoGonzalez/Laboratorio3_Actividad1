import socket

s = socket.socket()
host = socket.gethostname()
port = 1234
s.connect((host, port))

archivo = open("Recibido_{}".format("test.txt"), "wb")
#archivo = open("intro-domRecibido.mp4", "wb")

recibido = s.recv(65536)

while recibido != b'':
    archivo.write(recibido)
    recibido = s.recv(65536)

archivo.close()
s.close()
