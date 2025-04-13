import tkinter as tk
from tkinter import ttk
import threading
import time
import random

class CocinaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Proyecto - Uso de los quemadores")
        self.root.geometry("500x350")
        self.root.configure(bg="#98b7c9")

        # Estilo
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TLabel", font=("Cascadia Code", 12), padding=5)

        # Estado de los quemadores
        self.quemadores_status = tk.StringVar(value="Quemadores libres, ningún roomie está cocinando")
        self.quemadores_label = ttk.Label(
            self.root,
            textvariable=self.quemadores_status,
            font=("Cascadia Code", 12),
            background="#d3d3d3",
            anchor="center"
        )
        self.quemadores_label.pack(pady=15, ipadx=10, ipady=5)

        # Marco para personas
        self.personas_frame = ttk.Frame(self.root)
        self.personas_frame.pack(pady=10)

        # Lista de etiquetas de personas
        self.personas_labels = []

        # Semáforo para 4 quemadores
        self.quemadores = threading.Semaphore(4)

        # Iniciar hilos para cocinar
        self.iniciar_cocina()

    def add_persona(self, nombre):
        label = ttk.Label(self.personas_frame, text=f"{nombre} quiere cocinar", foreground="black")
        label.pack(pady=5, anchor="w")
        self.personas_labels.append(label)

    def cocinar(self, nombre, label):
        tiempo_espera = random.randint(7, 8)
        time.sleep(tiempo_espera)  # Simula espera

        label.config(text=f"{nombre} está esperando un quemador...")
        self.quemadores.acquire()

        self.toggle_quemadores(en_uso=True)
        label.config(text=f"{nombre} está cocinando")
        time.sleep(random.randint(7, 8))  # Simula cocinar

        label.config(text=f"{nombre} ha terminado de cocinar")
        self.quemadores.release()
        self.toggle_quemadores(en_uso=False)

    def toggle_quemadores(self, en_uso):
        if en_uso:
            self.quemadores_label.configure(background="#ff9999")
            self.quemadores_status.set("Los 4 quemadores están en uso")
        else:
            self.quemadores_label.configure(background="#77dd77")
            self.quemadores_status.set("Al menos hay un quemador libre")
        self.root.update_idletasks()

    def iniciar_cocina(self):
        nombres = ["Roomie 1", "Roomie 2", "Roomie 3", "Roomie 4", "Roomie 5", "Roomie 6"]
        for nombre in nombres:
            self.add_persona(nombre)
            label = self.personas_labels[-1]
            threading.Thread(target=self.cocinar, args=(nombre, label)).start()

# Ejecutar interfaz
if __name__ == "__main__":
    root = tk.Tk()
    app = CocinaApp(root)
    root.mainloop()
