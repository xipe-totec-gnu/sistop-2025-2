import threading
import sys
import time
import curses
from curses import wrapper
from sincronizacion_proyecto import (
    crearTrabajo,
    estado_miembros,
    miembro,
    miembros_totales,
    planificador,
    tareas_pendientes,
    trabajos,
    trabajos_totales
)

evento_cierre = threading.Event()

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
    y_miembros = 4 + trabajos_totales

    stdscr.addstr(y_miembros, 0, "ESTADO DE LOS MIEMBROS:", curses.A_UNDERLINE)
    for miembro_id, estado in estado_miembros.items():
        y = y_miembros + 1 + miembro_id
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
    curses.curs_set(0)
    stdscr.nodelay(1)

    while not evento_cierre.is_set():
        try:
            actualizar_pantalla(stdscr, trabajos, estado_miembros)
            time.sleep(0.1)

            # Si se presiona 'q', establecer el evento de cierre
            if stdscr.getch() == ord('q'):
                evento_cierre.set()
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

    # Forzar la salida del programa
    sys.exit(0)

if __name__ == '__main__':
    wrapper(main)
