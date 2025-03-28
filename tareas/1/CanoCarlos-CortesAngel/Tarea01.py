#CanoCarlos
#CortesAngel

#Tarea 1

import threading
import random
import time

# Constantes
MAX_PISOS = 5  # Número total de pisos
CAPACIDAD_ELEVADOR = 5  # Máximo de personas en el elevador
NUM_USUARIOS = 20  # Número total de usuarios


piso_actual = 0  # Piso en el que está el elevador
pasajeros = 0  # Número de personas dentro del elevador
mutex = threading.Semaphore(1)  # Semáforo para evitar condiciones de carrera
esperando = [0] * MAX_PISOS  # Usuarios esperando en cada piso
usuarios_listos = []  # Usuarios que han terminado su viaje

# Usuario
def usuario(id_usuario, piso_origen, piso_destino):
    global piso_actual, pasajeros

    print(f":) Usuario {id_usuario} espera en piso {piso_origen} para ir a piso {piso_destino}")

    # Sección crítica: el usuario registra su espera en el piso correspondiente
    mutex.acquire()
    esperando[piso_origen] += 1  # Aumenta el contador de usuarios esperando
    mutex.release()

    # Esperar a que el elevador llegue al piso de origen
    while True:
        mutex.acquire()
        if piso_actual == piso_origen and pasajeros < CAPACIDAD_ELEVADOR:
            pasajeros += 1  # Usuario aborda el elevador
            esperando[piso_origen] -= 1  # Reduce el contador de espera en el piso
            print(f"⬆ Usuario {id_usuario} subió en piso {piso_origen} (Ocupación: {pasajeros}/{CAPACIDAD_ELEVADOR})")
            mutex.release()
            break 
        mutex.release()
        time.sleep(1) 

    # Esperar a que el elevador llegue al piso de destino
    while piso_actual != piso_destino:
        time.sleep(1)

    # Sección crítica: usuario se baja del elevador
    mutex.acquire()
    pasajeros -= 1  # Reduce el número de pasajeros dentro del elevador
    print(f"⬇ Usuario {id_usuario} bajó en piso {piso_destino} (Ocupación: {pasajeros}/{CAPACIDAD_ELEVADOR})")
    usuarios_listos.append(id_usuario)  # Marca al usuario como "viaje completado"
    mutex.release()

# Elevador
def elevador():
    global piso_actual, pasajeros

    while len(usuarios_listos) < NUM_USUARIOS:  # Mientras haya usuarios pendientes el elevador seguirá funcionando
        # Recorrido hacia arriba
        for i in range(MAX_PISOS):
            mutex.acquire()
            piso_actual = i  
            print(f"🔼 Elevador en piso {piso_actual} (Ocupación: {pasajeros}/{CAPACIDAD_ELEVADOR})")

            # Si hay usuarios esperando y hay espacio en el elevador, los deja subir
            if esperando[piso_actual] > 0 and pasajeros < CAPACIDAD_ELEVADOR:
                print(f"<<:) Permitimos que usuarios suban en piso {piso_actual}")
            mutex.release()
            time.sleep(2)  

        # Recorrido hacia abajo
        for i in range(MAX_PISOS - 1, -1, -1):
            mutex.acquire()
            piso_actual = i  
            print(f"🔽 Elevador en piso {piso_actual} (Ocupación: {pasajeros}/{CAPACIDAD_ELEVADOR})")

            # Si hay usuarios esperando y hay espacio, permite que suban
            if esperando[piso_actual] > 0 and pasajeros < CAPACIDAD_ELEVADOR:
                print(f"<<:) Permitimos que usuarios suban en piso {piso_actual}")
            mutex.release()
            time.sleep(2)

# Creamos los hilos de los usuarios sus piso origen y piso destino y los ingresamos a la lista de usuarios
usuarios = []
for i in range(NUM_USUARIOS):
    piso_origen = random.randint(0, MAX_PISOS - 1)  
    piso_destino = random.randint(0, MAX_PISOS - 1)  
    while piso_destino == piso_origen:  
        piso_destino = random.randint(0, MAX_PISOS - 1)

    hilo_usuario = threading.Thread(target=usuario, args=(i, piso_origen, piso_destino))
    usuarios.append(hilo_usuario)

hilo_elevador = threading.Thread(target=elevador)

hilo_elevador.start()
for i in usuarios:
    i.start()

# Esperar a que todos los usuarios terminen su viaje
for i in usuarios:
    i.join()

# Esperar a que el elevador termine después de atender a todos
hilo_elevador.join()
