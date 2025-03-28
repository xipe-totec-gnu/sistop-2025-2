import pygame, sys
import threading
import random
import time
pygame.init()


#-------------------Backend------------------------------------------
mutex=threading.Semaphore(1)    #mutex que evita la concurrencia en la variable al momento de formar hackers para subir al barco,
mutexSubir=threading.Semaphore(1)   # mutex que evita concurrencia al momento de subir al barco
hackerQ=threading.Semaphore(0) #Queue de Hackers que nos permite que suban en pares
serfQ=threading.Semaphore(0) #Queue de Serfs que nos permite que suban en pares
esperaH=0   #Variable que nos permite identificar si es el primer hacker o el segundo
esperaS=0 #Variable que nos permite identificar si es el primer serf o el segundo
total=1 #Variable que nos permite saber si la balsa esta llena
xSerf=455
xHacker=455
serfSube=430
hackerSube=430
ybarco=15
#-------------------Backend------------------------------------------



#------------------------GRAFICA---------------------------------
GREEN=(82, 166, 41)
BLUE=(70, 130, 180)
BROWN=(202,116,65)
size=(700,100)


def aguaReinicio():
    pygame.draw.rect(screen,BLUE,(450,0,250,100))
    pygame.draw.rect(screen,BROWN,(450,10,80,80))
    pygame.display.flip()
#------------------------GRAFICA---------------------------------

    
    
#-------------------Backend------------------------------------------
    #Al final del documento se presenta el código sin la parte gráfica para facilitar la evaluación.
    #Se agregaron Timesleep para poder apreciar la animación
def hacker():
    global esperaH, total, xHacker, hackerSube, ybarco
    #Las siguientes 3 lineas son para representar la llegada de un hacker
    xHacker-= 25
    screen.blit(hackerImage, [xHacker,15])  # Agrega a tux en la pantalla
    pygame.display.flip()
    #Mutex que evita la concurrencia al momento subir al barco
    mutex.acquire()  
    if esperaH>0: #Si es el segundo Hacker en formarse se suben al barco
        esperaH-=1
        hackerQ.release() #Libera la queue de Hacker para formar otro par
#print("Subio un Hacker\n") Esta parte del codigo es la animacion de subir a la balsa
        screen.blit(hackerImage, [460,ybarco])
        pygame.draw.rect(screen,GREEN,(hackerSube,15,20,24))
        hackerSube-=25
        pygame.display.flip()
        time.sleep(0.3)
        screen.blit(hackerImage, [490,ybarco])
        pygame.draw.rect(screen,GREEN,(hackerSube,15,20,24))
        hackerSube-=25
        pygame.display.flip()
        #Llama a la función subir que es la que envia la balsa al destino y sube las parejas
        subir() 
        mutex.release() 
    else:
         #Le suma una a la variable que nos permite identificar al par de hackers
        esperaH+=1
        #Libera el mutex de Hackers para formar a otro hacker
        mutex.release()
        #Espera al segundo hacker
        hackerQ.acquire()

        
        
def serf():
    global esperaS, total,xSerf,serfSube,ybarco
#Las siguientes 3 lineas son para representar la llegada de un serf
    xSerf-= 25
    screen.blit(serfImage, [xSerf,55])
    pygame.display.flip()
    #Mutex que evita la concurrencia al momento de formarse para subir al barco
    mutex.acquire()
    #Si es el segundo serf en formarse se suben al barco
    if esperaS>0:
        esperaS-=1
        #Libera la queue de serf para formar otro par
        serfQ.release()
        screen.blit(serfImage, [460,ybarco])
        pygame.draw.rect(screen,GREEN,(serfSube,55,20,24))
        serfSube-=25
        pygame.display.flip()
        time.sleep(0.3)
        screen.blit(serfImage, [490,ybarco])
        pygame.draw.rect(screen,GREEN,(serfSube,55,20,24))
        serfSube-=25
        pygame.display.flip()
        #Llama a la función subir que es la que envia la balsa al destino y sube las parejas
        subir()
        #Libera el mutex
        mutex.release() 
    else: #Agrupa al primer serf para subirlo
        #Esta variable nos permite identificar al par de serfs
        esperaS+=1
        #Libera el mutex de serfs para formar a otro hacker
        mutex.release()
        #Espera al segundo serf
        serfQ.acquire() 
        
def subir(): #Funcion nos permite enviar la balsa con 4 personas
    global total,ybarco
    if total==0: #Condicion que envia la balsa cuando tiene 4 personas
        #print("El barco partio y regreso\n")
        time.sleep(.8)
        screen.blit(barco, [450,0])
        pygame.display.flip()
        time.sleep(.8)
        aguaReinicio()
        ybarco=15
        total=total+1   #Reinicia el contador
    else:
        total-=1
        ybarco=55
 
        
