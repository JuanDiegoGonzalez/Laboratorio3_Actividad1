import socket, hashlib, time, os
from datetime import datetime

# Declaracion de atributos
host = None
port = None
transfExitosa = None

def recibirArchivoDelServidor(s):
    global host, port, transfExitosa

    # Se envía la confirmacion de "listo"
    listo = input("Ingrese algun caracter cuando este listo para recibir: ")
    while not listo:
        listo = input("Ingrese algun caracter cuando este listo para recibir: ")
    s.send(b"Listo")
    print("Cliente listo para recibir")

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
    while recibido != b'Fin':
        contenido += recibido
        archivo.write(recibido)
        recibido = s.recv(65536)
    archivo.close()
    print("Archivo recibido")

    # Se comprueba el hash recibido
    hashCode = hashlib.sha512()
    hashCode.update(contenido)
    mensajeComprobacionHash = "La entrega del archivo fue exitosa" if hashCode.digest() == hashRecibido else "La entrega del archivo NO fue exitosa"
    print("La entrega del archivo fue exitosa")

    # Se envia el resultado de la comprobacion del hash
    s.send(mensajeComprobacionHash.encode())

    # Se crea y se escribe el log
    if not os.path.isdir('Logs'):
        os.mkdir(os.path.join(os.getcwd(), "Logs"))
    fechaStr = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    archivo = open("Logs/{}({}).txt".format(fechaStr, numCliente), "w")

    archivo.write("Nombre del archivo recibido: {}\n".format(nombreArchivo))
    archivo.write("Tamano del archivo recibido: {} bytes\n\n".format(os.path.getsize("ArchivosRecibidos/Cliente{}-Prueba-{}.txt".format(numCliente, cantConexiones))))

    archivo.write("Servidor desde el que se realizo la transferencia: ({}, {})\n\n".format(socket.gethostbyname(host), port))

    archivo.write("{}\n\n".format(mensajeComprobacionHash))

    # archivo.write()

    archivo.close()

    s.close()

if __name__ == "__main__":
    # Se crea el socket del cliente (donde se conecta al servidor)
    s = socket.socket()
    host = socket.gethostname()
    port = 1234
    s.connect((host, port))

    print("Conexion establecida. Listo para recibir el archivo desde el servidor")

    recibirArchivoDelServidor(s)
    time.sleep(2)
