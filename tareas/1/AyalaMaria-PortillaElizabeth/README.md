# 🔍 PROBLEMA: EL SERVIDOR WEB

Simula un sistema en el que un jefe recibe solicitudes de trabajo, este asignara dichas solicitudes a k trabajadores asignados, y estos trabajadores las procesan. El jefe elige a cualquier trabajador disponible. Cada hilo (trabajador)  debe notificar cuando termine su actividad solicitada. 

## 🛠 Lenguaje y Entorno

__Lenguaje__: Python 3 <br>
__Entorno__: Ejecutado en terminal con librerías estándar de Python
__Librerías utilizadas__:
- `Threading` : Para manejar hilos (trabajadores y jefe).
- `Queue`: Para gestionar la cola de solicitudes.
- ` Time y random`: Para simular tiempos de procesamiento y llegada de solicitudes. <br>

Decidimos emplear el lenguaje de programación Python, esto ya que consideramos que su sintaxis clara facilita la implementación y comprensión del código, además que sus bibliotecas incorporadas permiten gestionar concurrencia sin necesidad de dependencias externas.


## 🚀 ¿Cómo Ejecutar el Programa?
__Requisitos Previos__
* Tener instalado Python 3

* Asegurarse de que las librerías utilizadas estén disponibles (todas son estándar en Python)

__Pasos para Ejecutarlo__

1. Ejecutar el programa
2. Ingresar el número de trabajadores cuando se solicite.
3. Observar cómo las solicitudes son procesadas por los trabajadores y al final se muestras las solicitudes finales realizadas.

## ⚙️ Funcionamiento del programa:
1. El usuario ingresa el número de trabajadores disponibles.
2. Se crean hilos de trabajadores que esperan solicitudes.
3. Un hilo jefe genera solicitudes y las asigna a los trabajadores.
4. Los trabajadores procesan cada solicitud e indican cuando se termine de realizar.
5. Después de un tiempo, las solicitudes finalizan y se muestra un resumen del trabajo realizado.

## 🔄 Estrategia de Sincronización

Para manejar correctamente la concurrencia en el programa, se usaron los siguientes mecanismos:

- _Semáforo `(threading.Semaphore)`_: Se usa `hay_trabajo` para indicar a los trabajadores que hay solicitudes en la cola.
- _Cola `(queue.Queue)`_: Se emplea una cola para almacenar solicitudes y distribuirlas entre los trabajadores.
- _Mutex `(threading.Lock)`_: Se usa `mutex_registro` para garantizar que la contabilidad de solicitudes atendidas sea accesible solo por un trabajador a la vez, evitando condiciones de carrera.
- Se asegura que el jefe no agregue solicitudes después de finalizar la simulación mediante `hilo_jefe.join()`, evitando condiciones inesperadas.
- Se garantiza que los trabajadores no queden bloqueados al liberarles con `hay_trabajo.release()` tras el cierre del sistema.

## 💡Posibles Mejoras

- Implementar una priorización de solicitudes, para que ciertas tareas sean atendidas antes que otras.
