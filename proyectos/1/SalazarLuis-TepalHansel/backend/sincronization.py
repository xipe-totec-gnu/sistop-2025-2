import threading
import time

numWorkers=3
mutexTrabajador=threading.Semaphore(0)

def workers(id):
    while True:
        mutexTrabajador.acquire()
        print("Soy el trabajador f{id} y no tengo nada que hacer")
        
def alumnos(id):
    print("Don Rata atiendame")


#Se crean los trabajadores
def donRata():
    for i in range(numWorkers):
        threading.Thread(target=workers, args=[i]).start()
    cont = 0
    while(True):
        cont +=1
        threading.Thread(target=alumnos, args=[cont]).start()
        



