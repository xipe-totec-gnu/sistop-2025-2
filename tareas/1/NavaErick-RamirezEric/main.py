##Autores: NavaErick && RamirezEric
##Fecha:   25/Marzo/2025
##Descripción: Intersección de Caminos

#IMPORTACIÓN DE LIBRERIAS
import threading  ##biblioteca para utilizar hilos
from time import sleep      ##biblioteca para utilizar un reloj
from random import randint ##biblioteca para poder generar números al azar
import auto_carriles as ac

NUM_AUTOS = 3 #Número de autos que se simularán

#Notese la simulación en sentido antihorario iniciando del cuadrante inferior derecho
carril_a = [] #lista de autos provenientes del carril a  ▗   
carril_b = [] #lista de autos provenientes del carril b  ▝
carril_c = [] #lista de autos provenientes del carril c ▘   
carril_d = [] #lista de autos provenientes del carril d ▖ 

'''
----------------MAIN----------------------------
'''
def main():
        ##Se crean los hilos
    for j in range(NUM_AUTOS): 
        carril_a.append(threading.Thread(target=ac.auto, args=('a',j+1)))    #se crea un hilo que ejecutará la función y se almacenará e la lista
        carril_a[-1].start()                                                 #acceso al último hilo agregado en la lista del carril a
        carril_b.append(threading.Thread(target=ac.auto, args=('b',j+1)))    #se crea un hilo que ejecutará la función y se almacenará e la lista
        carril_b[-1].start()                                                 #acceso al último hilo agregado en la lista del carril b
        carril_c.append(threading.Thread(target=ac.auto, args=('c', j+1)))   #se crea un hilo que ejecutará la función y se almacenará e la lista
        carril_c[-1].start()                                                 #acceso al último hilo agregado en la lista del carril c
        carril_d.append(threading.Thread(target=ac.auto, args=('d', j+1)))   #se crea un hilo que ejecutará la función y se almacenará e la lista
        carril_d[-1].start()                                                   #acceso al último hilo agregado en la lista del carril d  
    
    #Se espera a que todos los hilos terminen
    for aut in carril_a:  #recorriendo la lista del carril a
        aut.join()          #frenando el programa hasta que termine el hilo
    for aut in carril_b:  #recorriendo la lista del carril b
        aut.join()          #frenando el programa hasta que termine el hilo
    for aut in carril_c:  #recorriendo la lista del carril c
        aut.join()          #frenando el programa hasta que termine el hilo
    for aut in carril_d:  #recorriendo la lista del carril d
        aut.join()          #frenando el programa hasta que termine el hilo
    print('Todos los autos han pasado por la intersección')    
        
main()
