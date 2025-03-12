#!/usr/bin/python3
import threading
import urllib.request
import time

def envia(s):
    print('Vamos a calcular a...')
    a = 0
    while a < 500000:
        a += 1
    s.acquire()
    print(f'Y ahora estoy enviando a a:{a}')

def conecta(s):
    print('Establezcamos una conexión de red...')
    urllib.request.Request('GET https://www.ingenieria.unam.mx/')
    # time.sleep(1)
    print('Señalizamos que la red está lista.')
    s.release()

sem = threading.Semaphore(0)
threading.Thread(target=envia, args=[sem]).start()
threading.Thread(target=conecta, args=[sem]).start()
