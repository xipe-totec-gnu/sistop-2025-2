"""
TAREA 1: EL ELEVADOR 

@Montiel Juarez Oscar Ivan
@Torres Delgadillo Mixctoaltl Samuel

Para este problema se usó:
- Hilos para manejar múltiples pasajeros concurrentemente
- Algoritmo LOOK
- Uso de semáforos y bloqueos
- Manejo dinámico de hilos

Clases principales:
    Elevador: simula el movimiento y operaciones del elevador
    Pasajero: simula al asuario de la facultad que hace uso del elevador
    Controlador: controla las interacciones

Funciones clave:
    generador_pasajeros: Crea pasajeros con destinos aleatorios
    handler_signal: maneja la interrupción del teclado para terminar el programa correctamente

Atributos configurables:
    MAX_PASAJEROS: Número máximo de pasajeros concurrentes (basado en núcleos CPU)
    Capacidad del elevador: Limitada por un semáforo (5)

Ejemplo de uso y salida:
    python tarea1_montielOscar_torresSamuel.py
    [Sistema] Hilos disponibles: 8
    [Sistema] Pasajeros concurrentes máximos: 8

    Elevador en piso 0 | Dirección: ↑
    Pasajero 0 esperando en piso 3
    Pasajero 1 esperando en piso 1

Dependencias:
    threading, time, random, signal, sys, os
"""

import threading
import time
import random
import signal
import sys
import os

# Ajuste dinámico basado en hilos de la CPU
MAX_PASAJEROS = max(1, os.cpu_count())

class Elevador(threading.Thread):
    """
    hilo que simula el elevador, contiene un algoritmo LOOK

    Atributos:
        controlador (Controlador): referencia al controlador principal
        piso_actual (int): piso actual del elevador (0-4)
        direccion (int): dirección actual del movimiento (1: arriba, -1: abajo)
        detener (threading.Event): evento para detener el hilo

    Métodos principales:
        run(): bucle principal de operación del elevador
        mover(): logica de movimiento y selección de piso
        manejar_paradas(): gestión de subida/bajada de alumnos (pasajeos)
    """
    
    def __init__(self, controlador):
        #Inicializa el elevador con valores predeterminados
        super().__init__(daemon=True)
        self.controlador = controlador
        self.piso_actual = 0
        self.direccion = 1  # 1: subir  -1: bajar
        self.detener = threading.Event()

    def run(self):
        while not self.detener.is_set():
            self.mover()
            self.manejar_paradas()
            print(f"Elevador en piso {self.piso_actual} | Dirección: {'↑' if self.direccion == 1 else '↓'}")
            time.sleep(1)

    def mover(self):
        """
        Determina el siguiente movimiento usando el algoritmo LOOK modificado.

        Estrategia del algoritmo:
            1. busca solicitudes en dirección actual (externas + internas).
            2. si no hay, cambia de dirección y repite la búsqueda.
            3. selecciona el piso más lejano con solicitudes en la dirección actual.
        """
        direccion_original = self.direccion
        solicitudes_totales = [
            ext + intern for ext, intern in zip(
                self.controlador.solicitudes, 
                self.controlador.destinos_internos
            )
        ]
        
        # Esto busca e la dirección actual
        if self.direccion == 1:
            rango = range(self.piso_actual + 1, 5)
        else:
            rango = range(self.piso_actual - 1, -1, -1)
        
        pisos_prioritarios = [p for p in rango if solicitudes_totales[p] > 0]
        
        # Esto busca en la dirección opuesta
        if not pisos_prioritarios:
            self.direccion *= -1
            if self.direccion == 1:
                rango = range(self.piso_actual + 1, 5)
            else:
                rango = range(self.piso_actual - 1, -1, -1)
            pisos_prioritarios = [p for p in rango if solicitudes_totales[p] > 0]
        
        # Si por algún motivo no hay solicitudes, se deteiene
        if not pisos_prioritarios:
            self.direccion = direccion_original  
            return
        
        # selecciona el piso mas lejando en la dirección que va
        if self.direccion == 1:
            self.piso_actual = max(pisos_prioritarios)
        else:
            self.piso_actual = min(pisos_prioritarios)

    def manejar_paradas(self):
        with self.controlador.lock:
            # Esto baja a los pasajeros
            pasajeros_a_bajar = [p for p in self.controlador.pasajeros if p.destino == self.piso_actual]
            for p in pasajeros_a_bajar:
                self.controlador.pasajeros.remove(p)
                self.controlador.capacidad.release()
                self.controlador.destinos_internos[p.destino] -= 1
                print(f"Pasajero {p.id} subió al elevador (Destino: piso {p.destino})")
            
            # sube a los pasajeros
            if self.piso_actual in self.controlador.paradas:
                for p in self.controlador.paradas[self.piso_actual][:]:
                    if self.controlador.capacidad.acquire(blocking=False):
                        p.evento_subir.set()
                        self.controlador.paradas[self.piso_actual].remove(p)
                        self.controlador.pasajeros.append(p)
                        self.controlador.destinos_internos[p.destino] += 1
                        print(f"Pasajero {p.id} subió al elevador")
            
            self.controlador.actualizar_solicitudes()

