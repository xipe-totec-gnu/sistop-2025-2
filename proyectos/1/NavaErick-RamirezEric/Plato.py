#Librerias a importar
import threading
from time import sleep
from random import randint
from Gato import Gato, TipoGato

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
        self.comida_disponible = Plato.TOPEPLATO #porciones en el plato 
        self.semaforo = threading.Semaphore(1) # semaforo para que un gato coma a la vez
        self.lock = threading.Lock() # lock para poder bloquear la concurrencia en el plato 
    
    def consumirPorcion(self, gato):
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
        with self.lock: #bloqueando para que no pueda comer más de un gato a la vez
            if gato.tipo == TipoGato.MACHO:  #validando que haya suficiente comida
                if self.comida_disponible >= 2:
                    self.comida_disponible -= 2 #reajustando las cantidades
                    self.__str__() #imprimiendo el estado del plato
            elif gato.tipo == TipoGato.HEMBRA:
                if self.comida_disponible >= 1:
                    self.comida_disponible -= 1
                    self.__str__()
            else:
                self.comida_disponible = 0                    
                    
    def rellenarPlato(self):
        """
        Función para rellenar los platos de los gatos a 3 porciones.
        """
        with self.lock: #lockeo para que no se lastime ningun gato(si no se hace se mezclan las interacciones)
            if self.comida_disponible == 0:
                self.comida_disponible += 3
            else:
                self.comida_disponible = 3
                print(f"Ohhh no, se ha desbordado la comida, ahora tendras que limpiar")
            print(f"El plato {self.num} ha sido reabastecido")
        
    def estado(self):
        with self.lock:
            print(f"Planto {self.num} con {self.comida_disponible} porciones")
        
    def __str__(self):
        print(f"El plato {self.num} ahora tiene {self.comida_disponible} porciones") #mensaje
    
    
                
"""INTRODUCIR METODOS PARA LA INTERFAZ GRAFICA"""        
"""INTRODUCIR ACTUALIZACION EN LOS METODOS PARA LA INTERFAZ GRAFICA """

