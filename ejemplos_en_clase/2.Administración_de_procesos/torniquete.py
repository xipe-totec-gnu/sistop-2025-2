#!/usr/bin/python3
import threading, random, time

t = threading.Semaphore(0)

def reporta(num, msg):
    print(f'{" " *num}{num}: {msg}')

def auto_que_cruza(yo):
    reporta(yo, 'aparece')
    t.acquire()
    t.release()
    reporta(yo,'ya cruzó')

def control_semaforo():
    while True:
        time.sleep(1)
        print('Abriendo el torniquete')
        t.release()
        time.sleep(1)
        print('Cerrando el torniquete')
        t.acquire()

threading.Thread(target=control_semaforo).start()

for i in range(100):
    time.sleep(0.33)
    threading.Thread(target=auto_que_cruza, args=[i]).start()

