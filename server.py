import socket
 
s = socket.socket()
host = socket.gethostname()
port = 1234
s.bind((host, port))
s.listen(25)

archivo = open("ArchivosATransferir/test.txt", "rb")
#archivo = open("intro-dom.mp4", "rb")
contenido = archivo.read()
archivo.close()

while True:
    sc, addr = s.accept()

    print('Connection obtained from ... ', addr)

    sc.send(contenido)
    sc.close()

s.close()
