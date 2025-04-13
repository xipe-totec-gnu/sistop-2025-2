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


# ================= CONSTANTES GLOBALES ================= #
NUMBER_OF_PARTICIPANTS = 3  # Numero equipos
NUMBER_OF_VALIDATORS = 2    # Numero validadores
NUMBER_OF_PRINTERS = 2      # Numero impresoras
NUMBER_OF_PROBLEMS = 9      # Numero de problemas
CONTEST_DURATION = 3        # Duracion del concurso en segundos
# ======================================================= #

# Cola de problemas a ser juzgados
problem_queue = deque()

# Semaforo para indicar cuantos problemas hay en la cola en ese momento
queue_size = threading.Semaphore(0)

# Mutex para evitar que varios hilos modifiquen a la cola de manera simultanea
mutex_queue = threading.Semaphore(1)

# Barrera para que los participantes esperen a que se junten 3 archivos antes de imprimir
barrier_printers = threading.Barrier(NUMBER_OF_PRINTERS)

# Mutex para responder clarificaciones
mutex_clarification = threading.Semaphore(1)

# Lista de eventos para que participantes esperen a que solucion sea juzgada antes de volver a subir
waiting_for_solution = [threading.Event() for i in range(NUMBER_OF_PARTICIPANTS)]

# Bandera para observar que problemas fueron aceptados
accepted = [0] * NUMBER_OF_PARTICIPANTS

# Evento global para conocer si ya se termino el concurso
contest_finished = threading.Event()


# A la lista de problemas se agregan las letras correspondiente a cada uno de los problemas
problem_list = list(string.ascii_uppercase[:NUMBER_OF_PROBLEMS])

# El color del globo de cada uno de los problemas de la lista 
problem_color_emojis = ["🔴", "🟠", "🟡", "🟢", "🔵", "🟣", "⚫", "⚪", "🟤"]
random.shuffle(problem_color_emojis)
problem_color_emojis = problem_color_emojis[:NUMBER_OF_PROBLEMS]

# Diccionario para almacenar que letra esta asignada a que color
color_dict = dict(zip(problem_list, problem_color_emojis))

# Almacenamiento de wa por problema por participante
wa_per_problem = {problem: [0] * NUMBER_OF_PARTICIPANTS for problem in problem_list}

# Almacenamiento del momento en el que el equipo obtuvo accepted por cada problema
accepted_per_problem = {problem: [0] * NUMBER_OF_PARTICIPANTS for problem in problem_list}

# Reloj de inicio del concurso
start_time = time.time()

# Posibles veredictos a solucion de un problema
possible_veredicts = [
  'AC (Accepted)', 'WA (Wrong Answer)', 
  'TLE (Time Limit Excedeed)', 
  'RTE (Runtime Error)', 
  'Presentation Error'
]



def ask_to_print(problem_num, participant_num):
  # Manejo de impresion de archivos
  # Se necesita que la barrera se llene para imprimir
  try: 
    barrier_printers.wait(timeout=5)
    # Se reinicia la barrera
    barrier_printers.reset()
    print(f" 📄 Participant {participant_num + 1} has received printed file about problem {problem_num}")
  except threading.BrokenBarrierError:
    print(f"Contest has finished so print for problem {problem_num}, ordered by {participant_num + 1} has not taken place.")



