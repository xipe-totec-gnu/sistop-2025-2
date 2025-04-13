# Proyecto 1: Una situación cotidiana con concurrencia y sincronización.

## Planteamiento del problema
### Concurso de Programación Competitiva (ICPC)

El ICPC es un concurso de programación competitiva que se lleva a cabo anualmente en todo el mundo. En este concurso, los participantes se reunen en equipos de 3 y deben resolver una serie de problemas de programación en un tiempo limitado. Cada problema tiene un puntaje asociado y los participantes deben enviar sus soluciones a través de un sistema de envío.
El sistema de envío es un componente crítico del concurso, ya que permite a los participantes enviar sus soluciones y recibir retroalimentación sobre su desempeño. Todos los participantes deben enviar sus soluciones a través del mismo sistema, lo que puede generar una gran cantidad de tráfico y competencia por los recursos del sistema.

Ademas del sistema de envío y retroalimentación, el ICPC también cuenta con la opción de que los participantes puedan imprimir documentos durante el concurso. Esto puede incluir la impresión de soluciones, notas o cualquier otro documento que los participantes necesiten durante el concurso, esto es importante ya que los participantes pueden necesitar imprimir documentos pues solo hay una computadora por equipo.

El tercer componente del ICPC es el sistema aclaraciones. Este sistema permite a los participantes enviar preguntas sobre los problemas y recibir respuestas de los jueces. Esto es importante porque los participantes pueden tener dudas sobre el enunciado de los problemas, dichas dudas pueden deberse a alguna oracion que pueda interpretarse de alguna manera o a algun problema en la traducción, ya que aunque la mayoria de las etapas de esta competencia se llevan a cabo en ingles, en la etapa local tambien se dan los problemas en español.

En este proyecto modelaremos el sistema de envío, impresión de documentos y aclaraciones del ICPC. Para ello, utilizaremos mecanismos de sincronización que permitan:
- Controlar el acceso al sistema de envío y retroalimentación y evitar que se intente evaluar una cantidad de soluciones mayor al numero de validadores disponibles.
- Controlar el acceso a la impresora y permitir que las personas que reparten las impresiones las repartan hasta que se haya juntado un número mínimo de impresiones (para evitar exceso de cansancio).
- Controlar el acceso al sistema de aclaraciones y permitir que los participantes envien sus preguntas y reciban respuestas de los jueces, con los jueces respondiendo una pregunta a la vez.

## Descripción de la solución

Para resolver el problema, utilizaremos los siguientes mecanismos de sincronización:
- 