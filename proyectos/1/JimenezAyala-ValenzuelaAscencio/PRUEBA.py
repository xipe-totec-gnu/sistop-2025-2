import pygame
import threading
import time
import random

pygame.init()
ANCHO, ALTO = 800, 500
screen = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Zona reservada con hilos activos")
clock = pygame.time.Clock()

# Zona reservada
ZONA_H = 200
ZONA_Y = ALTO - ZONA_H
ZONA_W = ANCHO
CUADRO = 180
NUM_SLOTS = 10  # Máximo 10 slots (y 10 hilos)
slots = [None] * NUM_SLOTS

lock = threading.Lock()

# Cargar fondo
imagen_fondo = pygame.image.load("fondoChamps.png").convert()
imagen_fondo = pygame.transform.scale(imagen_fondo, (ANCHO, ALTO))

class HiloCarita(threading.Thread):
    def __init__(self):
        super().__init__(daemon=True)
        self.slot_index = None
        self.activo = False

        # Imagen aleatoria
        num = random.randint(1, 8)
        path = f"Comiendo{num}.png"
        img = pygame.image.load(path).convert_alpha()
        self.image = pygame.transform.scale(img, (CUADRO, CUADRO))

    def run(self):
        while True:
            time.sleep(random.uniform(2, 5))

            with lock:
                try:
                    # Buscar slot libre aleatorio
                    indices_disponibles = [i for i, v in enumerate(slots) if v is None]
                    if indices_disponibles:
                        self.slot_index = random.choice(indices_disponibles)
                        slots[self.slot_index] = self
                        self.activo = True
                    else:
                        self.slot_index = None
                except:
                    self.slot_index = None

            if self.slot_index is not None:
                time.sleep(random.uniform(2, 4))
                with lock:
                    slots[self.slot_index] = None
                    self.activo = False
                    self.slot_index = None

# Crear los 10 hilos
hilos = [HiloCarita() for _ in range(10)]
for h in hilos:
    h.start()

# Bucle principal
running = True
while running:
    screen.blit(imagen_fondo, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    with lock:
        for i, hilo in enumerate(slots):
            if hilo:
                slot_width = ZONA_W // NUM_SLOTS
                x = i * slot_width + (slot_width - CUADRO) // 2
                y = ZONA_Y + ZONA_H - CUADRO + 30
                screen.blit(hilo.image, (x, y))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
