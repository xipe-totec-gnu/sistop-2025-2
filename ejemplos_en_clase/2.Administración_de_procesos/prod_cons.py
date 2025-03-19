#!/usr/bin/python3
import threading
import time
import random

max_obj = 5
buffer = []
max_buf = threading.Semaphore(max_obj)
mut_buffer = threading.Semaphore(1)
obj_listo = threading.Semaphore(0)

def productor(yo):
    while True:
        evento = random.random()
        print(f'P{yo}: {len(buffer)} objetos. Produce {evento}')
        time.sleep(1)
        max_buf.acquire()
        with mut_buffer:
            buffer.append(evento)
        obj_listo.release()

def consumidor(yo):
    while True:
        obj_listo.acquire()
        with mut_buffer:
            evento = buffer.pop()
        max_buf.release()
        print(f'C{yo}: Recibe {evento}')
        time.sleep(1)

for i in range(3):
    threading.Thread(target=productor, args=[i]).start()

for i in range(2):
    threading.Thread(target=consumidor, args=[i]).start()