class Pasajero(threading.Thread):
    """
    Hilo que simula a un alumno tomando el elevador

    Atributos:
        id (int): clave única de identificaciòn
        origen (int): piso de origen (0-4)
        destino (int):piso destino (0-4)
        controlador (Controlador): referencia al controlador
        evento_subir (threading.Event): evento para sincronizar subida
        semaforo (threading.Semaphore): semaforo para control concurrente

    Comportamiento:
        1. se registra en el piso de origen
        2. espera a que el elevador lo recoja
        3. da una notificación cuando llega a su destino
    """
    
    def __init__(self, id, origen, destino, controlador, semaforo):
        super().__init__(daemon=True)
        self.id = id
        self.origen = origen
        self.destino = destino
        self.controlador = controlador
        self.evento_subir = threading.Event()
        self.semaforo = semaforo

    def run(self):
        """
        Ejecuta el ciclo de vida completo del pasajero en el sistema del elevador

            Flujo:
                1. registro inicial:
                - adquiere el semáforo de concurrencia
                - bajo bloqueo, se registra en el piso de origen del controlador
                - actualiza las solicitudes del sistema

                2. Espera activa:
                - Permanece en espera hasta que el elevador lo recoja (evento_subir)
                - Una vez dentro, verifica constantemente si el elevador llega a su destino

                3. Fin:
                - Libera recursos al salir del contexto with
                - Notifica cuando llega a su piso destino

            Comportamiento:
                - Usa time.sleep(0.1) para evitar consumo excesivo 
                - Todos los accesos a recursos compartidos están sincronizados con lock
                - El pasajero permanece activo hasta completar su viaje
        """
        with self.semaforo:
            with self.controlador.lock:
                if self.origen not in self.controlador.paradas:
                    self.controlador.paradas[self.origen] = []
                self.controlador.paradas[self.origen].append(self)
                self.controlador.actualizar_solicitudes()
            
            print(f"Pasajero {self.id} esperando en piso {self.origen} (Destino: piso {self.destino})")
            self.evento_subir.wait()  # Espera hasta subir
            
            # Esperar a llegar al destino
            while True:
                with self.controlador.lock:
                    if self.controlador.elevador.piso_actual == self.destino:
                        break
                time.sleep(0.1)
            
            print(f"Pasajero {self.id} llegó al piso {self.destino}")
        

class Controlador:
    """
    control principal que maneja todo el sistema

    Atributos:
        paradas (dict): diccionario de personas esperando en cada piso
        pasajeros (list): lista de gente que está usando el elevador en un momento preciso 
        lock (threading.Lock): evita que muchos usuarios se suban a la vez
        capacidad (threading.Semaphore): control de capacidad del elevador (5)
        solicitudes (list[int]): solicitudes por antender (pendientes) por piso
        elevador (Elevador): Referencia al elevador

    Responsabilidades:
        - sincronizar acceso a recursos compartidos
        - mantener estado actual del sistema
        - coordina la interacción entre el elevador y los pasajeros
    """
    
    def __init__(self):
        self.paradas = {}
        self.pasajeros = []
        self.lock = threading.Lock()
        self.capacidad = threading.Semaphore(5)
        self.solicitudes = [0] * 5
        self.elevador = None
        self.destinos_internos = [0] * 5 

    def actualizar_solicitudes(self):

        self.solicitudes = [len(self.paradas.get(piso, [])) for piso in range(5)]

def generador_pasajeros(controlador, semaforo):
    """
    genera pasajeros continuamente con intervalos aleatorios
    
    Args:
        controlador (Controlador):instancia del controlador
        semaforo (threading.Semaphore): semaforo para límite concurrente
    
    Características:
        - intervalos entre 0.5 y 1.5 segundos
        - origen y destino aleatorios
        - pasajeros como hilos daemon
    """
    id_pasajero = 0
    while True:
        origen = random.randint(0, 4)
        destino = random.randint(0, 4)
        while destino == origen:
            destino = random.randint(0, 4)
        Pasajero(id_pasajero, origen, destino, controlador, semaforo).start()
        id_pasajero += 1
        time.sleep(random.uniform(0.5, 1.5))

def handler_signal(sig, frame):
    # se encarga de manejar la interrupción del programa
    print("\nDeteniendo sistema...")
    controlador.elevador.detener.set()
    sys.exit(0)

if __name__ == "__main__":
    # configuración inicial
    print(f"[Sistema] Hilos disponibles: {os.cpu_count()}")
    print(f"[Sistema] Pasajeros concurrentes máximos: {MAX_PASAJEROS}\n")
    
    controlador = Controlador()
    controlador.elevador = Elevador(controlador)
    semaforo_pasajeros = threading.Semaphore(MAX_PASAJEROS)
    
    signal.signal(signal.SIGINT, handler_signal)
    controlador.elevador.start()
    
    # generador de pasajeros
    threading.Thread(target=generador_pasajeros, args=(controlador, semaforo_pasajeros), daemon=True).start()
    
    # bucle principal
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        handler_signal(None, None)