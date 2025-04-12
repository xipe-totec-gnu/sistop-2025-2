import threading
from time import sleep
from enum import Enum
import random 
from itertools import count

contador = count()

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
    def __init__(self, nombre, tipo,platos, cola_gatos):
        threading.Thread.__init__(self) #llama a la clase para que garantice el ser un hilo
        self.nombre = nombre #Por que cada gato tiene un nombre
        self.tipo = tipo   #Si es hembra, macho o invasor
        self.estado = EstadoGato.SATISFECHO #Define el estado que tendra el gato 
        self.platos=platos
        self.cola_gatos=cola_gatos   
    """
    Método principal que se ejecuta al iniciar el hilo del gato.
    """
    def run(self):
        #cilo para que se repita esta acción
        while True:
            sleep(random.randint(20,30)) #Tiempo de reposo, al ser un gato, podriamos decir que duerme o hace cualquier otra cosa de gatos
            self.comer() #llamado a comer
            

    #funcion para que el gato coma
    """
Permite que un gato consuma una porción de comida del plato, dependiendo de su tipo.

Args:
    gato (Gato): Objeto de tipo Gato

    - Si el gato es de tipo MACHO, consume 2 porciones de comida si hay al menos 2 disponibles.
    - Si el gato es de tipo HEMBRA, consume 1 porción de comida si hay al menos 1 disponible.
    - Si el tipo del gato no es reconocido, se vacía el plato (comida_disponible = 0).
    - La operación está protegida por un lock para evitar condiciones de carrera y garantizar
        que solo un gato interactúe con el plato a la vez.
    - Después de ajustar las porciones, se imprime el estado actual del plato.
    - El uso del lock asegura que la concurrencia sea manejada correctamente.
"""
            
    def comer(self):
            platos_aleatorios = self.platos.copy()
            random.shuffle(platos_aleatorios)
            ya_comio = False
            for plato in platos_aleatorios:
                acquired = False
                try:
                    if plato.semaforo.acquire(blocking=False):
                        acquired = True
                        with plato.lock:
                            if plato.comida_disponible > 0:
                                self.estado = EstadoGato.COMIENDO
                                sleep(random.randint(2, 5))
                                self.estado = EstadoGato.SATISFECHO
                                if self.tipo == TipoGato.MACHO:                 
                                    if plato.comida_disponible >= 2:
                                        plato.comida_disponible -= 2      
                                        print(f"{self.nombre} ha comido")       
                                        print(f"Plato {plato.num} con {plato.comida_disponible} porciones")                          
                                elif self.tipo == TipoGato.HEMBRA:
                                    if plato.comida_disponible >= 1:
                                        plato.comida_disponible -= 1
                                        print(f"{self.nombre} ha comido")
                                        print(f"Plato {plato.num} con {plato.comida_disponible} porciones")                          
                                else:
                                    platos_aleatorios[0].comida_disponible = 0                    
                                    platos_aleatorios[1].comida_disponible = 0
                                    print(f"{self.nombre} ha comido")
                                        
                                ya_comio = True
                            else:
                                self.estado = EstadoGato.HAMBRIENTO
                finally:
                    if acquired:
                        plato.semaforo.release()
                    if ya_comio:
                        break

            if not ya_comio:
                
                print(f"{self.nombre} no encontró plato disponible o con comida. Pasa la cola")
                self.estado = EstadoGato.HAMBRIENTO
                self.cola_gatos.put((self.nivelPrioridad(), next(contador), self))


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

        