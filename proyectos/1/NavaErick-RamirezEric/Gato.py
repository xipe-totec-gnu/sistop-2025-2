import threading
from time import sleep
from enum import Enum
from random import randint

class EstadoGato(Enum):
    HAMBRIENTO = 1
    COMIENDO = 2
    SATISFECHO = 3
    ENFERMO = 4
    
class Gato(threading.Thread): #Herencia de threading.Thread Para la independencia de cada gato

    #Constructor de la clase gatito
    def __init__(self, nombre, genero):
        threading.Thread.__init__(self) #llama a la clase para que garantice el ser un hilo
        self.nombre = nombre #Por que cada gato tiene un nombre
        self.genero = genero   #Si es hembra, macho o invasor
        self.estado = EstadoGato.SATISFECHO #Define el estado que tendra el gato
        self.porciones   #cuantas porciones ha comido el gato
        #self.plato = plato  #en que plato esta llevando la accion, para el considerarlo en el semaphoro
    """INTRODUCIR ATRIBUTOS PARA QUE LA CLASE PUEDA INTERACTUAR CON LA INTERFAZ GRAFICA"""        
    #funcion para que el hilo trabaje
    def run(self):
        #cilo para que se repita esta acción
        while True:
            self.comer() #llamado a comer
            sleep(randint(1,19)) #Tiempo de reposo, al ser un gato, podriamos decir que duerme o hace cualquier otra cosa de gatos
    
    #funcion para que el gato coma
    def comer(self):
        #asignando las porciones que come cada tipo de gato
        if self.tipo.upper() == "MACHO" :
            self.porciones = 2
        elif self.tipo.upper() == "HEMBRA":
            self.porciones = 1 
        #accesos al plato, donde se verificara que no este lleno y asi 
        if self.plato.semaforo.acquire(blocking=True): #SI el metodo dice que si hay suficiente comida en el plato comera
            self.estado=EstadoGato.COMIENDO 
            sleep(randint(2,5))     #tiempo que se tarda en comer
            self.estado=EstadoGato.SATISFECHO
        else:
            self.estado="hambriento"
        self.plato.semaforo.realease() #libera el semaforo 

