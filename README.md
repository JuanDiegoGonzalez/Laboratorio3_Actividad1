# Instrucciones de instalacion y ejecucion de los programas:

## Servidor:

1. Ejecutar el archivo "servidor.py" en la carpeta "Servidor".
2. Ingresar por consola el nombre del archivo a enviar (incluyendo la extension). Este debe estar en la carpeta "Servidor/ArchivosAEnviar".
3. Ingresar por consola la cantidad de clientes que se van a atender en simultaneo (minimo 1).
4. El servidor va a intentar obtener automaticamente la direccion IP de la maquina donde se esta ejecutando:  
     a) Si se logra identificar la IP automaticamente, el servidor estara "listo para atender clientes".  
     b) Si ocurre algun error en este proceso, se debe ingresar manualmente por consola la direccion IP de esa maquina (se puede consultar ejecutando el comando "ipconfig" o "ifconfig" en una terminal). Luego de esto, el servidor estara "listo para atender clientes".

Nota: La carpeta "Logs" la crea automaticamente la aplicacion (en caso de que no este creada).


## Cliente:

1. Una vez el servidor este "listo para atender clientes", ejecutar el archivo "cliente.py" en la carpeta "Cliente".
2. Ingresar por consola la cantidad de clientes que se desea crear en esa ejecucion del programa (idealmente, indicar la misma cantidad establecida en el paso #3 del servidor).
3. Ingresar por consola la direccion IP del servidor. Esta fue indicada en la terminal donde se ejecuto el servidor.
4. Cuando se conecten todos los clientes que esta esperando el servidor, iniciara la transmision del archivo.

Nota: Las carpetas "Logs" y "ArchivosRecibidos" las crea automaticamente la aplicacion (en caso de que no esten creadas).
