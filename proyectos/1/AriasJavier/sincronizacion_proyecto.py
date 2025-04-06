import random
import threading
import time

trabajos_totales = 3
miembros_totales = 2

trabajos = []
tareas_pendientes = []
tareas_completadas = []

mutex_tareas_pendientes= threading.Semaphore(1)
mutex_tareas_completadas= threading.Semaphore(1)

semaf_planificador = threading.Semaphore(0)
semaf_tareas = threading.Semaphore(0)

def crearTrabajo(id):

    trabajo = {"id": id, "tareas": []}

    trabajo['tareas'].append(crearTarea(id, 0, []))
    trabajo['tareas'].append(crearTarea(id, 1, [0]))
    trabajo['tareas'].append(crearTarea(id, 2, [0]))
    trabajo['tareas'].append(crearTarea(id, 3, [1,2]))

    trabajos.append(trabajo)


def crearTarea(id_trabajo, id, requerimientos):
    tarea = {
        "id_trabajo": id_trabajo,
        "id": id,
        "estado": "no empezada",
        "requerimientos": requerimientos,
        "duracion": random.randint(2,5)
    }

    return tarea;

def planificador():

    trabajos_actualizados = {i for i in range(trabajos_totales)}

    while True:
        for trabajo in trabajos:
            if not trabajo['id'] in trabajos_actualizados:
                continue
            for tarea in trabajo['tareas']:
                if tarea['estado'] == "no empezada" and comprobarTarea(trabajo['tareas'], tarea):

                    mutex_tareas_pendientes.acquire()
                    tareas_pendientes.append(tarea)
                    tarea['estado'] = "pendiente"
                    print(f"La tarea {tarea['id']} del trabajo {tarea['id_trabajo']} puede empezar a realizarse.")
                    mutex_tareas_pendientes.release()

                    semaf_tareas.release()

        trabajos_actualizados.clear()

        semaf_planificador.acquire()

        mutex_tareas_completadas.acquire()
        while tareas_completadas:
            tarea = tareas_completadas.pop(0)
            trabajos_actualizados.add(tarea['id_trabajo'])
        mutex_tareas_completadas.release()

def miembro(id):
    while True:
        semaf_tareas.acquire()

        mutex_tareas_pendientes.acquire()
        tarea = tareas_pendientes.pop(0)
        mutex_tareas_pendientes.release()

        print(f"+ El miembro {id} ha empezado la tarea {tarea['id']} del trabajo {tarea['id_trabajo']}.")

        #Realizando la tarea
        time.sleep(tarea['duracion'])
        tarea['estado'] = "completado"

        mutex_tareas_completadas.acquire()
        tareas_completadas.append(tarea)
        mutex_tareas_completadas.release()

        print(f"- El miembro {id} ha realizado la tarea {tarea['id']} del trabajo {tarea['id_trabajo']}.")

        semaf_planificador.release()

#Comprobar que se hayan completado todos los requerimientos previos para empezar la tarea
def comprobarTarea(tareas, tarea):
    for requerimiento in tarea['requerimientos']:
        if tareas[requerimiento]['estado'] != "completado":
            return False
    return True


for i in range(trabajos_totales):
    crearTrabajo(i)

for i in range(miembros_totales):
    threading.Thread(target = miembro, args=[i]).start()

threading.Thread(target = planificador, args=[]).start()
