import pygame

def inicio(pantalla, fuente, ANCHO, ALTO):
    fondo = pygame.image.load("fondoChamps.png")  
    fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))

    corriendo = True
    while corriendo:
        pantalla.blit(fondo, (0, 0))  # Dibujar la imagen que vamos a ocupar de fondo

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False

        pygame.display.flip()


