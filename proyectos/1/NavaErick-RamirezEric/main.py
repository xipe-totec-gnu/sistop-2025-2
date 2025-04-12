from queue import PriorityQueue
from Gato import Gato, TipoGato
from Plato import Plato 
from Dispensador import Dispensador
import threading
import tkinter as tk
from PIL import Image, ImageTk
import sys

def main():
    #creando par de platos
    plato1 = Plato(1)
    plato2 = Plato(2)
    listaPlatos = [plato1, plato2]
    #cola para entrar a los platos
    colaGatos = PriorityQueue()
    #instanciando los gatos
    gatoMacho   = Gato("Kermit", TipoGato.MACHO     ,list(listaPlatos),colaGatos)
    gata1       = Gato("Violeta", TipoGato.HEMBRA  ,list(listaPlatos),colaGatos)
    gata2       = Gato("Luna", TipoGato.HEMBRA     ,list(listaPlatos),colaGatos  )
    gata3       = Gato("Zule", TipoGato.HEMBRA  ,list(listaPlatos),colaGatos)
    gata4       = Gato("Suiza", TipoGato.HEMBRA    ,list(listaPlatos),colaGatos)
    gatoInvasor = Gato("GatoInvasor", TipoGato.INVASOR,list(listaPlatos),colaGatos)
    gatos = [gatoMacho, gata1, gata2, gata3, gata4, gatoInvasor]

    
    
    #instanciando el dispensador con los platos
    dispensador = Dispensador(listaPlatos, gatos, colaGatos)



    # Interfaz gráfica
    ventana = tk.Tk()                                    #ventana de trabajo
    ventana.title("Proyecto 1, NavaErick-RamirezEric")                         #nombre ventana
    #cargando imagenes a la interfaz grafica
    dispensador_img = ImageTk.PhotoImage(Image.open("despenser.png").resize((150, 150)))  # Reemplaza con tu imagen
    gato_imgs = [ImageTk.PhotoImage(Image.open(f"{gato.nombre}.png").resize((100, 100))) for gato in gatos]  # Reemplaza con tus imágenes
     # Widgets de la interfaz
    label_dispensador = tk.Label(ventana, image=dispensador_img)       #para el dispensador
    label_dispensador.image = dispensador_img                           #imagen del dispensador
    label_dispensador.grid(row=1, column=0, columnspan=2, pady=10)      #ubicacion
    label_estado_dispensador = tk.Label(ventana, text="Estado: Cerrado")    #estado inicial
    label_estado_dispensador.grid(row=1, column=2, pady=10)                 #ubicacion del letrero

    ## para los gatos
    label_gatos = []            #gatos
    label_estados_gatos = []    #estado gatos
    for i, gato in enumerate(gatos):
        label_gato = tk.Label(ventana, image=gato_imgs[i]) #imagen de cada gato
        label_gato.image = gato_imgs[i]                    #imagen de cada gato
        label_gato.grid(row=3, column=i, padx=10, pady=10) # posicion
        label_gatos.append(label_gato)                      #etiqueta del gato
        label_estado_gato = tk.Label(ventana, text=f"{gato.nombre}: {gato.estado.name}")#estado de cada gato
        label_estado_gato.grid(row=4, column=i, padx=10, pady=10)                       #posicion de la etiqueta de cada gato
        label_estados_gatos.append(label_estado_gato)                                   #colocando su estado al gato

    # Funciones de actualización
    def actualizar_estados():
        label_estado_dispensador.config(text=f"Estado: {dispensador.estado.name}")  #modificara el estado del dispensador
        for i, gato in enumerate(gatos):                                            #modificara el estado de cada gato
            label_estados_gatos[i].config(text=f"{gato.nombre}: {gato.estado.name}")
        ventana.after(1000, actualizar_estados)  # Actualizar cada segundo          

    # Botones de control
    def iniciar_simulacion():
        threading.Thread(target=dispensador.gestion, daemon=True).start() #hilo para la gestion de la cola en el dispensador
        threading.Thread(target=dispensador.run, daemon=True).start()       #hilo para el dispensador
        for gato in gatos:
            gato.start()                        #inciializacion de cada gato    
        actualizar_estados()                    #actualizacion de estados

    #metodo para sacar al gato invasor
    def Sacar_invasor():
        if not dispensador.cola.empty():
            prioridad, _, gato = dispensador.cola.get()
            if gato.tipo == TipoGato.INVASOR:
                print(f"Gato invasor {gato.nombre} sacado manualmente de la cola.") #quita de la cola al gato invasor
                dispensador.retiradaGatoInvasor()                                   #solicita el metodo para que vuelva a funcionar
            else:
                dispensador.cola.put((prioridad, _, gato)) #devuelve el gato a la cola en caso de que no sea invasor
                print("No hay gato invasor en la cabeza de la cola")
        
    #metodo al que accedera el boton de finalizar
    def cerrar_simulacion():
        ventana.destroy()   #destruye la ventana
        sys.exit()          #utilizara esto para detener los procesos de los hilos

    #logica de cada boton. Posicion, tecto y funcion a realizar al ser presionados
    boton_iniciar = tk.Button(ventana, text="Iniciar", command=iniciar_simulacion)
    boton_iniciar.grid(row=0, column=0, padx=10, pady=10)
    boton_pausar = tk.Button(ventana, text="Sacar_Gato", command=Sacar_invasor)
    boton_pausar.grid(row=0, column=1, padx=10, pady=10)
    boton_cerrar = tk.Button(ventana, text="Cerrar", command=cerrar_simulacion)
    boton_cerrar.grid(row=0, column=2, padx=10, pady=10)

    #loop para que la ventana no se cierre
    ventana.mainloop()
        
main()
