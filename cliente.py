import socket

s = socket.socket()
host = socket.gethostname()
port = 1234
s.connect((host, port))

print("Conexion establecida. Esperando archivo por parte del servidor")

nombreArchivo = s.recv(1024).decode()
archivo = open("Recibido_{}".format(nombreArchivo), "wb")

recibido = s.recv(65536)
while recibido != b'':
    archivo.write(recibido)
    recibido = s.recv(65536)

archivo.close()

print("Archivo recibido")

s.close()
