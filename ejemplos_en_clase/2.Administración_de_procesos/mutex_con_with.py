#!/usr/bin/python3
import threading
from random import random
from time import sleep

def con_func_critica(yo, mutex):
    print(f'{yo} bienvenido a la vida.')
    # mutex.acquire()
    # print(f'{yo}: Entrando a la función crítica')
    # sleep(random())
    # mutex.release()
    with mutex:
        print(f'{yo}: Entrando a la función crítica')
        sleep(random())
    print(f'{yo}: Terminando la función crítica.')

s = threading.Semaphore(1)
for i in range(10):
    threading.Thread(target=con_func_critica, args=[i, s]).start()
