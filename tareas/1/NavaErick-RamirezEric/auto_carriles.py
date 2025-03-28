import threading  ##biblioteca para utilizar hilos
from time import sleep      ##biblioteca para utilizar un reloj
from random import randint ##biblioteca para poder generar números al azar
import ctes as c           ##iimportando el archivo con los valores asignados a los colores por carril
'''
Para no tener problemas en el caso de encontrarse un carro en cada cuadrante se utilizará un semaphore que permita la entrada de 3 autos a la 
interseccion de caminos, siendo que se posibilita que alguno de ellos avanza y libere el paso para los otros carriles. En el caso de ser 4 autos 
no habría espacio para que ninguno de ellos avance.
'''
interseccion_caminos = threading.Semaphore(3)

#Para cada cuadrante se tendra su propio mutex para garantizar la el uso de un solo auto a la vez por intersección
#Simulación del cuarante visto en el diagrama ╬
mutex_a = threading.Lock()
mutex_b = threading.Lock()
mutex_c = threading.Lock()
mutex_d = threading.Lock()


'''-------------------------------------Función -------------------------------------'''
def auto(carril_org, num_auto):
    interseccion_caminos.acquire()              #bloqueo para que un solo auto transite
    accion_dir = randint(0,2) #0 -> dobla a la derecha, 1 -> sigue recto, 2 -> dobla a la izquierda
    if carril_org == 'a':                       
        mutex_a.acquire()           #bloqueando mutex para que no entre otro carro 
        try:
            print(c.ROJO + f'Auto {carril_org}{num_auto} ha entrado por el carril a  🚗 ↑' + c.DEFAULT, sep='')  #ingresa un carro 
            sleep(randint(1,4))   #se da un margen de tiempo
        finally:
            cambioCuadrante(carril_org, num_auto, accion_dir)     #se llama al cambia de cuadrante
    elif carril_org == 'b':         #encaso de que sea a aprtir del carril b
        mutex_b.acquire()             #bloqueando mutex para que no entre otro carro 
        try:
            print(c.AZUL + f'Auto {carril_org}{num_auto} ha entrado por el carril b  🚗 ←' + c.DEFAULT, sep='')   #ingresa un carro 
            sleep(randint(1,4)) #se da un margen de tiempo
        finally:
            cambioCuadrante(carril_org, num_auto, accion_dir) #se llama al cambia de cuadrante
    elif carril_org == 'c':  #encaso de que sea a aprtir del carril c
        mutex_c.acquire()    #bloqueando mutex para que no entre otro carro 
        try:
            print(c.VERDE + f'Auto {carril_org}{num_auto} ha entrado por el carril c 🚗 ↓' + c.DEFAULT, sep='')  #ingresa un carro 
            sleep(randint(1,4))#se llama al cambia de cuadrante
        finally:
            cambioCuadrante(carril_org, num_auto, accion_dir) #se cambia de cuadrante 
    elif carril_org == 'd':  #encaso de que sea a aprtir del carril d
        mutex_d.acquire()    #bloqueando mutex para que no entre otro carro 
        try:
            print(c.AMARILLO + f'Auto {carril_org}{num_auto} ha entrado por el carril    🚗 →' + c.DEFAULT, sep='')  #ingresa un carro 
            sleep(randint(1,4)) #se da un margen de tiempo
        finally:
            cambioCuadrante(carril_org, num_auto, accion_dir) #se llama al cambia de cuadrante


