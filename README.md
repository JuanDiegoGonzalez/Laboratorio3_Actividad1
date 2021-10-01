# Instrucciones de instalacion y ejecucion de los programas:

## Servidor:

1. Ejecutar el archivo "servidor.py" en la carpeta "Servidor".
2. Ingresar por consola el nombre del archivo a enviar (incluyendo la extension). Este debe estar en la carpeta "Servidor/ArchivosAEnviar".
3. Ingresar por consola la cantidad de clientes en simultaneo (minimo 1). Luego de esto, el servidor esta "listo para atender clientes".

Nota: La carpeta "Logs" la crea automaticamente la aplicacion.


## Cliente:

1. Una vez el servidor este "listo para atender clientes", ejecutar el archivo "cliente.py" en la carpeta "Cliente".
2. Ingresar por consola cualquier caracter (no vacio) para indicar que el cliente esta listo para recibir el archivo. Luego de esto, el cliente quedara en espera hasta que los        demas clientes esten listos.
3. Repetir el paso #1 y #2 del Cliente tantas veces como se haya indicado en el paso #3 del Servidor. Es decir, ejecutar todos los clientes que este esperando el servidor.
4. Cuando todos los clientes esten listos, iniciara la transmision del archivo.

Nota: Las carpetas "Logs" y "ArchivosRecibidos" las crea automaticamente la aplicacion.
