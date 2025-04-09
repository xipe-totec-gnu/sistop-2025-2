import pygame

def dividir_texto(texto, fuente, max_ancho):
    palabras = texto.split(' ')
    lineas = []
    linea_actual = ""

    for palabra in palabras:
        prueba_linea = linea_actual + palabra + " "
        if fuente.size(prueba_linea)[0] <= max_ancho:
            linea_actual = prueba_linea
        else:
            lineas.append(linea_actual)
            linea_actual = palabra + " "
    
    if linea_actual:
        lineas.append(linea_actual)
    
    return lineas

def botonAcerca(pantalla, fuente, ANCHO, ALTO):
    boton_volver = pygame.Rect((ANCHO - 100) // 2, ALTO - 80, 100, 40)

    # Tus párrafos separados
    parrafos = [
        "Somos dos estudiantes de la Facultad de Ingeniería y como muchos, "
        "tenemos una tradición sagrada: ir al puesto del champion a comer tacos de canasta."
        "El champion es ya una leyenda entre los pasillos: siempre está ahí, "
        "de 7 AM a 7PM, esperando a que los estudiantes lleguemos con hambre."
        "Este proyecto rinde homenaje a ese personaje que alimenta a generaciones con sabor y cariño."
        "Cada vez que vamos, el proceso es el mismo… o al menos debería serlo:",

        "Primero, nos acercamos al puesto y le pedimos al champion nuestros tacos favoritos (o su famosa "
        "tortichamps, una torta de tacos de canasta). Pero tenemos que esperar a que no haya nadie "
        "más pidiendo, porque el champion solo atiende a una persona a la vez.",

        "Si está disponible alguno de sus 3 platos, el champion nos puede servir nuestros tacos para empezar "
        "a comer. De otro modo, debemos esperar a que alguien termine."
        " Finalmente, hablamos con el champs para pagarle los tacos que consumimos. ",
    ]

    # Dividir cada párrafo en líneas que quepan
    lineas_por_parrafo = [dividir_texto(parrafo, fuente, ANCHO - 60) for parrafo in parrafos]

    corriendo = True
    while corriendo:
        pantalla.fill((0, 0, 0))  

        # Mostrar cada párrafo con salto entre ellos
        y = 30
        for lineas in lineas_por_parrafo:
            for linea in lineas:
                texto_render = fuente.render(linea, True, (255, 255, 255))
                pantalla.blit(texto_render, (30, y))
                y += fuente.get_linesize()
            y += fuente.get_linesize()  # espacio extra entre párrafos

        # Botón "Volver"
        pygame.draw.rect(pantalla, (100, 149, 237), boton_volver, border_radius=10)
        texto_volver = fuente.render("Volver", True, (0, 0, 0))
        pantalla.blit(texto_volver, (
            boton_volver.x + (boton_volver.width - texto_volver.get_width()) // 2,
            boton_volver.y + (boton_volver.height - texto_volver.get_height()) // 2
        ))

        # Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_volver.collidepoint(evento.pos):
                    corriendo = False 
                    return "menu"

        pygame.display.flip()

    return "menu"