'''-----------------------------------Función de cambio de cuadrante--------------------------------------'''    
def cambioCuadrante(carril_org, num_auto, accion_dir):
    if carril_org == 'a':
        if accion_dir == 0: #Dobla a la derecha
            try:
                print(c.ROJO + f'Auto {carril_org}{num_auto} dobla  a la derecha en el cuadrante a (a -> a)  🚗 ↱' + c.DEFAULT, sep='')
                sleep(randint(1,4))
            finally:
                mutex_a.release()
                interseccion_caminos.release()
        elif accion_dir == 1: #Sigue recto
            mutex_b.acquire()
            mutex_a.release()
            try:
                print(c.ROJO + f'Auto {carril_org}{num_auto} ha entrado al cuadrante b  🚗' + c.DEFAULT, sep='')
                sleep(randint(1,4))
            finally:
                mutex_b.release()
                print(c.ROJO + f'Auto {carril_org}{num_auto} ha seguido recto por el cuadrante b (a -> b) 🚗 ↑' + c.DEFAULT, sep='')
                interseccion_caminos.release()
        elif accion_dir == 2: #Dobla a la izquierda
            mutex_b.acquire()
            mutex_a.release()
            try:
                print(c.ROJO + f'Auto {carril_org}{num_auto} ha entrado al cuadrante b   🚗 ' + c.DEFAULT, sep='')
                sleep(randint(1,4))
                mutex_c.acquire()
                mutex_b.release()
                print(c.ROJO + f'Auto {carril_org}{num_auto} ha doblado hacia el cuadrante c  🚗 ↰' + c.DEFAULT, sep='')
            finally:
                print(c.ROJO + f'Auto {carril_org}{num_auto} ha seguido por el cuadrante c (a -> b -> c)' + c.DEFAULT, sep='')
                mutex_c.release()
                interseccion_caminos.release()
    elif carril_org == 'b':
        if accion_dir == 0: #Dobla a la derecha
            try:
                print(c.AZUL + f'Auto {carril_org}{num_auto} dobla  a la derecha en el cuadrante b (b -> b) 🚗 ⮬ ' + c.DEFAULT, sep='')
                sleep(randint(1,4))
            finally:
                mutex_b.release()
                interseccion_caminos.release()
        elif accion_dir == 1: #Sigue recto
            mutex_c.acquire()
            mutex_b.release()
            try:
                print(c.AZUL + f'Auto {carril_org}{num_auto} ha entrado al cuadrante c 🚗 ←' + c.DEFAULT, sep='')
                sleep(randint(1,4))
            finally:
                mutex_c.release()
                print(c.AZUL + f'Auto {carril_org}{num_auto} ha salido de la intersección por el cuadrante c (b -> c) 🚗 ←' + c.DEFAULT, sep='')
                interseccion_caminos.release()
        elif accion_dir == 2: #Dobla a la izquierda
            mutex_c.acquire()
            mutex_b.release()
            try:
                print(c.AZUL + f'Auto {carril_org}{num_auto} ha entrado al cuadrante c🚗 ←' + c.DEFAULT, sep='')
                sleep(randint(1,4))
                mutex_d.acquire()
                mutex_c.release()
                print(c.AZUL + f'Auto {carril_org}{num_auto} ha doblado hacia el cuadrante d  ⮦🚗 ' + c.DEFAULT, sep='')
            finally:
                sleep(randint(1,4))                
                print(c.AZUL + f'Auto {carril_org}{num_auto} ha seguido por el cuadrante d (b -> c -> a)   ↆ🚗' + c.DEFAULT, sep='')
                mutex_d.release()
                interseccion_caminos.release()
    elif carril_org == 'c':
        if accion_dir == 0: #Dobla a la derecha
            try:
                print(c.VERDE + f'Auto {carril_org}{num_auto} dobla a la derecha en el cuadrante c (c -> c) 🚗↲ ' + c.DEFAULT, sep='')
                sleep(randint(1,4))
            finally:
                mutex_c.release()
                interseccion_caminos.release()
        elif accion_dir == 1: #Sigue recto
            mutex_d.acquire()
            mutex_c.release()
            try:
                print(c.VERDE + f'Auto {carril_org}{num_auto} ha entrado al cuadrante d 🚗 🡓'+ c.DEFAULT, sep='')
                sleep(randint(1,4))
            finally:
                mutex_d.release()
                print(c.VERDE + f'Auto {carril_org}{num_auto} ha salido de la intersección por el cuadrante d (c -> d) 🚗 🡓' + c.DEFAULT, sep='')
                interseccion_caminos.release()
        elif accion_dir == 2: #Dobla a la izquierda
            mutex_d.acquire()
            mutex_c.release()
            try:
                print(c.VERDE + f'Auto {carril_org}{num_auto} ha entrado al cuadrante d  🚗' + c.DEFAULT, sep='')
                sleep(randint(1,4))
                mutex_a.acquire()
                mutex_d.release()
                print(c.VERDE + f'Auto {carril_org}{num_auto} ha doblado hacia el cuadrante a   🚗↳ ' + c.DEFAULT, sep='')
            finally:
                sleep(randint(1,4))
                print(c.VERDE + f'Auto {carril_org}{num_auto} ha seguido por el cuadrante a (c -> d -> a) 🚗 ➙' + c.DEFAULT, sep='')
                mutex_a.release()
                interseccion_caminos.release()
    elif carril_org == 'd': #dobla derecha  
        if accion_dir == 0:
            try:
                print(c.AMARILLO + f'Auto {carril_org}{num_auto} dobla a la derecha en el cuadrante d (d -> d) 🚗↴' + c.DEFAULT, sep='')
                sleep(randint(1,4))
            finally:
                mutex_d.release()
                interseccion_caminos.release()
        elif accion_dir == 1: #sigue recto
            mutex_a.acquire()
            mutex_d.release()
            try:
                print(c.AMARILLO + f'Auto {carril_org}{num_auto} ha entrado al cuadrante a 🚗 ➙' + c.DEFAULT, sep='')
                sleep(randint(1,4))
            finally:
                mutex_a.release()
                print(c.AMARILLO + f'Auto {carril_org}{num_auto} ha salido de la intersección por el cuadrante a (d -> a) 🚗 ➙' + c.DEFAULT, sep='')
                interseccion_caminos.release()
        elif accion_dir == 2: #dobla izquierda
            mutex_a.acquire()
            mutex_d.release()
            try:
                print(c.AMARILLO + f'Auto {carril_org}{num_auto} ha entrado al cuadrante a 🚗 ➙' + c.DEFAULT, sep='')
                sleep(randint(1,4))
                mutex_b.acquire()
                mutex_a.release()
                print(c.AMARILLO + f'Auto {carril_org}{num_auto} ha doblado hacia el cuadrante  🚗⮥' + c.DEFAULT, sep='')
            finally:
                sleep(randint(1,4))
                print(c.AMARILLO + f'Auto {carril_org}{num_auto} ha seguido por el cuadrante b (d -> a -> b) 🚗🡩' + c.DEFAULT, sep='')
                mutex_b.release()
                interseccion_caminos.release()