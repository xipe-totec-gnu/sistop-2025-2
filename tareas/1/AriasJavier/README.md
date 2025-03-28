### Ejercicio

Se resolvió el ejercicio de sincronización del Servidor Web.

### Entorno

Se utilizó el lenguaje de programación python. Solo es necesario tener python 3 instalado para poder ejecutar el programa.

### Solución

Para poder resolverlo se usaron semáforos. Hay 3 tipos de hilos:

- El líder, que se encarga de recibir las solicitudes y de coordinar a los hilos trabajadores.

- Los trabajadores se encargan de procesar las solicitudes que llegan al servidor y esperan a que haya una solicitud lista para ser procesada.

- Los usuarios realizan las peticiones al servidor cada cierto periodo de tiempo.

Principalmente se utilizó el patrón de hilos jefe/trabajador. Para poder sincronizar los hilos se utilizaron distintos patrones basados en semáforos, estos fueron la señalización y el mutex.

Cuando un usuario realiza una solicitud esta se introduce en la cola de nuevas peticiones y se le notifica al hilo líder por medio de un semáforo que hay una nueva petición.

El hilo líder primero lanza a los hilos trabajadores, después adquiere el semáforo y espera hasta que se realice una nueva petición, liberando el semáforo y permitiendo continuar su ejecución. Obtiene la solicitud de la cola y la introduce en la cola de peticiones pendientes, indicando  a los trabajadores que hay una nueva petición y pueden empezar a procesarla.

Los hilos trabajadores al comenzar su ejecución adquieren el semáforo, esperando hasta que el líder le indique a uno de ellos que hay una nueva petición lista para ser procesada, de esta manera solo se despertará a los hilos que tengan que ser utilizados. El hilo que se le haya asignado la solicitud la obtiene de la cola y la procesa.

Las señalizaciones se usaron para poder sincronizar los procesos y que cada uno de estos le notifique a los otros cuando pueden empezar a procesar la información necesaria, de esta manera no es necesario utilizar la espera activa consumiendo recursos de manera innecesaria. Los mutex se utilizaron para que cada uno de los hilos puedan acceder a las variables globales y no haya irregularidades en las variables.
