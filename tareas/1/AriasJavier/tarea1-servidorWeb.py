import threading
import random
import time

metodos = ['GET', 'POST']

urls = [
    '/',
    '/home',
    '/about',
    '/contact',
    '/blog'
]

trabajadores = 3
usuarios = 5
trabajadores_disponibles = trabajadores

semaf_trabajadores = threading.Semaphore(0)
semaf_lider = threading.Semaphore(0)

mutex_nuevas = threading.Semaphore(1)
mutex_pendientes = threading.Semaphore(1)
mutex_trabajadores = threading.Semaphore(1)

q_solicitudes_nuevas = []
q_solicitudes_pendientes = []

def nuevaSolicitud(usuario):
    metodo = random.choice(metodos)
    url = random.choice(urls)
    duracion = random.random()

    solicitud = {
        'metodo': metodo,
        'url': url,
        'duracion': duracion,
        'usuario': usuario
    }

    #Mandar las solicitud al servidor
    mutex_nuevas.acquire()
    q_solicitudes_nuevas.append(solicitud)
    mutex_nuevas.release()

    #Notificar al servidor que ha recibido una nueva solicitud
    semaf_lider.release()

def trabajador(id):
    global trabajadores_disponibles

    while True:
        #Esperar que una solicitud este lista para ser procesada
        semaf_trabajadores.acquire()

        #Obtener la solicitud
        mutex_pendientes.acquire()
        solicitud = q_solicitudes_pendientes.pop(0)
        mutex_pendientes.release()

        mutex_trabajadores.acquire()
        trabajadores_disponibles -= 1
        mutex_trabajadores.release()

        #Procesar la solicitud
        time.sleep(solicitud['duracion'])
        print(f"El hilo {id} ha procesado la solicitud {solicitud['metodo']} {solicitud['url']}. Usuario {solicitud['usuario']}.")

        mutex_trabajadores.acquire()
        trabajadores_disponibles += 1
        mutex_trabajadores.release()

def lider():
    for i in range(trabajadores):
        threading.Thread(target=trabajador, args=[i]).start()

    while True:

        #Esperar a que llegue una nueva solicitud por parte de un usuario.
        semaf_lider.acquire()

        #Obtener la nueva solicitud
        mutex_nuevas.acquire()
        solicitud = q_solicitudes_nuevas.pop(0)
        mutex_nuevas.release()

        print(f"Nueva solicitud: {solicitud['metodo']} {solicitud['url']}. Usuario {solicitud['usuario']}.")

        #Poner la solicitud en la cola de solicitudes pendientes
        mutex_pendientes.acquire()
        q_solicitudes_pendientes.append(solicitud)
        print(f"Hay {len(q_solicitudes_pendientes)} solicitudes pendientes.")
        mutex_pendientes.release()

        #Notificar a los trabajadores que hay una nueva solicitud lista para ser procesada
        semaf_trabajadores.release()

        mutex_trabajadores.acquire()
        print(f"Hay {trabajadores_disponibles} hilos disponibles.")
        mutex_trabajadores.release()

def usuario(id):
    while True:
        time.sleep(random.random() * 3)

        #Realizar una nueva solicitud
        nuevaSolicitud(id)

threading.Thread(target=lider).start()
for i in range(usuarios):
    threading.Thread(target=usuario, args=[i]).start()