# Test case 0
#   Se previeron cuatro casos en los que se puede enviar la balsa:
#Cuando llegan 4 hackers.
#Cuando llegan 4 serfs.
#Cuando llegan 3 serfs y 1 hacker, para después llegar otro serf (no se hizo la prueba inversa,
#ya que las funciones son simétricas).
#Cuando se envía la balsa con 2 hackers y 2 serfs.
def testcase():
    #Cuando llegan 4 hackers.
    h = threading.Thread(target=hacker)
    h.start()
    time.sleep(.6)
    h = threading.Thread(target=hacker)
    h.start()
    time.sleep(.6)
    h = threading.Thread(target=hacker)
    h.start()
    time.sleep(.6)
    h = threading.Thread(target=hacker)
    h.start()
    time.sleep(.6)
    time.sleep(1)
    #Cuando llegan 4 serfs.
    s = threading.Thread(target=serf)
    s.start()
    time.sleep(.6)
    s = threading.Thread(target=serf)
    s.start()
    time.sleep(.6)
    s = threading.Thread(target=serf)
    s.start()
    time.sleep(.6)
    s = threading.Thread(target=serf)
    s.start()
    time.sleep(.6)
    time.sleep(1)
    #Cuando llegan 3 serfs y 1 hacker, para después llegar otro serf (no se hizo la prueba inversa,
    #ya que las funciones son simétricas).
    s = threading.Thread(target=serf)
    s.start()
    time.sleep(.6)
    s = threading.Thread(target=serf)
    s.start()
    time.sleep(.6)
    s = threading.Thread(target=serf)
    s.start()
    time.sleep(.6)
    h = threading.Thread(target=hacker)
    h.start()
    time.sleep(.6)
   #Cuando se envía la balsa con 2 hackers y 2 serfs. 
    s = threading.Thread(target=serf)
    s.start()
    time.sleep(.6)
    h = threading.Thread(target=hacker)
    h.start()
    time.sleep(.6)
    s = threading.Thread(target=serf)
    s.start()
    time.sleep(.6)
    s = threading.Thread(target=serf)
    s.start()
    time.sleep(.6)
    time.sleep(2.0)
#-------------------Backend------------------------------------------    

#Crear ventana
run=True
screen = pygame.display.set_mode(size)

serfImage=pygame.image.load("clippy.png").convert()
hackerImage=pygame.image.load("tux.png").convert()
barco=pygame.image.load("barco.png").convert()
serfImage.set_colorkey([0,100,0])
hackerImage.set_colorkey([0,100,0])
while run==True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
             pygame.quit()
             sys.exit()
    
    screen.fill(GREEN)
    #pygame.draw.rect(screen,BLUE,(450,0,250,100))
    aguaReinicio()
    
    #Hace que solo se ejecute una vez el programa
    if(run==True):
       testcase()
       run=False
    pygame.quit()
    sys.exit()

#---------------------------Programa sin pygame como referencia logica--------------
'''
    def hacker():
    global esperaH, total
    #El hacker ya esta formado
    #Mutex que evita la concurrencia al momento subir al barco
    mutex.acquire()  
    if esperaH>0: #Si es el segundo Hacker en formarse se suben al barco
        esperaH-=1
        hackerQ.release() #Libera la queue de Hacker para formar otro par
        #llama a la función subir que es la que envia la balsa al destino y sube las parejas
        subir() 
        mutex.release() 
    else:#Agrupa al primer hacker para subirlo
         #Le suma una a la variable que nos permite identificar al par de hackers
        esperaH+=1
        #Libera el mutex de Hackers para formar a otro hacker
        mutex.release()
        #Espera al segundo hacker
        hackerQ.acquire() 
        print("Subio un Hacker\n")
        
def serf():
    global esperaS, total
    #El serf esta formado
    #Mutex que evita la concurrencia al momento de formarse para subir al barco
    mutex.acquire()
    #Si es el segundo serf en formarse se suben al barco
    if esperaS>0: 
        esperaS-=1
        #Libera la queue de serf para formar otro par
        serfQ.release()
        #llama a la función subir que es la que envia la balsa al destino y sube las parejas
        subir()
        #Libera el mutex
        mutex.release() 
    else: #Agrupa al primer serf para subirlo
        #Esta variable nos permite identificar al par de serfs
        esperaS+=1
        #Libera el mutex de serfs para formar a otro hacker
        mutex.release()
        #Espera al segundo serf
        serfQ.acquire() 
        print("Subio un serf\n") 
        
def subir(): #Funcion nos permite enviar la balsa con 4 personas
    global total
    if total==0: #Condicion que envia la balsa cuando tiene 4 personas
        #print("El barco partio y regreso\n")
    else:
        total-=1
        ybarco=55
'''
