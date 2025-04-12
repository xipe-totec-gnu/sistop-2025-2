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
number_of_participants = 3

# El numero de validadores de soluciones del juez
number_of_validators = 3 

# El numero de problemas del concurso 
number_of_problems = 9

# El numero de impresoras
number_of_printers = 2

# Cola de problemas a ser juzgados
problem_queue = deque()

# Semaforo para indicar cuantos problemas hay en la cola en ese momento
queue_size = threading.Semaphore(0)

# Mutex para evitar que varios hilos modifiquen a la cola de manera simultanea
mutex_queue = threading.Semaphore(1)

# Barrera para que los participantes esperen a que se junten 3 archivos antes de imprimir
barrier_printers = threading.Barrier(number_of_printers)

# Mutex para responder clarificaciones
mutex_clarification = threading.Semaphore(1)

# Lista de eventos para que participantes esperen a que solucion sea juzgada antes de volver a subir
waiting_for_solution = [threading.Event() for _ in range(number_of_participants+1)]

# Bandera para observar que problemas fueron aceptados
accepted = [0] * (number_of_participants+1)



# A la lista de problemas se agregan las letras correspondiente a cada uno de los problemas
PROBLEM_LIST = list(string.ascii_uppercase[:number_of_problems])

# El color del globo de cada uno de los problemas de la lista 
PROBLEM_COLOR_EMOJIS = ["🔴", "🟠", "🟡", "🟢", "🔵", "🟣", "⚫", "⚪", "🟤"]
random.shuffle(PROBLEM_COLOR_EMOJIS)
PROBLEM_COLOR_EMOJIS = PROBLEM_COLOR_EMOJIS[:number_of_problems]

# Posibles veredictos a solucion de un problema
possible_veredicts = ['AC (Accepted)', 'WA (Wrong Answer)', 'TLE (Time Limit Excedeed)', 'RTE (Runtime Error)', 'Presentation Error']

def ask_to_print(problem_num):
  # aqui se va a recibir el numero de pregunta de problema pero se van a responder hasta que se junten 3 preguntas
  # Se espera a que se junten 3 preguntas
  barrier_printers.wait()
  # Se responde la pregunta
  print(f"Question {problem_num} has been answered")
  # Se reinicia la barrera
  barrier_printers.reset()


def participant(participant_num, problems_not_solved):
  # Mientras haya problemas por resolver
  while len(problems_not_solved) > 0:
    time.sleep(random.uniform(0, 1))
    # El equipo escoge uno de los problemas que no ha resuelto e intenta subir una solucion a este
    problem_to_submit = random.choice(problems_not_solved)
    # De manera aleatoria se decide si se va a a mandar una pregunta de aclaracion
    if random.choice([True, False]):
      print(f"Participant {participant_num} has a question about problem {problem_to_submit}")
      # Se manda una pregunta de aclaracion
      mutex_clarification.acquire()
      # Se duerme un poco para simular el tiempo que tarda en responder la pregunta
      time.sleep(random.uniform(0, 1))
      # Se responde la pregunta
      print(f"Participant {participant_num} has received answer to question about problem {problem_to_submit}")
      mutex_clarification.release()
    # De manera aleatoria se decide si se va a a mandar a imprimir problema
    if random.choice([True, False]):
      print(f"Participant {participant_num} wants to print code for problem {problem_to_submit}")
      # Se manda a imprimir un archivo
      ask_to_print(problem_to_submit)
      # Cuando se sale de la funcion ya se respondio la pregunta
      print(f"Participant {participant_num} has received printed file about problem {problem_to_submit}")
    # Se duerme un poco para simular el tiempo que tarda en subir la solucion
    time.sleep(random.uniform(0, 1))
    # Se sube la solucion al problema
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
