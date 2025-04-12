import tkinter as tk
from tkinter import ttk
import subprocess
import threading
from collections import defaultdict

# Acciones posibles dentro de la cocina
acciones = ["preparar", "cocinar-olla", "cocinar-sarten", "microondas", "licuadora", "tostar", "lavar", "comer"]

# Diccionarios para almacenar las referencias a los Listbox de la GUI
esperando_labels = {}
activo_labels = {}

# Estado actual de cada roomie (accion y si está esperando o activo)
estado_roomies = defaultdict(lambda: {"accion": None, "estado": None})

proceso_java = None

def crear_columna(master, accion, color):
    """
    Crea una columna en la GUI para una acción específica,
    con dos listbox: uno para los que esperan y otro para los activos.
    """
    frame = tk.Frame(master, bg=color, padx=10, pady=10)
    frame.grid_columnconfigure(0, weight=1)

    titulo = tk.Label(frame, text=accion.upper(), font=("Helvetica", 10, "bold"), bg=color)
    titulo.pack()

    esperando_title = tk.Label(frame, text="🕓 Esperando:", bg=color, font=("Helvetica", 10, "italic"))
    esperando_title.pack(anchor="w")

    esperando_list = tk.Listbox(frame, height=6)
    esperando_list.pack(fill="both", expand=True)
    esperando_labels[accion] = esperando_list

    activo_title = tk.Label(frame, text="✅ Activo:", bg=color, font=("Helvetica", 10, "italic"))
    activo_title.pack(anchor="w")

    activo_list = tk.Listbox(frame, height=6)
    activo_list.pack(fill="both", expand=True)
    activo_labels[accion] = activo_list

    return frame

def actualizar_gui(evento, nombre, accion):
    """
    Actualiza los listbox y el estado del roomie según el evento recibido.
    Borra su estado anterior antes de agregarlo al nuevo.
    """
    estado_prev = estado_roomies[nombre]
    if estado_prev["accion"]:
        if estado_prev["estado"] == "esperando":
            esperando_labels[estado_prev["accion"]].delete(
                *[i for i, val in enumerate(esperando_labels[estado_prev["accion"]].get(0, tk.END)) if val == nombre]
            )
        elif estado_prev["estado"] == "activo":
            activo_labels[estado_prev["accion"]].delete(
                *[i for i, val in enumerate(activo_labels[estado_prev["accion"]].get(0, tk.END)) if val == nombre]
            )
    # Insertar el nombre en la lista adecuada según el nuevo evento
    if evento == "esperando":
        esperando_labels[accion].insert(tk.END, nombre)
    elif evento == "activo":
        activo_labels[accion].insert(tk.END, nombre)
    elif evento == "comiendo":
        activo_labels["comer"].insert(tk.END, nombre)

    estado_roomies[nombre] = {"accion": accion, "estado": evento}

def escuchar_java():
    """
    Lanza el proceso Java y escucha su salida en tiempo real.
    Cada línea que recibe representa un cambio de estado de un roomie.
    """
    global proceso_java
    proceso_java = subprocess.Popen(
        ["java", "-cp", ".", "CocinaCompartida"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    for linea in proceso_java.stdout:
        if linea is None:
            break
        linea = linea.strip()
        if linea.count(";") >= 2:
            estado, nombre, accion = linea.split(";", 2)
            ventana.after(0, actualizar_gui, estado, nombre, accion)

    # Cuando el proceso Java termina, se reactiva el botón de iniciar
    ventana.after(0, lambda: boton_iniciar.config(state="normal"))

def iniciar_simulador():
    """
    Inicia la simulación creando un hilo que corre el proceso Java.
    """
    boton_iniciar.config(state="disabled")  # Desactiva botón
    threading.Thread(target=escuchar_java, daemon=True).start()

def reiniciar_simulador():
    """
    Detiene el proceso Java si está corriendo y reinicia el estado de la GUI.
    """
    global proceso_java, estado_roomies

    if proceso_java:
        proceso_java.terminate()
        proceso_java = None

    for lista in esperando_labels.values():
        lista.delete(0, tk.END)
    for lista in activo_labels.values():
        lista.delete(0, tk.END)

    estado_roomies.clear()

    # Reactivar el botón de iniciar
    boton_iniciar.config(state="normal")

# Colores usados para diferenciar cada tipo de acción
colores = {
    "preparar": "#f2f2f2",
    "cocinar-olla": "#f28e8e",
    "cocinar-sarten": "#f28e8e",
    "microondas": "#a3c4f3",
    "licuadora": "#c3f7c3",
    "tostar": "#fcd5a8",
    "lavar": "#d0c4f7",
    "comer": "#ffffc1"
}

# Configuración general de la ventana principal
ventana = tk.Tk()
ventana.title("Simulador de Cocina Compartida")
ventana.geometry("1600x550")

contenedor = tk.Frame(ventana)
contenedor.pack(fill="both", expand=True)

# Crear una columna por cada acción en la interfaz
for i, accion in enumerate(acciones):
    frame = crear_columna(contenedor, accion, colores[accion])
    frame.grid(row=0, column=i, sticky="nsew", padx=5, pady=5)
    contenedor.grid_columnconfigure(i, weight=1)


# Botones para iniciar o reiniciar la simulación
frame_botones = tk.Frame(ventana)
frame_botones.pack(pady=10)

boton_iniciar = tk.Button(frame_botones, text="▶️ Iniciar Simulación", command=iniciar_simulador, bg="#4CAF50", fg="white", font=("Helvetica", 12))
boton_iniciar.grid(row=0, column=0, padx=10)

boton_reiniciar = tk.Button(frame_botones, text="🔄 Reiniciar", command=reiniciar_simulador, bg="#FF9800", fg="white", font=("Helvetica", 12))
boton_reiniciar.grid(row=0, column=1, padx=10)

ventana.mainloop()

