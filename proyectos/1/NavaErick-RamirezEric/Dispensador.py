import threading
from time import sleep
from random import randint
from enum import Enum
from Plato import Plato
from Gato import Gato, TipoGato 
class EstadoDispensador(Enum):
    CERRADO = 1
    ABIERTO = 2
    ALERTA = 3

class Dispensador:
    
    def __init__(self, platos, gatos, cola):    # Inicializa el dispensador con los platos que administra a traves de una lista llamada platos
        self.platos = platos                    # Lista de platos
        self.estado = EstadoDispensador.CERRADO       # Estado inicial del dispensador
        self.gato_invasor = False               # Indica si hay un gato invasor presente
        self.gatos = gatos                      # Lista de gatos que pueden acceder al dispensador
        self.cola = cola                        # Cola de gatos que esperan para acceder a los platos
        self.lock=threading.Lock()

    def run(self):
        while True:
            if self.estado != EstadoDispensador.ALERTA:

                a=len(self.platos)
                for plato in self.platos:
                    if plato.comida_disponible < 1:
                        a = a-1
                        print("rellenando plato")
                if a == 0 :
                    self.dispensar()
                    self.estado=EstadoDispensador.CERRADO
                sleep(5)
         
    def dispensar(self):
        self.estado=EstadoDispensador.ABIERTO
        for plato in self.platos:
            with plato.lock:
                plato.comida_disponible = 3
                sleep(1)
                print(f"El plato {plato.num} ha sido rellenado")

    
    def detectarGatoInvasor(self):
      with self.Lock:
        self.gato_invasor = True
        self.estado = EstadoDispensador.ALERTA
    
    def retiradaGatoInvasor(self):
        with self.lock:
            self.gato_invasor = False
            self.estado = EstadoDispensador.ABIERTO
            self.dispensar()
            self.estado = EstadoDispensador.CERRADO
        
    def insertarGatoCola(self, gato):
        if gato.tipo == TipoGato.INVASOR:
            self.detectarGatoInvasor()
        self.cola.put(gato.nivelPrioridad(), gato.nombre)
        
    def gestion(self):
        while True:
            if not self.cola.empty():
                prioridad,_,gato=self.cola.get()
                print(f"{gato.nombre} volverá a intentar comer")
                gato.comer()
                if gato.tipo == TipoGato.INVASOR:
                    with self.lock:
                        self.gato_invasor = False
                        if self.cola.empty():
                            self.retiradaGatoInvasor()
                    print("Gato invasor neutralizado")
                    
            sleep(3)