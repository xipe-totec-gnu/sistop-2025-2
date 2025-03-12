import threading
import time
import random

class Duck(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name
        self.distance = 0

    def run(self):
        while self.distance < 60:
            self.distance += random.randint(1, 10)
            print(f"{self.name} ha avanzado a {self.distance} metros.")
            time.sleep(random.uniform(0.1, 0.5))
        print(f"{self.name} ha terminado la carrera!")

def main():
    ducks = [Duck(f"Pato {i}") for i in range(1, 6)]
    for duck in ducks:
        duck.start()
    for duck in ducks:
        duck.join()

if __name__ == "__main__":
    main()