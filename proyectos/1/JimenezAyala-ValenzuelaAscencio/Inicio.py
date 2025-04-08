import pygame
import random
from Cliente import Cliente
from Champion import Champion
from Platos import Platos

def inicio(pantalla, fuente, ANCHO, ALTO):
    fondo = pygame.image.load("fondoChamps.png")  
    fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))

    NUM_CLIENTES = 10
    NUM_PLATOS = 3

    champion = Champion()
    platos = Platos(NUM_PLATOS)

    clientes = [Cliente(i, champion, platos) for i in range(NUM_CLIENTES)]

    for c in clientes:
        c.nombre = "Cliente_" + str(random.randint(1, 100))  # Nombre random
        c.start()

    # Dibujar una sola vez la imagen de fondo
    pantalla.blit(fondo, (0, 0))
    pygame.display.flip()

    # Esperar a que terminen los hilos (sin cerrar la ventana)
    for c in clientes:
        c.join()

    print("FIN.")

    # Mantener ventana abierta sin modificar lo que ya está dibujado
    corriendo = True
    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
