import threading
import random
import time
from queue import Queue


class Laboratorio:  # Inicializa el laboratorio con el número de mesas
    def __init__(self, num_mesas, sync_type="semaforo"):
        # Utilizamos semaforo, apagador y barrera. Nuestro semafo controla el acceso al laboratorio.El apagador simula un interruptor 
        # que controla la entrada y la barrera sincroniza la apertura del laboratorio con las mesas.
        self.sync_type = sync_type
        self.jefe_presente = threading.Event() if sync_type == "apagador" else threading.Semaphore(1)
        self.barrera_mesas = threading.Barrier(num_mesas) if sync_type == "barrera" else None
        self.num_mesas = num_mesas
        self.mesas_funcionales = random.randint(1, num_mesas)   # mesas_funcionales se calcula aleatoriamente para simular que algunas mesas pueden estar fuera de servicio.
        self.mesas = [threading.Semaphore(3) for _ in range(self.mesas_funcionales)]
        self.entrada_queue = Queue()
        self.max_espera = 6
        self.max_alumnos = self.mesas_funcionales * 3
        self.alumnos_dentro = 0
        self.ocupacion_mesas = [0] * self.mesas_funcionales
        self.lock = threading.Lock()


   
    def abrir_laboratorio(self):  # Simula la apertura del laboratorio por parte del jefe.
        print("Jefe: Abriendo laboratorio...")
        time.sleep(2)
        print(f"Jefe: Hay {self.mesas_funcionales} mesas funcionales de {self.num_mesas}.")
        # "barrera" espera a que todas las mesas estén listas y "apagador" activa el evento para permitir la entrada.
        if self.sync_type == "barrera":
            self.barrera_mesas.wait()
        if self.sync_type == "apagador":
            self.jefe_presente.set()


    def cerrar_laboratorio(self): # Este método simula el cierre temporal del laboratorio.
        print("Jefe: Me voy a comer, nadie entra ni sale.")
        # "apagador", desactiva el evento para bloquear la entrada, "semaforo" adquiere el semáforo para bloquear la entrada.
        if self.sync_type == "apagador":
            self.jefe_presente.clear()
        elif self.sync_type == "semaforo":
            self.jefe_presente.acquire()
        time.sleep(random.randint(3, 6))
        print("Jefe: Volví, pueden entrar.")
        if self.sync_type == "apagador":
            self.jefe_presente.set()
        elif self.sync_type == "semaforo":
            self.jefe_presente.release()
            
    
    def gestionar_acceso(self): # Este método gestiona la cola de espera de los alumnos cuando el jefe no está.
        # Los alumnos en la cola son procesados uno por uno.
        while not self.entrada_queue.empty():
            alumno = self.entrada_queue.get()
            print(f"Jefe: Dejando entrar al {alumno}")
            alumno.start()

    def alumno_llega(self, alumno_id): # Este método simula la llegada de un alumno al laboratorio.
    # los alumnos esperan en una cola si el jefe no está ("apagador")
        with self.lock:
            if self.alumnos_dentro >= self.max_alumnos:
                print(f"Alumno {alumno_id}: No hay espacio disponible, me voy.")
                return
            if self.sync_type == "apagador" and not self.jefe_presente.is_set():
                if self.entrada_queue.qsize() >= self.max_espera:
                    print(f"Alumno {alumno_id}: No puedo esperar más, me voy.")
                    return
                print(f"Alumno {alumno_id}: Esperando al jefe...")
                self.entrada_queue.put(threading.Thread(target=self.asignar_mesa, args=(alumno_id,)))
            elif self.sync_type == "semaforo":
                if self.jefe_presente.acquire(blocking=False):
                    self.asignar_mesa(alumno_id)
                    self.jefe_presente.release()
                else:
                    print(f"Alumno {alumno_id}: No puedo entrar, el jefe no está.")

    
    def asignar_mesa(self, alumno_id): # Este método asigna una mesa a un alumno y simula el tiempo de trabajo.
        mesa_asignada = random.randint(0, self.mesas_funcionales - 1)
        # Actualiza las estadísticas de ocupación de las mesas
        with self.lock:
            self.ocupacion_mesas[mesa_asignada] += 1
            self.alumnos_dentro += 1
        print(f"Alumno {alumno_id} entra y ocupa la mesa {mesa_asignada}.")
        with self.mesas[mesa_asignada]:
            tiempo_trabajo = random.randint(2, 5)
            time.sleep(tiempo_trabajo)
            print(f"Alumno {alumno_id} terminó en mesa {mesa_asignada}.")
            with self.lock:
                self.ocupacion_mesas[mesa_asignada] -= 1
                self.alumnos_dentro -= 1
          
    def resumen_final(self): # Este método imprime un resumen de la ocupación de las mesas.
        print("\nResumen de ocupación de mesas:")
        for i, ocupacion in enumerate(self.ocupacion_mesas):
            print(f"Mesa {i}: {ocupacion} alumnos la usaron en total.")

#Prueba Funcional 
sync_method = "apagador"  
n_mesas = 5  # Se puede modificar para probar con más mesas
lab = Laboratorio(num_mesas=n_mesas, sync_type=sync_method)
jefe = threading.Thread(target=lab.abrir_laboratorio)
jefe.start()
jefe.join()

alumnos = [threading.Thread(target=lab.alumno_llega, args=(i,)) for i in range(20)]
for a in alumnos:
    a.start()
    time.sleep(0.5)

time.sleep(5)
lab.cerrar_laboratorio()

time.sleep(3)
lab.gestionar_acceso()

lab.resumen_final()