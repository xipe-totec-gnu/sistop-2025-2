# PROBLEMA EL SERVIDOR WEB
#Ayala Hernandez Maria Fenanda/ Portilla Hermenegildo Elizabeth

import threading
import queue
import time
import random

# Pedir al usuario el número de trabajadores
k_trabajadores = int(input("Ingrese el número de trabajadores disponibles: "))

# Cola de solicitudes recibidad por el jefe
cola_solicitudes = queue.Queue()

# Semáforo para indicar que hay trabajo disponible
hay_trabajo = threading.Semaphore(0)

# Mutex para registro
mutex_registro = threading.Lock() 
registro = []  # Lista para almacenar el registro de solicitudes atendidas

# Bandera para indicar el fin de las solicitudes
solicitudes_activas = True

# Conjunto para rastrear solicitudes ya atendidas
solicitudes_atendidas = set()

def trabajador(id):
    while solicitudes_activas or not cola_solicitudes.empty():
        print(f"\U0001F4A4 Trabajador {id} se duerme, está esperando trabajo.")  
        hay_trabajo.acquire()  # Espera hasta que haya una solicitud disponible
        
        if not solicitudes_activas and cola_solicitudes.empty():
            break  # Si la cola está vacía, sale del bucle

        try:
            solicitud = cola_solicitudes.get(timeout=3)  # Obtiene una solicitud
        except queue.Empty:
            continue  # Si no hay solicitudes, sigue esperando

        print(f"\U0001F6E0 Trabajador {id} atendiendo solicitud: {solicitud}")

        # Simula el procesamiento de la solicitud (tiempo aleatorio entre 1 y 3 sg)
        tiempo_trabajo = random.uniform(1, 3)
        time.sleep(tiempo_trabajo)

        # Registro de actividades atendidas
        with mutex_registro: #Mutex para evitar que dos trabajadores accedan al mismo tiempo
            registro.append((id, solicitud, tiempo_trabajo))
        
        print(f"✅ Trabajador {id} terminó de atender: {solicitud}")

        cola_solicitudes.task_done()  # Marca la tarea como terminada

    print(f"\U0001F4A4 Trabajador {id} se duerme definitivamente, ya no hay más trabajo.")

def jefe():
    solicitudes = ["Página 1", "Página 2", "Página 3", "Archivo A", "Archivo B", "Archivo C", "Video", "API /datos"] #Solicitudes posibles
    while solicitudes_activas:
        time.sleep(random.uniform(0.5, 2))  # Simula llegada de una nueva solicitud
        
        if not solicitudes_activas:  # Verifica antes de agregar nueva solicitud
            break

        solicitud = random.choice(solicitudes)
        
        # Verificar si la solicitud ya fue atendida
        if solicitud in solicitudes_atendidas:
            continue  # Si ya fue atendida, pasa a la siguiente iteración

        print(f"\U0001F4E9 Jefe recibió una nueva solicitud: {solicitud}")

        cola_solicitudes.put(solicitud)  # Agrega la solicitud a la cola
        hay_trabajo.release()  # Despierta a un trabajador

        # Registrar la solicitud como atendida
        solicitudes_atendidas.add(solicitud)

# Crear hilos de trabajadores
hilos = []
for i in range(k_trabajadores):
    hilo = threading.Thread(target=trabajador, args=(i,)) 
    hilos.append(hilo) # Agrega hilo a la lista
    hilo.start() 

# Iniciar al jefe
hilo_jefe = threading.Thread(target=jefe)
hilo_jefe.start()

# Simulación por un tiempo de 10 sg
time.sleep(10) 

# Finalizar la simulación
solicitudes_activas = False
print("\n🚨 El jefe ha dejado de recibir solicitudes. Cerrando sistema.")

# Esperar a que el jefe termine
hilo_jefe.join() 

# Liberar trabajadores en espera
for _ in range(k_trabajadores):
    hay_trabajo.release()

# Esperar a que los trabajadores terminen de atender las solicitudes
for h in hilos:
    h.join()

# Mostrar las actividades realizadas al final incluyendo el tiempo de ejecucion (random) de actividad y el trabajador que la realizo 
with mutex_registro:
    print("\n📊 Contabilidad de Solicitudes:")
    for log in registro:
        print(f"Trabajador {log[0]} atendió '{log[1]}' en {log[2]:.2f} seg.") 

print("\n✅ Todos los trabajadores han finalizado y ahora están libres. 💤")
