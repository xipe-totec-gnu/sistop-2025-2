#!/usr/bin/python3
import threading
import time
import random
num = 3
mult = threading.Semaphore(num)

def mis_espacios(yo):
    return(' ' * yo)

def reporta_para(yo,msg):
    print(f'{mis_espacios(yo)}{yo}: {msg}')

def funcion(yo):
    print(f'{yo} quiere sentarse a la mesa')
    time.sleep(random.random())
    mult.acquire()
    reporta_para(yo, 'Se sienta a la mesa.')
    for i in range(random.randint(1,8)):
        reporta_para(yo, f'pide el platillo {i}')
        time.sleep(0.1)
    mult.release()
    reporta_para(yo, '¡Qué rico! ¡hasta la otra!')

print(f'¡Bienvenido al restaurante! Tenemos {num} mesas.')
for i in range(10):
    threading.Thread(target=funcion,args=[i]).start()
