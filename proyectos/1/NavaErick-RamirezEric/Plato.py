#Librerias a importar
import threading
from time import sleep
from random import randint
from Gato import TipoGato

class Plato:
    
    TOPEPLATO = 3
    
    def __init__(self,num):
       
        self.num = num                                      #numero del plato
        self.comida_disponible = 3                         #porciones en el plato 
        self.semaforo = threading.Semaphore(1)              # semaforo para que un gato coma a la vez
        self.lock = threading.Lock()                        # lock para poder bloquear la concurrencia en el plato 
    

        
##