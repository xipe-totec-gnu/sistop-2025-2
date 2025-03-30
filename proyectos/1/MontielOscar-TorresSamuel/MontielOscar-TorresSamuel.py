import threading
import time
import random
from rich.console import Console
from rich.table import Table
from rich.live import Live

capacidadFisica = 15
sobreCupo = 20
espacios = {f"A{i}": False for i in range(1, capacidadFisica + 1)}
mutexEspacios = threading.Lock()
condicionEspacio = threading.Condition(mutexEspacios)
semaforo = threading.Semaphore(sobreCupo)
registroEventos = []
asignacionVehiculos = {}
consola = Console()

def ocuparDosEspacios(idVehiculo):
    registroEventos.append(f"Carro {idVehiculo} ocupó dos espacios mal estacionado")

def vehiculoLlegada(idVehiculo):
    semaforo.acquire()
    with condicionEspacio:
        if random.random() < 0.05:
            ocuparDosEspacios(idVehiculo)
        else:
            while all(espacios[espacio] for espacio in espacios):
                condicionEspacio.wait()
            for espacio in espacios:
                if not espacios[espacio]:
                    espacios[espacio] = True
                    asignacionVehiculos[idVehiculo] = espacio
                    registroEventos.append(f"Carro {idVehiculo} ocupó {espacio}")
                    break
    time.sleep(random.randint(5, 30))
    vehiculoSalida(idVehiculo)

def vehiculoSalida(idVehiculo):
    with condicionEspacio:
        if idVehiculo in asignacionVehiculos:
            espacioAsignado = asignacionVehiculos.pop(idVehiculo)
            espacios[espacioAsignado] = False
            registroEventos.append(f"Carro {idVehiculo} liberó {espacioAsignado}")
            condicionEspacio.notify()
    semaforo.release()

class Grua(threading.Thread):
    def run(self):
        while True:
            with mutexEspacios:
                pass
            time.sleep(10)

def interfazUsuario():
    with Live(console=consola, refresh_per_second=4) as live:
        while True:
            tabla = Table(title="Estacionamiento FI")
            tabla.add_column("Espacios Libres", justify="center")
            tabla.add_column("Eventos", justify="left")
            with mutexEspacios:
                libres = sum(1 for estado in espacios.values() if not estado)
                eventos = "\n".join(registroEventos[-5:])
            tabla.add_row(str(libres), eventos)
            live.update(tabla)
            time.sleep(0.5)

def main():
    grua = Grua(daemon=True)
    grua.start()
    hiloInterfaz = threading.Thread(target=interfazUsuario, daemon=True)
    hiloInterfaz.start()
    for i in range(1000):
        threading.Thread(target=vehiculoLlegada, args=(i,), daemon=True).start()
        time.sleep(random.uniform(0.1, 1.5))
    hiloInterfaz.join()

if __name__ == "__main__":
    main()