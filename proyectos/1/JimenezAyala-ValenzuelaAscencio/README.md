# Proyecto 1: Una situación cotidiana con concurrencia y sincronización.

## Planteamiento del problema

### Tacos el Champion

Somos dos estudiantes de la Facultad de Ingeniería y como muchos, tenemos una tradición sagrada: ir al puesto del champion a comer tacos de canasta. El champion es ya una leyenda entre los pasillos: siempre está ahí, de 7 AM a 7PM, esperando a que los estudiantes lleguemos con hambre.

Cada vez que vamos, el proceso es el mismo… o al menos debería serlo:

Primero, nos acercamos al puesto y le pedimos al champion nuestros tacos favoritos (o su famosa tortichamps, una torta de tacos de canasta). Pero tenemos que esperar a que no haya nadie más pidiendo, porque el champion solo atiende a una persona a la vez.

Si está disponible alguno de sus 4 platos, el champion nos puede servir nuestros tacos para empezar a comer. De otro modo, debemos esperar a que alguien termine.

Finalmente, hablamos con el champs para pagarle los tacos que consumimos.

Todo esto debe hacerse en orden, si alguien trata de pagar antes de pedir o se lanza a comer sin haber hecho la fila, el champion simplemente lo ignora. Reglas son reglas.
