import threading
from time import sleep
from random import randint

class Dispensador:
    
    CERRADO = 0
    ABIERTO = 1
    ALERTA = 2
    
    def __init__(self, platos):
        self.platos= platos
        self.estado = Dispensador.CERRADO   
    
    def dispensar(self, cantidad):
        # Simula el tiempo de dispensado
        sleep(1)
        print(f"Dispensando {cantidad} gramos de comida.")
        return cantidad
    