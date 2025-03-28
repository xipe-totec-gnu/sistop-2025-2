import threading
import time
import random

class Balsa:
    def __init__(self):
        self.mutex = threading.Lock()
        self.serfs = self.hackers = 0
        self.b_completa = threading.Condition(self.mutex)
        self.max_personas = 4

    def todo_listo(self):
        return self.hackers + self.serfs == self.max_personas and (
            self.hackers in [2, 4] or self.serfs in [2, 4]
        )

    def subir_a_balsa(self, tipo):
        with self.mutex:
            self.hackers += tipo == "hacker"
            self.serfs += tipo == "serf"

            while not self.todo_listo():
                if self.hackers + self.serfs >= 4:
                    print(f"No fue posible cumplir con la convivencia de los tripulantes...\n"
                          f"A la balsa solo consiguieron subirse:\n"
                          f" - {self.hackers} Hackers\n"
                          f" - {self.serfs} Serfs\n"
                          "No es posible realizar un viaje en balsa con esta tripulación...\n")
                    self.hackers = self.serfs = 0
                    self.b_completa.notify_all()
                    return
                self.b_completa.wait()

            print(f"{tipo.capitalize()} abordó la balsa.")
            self.b_completa.notify_all()

            if self.todo_listo():
                print(f"La tripulacion ha llegado a su limite, los tripulantes son:\n"
                      f" - {self.hackers} Hackers\n"
                      f" - {self.serfs} Serfs\n")
                time.sleep(2)
                print("¡La tripulación está completa! Iniciamos el viaje\n")
                self.hackers = self.serfs = 0
                self.b_completa.notify_all()

def persona(tipo, balsa):
    time.sleep(random.uniform(0.5, 2))  # Simula llegada aleatoria
    print(f"Atención! Un {tipo.capitalize()} intenta subir a la balsa, preparen la escalera...\n")
    balsa.subir_a_balsa(tipo)

# Instancia de la balsa
balsa = Balsa()

# Crear y gestionar hilos de manera más flexible
threads = [threading.Thread(target=persona, args=(tipo, balsa)) for tipo in ["hacker", "serf"] * 3]

for t in threads:
    t.start()

for t in threads:
    t.join()
