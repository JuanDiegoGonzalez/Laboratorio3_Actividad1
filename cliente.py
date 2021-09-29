import socket, hashlib, time

# Se crea el socket del cliente (donde se conecta al servidor)
s = socket.socket()
host = socket.gethostname()
port = 1234
s.connect((host, port))

print("Conexion establecida. Listo para recibir el archivo desde el servidor")

# Se recibe el nombre del archivo
nombreArchivo = s.recv(1024).decode()
archivo = open("Recibido_{}".format(nombreArchivo), "wb")

# Se recibe el hash del archivo
hashRecibido = s.recv(1024)
print(hashRecibido, "\n")

# Se recibe el contenido del archivo
recibido = s.recv(65536)
contenido = b''
while recibido != b'':
    contenido += recibido
    archivo.write(recibido)
    recibido = s.recv(65536)

archivo.close()
s.close()
print("Archivo recibido")

# Se comprueba el hash recibido
hashCode = hashlib.sha512()
hashCode.update(contenido)
if hashCode.digest() == hashRecibido:
    print("La entrega del archivo fue exitosa")
else:
    print("La entrega del archivo NO fue exitosa")

time.sleep(2)
