from tkinter import *
import threading


mutex=threading.Semaphore(1) # sirve para que se suban en orden
mutexbaja=threading.Semaphore(0) # sirve para que se bajen en la estacion correcta

#variables de lugares
asientoM=6
asientoR=2
asientoT=4
dePieH=2
dePieM=2
EstaciónCamion=0

def mujer(baja):
    global asientoM,asientoT,dePieH,dePieM
    mutex.acquire()
    if asientoM>0:
        asientoM -= 1
        lugarUtilizado=1
        print("se sienta en un asiento de mujer")
    elif asientoT>0:
        asientoT-=1
        lugarUtilizado=2
        print("se sienta en un asiento de todos")        
    elif dePieM>0:
        dePieM -= 1
        lugarUtilizado=4
        print("se va de pie en la seccion de mujeres")
    elif dePieH>0:
        dePieH -= 1
        lugarUtilizado=3
        print("se va de pie en la seccion de todos")
    else:
        print("No se sube va lleno")
        baja=20
    mutex.release()
    if baja!=20:
        bajar(baja,lugarUtilizado)

def mujerMayor(baja):
    global asientoM,asientoR,asientoT
    mutex.acquire()
    if asientoR>0:
        asientoR -= 1
        lugarUtilizado=0
        print("se sienta en un asiento reservado")
    elif asientoM>0:
        asientoM -= 1
        lugarUtilizado=1
        print("se sienta en un asiento de mujer")
    elif asientoT>0:
        asientoT-=1
        lugarUtilizado=2
        print("se sienta en un asiento de todos")
    else:
        print("No se sube va lleno")
        baja=20
    mutex.release()
    if baja!=20:
        bajar(baja,lugarUtilizado)

def hombre(baja):
    global asientoT,dePieH
    mutex.acquire()
    if asientoT>0:
        asientoT-=1
        lugarUtilizado=2
        print("se sienta en un asiento de todos")
    elif dePieH>0:
        dePieH -= 1
        lugarUtilizado=3
        print("se va de pie en la seccion de todos")
    else:
        print("No se sube va lleno")
        baja=20
    mutex.release()
    if baja!=20:
        bajar(baja,lugarUtilizado)

def hombreMayor(baja):
    global asientoR,asientoT
    mutex.acquire()
    if asientoR>0:
        asientoR -= 1
        lugarUtilizado=0
        print("se sienta en un asiento de mujer")
    elif asientoT>0:
        asientoT-=1
        lugarUtilizado=1
        print("se sienta en un asiento de todos")
    else:
        print("No se sube va lleno")
        baja=20
    mutex.release()
    if baja!=20:
        bajar(baja,lugarUtilizado)
    

def bajar(baja,lugarUtilizado):
    global EstaciónCamion,asientoM,asientoR,asientoT,dePieH,dePieM
    for i in range(5):
        mutexbaja.acquire()
        if baja == EstaciónCamion:
            print("se bajo")
            mutex.acquire()
            if lugarUtilizado==0:
                asientoR+=1
            elif lugarUtilizado==1:
                asientoM+=1
            elif lugarUtilizado==2:
                asientoT+=1
            elif lugarUtilizado==3:
                dePieH+=1
            elif lugarUtilizado==4:
                dePieM+=1
            mutex.release()
            break;
        mutexbaja.release()
    mutexbaja.release()
        
def avanzar():
    global EstaciónCamion
    EstaciónCamion += 1
    mutexbaja.release()

def pantallaInicio():
    #Canvas donde se dibuja la app
    canvas = Canvas( window, bg = "#FFFFFF", height = 700, width = 980 )
    canvas.place(x = 0, y = 0)

    #Titulo
    canvas.create_rectangle( 0.0, 0.0, 980.0, 91.0, fill="#121E9C", outline="")
    canvas.create_text(327.0, 24.0, anchor="nw", text="Trolebus", fill="#FFFFFF", font=("Kodchasan Bold", 48 * -1))
    #rectangulo del camion
    canvas.create_rectangle( 658.0, 107.0, 945.0, 671.0, fill="#3999FC", outline="")
    #rectangulo asientos y conductor
    
    #asiento conductor
    canvas.create_rectangle(878.0, 599.0, 919.0, 638.0, fill="#D9D9D9", outline="")
    #asiento reservado
    canvas.create_rectangle(878.0, 520.0, 918.0, 560.0, fill="#88BB69", outline="")
    canvas.create_rectangle(702.0, 520.0, 742.0, 560.0, fill="#88BB69", outline="")
    #asiento todos
    canvas.create_rectangle(702.0, 445.0, 742.0, 480.0, fill="#D9D9D9", outline="")
    canvas.create_rectangle(702.0, 375.0, 742.0, 410.0, fill="#D9D9D9", outline="")
    canvas.create_rectangle(878.0, 375.0, 918.0, 410.0, fill="#D9D9D9", outline="")
    canvas.create_rectangle(878.0, 445.0, 918.0, 480.0, fill="#D9D9D9", outline="")
    #asiento mujer
    canvas.create_rectangle(702.0, 290.0, 742.0, 330.0, fill="#FF93C7", outline="")
    canvas.create_rectangle(878.0, 290.0, 918.0, 330.0, fill="#FF93C7", outline="")
    canvas.create_rectangle(702.0, 205.0, 742.0, 245.0, fill="#FF93C7", outline="")
    canvas.create_rectangle(878.0, 205.0, 918.0, 245.0, fill="#FF93C7", outline="")
    canvas.create_rectangle(702.0, 120.0, 742.0, 160.0, fill="#FF93C7", outline="")
    canvas.create_rectangle(878.0, 120.0, 918.0, 160.0, fill="#FF93C7", outline="")
    # bolita conductor
    canvas.create_oval(888.0, 605.0, 910.0, 633.0, fill="#000000", outline="")

def threadMujer(baja):
    s1 = threading.Thread(target=mujerMayor,args=(baja,))
    s1.start()
    
def botones():
    button_1 = Button(text="Hombre Mayor", borderwidth=0,
                      highlightthickness=0, command=lambda: print("button_1 clicked"),
                      relief="flat", font=("Ariel", 32))
    button_1.place(    x=40.0,    y=117.0,    width=410.0,    height=111.0)

    button_2 = Button(text="Hombre", borderwidth=0,
                      highlightthickness=0, command=lambda: print("button_2 clicked"),
                      relief="flat", font=("Ariel", 32))
    button_2.place(    x=40.0,    y=259.0,    width=410.0,    height=111.0)

    button_3 = Button(text="MujerMayor", borderwidth=0,
                      highlightthickness=0, command=lambda: print("button_3 clicked"),
                      relief="flat", font=("Ariel", 32))
    button_3.place(    x=40.0,    y=415.0,    width=410.0,    height=111.0)

    button_4 = Button(text="Mujer", borderwidth=0,
                      highlightthickness=0, command=lambda: threadMujer(),
                      relief="flat", font=("Ariel", 32))
    button_4.place(x=40.0, y=560.0, width=410.0, height=55.0)

    button_5 = Button(text="Avanza", borderwidth=0,
                      highlightthickness=0, command=lambda: print("button_5 clicked"),
                      relief="flat", font=("Ariel", 32))
    button_5.place(x=40.0, y=633.0, width=410.0, height=55.0)
    

window = Tk() #instantiate an instance of a window
window.geometry("980x700")
window.title("Trolebus")
pantallaInicio()
botones()
