#!/usr/bin/python3
import threading
import time
import random

num_hilos = 5
cuenta = 0
mutex = threading.Semaphore(1)
barrera = threading.Semaphore(0)

def vamos(yo):
    global cuenta
    print(f'hilo {yo} iniciando')
    time.sleep(3*random.random())

    mutex.acquire()
    cuenta += 1
    print(f'Hay {cuenta} hilos esperando')

    if cuenta == num_hilos:
        print('¡Abran la barrera!')
        barrera.release()
    mutex.release()

    barrera.acquire()
    barrera.release()

    print(f'{yo} pasa corriendo')

for i in range(20):
    threading.Thread(target=vamos, args=[i]).start()
