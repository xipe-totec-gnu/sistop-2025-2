from tkinter import *
import threading


mutex=threading.Semaphore(1) # sirve para que se suban en orden
mutexbaja=threading.Semaphore(0) # sirve para que se bajen en la estacion correcta
mutexPantalla=threading.Semaphore(1)
#variables de lugares
asientoM=6
asientoR=2
asientoT=4
dePieH=2
dePieM=2
EstacionCamion=0
xUsuario=888.0
yUsuario=605.0
xUsuarioFin=910.0
yUsuarioFin=633.0
listaAsientosReservados=[0,0]
listaAsientosTodos=[0,0,0,0]
listaAsientosMujer=[0,0,0,0,0,0]
listaDePieHombres=[0,0]
listaDePieMujeres=[0,0]

#hombre='#C41111'
#hombreMayor='#0f6307'
#Mujer='#2600FF'
#MujerMayor='#FFBB00'
color='#000000'
def mujer(baja):
    global asientoM,asientoT,dePieH,dePieM,color
    mutex.acquire()
    if asientoM>0:
        asientoM -= 1
        lugarUtilizado=6
        print("se sienta en un asiento de mujer")
        color='#2600FF'
        for i in range(6):
            if listaAsientosMujer[i]==0:
                listaAsientosMujer[i]=1
                asientosMujer(i)
                lugarUtilizado+=i
                break
        window.after(0, persona())
    elif asientoT>0:
        asientoT-=1
        lugarUtilizado=2
        for i in range(4):
            if listaAsientosTodos[i]==0:
                listaAsientosTodos[i]=1
                asientosTodos(i)
                lugarUtilizado+=i
                break
        color='#2600FF'
        window.after(0, persona())
        print("se sienta en un asiento de todos")        
    elif dePieM>0:
        dePieM -= 1
        lugarUtilizado=12
        color='#2600FF'
        for i in range(2):
            if listaDePieMujeres[i]==0:
                listaDePieMujeres[i]=1
                dePieMujer(i)
                lugarUtilizado+=i
                break
        window.after(0, persona())
        print("se va de pie en la seccion de mujeres")
    elif dePieH>0:
        dePieH -= 1
        lugarUtilizado=14
        color='#2600FF'
        for i in range(2):
            if listaDePieHombres[i]==0:
                print('dentro if')
                listaDePieHombres[i]=1
                dePieHombre(i)
                lugarUtilizado+=i
                break
        window.after(0, persona())
        print("se va de pie en la seccion de todos")
    else:
        print("No se sube va lleno")
        baja=20
    mutex.release()
    if baja!=20:
        bajar(baja,lugarUtilizado)

def mujerMayor(baja):
    global asientoM,asientoR,asientoT,color
    mutex.acquire()
    if asientoR>0:
        asientoR -= 1
        lugarUtilizado=0
        print("se sienta en un asiento reservado")
        for i in range(2):
            if listaAsientosReservados[i]==0:
                listaAsientosReservados[i]=1
                asientosReservados(i)
                lugarUtilizado+=i
                break
        color='#FFBB00'
        window.after(0, persona())
    elif asientoM>0:
        asientoM -= 1
        lugarUtilizado=6
        color='#FFBB00'
        for i in range(6):
            if listaAsientosMujer[i]==0:
                listaAsientosMujer[i]=1
                asientosMujer(i)
                lugarUtilizado+=i
                break
        window.after(0, persona())

        print("se sienta en un asiento de mujer")
    elif asientoT>0:
        asientoT-=1
        lugarUtilizado=2
        color='#FFBB00'
        for i in range(4):
            if listaAsientosTodos[i]==0:
                listaAsientosTodos[i]=1
                asientosTodos(i)
                lugarUtilizado+=i
                break
        window.after(0, persona())
        print("se sienta en un asiento de todos")
    else:
        print("No se sube va lleno")
        baja=20
    mutex.release()
    if baja!=20:
        bajar(baja,lugarUtilizado)

