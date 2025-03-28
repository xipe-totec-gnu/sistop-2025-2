""""
Sistemas Operativos

Tarea 1 - Ejercicios de Sincronizacion 

Problema seleccionado: Interseccion de caminos

Autores:
Cervantes Mateos Leonardo Mikel
Sole Pi Arnau Roger Sole Pi


"""


import threading
import time
import random

# El numero de coches que utilizaran el cruce
number_of_cars = 5

# Un mutex para cada uno de los 4 cuadrantes de la interseccion
mutex = [threading.Semaphore(1), threading.Semaphore(1), threading.Semaphore(1), threading.Semaphore(1)]

# Un semaforo para que solo pueda haber 3 coches de manera simultanea en los cuadrantes de la interseccion
# Esto se hace para evitar que haya un bloqueo mutuo
mutex_intersection = threading.Semaphore(3)


# Lista para determinar que coche se encuentra en cada cuadrante de la interseccion
# Un 0 significa que el cuadrante se encuentra vacio
intersection_squares = [0, 0, 0, 0]


"""
Funcion para asignar un cuadrante de la interseccion a un coche
El cuadrante no puede estar ocupado ya que esto ocasionaria un choque por lo que se tiene el mutex del cuadrante
Args:
    square (int): el cuadrante de la interseccion que el coche que quiere ocupar
    carNum (int): el numero del coche que quiere ocupar el cuadrante

"""
def enter_square(square, carNum):
    print(f"    Coche  {carNum}  intentando entrar a cuadrante {square}")
    mutex[square].acquire()
    intersection_squares[square] = carNum
    print(f"        Coche  {carNum}  ha entrando a cuadrante {square}")



""""
Funcion para que un coche pueda abandonar un cuadrante y liberar su mutex
Args:
    square (int): el cuadrante de la interseccion que el coche abandona
    carNum (int): el numero del coche que abandona el cuadrante

"""
def leave_square(square, carNum):
    mutex[square].release()
    intersection_squares[square] = 0
    print(f"        Coche  {carNum}  ha salido del cuadrante {square}")




"""
Funcion para que un hilo realice sus movimientos necesarios
Args:
    road (int): el lado en el que empieza el coche (se puede pensar como el primer cuadrante al que quiere entrar)
    turn (int): el tipo de giros que realizara el coche
    - 0 indica que el coche no realizara giros y se seguira de frente utilizando dos cuadrantes
    - 1 indica que el coche realizara un giro a la derecha y utilizara un solo cuadrante
    - 2 indica que el coche realizara un giro a la izquierda y utilizara dos cuadrantes
    carNum (int): el numero del coche

"""
def intersection(road, turn, carNum):

    # se imprime que coche quiere entrar a interseccion y como quiere hacer su recorrido
    if(turn == 0):
        print(f"Coche  {carNum} quiere entrar al cuadrante {road} de la interseccion y piensa ir derecho")
    elif(turn == 1):
        print(f"Coche  {carNum} quiere entrar al cuadrante {road} de la interseccion y piensa girar a la derecha")
    else:
        print(f"Coche  {carNum} quiere entrar al cuadrante {road} de la interseccion y piensa girar a la izquierda")    
    
    # Se verifica que haya menos de 3 coches en ese momento en la interseccion
    mutex_intersection.acquire()

    square = road
    enter_square(square, carNum)
    

    # tiempo aleatorio que se queda el coche en el cuadrante
    time.sleep(random.uniform(0.5, 1.5))  

    # seguirse de frente
    if turn == 0:
        enter_square((road + 1) % 4, carNum)
        leave_square(road, carNum)

        time.sleep(random.uniform(0.5, 1.5))
        leave_square((road + 1) % 4, carNum)
        
    # giro a la derecha
    elif turn == 1:
        leave_square(road, carNum)
        time.sleep(random.uniform(0.5, 1.5))

    # giro a la izquierda
    else:
        enter_square((road + 1) % 4, carNum)
        leave_square(road, carNum)

        time.sleep(random.uniform(0.5, 1.5))
        enter_square((road + 2) % 4, carNum)
        leave_square((road + 1) % 4, carNum)

        time.sleep(random.uniform(0.5, 1.5))
        leave_square((road + 2) % 4, carNum)
        

    print(f"            Coche  {carNum}  ha salido de la interseccion")
    
    # se aumenta el semaforo en uno marcando que uno de los coches abandono la interseccion
    mutex_intersection.release()

def main():
    threads = []
    cars = []

    # Se crean 'number_of_cars' coches
    # Cada uno empieza en una direccion y metodo de giro que se selecciona de manera aleatoria
    # y un identificador entero (de 1 a numero de coches)
    for i in range(number_of_cars):
        road = random.randint(0,3)
        turn = random.randint(0,2)
        cars.append([road, turn, i + 1])
        
    # se imprime la informacion de cada coche para ver que funciona correctamente
    for i in range(number_of_cars):
        print(cars[i])


    # Se crea un hilo para cada uno
    for i in range(number_of_cars):
        t = threading.Thread(target=intersection, args=(cars[i][0], cars[i][1], cars[i][2]))
        threads.append(t)
        t.start()

    # Se espera a que finalicen 
    for t in threads:
        t.join()


main()
    
