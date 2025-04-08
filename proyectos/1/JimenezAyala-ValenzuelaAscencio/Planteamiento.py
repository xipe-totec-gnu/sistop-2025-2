import pygame

def botonAcerca(pantalla, fuente, ANCHO, ALTO):
    # Botón de regresar
    boton_volver = pygame.Rect((ANCHO - 100) // 2, 400, 100, 40)

    corriendo = True
    while corriendo:
        pantalla.fill((0, 0, 0))  

        texto = fuente.render("Planteamiento del problema:", True, (255, 255, 255))
        pantalla.blit(texto, (ANCHO // 2 - texto.get_width() // 2, 150))

        # Información del planteamiento
        texto_info = fuente.render("Ayuda me dio una diarrea nuclear por los tacos del champs D:", True, (255, 255, 255))
        pantalla.blit(texto_info, (ANCHO // 2 - texto_info.get_width() // 2, 200))

        # Dibujar el botón de "Volver"
        pygame.draw.rect(pantalla, (100, 149, 237), boton_volver, border_radius=10)
        texto_volver = fuente.render("Volver", True, (0, 0, 0))
        pantalla.blit(texto_volver, (boton_volver.x + (boton_volver.width - texto_volver.get_width()) // 2, boton_volver.y + (boton_volver.height - texto_volver.get_height()) // 2))

        # Manejo de eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                pos = evento.pos
                if boton_volver.collidepoint(pos):
                    corriendo = False 
                    return "menu"  

        pygame.display.flip()

    return "menu"  # Si la pantalla se cierra de cualquier otra forma
