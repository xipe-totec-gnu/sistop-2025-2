import threading
import random
import time

class Usuario(threading.Thread):
    """
    Representa a un usuario (hilo) que realiza acciones de reserva,
    cancelación o modificación en el sistema.
    """

    def __init__(self, user_id, priority, sistema, num_acciones=20):
        super().__init__()
        self.user_id = user_id
        self.priority = priority
        self.sistema = sistema
        self.num_acciones = num_acciones

        # Posibles acciones
        self.acciones = ["reservar", "cancelar", "modificar"]

    def run(self):
        for _ in range(self.num_acciones):
            accion = random.choice(self.acciones)

            # Elegimos canchas y horarios aleatoriamente
            cancha = random.randint(0, self.sistema.num_canchas - 1)
            horario = random.randint(0, self.sistema.num_horarios - 1)

            if accion == "reservar":
                self.sistema.reservar(self.user_id, self.priority, cancha, horario)

            elif accion == "cancelar":
                self.sistema.cancelar(self.user_id, cancha, horario)

            elif accion == "modificar":
                # Elegimos una cancha/horario destino distinto
                cancha_dest = random.randint(0, self.sistema.num_canchas - 1)
                horario_dest = random.randint(0, self.sistema.num_horarios - 1)
                self.sistema.modificar(
                    self.user_id,
                    self.priority,
                    cancha, horario,
                    cancha_dest, horario_dest
                )

            # Dormir para simular tiempo de decisión
            time.sleep(random.uniform(1.0, 3.0))  # Ajustar a tu gusto
