import threading
from time import sleep
from random import randint
from enum import Enum
from Gato import Gato
from Plato import Plato

class EstadoDispensador(Enum):
    CERRADO = 1
    ABIERTO = 2
    ALERTA = 3

class Dispensador:
    
    def __init__(self, platos, gatos, cola): # Inicializa el dispensador con los platos que administra a traves de una lista llamada platos
        self.platos = platos # Lista de platos
        self.estado = Dispensador.CERRADO # Estado inicial del dispensador
        self.gato_invasor = False # Indica si hay un gato invasor presente
        self.gatos = gatos # Lista de gatos que pueden acceder al dispensador
        self.cola = cola # Cola de gatos que esperan para acceder a los platos
         
    def dispensar(self, cantidad):
        # Simula el tiempo de dispensado
        sleep(1)
        print(f"Dispensando {cantidad} gramos de comida.")
        return cantidad
    
    def detectarGatoInvasor(self):
      with self.Lock:
        self.gato_invasor = True
        self.estado = EstadoDispensador.ALERTA
    
    def retiradaGatoInvasor(self):
        self.gato_invasor = False
        self.estado = EstadoDispensador.ABIERTO
        self.dispensar()
        self.estado = EstadoDispensador.CERRADO
        
    def insertarGatoCola(self, gato):
        self.cola.put(gato.nivelPrioridad(), gato.nombre)
        