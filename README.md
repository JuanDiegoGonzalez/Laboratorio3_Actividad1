# Instrucciones de instalacion y ejecucion de los programas:

## Servidor:

1. Ejecutar el archivo "servidor.py" en la carpeta "Servidor".
2. Ingresar por consola el nombre del archivo a enviar (incluyendo la extension). Este debe estar en la carpeta "Servidor/ArchivosAEnviar".
3. Ingresar por consola la cantidad de clientes en simultaneo (minimo 1). Luego de esto, el servidor esta "listo para atender clientes".

Nota: La carpeta "Logs" la crea automaticamente la aplicacion (en caso de que no este creadas).


## Cliente:

1. Una vez el servidor este "listo para atender clientes", ejecutar el archivo "cliente.py" en la carpeta "Cliente".
2. Ingresar por consola la cantidad de clientes que se desea crear en esa ejecucion del programa (idealmente, indicar la misma cantidad establecida en el paso #3 del servidor).
3. Cuando se conecten todos los clientes que esta esperando el servidor, iniciara la transmision del archivo.

Nota: Las carpetas "Logs" y "ArchivosRecibidos" las crea automaticamente la aplicacion (en caso de que no esten creadas).
