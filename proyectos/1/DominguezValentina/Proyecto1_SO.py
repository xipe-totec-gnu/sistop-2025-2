import threading
import time
import random
from tkinter import *

companero1 = threading.Semaphore(1)
comp_labels = {}  # clave: id_auto, valor: Label

def mostrar(id_companero):
    color = random.randint(1, 5)
    imagenes = {
        1: "lucham.png",
        2: "luchaa.png",
        3: "luchav.png",
        4: "luchan.png",
        5: "luchaam.png"
    }

    img_path = imagenes[color]
    imagen = PhotoImage(file=img_path)
    label = Label(MiFrame, image=imagen)
    label.image = imagen
    label.place(x=900 - (id_companero * 300), y=50)
    comp_labels[id_companero] = label  

def eliminar(id_companero):
    if id_companero in comp_labels:
        comp_labels[id_companero].destroy()  # Elimina el widget completamente
        del comp_labels[id_companero]        # Borra del diccionario

def avanzar(id_companero):
    nuevo_id = id_companero - 1
    if nuevo_id <= 0:
        return  

    label = comp_labels.get(id_companero)
    if label:
        x_nuevo = 900 - (nuevo_id * 300)
        label.place(x=x_nuevo, y=50)
        comp_labels[nuevo_id] = label
        del comp_labels[id_companero]

def proyeccion(id_companero):
    print(f"Compañero {id_companero} llega a ser proyectado.")
    raiz.after(0, mostrar, id_companero)

    with companero1:
        print(f"Compañero {id_companero} está siendo proyectado...")

        # Crear y mostrar la imagen de lucha en el hilo principal
        def mostrar_lucha():
            global label_lucha
            lucha = PhotoImage(file="lucha.png")
            label_lucha = Label(MiFrame, image=lucha)
            label_lucha.image = lucha
            label_lucha.place(x=600, y=50)

            label_companero1.config(image='')  # Limpia imagen estática
            label_companero1.image = None

        raiz.after(0, mostrar_lucha)
        raiz.after(0, eliminar, id_companero)

        # Espera simulando la duración de la proyección
        time.sleep(random.uniform(2, 7))

        # Eliminar la imagen de lucha después
        def finalizar_lucha():
            label_lucha.destroy()
            print(f"A Compañero {id_companero} lo tiran y se va.")

            comp_restantes = list(comp_labels.keys())
            for otro_id in comp_restantes:
                raiz.after(0, eliminar, otro_id)
                raiz.after(100, avanzar, otro_id)

        raiz.after(0, finalizar_lucha)

def iniciar_simulacion():
    comp = []
    for i in range(1, 6):
        hilo = threading.Thread(target=proyeccion, args=(i,))
        comp.append(hilo)
        hilo.start()
        time.sleep(random.uniform(0.5, 1.5))
    for hilo in comp:
        hilo.join()
    print("Se han terminado los compañeros.")

# --- Interfaz gráfica ---
raiz = Tk()
raiz.title("Proyecciones de Lucha")
raiz.resizable(False, False)
raiz.iconbitmap("logo.ico")
raiz.geometry("1000x500")

MiFrame = Frame(raiz, width=1000, height=500)
MiFrame.pack()

companero1i = PhotoImage(file="lucha1.png")
label_companero1 = Label(MiFrame, image=companero1i)
label_companero1.image = companero1i
label_companero1.place(x=600, y=50)

label_lucha = None  # Se define global para manipularla luego

boton = Button(MiFrame, text="Iniciar Proyecciones", command=lambda: threading.Thread(target=iniciar_simulacion).start())
boton.place(x=300, y=300)

raiz.mainloop()



