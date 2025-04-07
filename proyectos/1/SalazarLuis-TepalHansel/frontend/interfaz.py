import tkinter as tk
from tkinter import scrolledtext, messagebox
import sys
import os
# Add the parent directory of the 'backend' folder to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import queue 
import backend.sincronization as bs
import threading
import random
import time


class TiendaSprite:
    def __init__(self,canvas,leftUpperCorner,rightBottomCorner,base,diameter,dFromUpper):
        self.canvas=canvas
        self.leftUpperCorner=leftUpperCorner
        self.rightBottomCorner=rightBottomCorner
        self.base=base
        self.width=rightBottomCorner[0]-leftUpperCorner[0]
        self.height=rightBottomCorner[1]-leftUpperCorner[1]
        self.desplazamiento=self.width/2-self.base
        self.diameter=diameter
        self.dFromUpper=dFromUpper

    def build(self):
        workers=[]
        coords=[]
        self.canvas.create_rectangle(
                self.leftUpperCorner[0], self.leftUpperCorner[1],  # Esquina rightUpperCorner izquierda (x1, y1)
                self.rightBottomCorner[0], self.rightBottomCorner[1], # Esquina leftUpperCorner derecha (x2, y2)
                fill="white",  # Color de relleno
                outline="black",   # Color del borde
                width=2           # Grosor del borde
            )
        for i in range(bs.numWorkers):
            newX=self.leftUpperCorner[0]+self.base+self.desplazamiento*i-self.diameter/2
            newY=self.leftUpperCorner[1]+self.dFromUpper
            workers.append(
            self.canvas.create_oval(
                newX,newY,
                newX+self.diameter,newY+self.diameter,
                fill="white",  # Color de relleno
                outline="black",   # Color del borde
                width=2           # Grosor del borde
            ))
            coords.append([newX,newY,newX+self.diameter,newY+self.diameter])
        return workers,coords


class TiendaApp:
    def __init__(self, root):
        self.queries=queue.Queue()
        self.root = root
        self.workers=[]
        self.coords=[]
        self.canvas = tk.Canvas(root, width=400, height=300, bg="white")
        self.canvas.pack()
        #Título de la interfaz
        self.root.title("Simulación de Tienda - Pedidos Concurrentes")
        # Interfaz gráfica
        self.setup_ui()
        # Inicio de los trabajadores
        threading.Thread(target=self.inicio,args=[]).start()
        self.hearing()

    def inicio(self):
        for i in range(bs.numWorkers):
            threading.Thread(target=bs.workers, args=[i,self.queries,self.workers[i],self.canvas]).start()
        while True:
            threading.Thread(target=bs.alumnos, args=[self.queries,self.workers,self.canvas,self.coords]).start()


    def hearing(self):
        """Revisa periódicamente la cola y ejecuta las acciones en la UI."""
        try:
            #while True:  # Saca todos los disponibles
                task = self.queries.get_nowait()
                task.begin()  # Ejecuta el cambio en la UI (en el hilo principal)
        except queue.Empty:
            pass
        self.root.after(500, self.hearing)  # Vuelve a revisar en 100ms

    
    def setup_ui(self):
        # Frame principal
        frame = tk.Frame(self.root, padx=10, pady=10)
        frame.pack(fill=tk.BOTH, expand=True)
        # Título
        tk.Label(frame, text="🏪 Simulación de Don Rata", font=("Arial", 16)).pack(pady=5)

        tienda=TiendaSprite(canvas=self.canvas,leftUpperCorner=(50,50),rightBottomCorner=(350,100),base=30,diameter=20,dFromUpper=20)
        self.workers,self.coords=tienda.build()
        
        # Botón para detener la simulación
        tk.Button(frame, text="Detener Simulación", command=self.detener_simulacion).pack(pady=5)
    
    
    def detener_simulacion(self):
        """Detiene la simulación y cierra la aplicación."""
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = TiendaApp(root)
    root.mainloop()