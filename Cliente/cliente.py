import socket, hashlib, time, os
from datetime import datetime

# Declaracion de atributos
host = None
port = None

def recibirArchivoDelServidor(s):

    # Se recibe el numero del cliente
    numCliente = s.recv(1024).decode()

    # Se recibe la cantidad de conexiones concurrentes
    cantConexiones = s.recv(1024).decode()

    # Se recibe el nombre del archivo
    nombreArchivo = s.recv(1024).decode()

    # Se recibe el hash del archivo
    hashRecibido = s.recv(1024)

    # Se abre el archivo donde se guardara el contenido recibido
    if not os.path.isdir('ArchivosRecibidos'):
        os.mkdir(os.path.join(os.getcwd(), "ArchivosRecibidos"))
    archivo = open("ArchivosRecibidos/Cliente{}-Prueba-{}.txt".format(numCliente, cantConexiones), "wb")

    # Se recibe y se escribe el contenido del archivo
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

    # Se crea y se escribe el log
    if not os.path.isdir('Logs'):
        os.mkdir(os.path.join(os.getcwd(), "Logs"))
    fechaStr = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    archivo = open("Logs/{}({}).txt".format(fechaStr, numCliente), "w")

    archivo.write("Nombre del archivo recibido: {}\n".format(nombreArchivo))
    archivo.write("Tamaño del archivo recibido: {} bytes\n\n".format(os.path.getsize("ArchivosRecibidos/Cliente{}-Prueba-{}.txt".format(numCliente, cantConexiones))))

    archivo.write("Servidor desde el que se realizo la transferencia: ({}, {})\n\n".format(host, port))

    # archivo.write()

    archivo.close()

if __name__ == "__main__":
    # Se crea el socket del cliente (donde se conecta al servidor)
    s = socket.socket()
    host = socket.gethostname()
    port = 1234
    s.connect((host, port))

    print("Conexion establecida. Listo para recibir el archivo desde el servidor")

    recibirArchivoDelServidor(s)
    time.sleep(2)
