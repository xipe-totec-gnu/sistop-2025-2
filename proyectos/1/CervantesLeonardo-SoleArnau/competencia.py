""""
Sistemas Operativos

Proyecto 1 - Una situación cotidiana con concurrencia y sincronización

Problema seleccionado: Juez de compentencia de programacion

Autores:
Cervantes Mateos Leonardo Mikel
Sole Pi Arnau Roger Sole Pi


"""


import threading
import time
import random
import string
import copy
from collections import deque


# El numero de equipos participantes en la competencia de programacion
number_of_participants = 2

# El numero de validadores de soluciones del juez
number_of_validators = 3 

# El numero de problemas del concurso 
number_of_problems = 9

# Cola de problemas a ser juzgados
problem_queue = deque()

# Semaforo para indicar cuantos problemas hay en la cola en ese momento
queue_size = threading.Semaphore(0)

# Mutex para evitar que varios hilos modifiquen a la cola de manera simultanea
mutex_queue = threading.Semaphore(1)


# Lista de eventos para que participantes esperen a que solucion sea juzgada antes de volver a subir
waiting_for_solution = [threading.Event(), threading.Event(), threading.Event()]

# Bandera para observar que problemas fueron aceptados
accepted = [0, 0, 0]



# A la lista de problemas se agregan las letras correspondiente a cada uno de los problemas
PROBLEM_LIST = list(string.ascii_uppercase[:number_of_problems])

# El color del globo de cada uno de los problemas de la lista 
PROBLEM_COLOR_EMOJIS = ["🔴", "🟠", "🟡", "🟢", "🔵", "🟣", "⚫", "⚪", "🟤"]
random.shuffle(PROBLEM_COLOR_EMOJIS)
PROBLEM_COLOR_EMOJIS = PROBLEM_COLOR_EMOJIS[:number_of_problems]

# Posibles veredictos a solucion de un problema
possible_veredicts = ['AC (Accepted)', 'WA (Wrong Answer)', 'TLE (Time Limit Excedeed)', 'RTE (Runtime Error)', 'Presentation Error']



def participant(participant_num, problems_not_solved):
  # Mientras haya problemas por resolver
  while len(problems_not_solved) > 0:
    time.sleep(random.uniform(0, 1))
    # El equipo escoge uno de los problemas que no ha resuelto e intenta subir una solucion a este
    problem_to_submit = random.choice(problems_not_solved)
    print(f"Participant number {participant_num} has submitted a solution to {problem_to_submit}")
    mutex_queue.acquire()
    # Se inserta la solucion a la cola de problemas a ser juzgados
    problem_queue.append((participant_num, problem_to_submit))
    mutex_queue.release()
    # Se aumenta en uno el semaforo que cuenta numero de elementos en la cola
    queue_size.release()
    # Se espera a conocer respuesta del juez
    event_wait = waiting_for_solution[participant_num].wait()
    # Si el problema fue aceptado se elimina de la lista de problemas a solucionar
    if accepted[participant_num]:
      problems_not_solved.remove(problem_to_submit)
    # Se reinicia la bandera
    accepted[participant_num] = 0

  print(f"Participant {participant_num} has solved all the problems");


# Devuelve un veredicto aleatorio de la lista de veredictos
def veredict():
  return (random.choice(possible_veredicts))



def validator(validator_num):
  while True:
    queue_size.acquire()
    mutex_queue.acquire()
    # Se identifica problema a juzgar y se juzga (siguiendo el orden de la cola)
    participant_num, problem_to_judge = problem_queue.popleft()
    mutex_queue.release()
    print(f"Judging solution to problem {problem_to_judge} by participant {participant_num}")
    time.sleep(random.uniform(0, 1))
    # Se obtiene veredicto aleatorio
    veredict_obtained = veredict()
    if veredict_obtained == possible_veredicts[0]:
      print(f"  Participant {participant_num} has solved problem {problem_to_judge}.")
      accepted[participant_num] = 1
    else:
      print(f"  Participant {participant_num} sumbitted incorrect solution to problem {problem_to_judge}. Veredict obtained {veredict_obtained}")
    waiting_for_solution[participant_num].set()




def main():
  threads = []
  

  for i in range(number_of_validators):
    t = threading.Thread(target=validator, args=(i + 1, ))
    threads.append(t)
    t.start()

  for i in range(number_of_participants):
    t = threading.Thread(target=participant, args=(i + 1, copy.copy(PROBLEM_LIST)))
    threads.append(t)
    t.start()


  # Se espera a que finalicen 
  for t in threads:
    t.join()



main()
