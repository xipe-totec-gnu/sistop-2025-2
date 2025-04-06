# Proyecto 1: Don Rata

## Planteamiento del problema
Dentro de la facultad es normal que en un día normal de clases,a los alumnos se nos olvide traer los materiales, la bata o las impresiones que van a ser requeridas para una clase. Por lo que nos vemos en la sitaución desesperada de acudir a "Don Rata". Sin embargo, como a muchos en el anexo de Ingenieria les pasa esta situación, Don Rata no puede darse abasto a todos los alumnos que acuden a su local y muchas veces el orden con el que llegas a la fila no es el mismo orden en el que te atienden, aunque casi siempre te atienden si ven que llevas mucho tiempo esperando.

En don rata usualemente suelen trabajar tres persona, por lo que cada uno de ellos puede atender solo a una persona a la vez, es decir el estudiante que llegue mientras los trabajadores están atendiendo a otro debe esperar como todos. Ya que si no lo hace puede desatar una confusión entre Don Rata y los pedidos de los alumnos.

## Problemas de Concurrencia
1. **Condición de carrera**: Si dos o más estudiantes intentan acceder al mismo trabajador al mismo tiempo, puede que los pedidos se confundan.
2. **Espera Activa**: Si no hay estudiantes que atender, sería buena práctica que los hilos trabajadores se bloqueen hasta que llegue un estudiante.
3. **Inanición**: Si hay muchos estudiantes en la fila y Don Rata solo atiende a uno a la vez, algunos estudiantes pueden quedar esperando indefinidamente.
