#!/usr/bin/python3
import threading

num_filosofos = 5
palillos = [threading.Semaphore(1) for i in range(num_filosofos)]

def filosofo(yo):
    while True:
        piensa(yo)
        # ¡Hace hambre!
        come(yo)

def piensa(yo):
    print(f'{" " * yo}{yo} tengo asuntos muuuuy importantes por pensar')
    print(f'{" " * yo}{yo} como que ya hace hambre...')

def come(yo):
    # Para evitar los bloqueos mutuos, los filósofos diestros toman primero el
    # palillo derecho, y los zurdos toman primero el derecho: ya no se pueden
    # formar ciclos de todos esperando al de junto.
    if yo % 2 == 0:
        print(f'{" " * yo}{yo}: Diestro. Tomo palillo derecho')
        palillos[yo].acquire()
        print(f'{" " * yo}{yo}: Diestro. Tomo palillo izquierdo')
        palillos[(yo + 1) % num_filosofos].acquire()
    else:
        print(f'{" " * yo}{yo}: Zurdo. Tomo palillo izquierdo')
        palillos[(yo + 1) % num_filosofos].acquire()
        print(f'{" " * yo}{yo}: Zurdo. Tomo palillo derecho')
        palillos[yo].acquire()

    print(f'{" " * yo}{yo}: ¡Rico! Arroz amargo')

    # Ya terminamos de comer, dejamos ambos palillos. No reportamos, porque esta
    # operación no puede llevar a bloqueo de ningún tipo.
    palillos[yo].release()
    palillos[(yo + 1) % num_filosofos].release()

for i in range(num_filosofos):
    threading.Thread(target=filosofo, args=[i]).start()
