#!/usr/bin/python3

''' Suma todos los enteros entre MENOR y MAYOR, dividiéndolo en NUM procesos

OJO: Hace cosas MUY horribles que ustedes ya comprenderán pronto. NO LO USEN
en código real.'''

import os
import time

MENOR = 0
MAYOR = 100
NUM = 4

procesos = []

def realiza_suma(minimo, maximo):
    print(f'{os.getpid()}: Sumando de {minimo} a {maximo}')
    acum = 0
    i = minimo
    while i < maximo:
        acum += i
        i += 1
    print(f'{os.getpid()}: Entregando {acum}')
    return acum

def entrega_resultados():
    total = 0
    print('--------')
    print('¡TOTAL!')
    for pid in procesos:
        f = open(f'/tmp/{pid}', 'r')
        valor = float(f.read())
        total += valor
    print(total)

print(f'Sumando de {MENOR} a {MAYOR} en {NUM} procesos')
total = 0
for i in range(NUM):
    porcion = (MAYOR - MENOR) / NUM
    mi_menor = MENOR + (i * porcion)
    mi_mayor = (MENOR + (i * (porcion)) + porcion) - 1
    pid = os.fork()
    if pid == 0:
        print(f'{i}. Iniciando la suma de {porcion} elementos, de {mi_menor} a {mi_mayor}')
        total += realiza_suma(mi_menor, mi_mayor)
        print(f'{i}. Total ahora vale: {total}')
        f = open(f'/tmp/{os.getpid()}', 'w') #### ESTO ES MALO Y FEO, no lo hagan en casa
        f.write(f'{total}')
        f.close()
        exit()
    elif pid > 0:
        print(f'{i}. Agregando el proceso {pid} a la lista...')
        procesos.append(pid)
        # falta un par de detalles... esperen
        
    else:
        raise(RuntimeError, 'CHIN!')

time.sleep(0.1)
entrega_resultados()
