from threading import *
import random
import time
import random

# Creamos un número aleatorio de elfos
random_elf_number = random.randint(1, 20)

# Definimos los semaforos necesarios: uno para los elfos...
elves_queue = Semaphore(3)
# ...otro para Santa Claus...
santa_active = Semaphore()
# ...y otro para los renos.
reindeers_active = Semaphore(9)

# Debido a la implementación de barrera, debemos de añadir
# variables adicionales
elf_counter = 0
reindeer_counter = 0

# Variable divertida que nos permite dar un valor arbitrario
# a los regalos producidos.
total_toys = 0

# Al menos gracias a mi interpretación del problema, vi necesario que
# los elfos y los renos dejaran de actuar cada vez que hacían un acquire.
# Por esto mismo, añadí objetos de la clase Threading.Event, en donde
# podemos congelar el actuar de cada hilo según el valor de estos eventos.
toy_breaks = Event()
reindeer_arrives = Event()

# Nombres de los renos
reindeer_names = ["Dasher", "Dancer", "Prancer", "Vixen", "Comet", "Cupid", "Donner", "Blitzen", "Rudolph"]


def main():
    # Nos aseguramos de que los eventos se encuentren en falso.
    toy_breaks.clear()
    reindeer_arrives.clear()

    # Creamos hilos de elfos
    for i in range(random_elf_number):
        new_Elf = Thread(target=elfWorking, args=(i+1,))
        new_Elf.start()
        time.sleep(2)

    # Creamos hilos de renos
    for i in range(9):
        new_Reindeer = Thread(target=reindeerVacations, args=(reindeer_names[i],))
        new_Reindeer.start()
        time.sleep(2)

#
def elfWorking(id):
    global elf_counter, total_toys
    # Ciclo infinito
    while True:
        # Pretendemos que algo se está haciendo
        print(f"Elf number {id} is currently working on a toy...\n")
        time.sleep(2)
        # Si se activa una condición aleatoria, suponemos que se rompió un juguete.
        if(random.randint(1, 6) == 1):
            print(f"Whoa! Elf {id} broke its toy! Better go ask Santa!\n")
            # Logramos hacer un acquire.
            elves_queue.acquire()
            # Actualizamos la variable para la barrera.
            elf_counter += 1
            # Si el contador de elfos es mayor o igual que 3, tenemos un grupo de 3 elfos.
            if(elf_counter >= 3):
                print("Queue full!")
                # Utilizamos el apagador para que los renos no interfieran, o si ya se encuentra ocupado,
                # que nuestros elfos esperen a que Santa regrese.
                santa_active.acquire()
                print("The three elves dared go into Santa's Den...")
                print("And they got their fair share of advice!")
                # Hacemos un release para que los demás elfos que estén esperando puedan agarrar el semáforo.
                elves_queue.release(3)
                # Desocupamos a santa.
                santa_active.release()
                # Disminuimos la variable de elfos.
                elf_counter -= 3
                # Reiniciamos la variable de evento para poder permitir que los hilos continúen haciendo su trabajo.
                toy_breaks.set()
                toy_breaks.clear()
                # Sumamos a los juguetes que Santa ayudó a crear.
                total_toys += 3
            else:
                # Si no tenemos un grupo de 3 elfos, ponemos a que los que sí se encuentran en el grupo
                # esperen.
                toy_breaks.wait()     
        else: 
            # Si no se activa la condición aleatoria, podemos asumir que el juguete se construyó exitosamente.
            print(f"Nice going! Elf {id} has made a new toy!\n")
            total_toys += 1
            time.sleep(2)


def reindeerVacations(name):
    global reindeer_counter, total_toys
    # Ciclo infinito
    while True:
        print(f"{name} is currently taking a vacation...")
        time.sleep(2)
        # Si se cumple una variable aleatoria, asumimos que el reno regresó de vacacionar.
        if(random.randint(1, 3) == 1):
            print(f"{name} decided to pickup the slack!")
            # Añadimos a la variable contadora para aplicar la barrera.
            reindeer_counter += 1
            # Si tenemos un contador de renos de 9, entonces todos los renos están listos.
            if(reindeer_counter == 9):
                print("All reindeers ready to go!")
                # Apartamos a Santa para que los elfos no interfieran, o esperamos a que este
                # termine de ayudar a los elfos.
                santa_active.acquire()
                print("The reindeer are currently on their way to deliver the presents...")
                time.sleep(5)
                print("Great! Santa and his reindeer delivered all of the gifts!")
                print(f"Gift total: {total_toys}")
                print("The reindeer are off to vacation again!")
                # Como los regalos se repartieron, podemos suponer que ya no hay.
                total_toys = 0
                # Hacemos el release del semáforo de los renos
                reindeers_active.release(9)
                # Desapartamos a Santa
                santa_active.release()
                # Reseteamos el contador de los renos
                reindeer_counter = 0
                # Reiniciamos el evento
                reindeer_arrives.set()
                reindeer_arrives.clear()
            else:
                # Si no están listos los renos, hacemos que esperen.
                reindeer_arrives.wait()
        else:
            # En caso de que el valor aleatorio no se ejecute, podemos suponer que los renos siguen de vacaciones.
            print(f"{name} does not seem to be wanting to come back from vacation any time soon...")
            time.sleep(2)

main()