def hombre(baja):
    print(baja)
    global asientoT,dePieH,color
    mutex.acquire()
    if asientoT>0:
        asientoT-=1
        lugarUtilizado=2
        print("se sienta en un asiento de todos")
        color='#C41111'
        for i in range(4):
            if listaAsientosTodos[i]==0:
                listaAsientosTodos[i]=1
                asientosTodos(i)
                lugarUtilizado+=i
                break
        window.after(0, persona())

    elif dePieH>0:
        dePieH -= 1
        lugarUtilizado=14
        color='#C41111'
        for i in range(2):
            print('si llega al for')
            if listaDePieHombres[i]==0:
                print('si llega al if')
                listaDePieHombres[i]=1
                dePieHombre(i)
                lugarUtilizado+=i
                break
        window.after(0, persona())
        print("se va de pie en la seccion de todos")
    else:
        print("No se sube va lleno")
        baja=20
    mutex.release()
    if baja!=20:
        bajar(baja,lugarUtilizado)

def hombreMayor(baja):
    global asientoR,asientoT,color
    mutex.acquire()
    if asientoR>0:
        asientoR -= 1
        lugarUtilizado=0
        for i in range(2):
            if listaAsientosReservados[i]==0:
                listaAsientosReservados[i]=1
                asientosReservados(i)
                lugarUtilizado+=i
                break
        color='#0F6307'
        window.after(0, persona())
        print("se sienta en un asiento RESERVADO")
    elif asientoT>0:
        asientoT-=1
        lugarUtilizado=2
        color='#0F6307'
        for i in range(4):
            if listaAsientosTodos[i]==0:
                listaAsientosTodos[i]=1
                asientosTodos(i)
                lugarUtilizado+=i
                break
        window.after(0, persona())
        print("se sienta en un asiento de todos")
    else:
        print("No se sube va lleno")
        baja=20
    mutex.release()
    if baja!=20:
        bajar(baja,lugarUtilizado)
    

def bajar(baja,lugarUtilizado):
    global EstacionCamion,asientoM,asientoR,asientoT,dePieH,dePieM,color
    for i in range(5):
        print('se forma',i)
        mutexbaja.acquire()
        if baja == EstacionCamion:
            print("se bajo")
            mutex.acquire()
            if lugarUtilizado<2:
                asientoR+=1
                listaAsientosReservados[lugarUtilizado]=0
                color='#88BB69'
                asientosReservados(lugarUtilizado)
                window.after(0, persona())
                
            elif lugarUtilizado<6:
                asientoT+=1
                listaAsientosTodos[lugarUtilizado-2]=0
                color='#D9D9D9'
                asientosTodos(lugarUtilizado-2)
                window.after(0, persona())
                
            elif lugarUtilizado<12:
                asientoM+=1
                listaAsientosMujer[lugarUtilizado-6]=0
                color='#FF93C7'
                asientosMujer(lugarUtilizado-6)
                window.after(0, persona())
            elif lugarUtilizado<14:
                dePieM+=1
                listaDePieMujeres[lugarUtilizado-12]=0
                color='#3999FC'
                dePieMujer(lugarUtilizado-12)
                window.after(0, persona())
            else:
                dePieH+=1
                listaDePieHombres[lugarUtilizado-14]=0
                color='#3999FC'
                dePieHombre(lugarUtilizado-14)
                window.after(0, persona())
            print('no entra')
            mutex.release()
            break;
        mutexbaja.release()
            
    
        
def avanzar():
    global EstacionCamion
    EstacionCamion += 1
    mutexbaja.release()

def pantallaInicio():
    #Canvas donde se dibuja la app

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
    s1 = threading.Thread(target=mujer,args=(baja,))
    s1.start()
def threadHombre(baja):
    s1 = threading.Thread(target=hombre,args=(baja,))
    s1.start()
def threadMujerMayor(baja):
    s1 = threading.Thread(target=mujerMayor,args=(baja,))
    s1.start()    
