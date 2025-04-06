import threading
import time
import random
from queue import Queue

NUM_MAQUINAS = 2
NUM_USUARIOS = 10

maquinas = [threading.Semaphore(1) for _ in range(NUM_MAQUINAS)]
fila = Queue()
lock_fila = threading.Lock()


estado_maquinas = ["Libre" for _ in range(NUM_MAQUINAS)]

def log_usuario(id_usuario, mensaje):
    """Log para el usuario con colores"""
    print(f"\033[94m[Usuario {id_usuario}] \033[0m{mensaje}")

def log_maquina(maquina, id_usuario, mensaje):
    """Log para las máquinas con colores"""
    print(f"\033[92m[Maquina {maquina+1}] \033[0m{mensaje} \033[93m(Usuario {id_usuario})\033[0m")

def log_error(maquina, id_usuario, mensaje):
    """Log para errores con colores"""
    print(f"\033[91m[Maquina {maquina+1}] \033[0m{mensaje} \033[93m(Usuario {id_usuario})\033[0m")


def usar_maquina(id_usuario):
    global estado_maquinas

    atendido = False
    while not atendido:
        for i in range(NUM_MAQUINAS):
            if maquinas[i].acquire(blocking=False): 
                with lock_fila:
                    if not fila.empty() and fila.queue[0] == id_usuario:
                        fila.get() 

                estado_maquinas[i] = f"Usando por Usuario {id_usuario}"
                log_maquina(i, id_usuario, "🔄 Usuario está recargando...")

                tiempo_recarga = random.uniform(1.5, 3.5)
                time.sleep(tiempo_recarga)

                if random.random() < 0.15: 
                    log_error(i, id_usuario, "❌ La máquina no aceptó la tarjeta. Volviendo a la fila...")
                    estado_maquinas[i] = "Libre"
                    maquinas[i].release()
                    time.sleep(1)

                    with lock_fila:
                        fila.put(id_usuario)  
                else:
                    log_maquina(i, id_usuario, f"✅ Recargó con éxito en {tiempo_recarga:.2f}s")
                    estado_maquinas[i] = "Libre"
                    maquinas[i].release()
                    atendido = True
                    break
            else:
                continue
        time.sleep(0.5)  
        
def usuario(id_usuario):
    with lock_fila:
        fila.put(id_usuario)
        log_usuario(id_usuario, f"Usuario {id_usuario} se formó en la fila.")  # Especifica el usuario

    usar_maquina(id_usuario)

hilos = []
for i in range(1, NUM_USUARIOS + 1): 
    hilo = threading.Thread(target=usuario, args=(i,))
    hilos.append(hilo)
    hilo.start()
    time.sleep(1)  

for h in hilos:
    h.join()

print("\n🎉 Todos los usuarios han recargado su tarjeta.")