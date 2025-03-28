# Tarea 1 - Ejercicios de Sincronizacion 

**Problema - Interseccion de caminos**

**Autores:** 
- Cervantes Mateos Leonardo Mikel
- Sole Pi Arnau Roger Sole Pi

# Lenguaje y entorno
Desarrollado en el lenguaje de programacion Python 3.12.3 y probado en Ubuntu 24.04.02.
\
No es necesario instalacion de paquetes externos para ejecutar los archivos. Solo es necesario tener Python instalado.

# Refinamientos

Se implementaron ambos refinamientos.

# Resolucion 

Para resolver este problema se utilizaron 4 mutex para cada una de las cuadriculas de la interseccion y un semaforo para mantener el numero de coches dentro de la interseccion completa menor a 4. 
\
Cada uno de los 4 mutex evita que mas de un coche entre a una misma cuadricula de la interseccion de manera simultanea. A su vez, el semaforo permite que haya de 0 a 3 coches al mismo tiempo en la interseccion. 
No se permite que haya 4 coches en la interseccion debido a que esto nos puede llevar a un bloqueo mutuo en donde todos los coches esperan que el siguiente avance pero como estos forman un ciclo nunca avanzan.

Cada uno de los coches empieza en una direccion especifica (o como tal una cuadricula) y un destino determinado. Este destino puede ser cualquiera de los 3 casos presentados en el refinamiento numero 2.
- Un auto podría girar a la derecha (y emplear sólo un cuadrante)
- Podría seguir de frente (y emplear dos cuadrantes)
- Podría girar a la izquierda (y emplear tres cuadrantes).

Los coches se crean al inicio de la ejecucion del programa de manera aleatoria, se les asigna direccion inicial y destino final de acuerdo a las reglas establecidas. De igual manera, se les asigna un numero entero a cada uno para poder identificarlos.

La cuadricula de la interseccion es representada como una lista de 4 elementos en donde cada indice representa uno de los cuadrantes de la siguiente manera:

0 -> 0, 
1 -> 1, 
2 -> 3, 
3 -> 2 

o, ya como tal en la cuadricula:

<p style="text-align:center;">0   |  1</p>
<p style="text-align:center;">3   |   2</p>

De esta manera, al sumar 1 modulo 4, se obtiene el nuevo cuadrante al que quiere ir el coche. Si se suma 2 modulo 4 se obtiene el cuadrante despues de 2 giros(hacia la izquierda). Esto facilita la implementacion de los giros.


# Notas
Se entregan dos archivos distintos 'intersecciones.py' e 'intersecciones_graficamente.py'. Ambos resuleven el problema pero la version grafica utiliza un mutex adicional para la impresion de la interseccion despues de que cada coche se mueva. Esto se hace para que no se modifique que coche esta en cada cuadrante antes de que se complete la impresion.
La version 'intersecciones.py' muestra el funcionamiento solamente en la terminal.
