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

tiempo_inhabilitado = [0, 0]

reparando = [False, False]  

def log_usuario(id_usuario, mensaje):
    """Log para el usuario con colores"""
    print(f"\033[94m[Usuario {id_usuario}] \033[0m{mensaje}")

def log_maquina(maquina, id_usuario, mensaje):
    """Log para las máquinas con colores"""
    print(f"\033[92m[Maquina {maquina+1}] \033[0m{mensaje} \033[93m(Usuario {id_usuario})\033[0m")

def log_error(maquina, id_usuario, mensaje):
    """Log para errores con colores"""
    print(f"\033[91m[Maquina {maquina+1}] \033[0m{mensaje} \033[93m(Usuario {id_usuario})\033[0m")

def log_tecnico(maquina, mensaje):
    """Log para la llegada del técnico"""
    print(f"\033[93m[Técnico Maquina {maquina+1}] \033[0m{mensaje}")

def usar_maquina(id_usuario):
    global estado_maquinas, tiempo_inhabilitado, reparando

    atendido = False
    maquina_actual = 0  

    while not atendido:
        for i in range(maquina_actual, NUM_MAQUINAS):  
            if time.time() < tiempo_inhabilitado[i]:
                continue  
            if reparando[i]:
                continue  

            if maquinas[i].acquire(blocking=False):  
                with lock_fila:
                    if not fila.empty() and fila.queue[0] == id_usuario:
                        fila.get() 

                estado_maquinas[i] = f"Usando por Usuario {id_usuario}"
                log_maquina(i, id_usuario, "🛠️ Usuario está recargando...")

                tiempo_recarga = random.uniform(1.5, 3.5)
                time.sleep(tiempo_recarga)

                if random.random() < 0.15: 
                    log_error(i, id_usuario, "❌ Error con máquina. Reintentando...")
                    estado_maquinas[i] = "Libre"
                    maquinas[i].release()
                    time.sleep(1)
                    tiempo_inhabilitado[i] = time.time() + 5  
                    reparando[i] = True  

                    log_tecnico(i, "El técnico llegó para reparar la máquina. Esperando 5 segundos...")

                    time.sleep(5)
                    reparando[i] = False  
                    log_tecnico(i, "La máquina ha sido reparada y ahora está habilitada.")

                    if i == 0: 
                        maquina_actual = 1  
                    else: 
                        maquina_actual = 0  

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
        log_usuario(id_usuario, f"Usuario {id_usuario} se formó en la fila.") 
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