import pygame
import sys
from Planteamiento import botonAcerca 
from Inicio import inicio 

# Inicializar Pygame
pygame.init()

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
MORADO = (255, 111, 20)

# Configuración de pantalla
ANCHO, ALTO = 800, 500
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("TACOS EL CHAMPION")

# Fuente
fuente = pygame.font.SysFont(None, 30)

# Cargar imagen (reemplaza con tu archivo)
imagen = pygame.image.load("champsLogo.png")
imagen = pygame.transform.scale(imagen, (400, 200))

# Estado de la pantalla
pantalla_actual = "menu"  # Puede ser "menu" o "pantalla2"

# Tamaño de los botones
boton_ancho = 180
boton_alto = 50

# Posición de los botones centrados
botones_menu = {
    "INICIO": pygame.Rect((ANCHO - boton_ancho) // 2, 250, boton_ancho, boton_alto),
    "ACERCA DE": pygame.Rect((ANCHO - boton_ancho) // 2, 320, boton_ancho, boton_alto),
    "SALIR :(": pygame.Rect((ANCHO - boton_ancho) // 2, 390, boton_ancho, boton_alto),
}

# Bucle principal
corriendo = True
while corriendo:
    pantalla.fill(NEGRO)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            pos = evento.pos

            if pantalla_actual == "menu":
                for nombre, rect in botones_menu.items():
                    if rect.collidepoint(pos):
                        if nombre == "INICIO":
                            inicio(pantalla, fuente, ANCHO, ALTO)
                            pygame.quit()
                            sys.exit()
                        elif nombre == "ACERCA DE":
                            pantalla_actual = botonAcerca(pantalla, fuente, ANCHO, ALTO)  # Informacion del planteamiento del problema
                        elif nombre == "SALIR :(": # No quisieron probar y mejor se salen
                            corriendo = False

    # Dibujar según la pantalla actual (por las modificaciones que hacemos constantemente segun el boton que se aprieta)
    if pantalla_actual == "menu":
        # Mostrar imagen
        pantalla.blit(imagen, (ANCHO // 2 - imagen.get_width() // 2, 50))

        # Dibujar botones
        for nombre, rect in botones_menu.items():
            pygame.draw.rect(pantalla, MORADO, rect, border_radius=10)
            texto_boton = fuente.render(nombre, True, BLANCO)
            pantalla.blit(texto_boton, (rect.x + (rect.width - texto_boton.get_width()) // 2, rect.y + (rect.height - texto_boton.get_height()) // 2))

    pygame.display.flip()

pygame.quit()
sys.exit()
