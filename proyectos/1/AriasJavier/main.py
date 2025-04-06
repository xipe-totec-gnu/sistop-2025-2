import threading
import time
import curses
from curses import wrapper
from sincronizacion_proyecto import planificador, crearTrabajo, trabajos, tareas_pendientes, miembro, estado_miembros

trabajos_totales = 6
miembros_totales = 2

def actualizar_pantalla(stdscr, trabajos, estado_miembros):
    stdscr.clear()

    # Mostrar título
    stdscr.addstr(0, 0, "SISTEMA DE GESTIÓN DE TAREAS", curses.A_BOLD)

    # Mostrar estado de los trabajos
    stdscr.addstr(2, 0, "ESTADO DE LOS TRABAJOS:", curses.A_UNDERLINE)
    for trabajo in trabajos:
        y = 3 + trabajo['id']
        # Contar tareas completadas
        completadas = sum(1 for tarea in trabajo['tareas'] if tarea['estado'] == "completado")
        total = len(trabajo['tareas'])
        stdscr.addstr(y, 2, f"Trabajo {trabajo['id']}: {completadas}/{total} tareas completadas")

        # Mostrar detalles de las tareas
        for j, tarea in enumerate(trabajo['tareas']):
            estado_symbol = "✓" if tarea['estado'] == "completado" else "⧖" if tarea['estado'] == "pendiente" else "□"
            stdscr.addstr(y, 40 + j*8, f"T{tarea['id']}[{estado_symbol}]")

    # Mostrar estado de los miembros
    stdscr.addstr(4 + trabajos_totales, 0, "ESTADO DE LOS MIEMBROS:", curses.A_UNDERLINE)
    for miembro_id, estado in estado_miembros.items():
        y = 5 + trabajos_totales + miembro_id
        if estado:
            stdscr.addstr(y, 2, f"Miembro {miembro_id}: Trabajando en Tarea {estado['id']} del Trabajo {estado['id_trabajo']}")
        else:
            stdscr.addstr(y, 2, f"Miembro {miembro_id}: Esperando")

    y_tareas = 6 + trabajos_totales + miembros_totales
    # Mostrar tareas pendientes
    stdscr.addstr(y_tareas, 0, "TAREAS PENDIENTES:", curses.A_UNDERLINE)
    for i, tarea in enumerate(tareas_pendientes):
        stdscr.addstr(y_tareas + 1 + i, 2, f"Tarea {tarea['id']} del Trabajo {tarea['id_trabajo']}")

    stdscr.refresh()

def pantalla_principal(stdscr):
    # Configuración inicial de curses
    curses.curs_set(0)
    stdscr.nodelay(1)

    while True:
        try:
            actualizar_pantalla(stdscr, trabajos, estado_miembros)
            # Actualizar cada 100ms
            time.sleep(0.1)

            # Salir si se presiona 'q'
            if stdscr.getch() == ord('q'):
                break
        except:
            break

def main(stdscr):
    for i in range(trabajos_totales):
        crearTrabajo(i)

    # Iniciar hilos
    threads = []
    for i in range(miembros_totales):
        t = threading.Thread(target=miembro, args=[i])
        t.daemon = True
        t.start()
        threads.append(t)

    t = threading.Thread(target=planificador)
    t.daemon = True
    t.start()
    threads.append(t)

    # Iniciar interfaz
    pantalla_principal(stdscr)

if __name__ == '__main__':
    wrapper(main)
