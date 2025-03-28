import threading
import random
import time

class Intersection:
    def __init__(self):
        self.multiplex = threading.Semaphore(4)  # Permite hasta 4 autos simultáneamente
        self.sem_carril = threading.Semaphore(1)  # Controla el acceso a la selección del carril
        self.sem_intersecciones = [threading.Semaphore(1) for _ in range(4)]  # Un semáforo por intersección
        self.intersecciones = [[] for _ in range(4)]  # Lista de autos en cada intersección

    def change_intersection(self, auto_id, carril):
        """Gestiona el cruce de un auto en la intersección correspondiente."""
        self.sem_intersecciones[carril - 1].acquire()
        self.intersecciones[carril - 1].append(f"Auto: {auto_id}")
        print(f'ENTRADA - Auto {auto_id} llegó a la intersección {carril}')
        time.sleep(random.random())  # Simula el tiempo de cruce
        print(f'SALIDA - Auto {auto_id} salió de la intersección {carril}')
        self.sem_intersecciones[carril - 1].release()

    def traffic_zone(self, auto_id, carril, destino):
        """Gestiona la transición de un auto a través de dos intersecciones."""
        self.change_intersection(auto_id, carril)
        self.change_intersection(auto_id, destino)
        print(f'FINAL - Auto {auto_id} continúa su camino sin choques, carro completo c:')

    def transit(self, auto_id):
        """Simula el tráfico generando autos en los carriles y gestionando su cruce."""
        self.multiplex.acquire()
        self.sem_carril.acquire()
        
        carril = random.randint(1, 4)
        print(f'INICIO - Auto {auto_id} va por el carril {carril}')
        
        self.sem_carril.release()

        destinos = {1: 4, 2: 3, 3: 1, 4: 2}  # Diccionario para elegir el destino
        self.traffic_zone(auto_id, carril, destinos[carril])

        self.multiplex.release()

class TrafficSimulation:
    def __init__(self, num_autos=5):
        self.intersection = Intersection()
        self.num_autos = num_autos
    
    def run(self):
        """Inicia la simulación del tráfico."""
        for i in range(self.num_autos):
            threading.Thread(target=self.intersection.transit, args=[i]).start()

if __name__ == "__main__":
    simulation = TrafficSimulation(num_autos=5)
    simulation.run()