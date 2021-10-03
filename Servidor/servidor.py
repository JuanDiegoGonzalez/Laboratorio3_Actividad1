import socket, threading, hashlib, time, os
from datetime import datetime

# Declaracion de atributos
nombreArchivo = None
contenidoArchivo = None
cantConexiones = None
threadsClientes = []
direccionesClientes = []
cantidadListos = 0
resultComprobacionHash = []
tiemposDeTransmision = []

def enviarArchivoAlCliente(socket, infoCliente, numCliente):
    global cantidadListos

    # Se recibe la confirmacion de listo
    socket.recv(1024).decode()
    cantidadListos += 1

    # Se espera a que los demas clientes esten listos
    while cantidadListos < cantConexiones:
        print("Cantidad de clientes listos: {}".format(cantidadListos))
        ...

    # Se envia el id del cliente
    socket.send(numCliente.encode())
    time.sleep(0.2)

    # Se envia la cantidad de conexiones concurrentes
    socket.send(str(cantConexiones).encode())
    time.sleep(0.2)

    # Se envia el nombre del archivo
    socket.send(nombreArchivo.encode())
    time.sleep(0.2)

    # Se envia el codigo de hash del archivo
    hashCode = hashlib.sha512()
    hashCode.update(contenidoArchivo)
    socket.send(hashCode.digest())
    time.sleep(0.2)

    inicioTransmision = time.time()

    # Se envia el contenido del archivo
    socket.send(contenidoArchivo)
    socket.send('Fin'.encode())
    time.sleep(0.2)

    tiemposDeTransmision[int(numCliente)-1] = time.time() - inicioTransmision

    # Se recibe el resultado de la comprobacion del hash
    resultComprobacionHash[int(numCliente)-1] = socket.recv(1024).decode()
    socket.close()
    print("Archivo enviado al cliente ... ", infoCliente)

def escribirLog(tiemposDeTransmision):
    # a.
    fechaStr = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    archivo = open("Logs/{}.txt".format(fechaStr), "w")

    # b.
    archivo.write("Nombre del archivo enviado: {}\n".format(nombreArchivo))
    archivo.write(
        "Tamano del archivo enviado: {} bytes\n\n".format(os.path.getsize("ArchivosAEnviar/{}".format(nombreArchivo))))

    # c.
    archivo.write("Clientes a los que se realizo la transferencia:\n")
    for i in range(cantConexiones):
        archivo.write("Cliente {}: {}\n".format(i + 1, direccionesClientes[i]))
    archivo.write("\n")

    # d.
    archivo.write("Resultados de la transferencia:\n")
    for i in range(cantConexiones):
        archivo.write("Cliente {}: {}\n".format(i + 1, resultComprobacionHash[i]))
    archivo.write("\n")

    # e.
    archivo.write("Tiempos de transmision:\n")
    for i in range(cantConexiones):
        archivo.write("Cliente {}: {:.2f} segundos\n".format(i + 1, tiemposDeTransmision[i]))
    archivo.write("\n")

    archivo.close()

if __name__ == "__main__":
    try:
        # Se carga el contenido del archivo
        nombreArchivo = input("Ingrese el nombre del archivo a transferir (incluyendo la extension): ")
        archivo = open("ArchivosAEnviar/{}".format(nombreArchivo), "rb")
        contenidoArchivo = archivo.read()
        archivo.close()

        # Se establece la cantidad de clientes a atender al tiempo
        cantConexiones = int(input("Ingrese la cantidad de conexiones concurrentes: "))
        if cantConexiones < 1:
            raise ValueError("[Error] El numero debe ser mayor a 0")

        print("\nServidor listo para atender clientes")

        # Se crea el socket del servidor (donde recibe a los clientes)
        s = socket.socket()
        host = socket.gethostname()
        port = 1234
        s.bind((host, port))
        s.listen(25)
        print("Direccion IP del servidor:", socket.gethostbyname(host))

        # Se crea la carpeta para guardar el log (si no existe)
        if not os.path.isdir('Logs'):
            os.mkdir(os.path.join(os.getcwd(), "Logs"))

        # Se inicializan las listas de clientes
        resultComprobacionHash = [None for i in range(cantConexiones)]
        tiemposDeTransmision = [None for i in range(cantConexiones)]

        # Se reciben y se atienden a los clientes
        while True:
            clientSocket, addr = s.accept()
            print('Conexion establecida desde ... ', addr)
            thread = threading.Thread(target=enviarArchivoAlCliente, args=(clientSocket, addr, str(len(threadsClientes)+1)))
            threadsClientes.append(thread)
            direccionesClientes.append(addr)

            # Cuando se completa el grupo de clientes, se les envia el archivo y se escribe el log
            if len(threadsClientes) == cantConexiones:
                for thread in threadsClientes:
                    thread.start()

                for thread in threadsClientes:
                    thread.join()

                escribirLog(tiemposDeTransmision)

                # Se reinician las listas de clientes
                threadsClientes = []
                direccionesClientes = []
                cantidadListos = 0
                resultComprobacionHash = [None for i in range(cantConexiones)]
                tiemposDeTransmision = [None for i in range(cantConexiones)]

    except (FileNotFoundError, ValueError, ConnectionResetError) as e:
        print("\n", e, sep="")