def participant(participant_num, problems_not_solved):
  # Mientras haya problemas por resolver
  while len(problems_not_solved) > 0 and not contest_finished.is_set():
    time.sleep(random.uniform(0, 1))
    # El equipo escoge uno de los problemas que no ha resuelto e intenta subir una solucion a este
    problem_to_submit = random.choice(problems_not_solved)
    random_decision = random.uniform(0, 1)

    # Cuando equipo tiene una pregunta
    if random_decision > 0.75:
      print(f"❓ Participant {participant_num + 1} has a question about problem {problem_to_submit}")
      # Se manda una pregunta de aclaracion
      mutex_clarification.acquire()
      # Se duerme un poco para simular el tiempo que tarda en responder la pregunta
      time.sleep(random.uniform(0, 1))
      # Se responde la pregunta
      print(f"Participant {participant_num + 1} has received answer to question about problem {problem_to_submit}")
      mutex_clarification.release()

    # Cuando mandan a imprimir
    elif random_decision > 0.5:
      print(f" 🖨️ Participant {participant_num} wants to print code for problem {problem_to_submit}")
      # Se manda a imprimir un archivo como nuevo hilo
      t1 = threading.Thread(target=ask_to_print, args=(problem_to_submit, participant_num))
      t1.start()
      # Cuando se sale de la funcion ya se respondio la pregunta
    
    # Cuando el equipo sube una solucion a un problema
    else:
      print(f"Participant number {participant_num + 1} has submitted a solution to {problem_to_submit}")
      mutex_queue.acquire()
      # Se inserta la solucion a la cola de problemas a ser juzgados
      problem_queue.append((participant_num, problem_to_submit))
      mutex_queue.release()
      # Se aumenta en uno el semaforo que cuenta numero de elementos en la cola
      queue_size.release()
      # Se espera a conocer respuesta del juez
      waiting_for_solution[participant_num].wait()
      # Si el problema fue aceptado se elimina de la lista de problemas a solucionar
      if accepted[participant_num]:
        problems_not_solved.remove(problem_to_submit)
        accepted_per_problem[problem_to_submit][participant_num] = time.time() - start_time
      else:
        wa_per_problem[problem_to_submit][participant_num] += 1
      # Se reinicia la bandera
      accepted[participant_num] = 0
      # Se reinicia evento
      waiting_for_solution[participant_num].clear()
  if len(problems_not_solved) == 0: 
    print(f"   🎈 Participant {participant_num + 1} has solved all the problems")

# Devuelve un veredicto aleatorio de la lista de veredictos
def veredict():
  return (random.choice(possible_veredicts))



def validator(validator_num):
  while True:
    if queue_size.acquire(timeout=5) == False:
      break
    mutex_queue.acquire()
    # Se identifica problema a juzgar y se juzga (siguiendo el orden de la cola)
    participant_num, problem_to_judge = problem_queue.popleft()
    mutex_queue.release()
    print(f" ⏳Judging solution to problem {problem_to_judge} by participant {participant_num + 1}")
    time.sleep(random.uniform(0, 1))
    # Se obtiene veredicto aleatorio
    veredict_obtained = veredict()
    if veredict_obtained == possible_veredicts[0]:
      print(f" {color_dict[problem_to_judge]} {validator_num} Participant {participant_num + 1} has solved problem {problem_to_judge}.")
      accepted[participant_num] = 1
    else:
      print(f" ❌ Participant {participant_num + 1} sumbitted incorrect solution to problem {problem_to_judge}. Veredict obtained {veredict_obtained}")
    waiting_for_solution[participant_num].set()




def thread_stopper():
  contest_finished.set()
  print("¡¡¡¡¡¡¡¡¡CONTEST IS FINISHED!!!!!!!!! \n Solutions currently being judged will be judged and results will be shown on the scoreboard.")

def print_scoreboard():
  # Se genera el scoreboard ordenando primero por problemas y luego por penalty
  scoreboard = []
  for i in range(NUMBER_OF_PARTICIPANTS):
    penalty = 0
    solved = 0
    for problem in problem_list:
      if accepted_per_problem[problem][i] > 0:
        solved += 1
        penalty += accepted_per_problem[problem][i]
        penalty += wa_per_problem[problem][i] * 20
    scoreboard.append((solved, penalty, i ))
  scoreboard.sort(key=lambda x: (-x[0], x[1]))
  print("\n\nScoreboard:")
  print("Participant\tSolved\tPenalty")
  for solved, penalty, i in scoreboard:
    print(f"{i + 1}\t\t{solved}\t{penalty}")
  # Se imprime el scoreboard
  print("\n\nProblems solved by each participant:")
  for i in range(NUMBER_OF_PARTICIPANTS):
    print(f"Participant {i + 1}: ", end="")
    for problem in problem_list:
      if accepted_per_problem[problem][i] > 0:
        print(f"{problem} {color_dict[problem]}", end="")
    print()


def main():
  threads_validators = []
  threads_participants = []
  
  global start_time
  start_time = time.time()

  for i in range(NUMBER_OF_VALIDATORS):
    t = threading.Thread(target=validator, args=(i, ))
    threads_validators.append(t)
    t.start()

  for i in range(NUMBER_OF_PARTICIPANTS):
    t = threading.Thread(target=participant, args=(i, copy.copy(problem_list)))
    threads_participants.append(t)
    t.start()

  timer = threading.Timer(CONTEST_DURATION, thread_stopper)
  timer.start()


  # Se espera a que finalicen 
  for t in threads_validators:
    t.join()

  for t in threads_participants:
    t.join()

  print_scoreboard()

main()