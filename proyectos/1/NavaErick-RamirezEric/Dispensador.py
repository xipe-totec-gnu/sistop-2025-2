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

    #A este metodo se le asigna tal cual un hilo
    def run(self):
        while True: #esto hace que sea un loop sin fin
            if self.estado != EstadoDispensador.ALERTA: #en caso de que no este en alerta

                a=len(self.platos)                      #cantidad de platos
                for plato in self.platos:               #verificara la comida de cada plato
                    if plato.comida_disponible < 1:     #si no hay comida en un plato se restara a 'a'
                        a = a-1
                if a == 0 :
                    self.dispensar()                       #si ya no hay comida en los dos platos se rellenaran
                    self.estado=EstadoDispensador.CERRADO   # una vez rellenado se cerrra el sipensador
                sleep(5)
         
    #metodo para rellear los plato
    def dispensar(self):
        self.estado=EstadoDispensador.ABIERTO  #se abre el dispensador
        for plato in self.platos:               #iterara sobre los platos
            with plato.lock:                    #bloqueo para que los gatos no se amensen 
                plato.comida_disponible = 3     #rellena 
                sleep(1)                        #tiempo en el que rellena
                print(f"El plato {plato.num} ha sido rellenado")

    #metodo por s el gato invasor se queda en la coa
    def detectarGatoInvasor(self):          
        self.estado = EstadoDispensador.ALERTA  #actualiza el estado del dispensador
    #metodo para cuando se de la orden de sacar al invasor
    def retiradaGatoInvasor(self):
        with self.lock:
            self.gato_invasor = False               #se dice que no estara el gato invasor
            self.estado = EstadoDispensador.ABIERTO #se abre le dispensador
            self.dispensar()                        #se dispensa
            self.estado = EstadoDispensador.CERRADO #se cierra el dispensador
    #metodo para insertar eldato a la cola
    def insertarGatoCola(self, gato):
        if gato.tipo == TipoGato.INVASOR:   #si es el invasor se advierte
            self.detectarGatoInvasor()
        self.cola.put(gato.nivelPrioridad(), gato.nombre)   #se forma el gato
        
    #metodo para la gestion de la cola
    def gestion(self):
        while True:
            if not self.cola.empty():  #en caso de que la cola no este vacia
                prioridad, _, gato = self.cola.get()    #se saca el gato con mayor prioridad, el _ es el numero de ingreso,esto por si empatan en prioridad
                print(f"{gato.nombre} volverá a intentar comer")#mensaje
                gato.comer()                #se le manda a comer otra ves al gato
                if gato.tipo == TipoGato.INVASOR:
                    self.detectarGatoInvasor()
                    with self.lock:
                        if self.cola.empty():
                            self.retiradaGatoInvasor()
                            print("Gato invasor neutralizado")
            sleep(3)
                    
