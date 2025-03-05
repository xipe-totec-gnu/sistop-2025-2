#!/usr/bin/python3

''' Suma todos los enteros entre MENOR y MAYOR, dividiéndolo en NUM hilos.

OJO: Hace cosas MUY horribles que ustedes ya comprenderán pronto. NO LO USEN
en código real.
'''

import threading
import time

MENOR = 0
MAYOR = 100
NUM = 4
total = 0

def realiza_suma(hilo, minimo, maximo):
    global total
    print(f'{hilo}: Sumando de {minimo} a {maximo}')
    acum = 0
    i = minimo
    while i < maximo:
        acum += i
        i += 1
    print(f'{hilo}: Entregando {acum}')
    total += acum  #### HORROR HORROR HORROR Nunca hagan esto!!!!!!

def entrega_resultados():
    global total
    print('--------')
    print('¡TOTAL!')
    print(total)

print(f'Sumando de {MENOR} a {MAYOR} en {NUM} hilos')
for i in range(NUM):
    porcion = (MAYOR - MENOR) / NUM
    mi_menor = MENOR + (i * porcion)
    mi_mayor = (MENOR + (i * (porcion)) + porcion) - 1
    threading.Thread(target = realiza_suma, args = [i, mi_menor, mi_mayor]).start()

time.sleep(0.1)
entrega_resultados()
