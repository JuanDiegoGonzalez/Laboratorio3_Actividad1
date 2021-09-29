import socket, threading, hashlib, time, os
from datetime import datetime

# Declaracion de atributos
nombreArchivo = None
contenidoArchivo = None
threadsClientes = []
direccionesClientes = []
cantConexiones = None

def enviarArchivoAlCliente(socket, infoCliente, numCliente):
    global nombreArchivo, contenidoArchivo

    # Se envia el numero del cliente
    socket.send(numCliente.encode())
    time.sleep(0.1)

    # Se envia la cantidad de conexiones concurrentes
    socket.send(str(cantConexiones).encode())
    time.sleep(0.1)

    # Se envia el nombre del archivo
    socket.send(nombreArchivo.encode())
    time.sleep(0.1)

    # Se envia el codigo de hash del archivo
    hashCode = hashlib.sha512()
    hashCode.update(contenidoArchivo)
    socket.send(hashCode.digest())
    time.sleep(0.1)

    # Se envia el contenido del archivo
    socket.send(contenidoArchivo)
    time.sleep(0.1)

    socket.close()
    print("Archivo enviado al cliente ... ", infoCliente)

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

        # Se reciben y se atienden a los clientes
        while True:
            clientSocket, addr = s.accept()
            print('Conexion establecida desde ... ', addr)
            thread = threading.Thread(target=enviarArchivoAlCliente, args=(clientSocket,addr, str(len(threadsClientes)+1)))
            threadsClientes.append(thread)
            direccionesClientes.append(addr)

            # Cuando se completa el grupo de clientes, se les envia el archivo y se escribe el log
            if len(threadsClientes) == cantConexiones:
                for thread in threadsClientes:
                    thread.start()

                for thread in threadsClientes:
                    thread.join()

                # Se crea y se escribe el log
                if not os.path.isdir('Logs'):
                    os.mkdir(os.path.join(os.getcwd(), "Logs"))
                fechaStr = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
                archivo = open("Logs/{}.txt".format(fechaStr), "w")

                archivo.write("Nombre del archivo enviado: {}\n".format(nombreArchivo))
                archivo.write("Tamaño del archivo enviado: {} bytes\n\n".format(os.path.getsize("ArchivosAEnviar/{}".format(nombreArchivo))))

                archivo.write("Clientes a los que se realizo la transferencia:\n")
                for cliente in direccionesClientes:
                    archivo.write("{}\n".format(cliente))
                archivo.write("\n")

                # archivo.write()

                archivo.close()

                # Se reinician las listas de clientes
                threadsClientes = []
                direccionesClientes = []

    except (FileNotFoundError, ValueError, ConnectionResetError) as e:
        print("\n", e, sep="")
