import random
import threading
import time

class Jugador:
    def __init__(self, id_jugador, es_vip=False):
        self.id = id_jugador
        self.es_vip = es_vip
        self.kills = 0
        self.deaths = 0
        self.monedas = 0
        self.kd = 0.0
        self.conectado = False
        self._detener = False

    def detener(self):
        self._detener = True

    def jugar(self, servidor, actualizar_historial, actualizar_ui):
        tiempo_conexion = random.randint(20, 40)
        segundos = 0

        while segundos < tiempo_conexion and not self._detener:
            time.sleep(4)
            self.kills += 1
            self.deaths += random.choice([0, 1])
            self.kd = self.kills / self.deaths if self.deaths > 0 else self.kills

            actualizar_historial(f"Jugador {self.id} hizo una kill. KD: {self.kd:.2f}")

            if self.kd > 2:
                self.monedas += 100
                actualizar_historial(f"Jugador {self.id} recibió 100 monedas. Total: {self.monedas}")

            actualizar_ui()
            segundos += 4

        servidor.desconectar_jugador(self)
        actualizar_historial(f"Jugador {self.id} salió del servidor.")
        actualizar_ui()