def threadHombreMayor(baja):
    s1 = threading.Thread(target=hombreMayor,args=(baja,))
    s1.start()
    
    

    
def botones():
    global var
    button_1 = Button(text="Hombre Mayor", borderwidth=0,
                      highlightthickness=0, command=lambda: threadHombreMayor(int(var.get()),),
                      relief="flat", font=("Ariel", 32))
    button_1.place(    x=40.0,    y=117.0,    width=410.0,    height=111.0)

    button_2 = Button(text="Hombre", borderwidth=0,
                      highlightthickness=0, command=lambda: threadHombre(int(var.get()),),
                      relief="flat", font=("Ariel", 32))
    button_2.place(    x=40.0,    y=259.0,    width=410.0,    height=111.0)

    button_3 = Button(text="MujerMayor", borderwidth=0,
                      highlightthickness=0, command=lambda: threadMujerMayor(int(var.get()),),
                      relief="flat", font=("Ariel", 32))
    button_3.place(    x=40.0,    y=415.0,    width=410.0,    height=111.0)

    button_4 = Button(text="Mujer", borderwidth=0,
                      highlightthickness=0, command=lambda: threadMujer(int(var.get()),),
                      relief="flat", font=("Ariel", 32))
    button_4.place(x=40.0, y=560.0, width=410.0, height=55.0)

    button_5 = Button(text="Avanza", borderwidth=0,
                      highlightthickness=0, command=lambda: avanzar(),
                      relief="flat", font=("Ariel", 32))
    button_5.place(x=40.0, y=633.0, width=410.0, height=55.0)
    
def menudesplegable():
    global var
    var = StringVar(window)  # Crear una StringVar asociada con la ventana
    var.set(1)  # Establecer el valor inicial de la variable
    opciones = [1, 2, 3, 4, 5]  # Las opciones del menú desplegable
    opcion= OptionMenu(window, var, *opciones)  # Crear el menú desplegable
    opcion.config(width=3)  # Configurar el ancho del menú
    opcion.pack(side="top", anchor="w", pady=30, ipadx=20,padx=100)

def persona():
    global xUsuario,yUsuario,xUsuarioFin,yUsuarioFin
    canvas.create_oval(xUsuario,yUsuario,xUsuarioFin,yUsuarioFin, fill=color, outline="")

def asientosReservados(i):
    global xUsuario,yUsuario,xUsuarioFin,yUsuarioFin
    print(listaAsientosReservados, i)
    xUsuario=710.0+180*i
    yUsuario=525.0
    xUsuarioFin=730+180*i
    yUsuarioFin=555.0


def asientosTodos(i):
    global xUsuario,yUsuario,xUsuarioFin,yUsuarioFin
    xUsuario=710.0+180*(i%2)
    yUsuario=375.0+70*(i//2)
    xUsuarioFin=730+180*(i%2)
    yUsuarioFin=410.0+70*(i//2)
    
def asientosMujer(i):
    global xUsuario,yUsuario,xUsuarioFin,yUsuarioFin
    xUsuario=710.0+180*(i%2)
    yUsuario=120.0+85*(i//2)
    xUsuarioFin=730+180*(i%2)
    yUsuarioFin=160.0+85*(i//2)


def dePieHombre(i):
    global xUsuario,yUsuario,xUsuarioFin,yUsuarioFin
    xUsuario=800.0
    yUsuario=415+80*i
    xUsuarioFin=820.0
    yUsuarioFin=445+80*i
        
def dePieMujer(i):
    global xUsuario,yUsuario,xUsuarioFin,yUsuarioFin
    xUsuario=800.0
    yUsuario=175+90*i
    xUsuarioFin=820.0
    yUsuarioFin=205+90*i
    
            
window = Tk() #instantiate an instance of a window
window.geometry("980x700")
window.title("Trolebus")
canvas = Canvas( window, bg = "#FFFFFF", height = 700, width = 980 )
canvas.place(x = 0, y = 0)
pantallaInicio()
botones()
menudesplegable()
window.mainloop()

