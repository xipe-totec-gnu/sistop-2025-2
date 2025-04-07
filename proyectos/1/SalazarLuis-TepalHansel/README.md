# Proyecto 1: Don Rata

## Planteamiento del problema
Dentro de la facultad es normal que en un día normal de clases,a los alumnos se nos olvide traer los materiales, la bata o las impresiones que van a ser requeridas para una clase. Por lo que nos vemos en la sitaución desesperada de acudir a "Don Rata". Sin embargo, como a muchos en el anexo de Ingenieria les pasa esta situación, Don Rata no puede darse abasto a todos los alumnos que acuden a su local y muchas veces el orden con el que llegas a la fila no es el mismo orden en el que te atienden, aunque casi siempre te atienden si ven que llevas mucho tiempo esperando.

En don rata usualemente suelen trabajar tres persona, por lo que cada uno de ellos puede atender solo a una persona a la vez, es decir el estudiante que llegue mientras los trabajadores están atendiendo a otro debe esperar como todos. Ya que si no lo hace puede desatar una confusión entre Don Rata y los pedidos de los alumnos.

## Problemas de Concurrencia
1. **Condición de carrera**: Si dos o más estudiantes intentan acceder al mismo trabajador al mismo tiempo, puede que los pedidos se confundan.
2. **Espera Activa**: Si no hay estudiantes que atender, sería buena práctica que los hilos trabajadores se bloqueen hasta que llegue un estudiante.
3. **Inanición**: Si hay muchos estudiantes en la fila y Don Rata solo atiende a uno a la vez, algunos estudiantes pueden quedar esperando indefinidamente.

## Solución
Para solucionar este problema y ayudar a los trabajadores de Don Rata a mejorar la forma en la que atienden a los alumnos, se siguió la siguiente lógica de desarrollo:

- Se utilizaron semáforos tipo mutex con la finalidad de sincronizar la atención entre los alumnos y trabajadores, evitando condiciones de carrera al asegurarnos de que ningún alumno pueda interrumpir o colarse mientras se está atendiendo a otro.

- Para evitar problemas con la espera activa, los trabajadores permanecen bloqueados (dormidos) hasta que llegue un alumno que necesite ser atendido. Esto nos permite ahorrar recursos y hace que la solución sea más limpia y eficiente.

- Con el fin de reducir la posibilidad de inanición, se implementó una especie de cola de trabajadores disponibles. De esta forma, los alumnos van tomando al trabajador que esté libre a medida que llegan.

### Flujo de trabajo
1. El trabajador permanece bloqueado hasta que reciba una solicitud de un alumno.
2. Durante este tiempo, se encuentra en la cola de disponibilidad.
3. Un alumno lo toma de esa cola y lo despierta para que lo atienda.
4. Cuando termine de atenderlo este vuelve a añadirse a la cola de disponibilidad y permanece así hasta que llegue otro alumno.

## Bibliotecas y herramientas utilizadas
- `threading`: Para manejar los hilos de los estudiantes y trabajadores.
- `queue`: Para manejar la cola de estudiantes que esperan ser atendidos.
- `random`: Para simular el tiempo de espera y el tiempo de atención.
- `tkinter`: Para crear la interfaz gráfica de usuario (GUI) que simula la tienda de Don Rata.
- `math`: Para realizar cálculos en a la ubicación de un objeto dentro de la interfaz.

## Ejecución
Para ejecutar el programa, simplemente ejecute el archivo `interfaz.py` que se encuentra dentro de la carpeta de frontend. Asegúrese de tener instaladas las bibliotecas necesarias.
```bash
sudo apt-get install python3-tk
```
Si usa un sistema basado en Red Hat como Fedora, use el siguiente comando:
```bash
sudo dnf install python3-tkinter
```