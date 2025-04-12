import threading
from time import sleep
from enum import Enum
from random import randint

class EstadoGato(Enum):
    HAMBRIENTO = 1
    COMIENDO = 2
    SATISFECHO = 3
    ENFERMO = 4
    
class TipoGato(Enum):
    MACHO = "macho"
    HEMBRA = "hembra"
    INVASOR = "invasor"
    
class Gato(threading.Thread): #Herencia de threading.Thread Para la independencia de cada gato
    """
    Constructor de la clase Gato.
    Args:            
        nombre (str):
       tipo (str):
    Atributos:
        nombre (str):
        tipo (str):
        estado (EstadoGato):
        porciones (int):
    """
    def __init__(self, nombre, tipo):
        threading.Thread.__init__(self) #llama a la clase para que garantice el ser un hilo
        self.nombre = nombre #Por que cada gato tiene un nombre
        self.tipo = tipo   #Si es hembra, macho o invasor
        self.estado = EstadoGato.SATISFECHO #Define el estado que tendra el gato    
    """
    Método principal que se ejecuta al iniciar el hilo del gato.
    """
    def run(self):
        #cilo para que se repita esta acción
        while True:
            sleep(randint(20,30)) #Tiempo de reposo, al ser un gato, podriamos decir que duerme o hace cualquier otra cosa de gatos
            self.comer() #llamado a comer

    #funcion para que el gato coma
    def comer(self):
        #accesos al plato, donde se verificara que no este lleno y asi 
        if self.plato.semaforo.acquire(blocking=True): #SI el metodo dice que si hay suficiente comida en el plato comera
            self.estado=EstadoGato.COMIENDO 
            sleep(randint(2,5))     #tiempo que se tarda en comer
            self.estado=EstadoGato.SATISFECHO
        else:
            self.estado="hambriento"
        self.plato.semaforo.realease() #libera el semaforo 
        
    def nivelPrioridad(self):
        """
        Método para determinar el nivel de prioridad del gato.
        Returns:
            int: Nivel de prioridad del gato en la cola para entrar a los platos.
        """
        if self.tipo == TipoGato.INVASOR:
            return 0
        elif self.estado == EstadoGato.ENFERMO:
            return 1
        elif self.tipo == TipoGato.HEMBRA:
            return 2
        elif self.tipo == TipoGato.MACHO:
            return 3

        
