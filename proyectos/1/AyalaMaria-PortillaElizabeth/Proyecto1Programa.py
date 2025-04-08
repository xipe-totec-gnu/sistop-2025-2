import threading
import queue
import time
import random

class Laboratorio:
    def __init__(self, num_mesas):
        self.total_mesas = num_mesas # Inicializa el laboratorio con el número total de mesas
        self.mesas_funcionales = random.randint(1, num_mesas) # Mesas disponibles aleatorias
        self.mesas = {i: [] for i in range(self.mesas_funcionales)}  # Diccionario de mesas con listas de alumnos
        self.historial_mesas = {i: 0 for i in range(self.mesas_funcionales)} # Historial para registrar cuántos alumnos usaron cada mesa
        self.max_alumnos_por_mesa = 3
        self.max_espera = 6
        self.alumnos_espera = queue.Queue(self.max_espera) # Cola para los alumnos en espera
        self.jefe_presente = threading.Event()
        self.jefe_presente.set()  # El jefe inicia presente (estando en el laboratorio)
        self.lock = threading.Lock() # Bloque para evitar condiciones de carrera
        self.alumnos_activos = []  # Lista para hacer un seguimiento de los alumnos en el laboratorio 
        self.jefe_trabajando = True  # Controla si el jefe sigue operando (se ha ido a comer)
    
    def alumno_intenta_entrar(self, nombre): # Método para que un alumno intente entrar al laboratorio
        while self.jefe_trabajando:
            if not self.jefe_presente.is_set():
                if self.alumnos_espera.full():
                    print(f"{nombre} no puede esperar y se va.")
                    return
                print(f"{nombre} está esperando en la fila de entrada.") # El alumno se pone en la fila de espera
                self.alumnos_espera.put(nombre)
                return
            else:
                self.asignar_mesa(nombre) # Si el jefe está presente, intenta asignar una mesa al alumno
                return
    
    def asignar_mesa(self, nombre):
        with self.lock: # Permite controlar el acceso
            for mesa, alumnos in self.mesas.items():
                if len(alumnos) < self.max_alumnos_por_mesa: # Si la mesa tiene espacio
                    alumnos.append(nombre)
                    self.historial_mesas[mesa] += 1  # Registrar uso de mesa
                    self.alumnos_activos.append(nombre)  # Añadir alumno a lista de activos
                    print(f"{nombre} ha tomado un lugar en la mesa {mesa}.")
                    threading.Thread(target=self.uso_mesa, args=(nombre, mesa)).start() # Inicia un hilo para simular el uso de la mesa
                    return
        print(f"{nombre} no encontró mesa y se va.")  # Si no hay mesas disponibles, el alumno se va
    
    def uso_mesa(self, nombre, mesa):
        tiempo = random.randint(3, 7)
        time.sleep(tiempo)  # Simula el tiempo de uso de la mesa
        with self.lock: # Bloquea el acceso a recursos compartidos
            self.mesas[mesa].remove(nombre)  # Elimina al alumno de la mesa
            self.alumnos_activos.remove(nombre)  # Eliminar de la lista de activos
        print(f"{nombre} ha dejado la mesa {mesa} después de {tiempo} minutos.")
    
    def jefe_se_va_a_comer(self):
        while self.jefe_trabajando:
            time.sleep(random.randint(10, 20))  # Intervalo antes de que el jefe se vaya
            self.jefe_presente.clear()  # Indica que el jefe no está presente
            with self.lock:
                print(f"El jefe se ha ido a comer. Actualmente hay {len(self.alumnos_activos)} alumnos dentro del laboratorio.")
            time.sleep(random.randint(5, 10))  # Simula el tiempo de comida
            self.jefe_presente.set() # Indica que el jefe ha regresado
            print("El jefe ha regresado. Los alumnos en espera pueden entrar.")
            while not self.alumnos_espera.empty(): # Asigna mesas a los alumnos en espera
                self.asignar_mesa(self.alumnos_espera.get())
    
    def esperar_a_que_terminen(self):
        while self.alumnos_activos or not self.alumnos_espera.empty():  # Esperar a que todos los alumnos terminen
            time.sleep(1)
        self.jefe_trabajando = False  # Finaliza el turno del jefe
    
    def mostrar_resultados(self): # Método para mostrar el registro del uso de mesas del dia
        print("\nResumen del día:")
        for mesa, cantidad in self.historial_mesas.items(): # Recorre el historial de mesas
            print(f"Mesa {mesa}: {cantidad} alumnos la usaron en total.")

# Configuración del laboratorio
num_mesas = int(input("Ingrese el número total de mesas disponibles en el laboratorio: "))
laboratorio = Laboratorio(num_mesas) # Crea una instancia del laboratorio

# Muestra cuántas mesas están funcionales
print(f"Hoy funcionan {laboratorio.mesas_funcionales} mesas de {num_mesas}.") 
num_alumnos = laboratorio.mesas_funcionales * laboratorio.max_alumnos_por_mesa # Calcula el número de alumnos

# Iniciar hilo del jefe que se va a comer en intervalos
threading.Thread(target=laboratorio.jefe_se_va_a_comer, daemon=True).start()

# Crear alumnos intentando ingresar
alumnos = [f"Alumno {i+1}" for i in range(num_alumnos + 5)]
for alumno in alumnos:
    threading.Thread(target=laboratorio.alumno_intenta_entrar, args=(alumno,)).start()
    time.sleep(random.uniform(0.5, 2))  # Simula llegada aleatoria

# Esperar a que todos los alumnos terminen
laboratorio.esperar_a_que_terminen()

# Mostrar resultados
laboratorio.mostrar_resultados() 