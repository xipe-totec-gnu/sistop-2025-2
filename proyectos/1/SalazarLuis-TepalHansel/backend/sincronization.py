import threading
import time
import tkinter as tk
import random
import queue
numWorkers=3
contador=0
mutexContador=threading.Semaphore(1)
TrabajadorSleep=[threading.Semaphore(0) for _ in range(numWorkers)]
TrabajadorActivo=[threading.Semaphore(0) for _ in range(numWorkers)]
mutexAtendiendo=[threading.Semaphore(1) for _ in range(numWorkers)]
mutexAvailable=threading.Semaphore(1)
available=queue.Queue()


for i in range(numWorkers):
    available.put(i)

capacityAlumnos=threading.Semaphore(numWorkers)
verticalDes=10

class AlumnoSprite:
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
        

def workers(id,worker=None,canvas=None):
    while True:
        if __name__=="__main__":
            print(f"Soy el trabajador {id} y no tengo nada que hacer")
            TrabajadorSleep[id].acquire()
            print(f"Atendiendo {id}")
            TrabajadorActivo[id].acquire()


        else:
            canvas.itemconfig(worker,fill="white")
            #TrabajadorSleep[id].acquire()
            canvas.itemconfig(worker,fill="red")
        
def alumnos(workers=None,canvas=None):
    global verticalDes
    global available
    global contador
    with mutexContador:
        contador+=1
        idAlumno=contador
    
    if __name__=="__main__":
        idWorker=available.get(block=True,timeout=None)
        print(f"Es el turno de {idAlumno}, pasa a {idWorker}")

        #Pasa por algunas fases

        TrabajadorSleep[idWorker].release()
        print(f"{idAlumno} recibio su pedido")
        TrabajadorActivo[idWorker].release()
        print(f"Se libera {idWorker}")
        available.put(idWorker)

    else:
            #capacityAlumnos.acquire()
        with mutexAvailable:
            #idWorker=available.pop()
            idWorker=2
        with mutexAtendiendo[idWorker]:
            coords=canvas.coords(workers[idWorker])
            coords[1]+=verticalDes
            alumno=AlumnoSprite((coords[0],coords[1]),(coords[0]+20,coords[1]+20))
            alumno.build()
            print("Don Rata atiendame")
            with mutexAvailable:
                available.append(idWorker)
            #TrabajadorSleep[idWorker].release()

if __name__=="__main__":
    for i in range(numWorkers):
        threading.Thread(target=workers,args=[i]).start()
    while True:
        threading.Thread(target=alumnos,args=[]).start()
    


    

        



