import threading
import time
import random

class Balsa:
    def __init__(self):
        self.mutex = threading.Lock()
        self.hackers = 0
        self.serfs = 0
        self.balsa_lista = threading.Condition(self.mutex)
        self.max_personas = 4
    
    def abordar(self, tipo):
        with self.mutex:
            if tipo == 'hacker':
                self.hackers += 1
            else:
                self.serfs += 1
            
            # Esperar hasta que haya una combinación válida para abordar
            while not self.validar_abordaje():
                self.balsa_lista.wait()
            
            print(f"{tipo.capitalize()} abordó la balsa.")
            
            # Si es el último en abordar, cruzar el río
            if self.hackers + self.serfs == self.max_personas:
                print("Balsa cruzando el río con:")
                print(f" - {self.hackers} Hackers")
                print(f" - {self.serfs} Serfs")
                time.sleep(2)
                print("Balsa regresando...")
                self.hackers = 0
                self.serfs = 0
                self.balsa_lista.notify_all()
    
    def validar_abordaje(self):
        return (self.hackers + self.serfs == self.max_personas and 
                (self.hackers == 4 or self.serfs == 4 or (self.hackers == 2 and self.serfs == 2)))

# Función para representar un desarrollador tratando de abordar
def desarrollador(tipo, balsa):
    time.sleep(random.uniform(0.5, 2))  # Simular llegada aleatoria
    print(f"{tipo.capitalize()} quiere abordar.")
    balsa.abordar(tipo)

# Instancia de la balsa
balsa = Balsa()

# Crear y gestionar un número reducido de hilos
num_hackers = 6  # Reducido para evitar saturación de hilos
num_serfs = 6

threads = []
for _ in range(num_hackers // 2):
    t = threading.Thread(target=desarrollador, args=("hacker", balsa))
    threads.append(t)
    t.start()
    t = threading.Thread(target=desarrollador, args=("serf", balsa))
    threads.append(t)
    t.start()

# Esperar a que los hilos terminen
for t in threads:
    t.join()