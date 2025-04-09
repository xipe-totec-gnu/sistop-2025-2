import pygame
import sys
from Planteamiento import botonAcerca 
from Inicio import inicio 

# Inicializar Pygame
pygame.init()

# --- Colores ---
NEGRO = (0, 0, 0)

# --- Configuración de pantalla ---
ANCHO, ALTO = 800, 500
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("TACOS EL CHAMPION")

# --- Fuente base para otros elementos (no se usa en los botones con imagen) ---
fuente = pygame.font.SysFont(None, 30)

# --- Cargar logo principal y escalarlo ---
logo = pygame.image.load("champsLogo.png")
logo = pygame.transform.scale(logo, (500, 300))

# --- Configuración de botones ---
BOTON_ANCHO = 150
BOTON_ALTO = 60
espaciado = 5  # espacio vertical entre botones
x_centro = (ANCHO - BOTON_ANCHO) // 2  # Centrar horizontalmente
inicio_y = 250  # Coordenada Y inicial para el primer botón

# --- Cargar imágenes para cada botón en estado normal y hover ---
# Cada botón se representa como un diccionario con su imagen normal, hover y su rectángulo
botones = {
    "INICIO": {
        "normal": pygame.transform.scale(pygame.image.load("Inicio.png"), (BOTON_ANCHO, BOTON_ALTO)),
        "hover": pygame.transform.scale(pygame.image.load("InicioH.png"), (BOTON_ANCHO, BOTON_ALTO)),
        "rect": pygame.Rect(x_centro, inicio_y, BOTON_ANCHO, BOTON_ALTO)
    },
    "ACERCA DE": {
        "normal": pygame.transform.scale(pygame.image.load("Acerca.png"), (BOTON_ANCHO, BOTON_ALTO)),
        "hover": pygame.transform.scale(pygame.image.load("AcercaH.png"), (BOTON_ANCHO, BOTON_ALTO)),
        "rect": pygame.Rect(x_centro, inicio_y + BOTON_ALTO + espaciado, BOTON_ANCHO, BOTON_ALTO)
    },
    "SALIR :(": {
        "normal": pygame.transform.scale(pygame.image.load("Salir.png"), (BOTON_ANCHO, BOTON_ALTO)),
        "hover": pygame.transform.scale(pygame.image.load("SalirH.png"), (BOTON_ANCHO, BOTON_ALTO)),
        "rect": pygame.Rect(x_centro, inicio_y + 2 * (BOTON_ALTO + espaciado), BOTON_ANCHO, BOTON_ALTO)
    }
}

# Estado actual de la pantalla (cambiamos entre 2 pantallas cuando se selecciona la opcion 'INFO')
pantalla_actual = "menu"

# --- Bucle principal ---
corriendo = True
while corriendo:
    pantalla.fill(NEGRO)  # Fondo negro
    mouse_pos = pygame.mouse.get_pos()  # Obtener posición actual del mouse

    # Manejo de eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False

        elif evento.type == pygame.MOUSEBUTTONDOWN:
            # Verificar si se hizo clic en algún botón
            for nombre, datos in botones.items():
                if datos["rect"].collidepoint(evento.pos):
                    if nombre == "INICIO":
                        inicio(pantalla, fuente, ANCHO, ALTO)
                        pygame.quit()
                        sys.exit()
                    elif nombre == "ACERCA DE":
                        pantalla_actual = botonAcerca(pantalla, fuente, ANCHO, ALTO)
                    elif nombre == "SALIR :(":
                        corriendo = False

    # Si estamos en el menú principal
    if pantalla_actual == "menu":
        # Mostrar el logo centrado en la parte superior
        pantalla.blit(logo, (ANCHO // 2 - logo.get_width() // 2, 0))

        # Dibujar los botones con sus respectivas imágenes (hover o normal)
        for nombre, datos in botones.items():
            imagen = datos["hover"] if datos["rect"].collidepoint(mouse_pos) else datos["normal"]
            pantalla.blit(imagen, datos["rect"].topleft)

    # Actualizar pantalla
    pygame.display.flip()

# Salir correctamente del programa
pygame.quit()
sys.exit()
