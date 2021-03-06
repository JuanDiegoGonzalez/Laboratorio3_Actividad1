import socket, threading, hashlib, time, os
from datetime import datetime

# Declaracion de atributos
host = None
port = None
transfExitosa = None
tiempoDeTransmision = None

def recibirArchivoDelServidor(s, listo):
    global host, port, transfExitosa, tiempoDeTransmision

    # Se envía la confirmacion de "listo"
    while not listo:
        listo = input("Ingrese cualquier caracter cuando este listo para recibir: ")
    s.send(b"Listo")
    print("Cliente listo para recibir, esperando a los demas clientes")

    # Se recibe el numero del cliente
    numCliente = s.recv(1024).decode()

    # Se recibe la cantidad de conexiones concurrentes
    cantConexiones = s.recv(1024).decode()

    # Se recibe el nombre del archivo
    nombreArchivo = s.recv(1024).decode()

    # Se recibe el hash del archivo
    hashRecibido = s.recv(1024)

    # Se abre el archivo donde se guardara el contenido recibido
    archivo = open("ArchivosRecibidos/Cliente{}-Prueba-{}.{}".format(numCliente, cantConexiones, nombreArchivo.split(".")[-1]), "wb")

    print("Transmision iniciada, recibiendo archivo desde el servidor...")
    inicioTransmision = time.time()

    # Se recibe y se escribe el contenido del archivo
    recibido = s.recv(65536)
    i = 0
    while not str(recibido).endswith('Fin\''):
        archivo.write(recibido)
        i+=1
        print("Cliente {}: Parte {} recibida".format(numCliente,i))
        recibido = s.recv(65536)
    archivo.write(recibido[:-3])

    tiempoDeTransmision = time.time() - inicioTransmision
    print("Transmision completa. Archivo recibido.")

    archivo.close()

    # Se comprueba el hash recibido
    hashCode = hashlib.sha512()
    archivo = open("ArchivosRecibidos/Cliente{}-Prueba-{}.{}".format(numCliente, cantConexiones, nombreArchivo.split(".")[-1]), "rb")
    hashCode.update(archivo.read())
    archivo.close()
    mensajeComprobacionHash = "La entrega del archivo fue exitosa" if hashCode.digest() == hashRecibido else "La entrega del archivo NO fue exitosa"
    print(mensajeComprobacionHash)

    # Se envia el resultado de la comprobacion del hash
    s.send(mensajeComprobacionHash.encode())

    # Se crea y se escribe el log
    escribirLog(numCliente, nombreArchivo, cantConexiones, mensajeComprobacionHash, tiempoDeTransmision)

    s.close()

def escribirLog(numCliente, nombreArchivo, cantConexiones, mensajeComprobacionHash, tiempoDeTransmision):
    # a.
    fechaStr = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    archivo = open("Logs/{} (Cliente {}).txt".format(fechaStr, numCliente), "w")

    # b.
    archivo.write("Nombre del archivo recibido: {}\n".format(nombreArchivo))
    archivo.write("Tamano del archivo recibido: {} bytes\n\n".format(os.path.getsize("ArchivosRecibidos/Cliente{}-Prueba-{}.{}".format(numCliente, cantConexiones, nombreArchivo.split(".")[-1]))))

    # c.
    archivo.write("Servidor desde el que se realizo la transferencia: ({}, {})\n\n".format(host, port))

    # d.
    archivo.write("Resultado de la transferencia: {}\n\n".format(mensajeComprobacionHash))

    # e.
    archivo.write("Tiempo de transmision: {:.2f} segundos\n".format(tiempoDeTransmision))

    archivo.close()

if __name__ == "__main__":
    try:
        # Se establece la cantidad de clientes que se van a crear
        cantThreads = int(input("Ingrese la cantidad de clientes a crear: "))
        if cantThreads < 1:
            raise ValueError("[Error] El numero debe ser mayor a 0")

        # Se crea la carpeta para guardar los archivos (si no existe)
        if not os.path.isdir('ArchivosRecibidos'):
            os.mkdir(os.path.join(os.getcwd(), "ArchivosRecibidos"))

        # Se crea la carpeta para guardar los logs (si no existe)
        if not os.path.isdir('Logs'):
            os.mkdir(os.path.join(os.getcwd(), "Logs"))

        # Se crean los threads de los clientes
        host = input("Ingrese la direccion IP del servidor (esta fue indicada en la terminal donde se ejecuto el servidor): ")
        port = 1234
        threads = []

        for i in range(cantThreads):
            s = socket.socket()
            s.connect((host, port))
            print("Conexion establecida (Thread {}).".format(i+1))
            thread = threading.Thread(target=recibirArchivoDelServidor, args=(s, '1'))
            threads.append(thread)

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        time.sleep(2)

    except (ValueError, ConnectionResetError) as e:
        print("\n", e, sep="")
