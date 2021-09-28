import socket, threading, hashlib, time, os

# Atributos
nombreArchivo = None
contenidoArchivo = None
threadsClientes = []
cantConexiones = None

def enviarArchivoAlCliente(socket, infoCliente):
    global nombreArchivo, contenidoArchivo

    # Se envia el nombre del archivo
    socket.send(bytes(nombreArchivo.encode()))

    # Se envia el codigo de hash del archivo
    hashCode = hashlib.sha512()
    hashCode.update(contenidoArchivo)
    socket.send(hashCode.digest())
    time.sleep(0.5)

    # Se envia el contenido del archivo
    socket.send(contenidoArchivo)

    socket.close()
    print("Archivo enviado al cliente ... ", infoCliente)

if __name__ == "__main__":
    try:
        # Se carga el contenido del archivo
        nombreArchivo = input("Ingrese el nombre del archivo a transferir (incluyendo la extension): ")
        archivo = open(nombreArchivo, "rb")
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
            thread = threading.Thread(target=enviarArchivoAlCliente, args=(clientSocket,addr))
            threadsClientes.append(thread)

            if len(threadsClientes) == cantConexiones:
                for thread in threadsClientes:
                    thread.start()

                for thread in threadsClientes:
                    thread.join()

                threadsClientes = []

                # Se crea y se escribe el log
                if not os.path.isdir('Logs'):
                    os.mkdir(os.path.join(os.getcwd(), "Logs"))

        s.close()

    except (FileNotFoundError, ValueError, ConnectionResetError) as e:
        print("\n", e, sep="")
