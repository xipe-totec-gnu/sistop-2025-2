import threading
import time
import random

TOTAL_ASIENTOS = 4       # Capacidad máxima del cubículo
TOTAL_ALUMNOS = 7        # Total de alumnos que intentarán asesorarse
MAX_DUDAS = 3            # Máximo de dudas que un alumno puede tener

# Sincronización 
asientos_libres = threading.Semaphore(TOTAL_ASIENTOS)    # Controla la entrada al cubículo / los que entran a cubículo son los que preguntan a profesor
turno_para_preguntar = threading.Lock()                  # Solo un alumno puede preguntar a la vez
barrera_de_inicio = threading.Barrier(TOTAL_ALUMNOS)     # Todos los alumnos esperan para comenzar juntos

# Mis contadores para alumnos que entran o no a la asesoría, los inicializo en 0
alumnos_que_entraron = 0
alumnos_que_no_lograron_entrar = 0

# Lock para proteger las estadísticas 
lock_estadisticas = threading.Lock()

#  Clase Profesor 
class Profesor(threading.Thread):
    def run(self):
        print("\n[Profesor] El profesor está listo en su cubículo.\n")
        while True:
            if asientos_libres._value == TOTAL_ASIENTOS:
                print("[Profesor] No hay alumnos, aprovecha para descansar. 🥱\n")
                time.sleep(2)
            else:
                # Simplemente espera y está disponible
                time.sleep(1)

# Clase Alumno 
class Alumno(threading.Thread):
    def __init__(self, numero):
        threading.Thread.__init__(self)
        self.id = numero

    def run(self):
        global alumnos_que_entraron, alumnos_que_no_lograron_entrar

        print(f"Alumno {self.id} llegó al cubículo y espera al resto.")
        barrera_de_inicio.wait()   # Todos inician al mismo tiempo

        # Verificamos si hay asientos disponibles
        if asientos_libres.acquire(blocking=False):
            with lock_estadisticas:
                alumnos_que_entraron += 1

            print(f"Alumno {self.id} entra al cubículo y ocupa una silla.")

            dudas = random.randint(1, MAX_DUDAS)

            for num_duda in range(1, dudas + 1):
                with turno_para_preguntar:
                    print(f"Alumno {self.id} hace su pregunta {num_duda}/{dudas} al profesor. ❓")
                    time.sleep(random.uniform(1, 2))  # Tiempo de respuesta del profesor (el profesor no es una maquina)
                    print(f"Alumno {self.id} recibe respuesta a su pregunta {num_duda}.\n")
                time.sleep(random.uniform(0.5, 1))

            print(f"Alumno {self.id} ha terminado y deja su asiento. 🙏🏻\n")
            asientos_libres.release()
        
        else:
            # En caso de que no haya asiento disponible
            with lock_estadisticas:
                alumnos_que_no_lograron_entrar += 1
            print(f"Alumno {self.id} no encontró asiento y decidió volver después.\n")

# Inicio del programa
profesor = Profesor()
profesor.daemon = True  # El profesor se detiene cuando acabe la simulación
profesor.start()

# Creo e inicio alumnos
lista_de_alumnos = []
for i in range(1, TOTAL_ALUMNOS + 1):
    alumno = Alumno(i)
    lista_de_alumnos.append(alumno)
    alumno.start()

# Esperamos a que todos terminen 
for alumno in lista_de_alumnos:
    alumno.join()

# Reporte final 
print("_____________________________________")
print("   >> RESUMEN DE LA SESIÓN <<")
print(f"   Alumnos que lograron asesorarse: {alumnos_que_entraron}")
print(f"   Alumnos que no pudieron entrar: {alumnos_que_no_lograron_entrar}")
print("____________________________________")
print(">>> Fin de las asesoría <<<")
