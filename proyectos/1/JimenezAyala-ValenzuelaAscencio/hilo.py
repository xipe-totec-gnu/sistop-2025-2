import pygame
import threading
import time
import random

# Inicializar Pygame
pygame.init()
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Estados de Hilos")
clock = pygame.time.Clock()

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)

# Cantidad de hilos y sus posiciones
NUM_HILOS = 4
hilos_estado = [{"trabajando": True} for _ in range(NUM_HILOS)]
posiciones = [(150 * i + 50, 200) for i in range(NUM_HILOS)]

def hilo_trabajo(index):
    # Simula trabajo con duración aleatoria
    tiempo_trabajo = random.randint(5, 10)
    time.sleep(tiempo_trabajo)
    hilos_estado[index]["trabajando"] = False

def dibujar_cara(pos, feliz=True):
    x, y = pos
    color = YELLOW if feliz else BLUE

    # Cara
    pygame.draw.circle(screen, color, (x, y), 50)
    # Ojos
    pygame.draw.circle(screen, BLACK, (x - 15, y - 15), 5)
    pygame.draw.circle(screen, BLACK, (x + 15, y - 15), 5)
    # Boca
    if feliz:
        pygame.draw.arc(screen, BLACK, (x - 25, y - 10, 50, 30), 3.14, 2 * 3.14, 3)
    else:
        pygame.draw.arc(screen, BLACK, (x - 25, y + 10, 50, 30), 0, 3.14, 3)

# Lanzar los hilos
for i in range(NUM_HILOS):
    t = threading.Thread(target=hilo_trabajo, args=(i,))
    t.start()

# Bucle principal
running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Dibujar una cara por hilo
    for i in range(NUM_HILOS):
        estado = hilos_estado[i]["trabajando"]
        dibujar_cara(posiciones[i], feliz=estado)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
