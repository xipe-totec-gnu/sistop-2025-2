#Librerias a importar
import threading
from time import sleep
from random import randint
from Gato import TipoGato

class Plato:
    
    TOPEPLATO = 3
    
    def __init__(self,num):
        """
        Inicializa clase Plato.
        Args:
            num (int): 
        Atributos:
            num (int):
            comida_disponible (int): 
            semaforo (threading.Semaphore):
            lock (threading.Lock):
        """
        self.num = num
        self.comida_disponible = 3           #porciones en el plato 
        self.semaforo = threading.Semaphore(1)              # semaforo para que un gato coma a la vez
        self.lock = threading.Lock()                        # lock para poder bloquear la concurrencia en el plato 
    

        
    def estado(self):
        with self.lock:
            print(f"Planto {self.num} con {self.comida_disponible} porciones")
        
    def __str__(self):
        print(f"El plato {self.num} ahora tiene {self.comida_disponible} porciones") #mensaje
    
    
                
"""INTRODUCIR METODOS PARA LA INTERFAZ GRAFICA"""        
"""INTRODUCIR ACTUALIZACION EN LOS METODOS PARA LA INTERFAZ GRAFICA """