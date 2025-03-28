import threading as thr
import time
import random

num_sillas = 3
alumnos_actuales = 0
alumno_espera = 0
preguntas = []

mutex_asesoria=thr.Semaphore(num_sillas)  #Permite tantos alumnos como sillas dentro del salon
mutex_prof=thr.Semaphore(1)
mutex_alumno_activo=thr.Semaphore(1)

rendA=thr.Semaphore(0)
rendP=thr.Semaphore(0)

def Profe():
    while True:
        if alumnos_actuales>0:
            print('[Profesor]: *Pensando* Ughh, que sueño')
        else:
            print('\n[Profesor]: No hay alumnos, Hora de la siesta ZZZ...\n')
        rendA.release()                 
        rendP.acquire()
        time.sleep(2/10)

def alumno(num_alum):
    vueltas=1
    
    while True:
        #time.sleep(random.randint(1,3)/10) #Patra evitar que siempre entren en orden 1,2,3
        global alumnos_actuales
        global alumno_espera
        print('Alumno[',num_alum,']: Toc toc, Puedo entrar?')
        with mutex_prof:
            alumno_espera=alumno_espera+1

        with mutex_asesoria:     
            with mutex_prof:
                alumnos_actuales=alumnos_actuales+1
                alumno_espera=alumno_espera-1

            print('Alumno[',num_alum,']: *Entra, es su vuelta numero,',vueltas,'* Hay',alumnos_actuales,' en el salon')
          
            while preguntas[num_alum]>0:          #Mientras el alumno tenga preguntas
                with mutex_alumno_activo:         #Pregunta al profe
                    rendP.release()
                    rendA.acquire()
                    
                    print('Alumno[',num_alum,']: Hola Profe, tengo',preguntas[num_alum],' preguntas.  Blablabla?')
                  
                    if (random.randint(1,5))==2:  #20% de probailidades de pensar en otra pregunta antes de salir
                        print('             Oh, se me ocurrio otra cosa. Aún no me ire')
                        
                    else:
                        print('             Gracias por la explicacion *Reflexiona un poco el conocimiento*')
                        preguntas[num_alum]=preguntas[num_alum]-1
                    
                time.sleep(random.randint(1,3)/10)  #Evita que un mismo alumno haga todas sus preguntas seguidas cuando no es el único en el salón
    
            with mutex_prof:
                alumnos_actuales=alumnos_actuales-1
                print('Alumno[',num_alum,']: Me voy, ya no tengo preguntas. Quedan',alumnos_actuales,'compañeros en el salon, y hay',alumno_espera,'esperando a entrar')
                
        vueltas=vueltas+1
        preguntas[num_alum]=random.randint(1,3)     #Re instancia las preguntas
        time.sleep(random.randint(8,10)/10)         #Para alcanzar el estado en el que el profesor puede dormir un poco,
                                                    #los alumnos toman un tiempo en regresar a la asesoría si es que ya salieron

thr.Thread(target=Profe).start()

for i in range(num_sillas+1):                   #Para este caso, se tienen 3 sillas y 4 alumnos
  thr.Thread(target=alumno, args=[i]).start()
  preguntas.append(random.randint(1,3))        #Inicializa cada alumno con máx 3 preguntas
 

