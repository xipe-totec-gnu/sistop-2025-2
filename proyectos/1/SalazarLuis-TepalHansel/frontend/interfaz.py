import tkinter as tk
from tkinter import scrolledtext, messagebox
import sys
import os
# Add the parent directory of the 'backend' folder to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import backend.sincronization as sinc
import threading
import queue
import random
import time

class alumnoSprite:
    contador=0
    def __init__(self,canvas,leftUpperCorner,rightBottomCorner):
        self.contador+=1
        self.setImage(canvas,leftUpperCorner,rightBottomCorner)
        self.colors=["red","yellow","blue","green","orange","purple"]

    def setImage(self,canvas,leftUpperCorner,rightBottomCorner):
        self.canvas=canvas
        self.leftUpperCorner=leftUpperCorner
        self.rightBottomCorner=rightBottomCorner
        self.width,self.height=tuple(rightBottomCorner[i]-leftUpperCorner[i] for i in range(len(leftUpperCorner)))
        self.widthHead=self.width
        self.heightHead=self.height/2
        self.circleLeftUpperCorner=self.leftUpperCorner
        self.circleRightBottomCorner=(self.leftUpperCorner[0]+self.widthHead,self.leftUpperCorner[1]+self.heightHead)
        self.widthBody=self.width
        self.heightBody=self.height-self.heightHead
        self.bodyLeftUpperCorner=(self.rightBottomCorner[0]-self.widthBody,self.rightBottomCorner[1]-self.heightBody)
        self.bodyRightBottomCorner=self.rightBottomCorner

    def build(self):
        self.canvas.create_oval(
            *self.circleLeftUpperCorner,
            *self.circleRightBottomCorner,
            fill="pink",
            outline="black",
            width=2
        )
        self.canvas.create_rectangle(
            *self.bodyLeftUpperCorner,
            *self.bodyRightBottomCorner,
            fill=self.colors[random.randint(0,len(self.colors)-1)],
            outline="black",
            width=2
        )
        centerX=(self.bodyLeftUpperCorner[0]+self.bodyRightBottomCorner[0])/2
        centerY=(self.bodyLeftUpperCorner[1]+self.bodyRightBottomCorner[1])/2
        self.canvas.create_text(
            centerX,centerY,
            text=f"{self.contador}",
            font=("Arial",10,"bold")
        )
        

class tiendaSprite:
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
        
        self.canvas.create_rectangle(
                self.leftUpperCorner[0], self.leftUpperCorner[1],  # Esquina rightUpperCorner izquierda (x1, y1)
                self.rightBottomCorner[0], self.rightBottomCorner[1], # Esquina leftUpperCorner derecha (x2, y2)
                fill="white",  # Color de relleno
                outline="black",   # Color del borde
                width=2           # Grosor del borde
            )
        for i in range(sinc.numWorkers):
            newX=self.leftUpperCorner[0]+self.base+self.desplazamiento*i-self.diameter/2
            newY=self.leftUpperCorner[1]+self.dFromUpper
            self.canvas.create_oval(
                newX,newY,
                newX+self.diameter,newY+self.diameter,
                fill="white",  # Color de relleno
                outline="black",   # Color del borde
                width=2           # Grosor del borde
            )

class TiendaApp:
    def __init__(self, root):
        self.root = root
        self.lights=[]
        #Título de la interfaz
        self.root.title("Simulación de Tienda - Pedidos Concurrentes")
        # Interfaz gráfica
        self.setup_ui()
        # Inicio de los trabajadores

        

    def log(self, mensaje):
        """Muestra un mensaje en el área de logs."""
        self.log_area.config(state="normal")
        self.log_area.insert(tk.END, mensaje + "\n")
        self.log_area.config(state="disabled")
        self.log_area.see(tk.END)  # Auto-scroll
    
    def setup_ui(self):
        # Frame principal
        frame = tk.Frame(self.root, padx=10, pady=10)
        frame.pack(fill=tk.BOTH, expand=True)
        #frame.pack(expand=True)
        # Título
        tk.Label(frame, text="🏪 Simulación de Don Rata", font=("Arial", 16)).pack(pady=5)
        
        canvas = tk.Canvas(root, width=400, height=300, bg="white")
        canvas.pack()

        tienda=tiendaSprite(canvas=canvas,leftUpperCorner=(50,50),rightBottomCorner=(350,100),base=30,diameter=20,dFromUpper=20)
        tienda.build()

        alumno=alumnoSprite(canvas=canvas,leftUpperCorner=(50,200),rightBottomCorner=(80,230))
        alumno.build()
                
        # Área de logs (para mostrar eventos)
        
        #self.log_area = scrolledtext.ScrolledText(frame, width=60, height=20, state="disabled")
        #self.log_area.pack(pady=10)
        
        # Botón para agregar cliente manualmente
        
        # Botón para detener la simulación
        tk.Button(frame, text="Detener Simulación", command=self.detener_simulacion).pack(pady=5)
    
    
    def detener_simulacion(self):
        """Detiene la simulación y cierra la aplicación."""
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = TiendaApp(root)
    root.mainloop()