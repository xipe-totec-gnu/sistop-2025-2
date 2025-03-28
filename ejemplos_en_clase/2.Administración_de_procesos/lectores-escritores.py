#!/usr/bin/python3
import threading
import time
import random

num_lectores = 10
num_escritores = 2
mutex_pizarron = threading.Semaphore(1)
cuantos_lectores = 0
mutex_lectores = threading.Semaphore(1)
torniquete = threading.Semaphore(1)

def escritor(yo):
    vueltas = 0
    while True:
        vueltas += 1
        print(f'E{yo}: Quiero escribir')
        torniquete.acquire()
        mutex_pizarron.acquire()
        print(f'/E{yo}: Escribiendo. Vuelta {vueltas}. Hay {cuantos_lectores} lectores...')
        time.sleep(random.random())
        print(f'\\E{yo}: Suficiente.')
        mutex_pizarron.release()
        torniquete.release()
        time.sleep(random.random())

def lector(yo):
    global cuantos_lectores
    vueltas = 0
    while True:
        vueltas += 1
        print(f'     L{yo}: Quiero leer')
        torniquete.acquire()
        torniquete.release()

        with mutex_lectores:
            cuantos_lectores += 1
            if cuantos_lectores == 1:
                mutex_pizarron.acquire()

        print(f'   /L{yo}: Leyendo (vuelta {vueltas}; somos {cuantos_lectores})...')
        time.sleep(random.random())
        print(f'   \\L{yo}: Suficiente.')

        with mutex_lectores:
            cuantos_lectores -= 1
            if cuantos_lectores == 0:
                mutex_pizarron.release()

        time.sleep(random.random())

for i in range(num_lectores):
    threading.Thread(target=lector, args=[i]).start()

for i in range(num_escritores):
    threading.Thread(target=escritor, args=[i]).start()
