import threading
import time

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

s1 = threading.Thread(target=mujerMayor,args=(1,))
s1.start()
s1 = threading.Thread(target=mujerMayor,args=(1,))
s1.start()
s1 = threading.Thread(target=mujerMayor,args=(1,))
s1.start()
s1 = threading.Thread(target=mujerMayor,args=(1,))
s1.start()
s1 = threading.Thread(target=mujerMayor,args=(1,))
s1.start()
s1 = threading.Thread(target=mujerMayor,args=(1,))
s1.start()
s1 = threading.Thread(target=mujerMayor,args=(1,))
s1.start()
s1 = threading.Thread(target=mujerMayor,args=(1,))
s1.start()
s1 = threading.Thread(target=mujerMayor,args=(1,))
s1.start()
s1 = threading.Thread(target=mujerMayor,args=(1,))
s1.start()
s1 = threading.Thread(target=mujerMayor,args=(1,))
s1.start()
s1 = threading.Thread(target=mujerMayor,args=(1,))
s1.start()
s1 = threading.Thread(target=mujerMayor,args=(1,))
s1.start()
s1 = threading.Thread(target=mujerMayor,args=(1,))
s1.start()
s1 = threading.Thread(target=mujerMayor,args=(1,))
s1.start()
s1 = threading.Thread(target=mujerMayor,args=(1,))
s1.start()
s1 = threading.Thread(target=mujerMayor,args=(1,))
s1.start()
s1 = threading.Thread(target=mujerMayor,args=(1,))
s1.start()
s1 = threading.Thread(target=mujerMayor,args=(1,))
s1.start()
s1 = threading.Thread(target=mujerMayor,args=(1,))
s1.start()
s1 = threading.Thread(target=mujerMayor,args=(1,))
s1.start()
s1 = threading.Thread(target=mujerMayor,args=(1,))
s1.start()

s2 = threading.Thread(target=avanzar)
s2.start()
time.sleep(3)
s1 = threading.Thread(target=mujerMayor,args=(1,))
s1.start()
s1 = threading.Thread(target=mujerMayor,args=(1,))
s1.start()
s1.join()
s2.join()

print("Todos los hilos han terminado.")
