import threading
import random
import time


#Acosta Jacinto Alan
#Rubio Carmona Jose Angel
#Tarea 1: El cruce del rio
#Sistemas Operativos  grupo: 6 2025-2

# Contadores globales
hackers = 0
serfs = 0

# Semáforos
mutex = threading.Semaphore(1)     # Para proteger el acceso a los contadores
balsa = threading.Semaphore(0)     # Para permitir que crucen cuando hay suficientes

# Número de personas que pueden cruzar por viaje
PERSONAS_POR_BALSA = 4


    
# Lógica cuando una persona llega
def persona_llega(id_persona, tipo):
    global hackers, serfs
  
    with mutex:
        if tipo == "hacker":
            hackers += 1
            print(f"Hacker {id_persona} espera para subir a la balsa")
        else:
            serfs += 1
            print(f"Serf {id_persona} espera para subir a la balsa")

        # Se revisa si hay combinación válida para zarpar
        if hackers >= 2 and serfs >= 2:
            print("Se reúnen 2 hackers y 2 serfs, suben a la balsa y viajan\n")
            for _ in range(PERSONAS_POR_BALSA):
                balsa.release()
            hackers -= 2
            serfs -= 2
        elif hackers >= 4:
            print("Se reúnen 4 hackers, suben a la balsa y viajan\n")
            for _ in range(PERSONAS_POR_BALSA):
                balsa.release()
            hackers -= 4
        elif serfs >= 4:
            print("Se reúnen 4 serfs, suben a la balsa y viajan\n")
            for _ in range(PERSONAS_POR_BALSA):
                balsa.release()
            serfs -= 4



def main():
    threads = []
  
    for i in range(1,21):  # Total de personas
        tipo = random.choice(["hacker", "serf"])
        t = threading.Thread(target=persona_llega, args=(i, tipo))
        threads.append(t)
        t.start()
        time.sleep(random.uniform(1, 1))  # Simula llegadas en tiempos distintos
    
    for t in threads:
        t.join()

    print("\nLos viajes finalizaron. Lamentamos aquellos que ya no pudieron viajar.")

if __name__ == "__main__":
    main()
    

#Explicacion basica:Los serf y Hackers llegan de forma aletoria, cuando se juntan 2 y 2, o 4 de uno mismo. 
#Si se llegasen a juntar los necesarios pero quedara alguno que no pudo subir, se queda para abordar , si se juntan los necesarios mas el sobrante pueden abordar.