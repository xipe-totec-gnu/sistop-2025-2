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
    def __init__(self, nombre, tipo,platos, cola_gatos):
        threading.Thread.__init__(self) #llama a la clase para que garantice el ser un hilo
        self.nombre = nombre #Por que cada gato tiene un nombre
        self.tipo = tipo   #Si es hembra, macho o invasor
        self.estado = EstadoGato.SATISFECHO #Define el estado que tendra el gato 
        self.platos=platos
        self.cola_gatos=cola_gatos   

    def run(self):
        #cilo para que se repita esta acción
        while True:
            sleep(random.randint(20,30)) #Tiempo de reposo, al ser un gato, podriamos decir que duerme o hace cualquier otra cosa de gatos
            self.comer() #llamado a comer
            

   #funcion para que el gato coma
    """
P.
    - Si el gato es de tipo MACHO, consume 2 porciones de comida si hay al menos 2 disponibles.
    - Si el gato es de tipo HEMBRA, consume 1 porción de comida si hay al menos 1 disponible.
    - Si el tipo del gato no es reconocido, se vacía el plato (comida_disponible = 0).
    - La operación está protegida por un lock para evitar condiciones de carrera y garantizar
        que solo un gato interactúe con el plato a la vez.
    - Después de ajustar las porciones, se imprime el estado actual del plato.
    - El uso del lock asegura que la concurrencia sea manejada correctamente.
"""
            
    def comer(self):
            platos_aleatorios = self.platos.copy() #copia lista del plato para que no sea tan lineal
            random.shuffle(platos_aleatorios)       #mexcla la copia de la lista
            ya_comio = False                        #banderita para saber si ya comio
            for plato in platos_aleatorios:         #recorre los platos que etabn en la lista
                acquired = False                    #bandera para la adquisicion del semaforo       
                try:                                #bloque try and finally, intenta hacer que el gato coma, si no puede se ira a la cola
                    if plato.semaforo.acquire(blocking=False): #condicion para acceder al control del semaforo
                        acquired = True             #la andera pasara a true
                        with plato.lock:            #bloquea el platopara evitar concurrencias
                            if plato.comida_disponible > 0:     #evalua que haya comida en el plato
                                self.estado = EstadoGato.COMIENDO #actualiza el estado del gatito
                                sleep(random.randint(2, 5))   #simulaciondel tiempo en que come
                                self.estado = EstadoGato.SATISFECHO     #afirma que el gato ya ha comido
                                if self.tipo == TipoGato.MACHO:         ##condiciones puestas al principio de este metodo        
                                    if plato.comida_disponible >= 2:
                                        plato.comida_disponible -= 2      
                                        print(f"{self.nombre} ha comido")       
                                        print(f"Plato {plato.num} con {plato.comida_disponible} porciones")                          
                                elif self.tipo == TipoGato.HEMBRA:
                                    if plato.comida_disponible >= 1:
                                        plato.comida_disponible -= 1
                                        print(f"{self.nombre} ha comido")
                                        print(f"Plato {plato.num} con {plato.comida_disponible} porciones")                          
                                else:               #el gato invasor va a arrasar
                                    platos_aleatorios[0].comida_disponible = 0                    
                                    platos_aleatorios[1].comida_disponible = 0
                                    print(f"{self.nombre} ha comido")
                                        
                                ya_comio = True # si comio un gato, la bandera indicara que ya comio
                            else:
                                self.estado = EstadoGato.HAMBRIENTO #si no ha comido significara que el gato sigue con hambre
                finally:            
                    if acquired:
                        plato.semaforo.release()
                    if ya_comio:
                        break

            if not ya_comio: #si no ha comido
                
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

        