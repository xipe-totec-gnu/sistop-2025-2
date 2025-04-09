import pygame
import random
import threading
from Cliente import *
from Champion import Champion
from Platos import *

def inicio(pantalla, fuente, ANCHO, ALTO):
    # Cargar fondo
    fondo = pygame.image.load("assets/fondoChamps.png")  
    fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))

    NUM_CLIENTES = 10
    NUM_PLATOS = 3
    NUM_SLOTS = 10
    CUADRO = 180
    ZONA_H = 200
    ZONA_Y = ALTO - ZONA_H
    ZONA_W = ANCHO

    # Crear lock y slots compartidos
    lock = threading.Lock()
    slots = [None] * NUM_SLOTS

    # Crear champion y platos
    champion = Champion()
    platos = Platos(NUM_PLATOS)

    # Crear e iniciar hilos de clientes
    clientes = [Cliente(i, champion, platos) for i in range(NUM_CLIENTES)]
    for c in clientes:
        c.nombre = "Cliente_" + str(random.randint(1, 100))  # Nombre random
        c.lock = lock
        c.slots = slots
        c.start()

    corriendo = True
    while corriendo:
        pantalla.blit(fondo, (0, 0))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False

        # HUD visual de los clientes activos
        with lock:
            for i, cliente in enumerate(slots):
                if cliente:
                    slot_width = ZONA_W // NUM_SLOTS
                    x = i * slot_width + (slot_width - CUADRO) // 2
                    y = ZONA_Y + ZONA_H - CUADRO + 30
                    pantalla.blit(cliente.image, (x, y))
        
        pygame.display.flip()
        clock.tick(60)

    print("FIN.")

    