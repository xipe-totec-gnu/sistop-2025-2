#!/usr/bin/python3
import threading
import time
import random

num_hilos = 5
barrera = threading.Barrier(num_hilos)

def vamos(yo):
    print(f'hilo {yo} iniciando')
    time.sleep(3*random.random())
    barrera.wait()
    print(f'{yo}: Pasamos la barrera!')

for i in range(20):
    threading.Thread(target=vamos, args=[i]).start()
