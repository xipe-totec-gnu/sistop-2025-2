#Librerias a importar
import threading
from time import sleep
from random import randint

class Plato:
    def __init__(self,num):
        self.num = num #numero de plato
        self.comida_disponible = 3 #porciones en el plato 
        self.semaforo = threading.Semaphore(1) # semaforo para dos gato simultaneos
        self.lock = threading.Lock() # lock para poder bloquear la concurrencia en el plato 
    
    def comiendo(self, porcion):
        with self.lock: #bloqueando para que no pueda comer más de un gato a la vez
            if self.porciones >= porcion:   #validando que haya suficiente comida
                self.comida_disponible -= porcion #reajustando las cantidades
                print(f"El plato {self.num} ahora tiene {self.comida_disponible} porciones") #mensaje
                return True             #indicacion de que si comio
            else:
                print(f"El plato {self.num} no tiene suficientes porciones")
                return False            #indicacion de que no comió

    def rellenar(self):
        with self.lock: #lockeo para que no se lastime ningun gato(si no se hace se mezclan las interacciones)
            if self.comida_disponible < 5:
                self.comida_disponible += 3
                if self.comida_disponible > 5:
                    self.comida_disponible = 5
                    print(f"Ohhh no, se ha desvordado la comida, ahora tendras que limpiar")
                print(f"El plato {self.num} ha sido re abastecido")
        

    def estado(self):
        with self.lock:
            print(f"Planto {self.num} con {self.comida_disponible} porciones")
    


"""INTRODUCIR METODOS PARA LA INTERFAZ GRAFICA"""        
"""INTRODUCIR ACTUALIZACION EN LOS METODOS PARA LA INTERFAZ GRAFICA """    

