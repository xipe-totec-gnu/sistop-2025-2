# Ejercicio de intersección de caminos 😎🐧

Autores: Enrique Calderón & Luis Ugartechea

## Solución 🤨

Para la solución del problema se propusieron varias estructuras a utilizar. En primer lugar un arreglo de mutex para identificar y proteger cada cuadrante de la matriz formada por la intersección. En segundo lugar una estructura que llamamos `fifoMutex`, como su nombre lo indica, es un mutex con comportamiento FIFO.

Contando con ambas estructuras modelamos a los autos de tal forma que aleatoriamente cuenten con un origen y un destino. En cuanto son creados, se "forman" para entrar a la intersección. Esperan a que los cuadrantes que ocuparán estén libres y una vez que lo están, apartan estos con el mutex de la intersección y avanzan. Una vez que llegan a su destino, liberan los cuadrantes que ocuparon y se van.

Para evitar los bloqueos mutuos pensamos en el problema de los filósofos, donde evitamos el bloqueo realizando los acquire en un orden en específico, eso mismo hicimos con los cuadrantes de la intersección. Ordenamos los locks antes de realizar el acquire, por lo que se piden en un orden específico sin importar el origen o destino.

## Implementación 🤙🐤


Para la implementación utilizamos Python junto con algunas librerías (*muere un gato 🐈☠️).

En cuanto a la implementación lógica utilizamos **threading** para simular concurrencia y la intersección misma junto a sus respectivos locks. En cuanto a la interfaz gráfica utilizamos **tkinter** para mostrar la intersección y los autos.

Un pequeño detalle a resaltar, en nuestra implementación se muestran ciertos contactos entre los autos. Esto se debe a que la distancia entre autos puede ser mínima, siendo imposible visualizarla, sin embargo, no hay colisiones.

_Esperamos le guste :)_


