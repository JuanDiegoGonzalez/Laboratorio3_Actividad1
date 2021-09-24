import socket
 
s = socket.socket()
host = socket.gethostname()
port = 1234
s.bind((host, port))
s.listen(25)

nombreArchivo = input("Ingrese el nombre del archivo a transferir (incluyendo la extension): ")
archivo = open(nombreArchivo, "rb")
contenido = archivo.read()
archivo.close()

while True:
    sc, addr = s.accept()

    print('Connection obtained from ... ', addr)

    sc.send(bytes(nombreArchivo.encode()))
    sc.send(contenido)
    sc.close()

s.close()
