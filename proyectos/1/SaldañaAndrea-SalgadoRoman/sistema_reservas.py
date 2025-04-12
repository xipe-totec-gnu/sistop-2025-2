import threading
from collections import defaultdict

class SistemaReservas:
    """
    Clase que administra las canchas, sus horarios y la sincronización con Locks.
    Incluye:
      - estado_canchas: matriz con (user_id, priority) o None.
      - lock_canchas: evita race conditions al modificar estado_canchas.
      - lock_logs: protege la escritura de logs en archivo.
      - log_queue: (opcional) si se desea mostrar acciones en vivo en la GUI.
      - stats_reservas: lleva el conteo de reservas exitosas por user_id.
    """

    def __init__(self, num_canchas=3, num_horarios=8):
        """
        Inicializa el sistema de reservas:
          - estado_canchas: 2D [cancha][horario].
          - stats_reservas: dict para contar reservas exitosas de cada usuario.
        """
        self.num_canchas = num_canchas
        self.num_horarios = num_horarios

        # Cada celda contendrá (user_id, priority) o None si está libre
        self.estado_canchas = [
            [None for _ in range(num_horarios)]
            for _ in range(num_canchas)
        ]

        # Para exclusión mutua en la estructura de canchas
        self.lock_canchas = threading.Lock()
        # Para escribir en el log
        self.lock_logs = threading.Lock()

        self.log_queue = None

        # Contador de reservas exitosas 
        self.stats_reservas = defaultdict(int)

        with open("acciones.log", "w", encoding="utf-8") as f:
            f.write("==== Log de acciones de reservas ====\n")

    def set_log_queue(self, queue_obj):
        """
        Permite que la GUI pase una cola (Queue) para recibir los logs y mostrarlos en tiempo real.
        """
        self.log_queue = queue_obj

    def reservar(self, user_id, priority, cancha, horario):
        """
        Intenta reservar la cancha-horario con la prioridad dada.
        Retorna True si la reserva fue exitosa, False en caso contrario.
        """
        with self.lock_canchas:
            actual = self.estado_canchas[cancha][horario]
            if actual is None:
                self.estado_canchas[cancha][horario] = (user_id, priority)
                self.stats_reservas[user_id] += 1
                self._log_accion(f"Usuario {user_id} (prio={priority}) reservó cancha {cancha} horario {horario}")
                return True
            else:
                # Ocupada, revisamos prioridades
                (ocupante_id, ocupante_prio) = actual
                if priority > ocupante_prio:
                    # Desbanca al ocupante
                    self.estado_canchas[cancha][horario] = (user_id, priority)
                    self.stats_reservas[user_id] += 1
                    self._log_accion(
                        f"Usuario {user_id} (prio={priority}) DESBANCÓ a usuario {ocupante_id} (prio={ocupante_prio}) "
                        f"en cancha {cancha}, horario {horario}"
                    )
                    return True
                else:
                    # No puede reservar
                    self._log_accion(
                        f"Usuario {user_id} (prio={priority}) NO pudo reservar cancha {cancha}, "
                        f"ocupada por {ocupante_id} (prio={ocupante_prio})"
                    )
                    return False

    def cancelar(self, user_id, cancha, horario):
        """
        Cancela la reserva si pertenece a user_id.
        Retorna True si se canceló, False si no pertenecía a user_id o estaba libre.
        """
        with self.lock_canchas:
            actual = self.estado_canchas[cancha][horario]
            if actual is not None:
                (ocupante_id, ocupante_prio) = actual
                if ocupante_id == user_id:
                    self.estado_canchas[cancha][horario] = None
                    self._log_accion(
                        f"Usuario {user_id} canceló reserva de cancha {cancha}, horario {horario}"
                    )
                    return True
                else:
                    self._log_accion(
                        f"Usuario {user_id} intentó cancelar reserva de otro usuario ({ocupante_id}) "
                        f"en cancha {cancha}, horario {horario}"
                    )
                    return False
            else:
                self._log_accion(
                    f"Usuario {user_id} intentó cancelar, pero cancha {cancha}, horario {horario} estaba libre."
                )
                return False

    def modificar(self, user_id, priority, cancha_orig, horario_orig, cancha_dest, horario_dest):
        """
        Modifica la reserva: libera la original (si pertenece a user_id) y
        reserva la nueva posición (con la misma prioridad).
        Retorna True si la modificación fue exitosa, False si falla.
        """
        with self.lock_canchas:
            actual = self.estado_canchas[cancha_orig][horario_orig]
            if actual is not None:
                (ocupante_id, ocupante_prio) = actual
                if ocupante_id == user_id:
                    # Revisamos si la nueva está libre o con menor prioridad
                    destino = self.estado_canchas[cancha_dest][horario_dest]
                    if destino is None:
                        # Simplemente reservamos
                        self.estado_canchas[cancha_orig][horario_orig] = None
                        self.estado_canchas[cancha_dest][horario_dest] = (user_id, priority)
                        self.stats_reservas[user_id] += 1
                        self._log_accion(
                            f"Usuario {user_id} modificó su reserva de cancha {cancha_orig}, h:{horario_orig} "
                            f"a cancha {cancha_dest}, h:{horario_dest}"
                        )
                        return True
                    else:
                        (dest_id, dest_prio) = destino
                        if priority > dest_prio:
                            # Desbanca
                            self.estado_canchas[cancha_orig][horario_orig] = None
                            self.estado_canchas[cancha_dest][horario_dest] = (user_id, priority)
                            self.stats_reservas[user_id] += 1
                            self._log_accion(
                                f"Usuario {user_id} (prio={priority}) modificó su reserva y DESBANCÓ a "
                                f"{dest_id} (prio={dest_prio}) en cancha {cancha_dest}, horario {horario_dest}"
                            )
                            return True
                        else:
                            self._log_accion(
                                f"Usuario {user_id} NO pudo modificar, destino ocupado "
                                f"por {dest_id} (prio={dest_prio}) con mayor o igual prioridad."
                            )
                            return False
                else:
                    self._log_accion(
                        f"Usuario {user_id} intentó modificar una reserva que pertenece a {ocupante_id} "
                        f"(cancha {cancha_orig}, horario {horario_orig})"
                    )
                    return False
            else:
                self._log_accion(
                    f"Usuario {user_id} intentó modificar, pero no había reserva en cancha {cancha_orig}, "
                    f"horario {horario_orig}"
                )
                return False

    def get_stats_string(self):
        """
        Retorna un string con las estadísticas de reservas exitosas por usuario.
        """
        with self.lock_canchas:
            if not self.stats_reservas:
                return "Sin reservas exitosas aún."
            # Ordenamos por user_id solo para mostrar
            lines = []
            for uid in sorted(self.stats_reservas.keys()):
                count = self.stats_reservas[uid]
                lines.append(f"Usuario {uid}: {count} reservas exitosas")
            return "\n".join(lines)

    def _log_accion(self, mensaje):
        """
        Registra la acción en acciones.log usando lock_logs para evitar colisiones
        y, además, lo envía a la cola de la GUI (si existe) para mostrarlo en tiempo real.
        """
        with self.lock_logs:
            with open("acciones.log", "a", encoding="utf-8") as f:
                f.write(mensaje + "\n")

        if self.log_queue:
            self.log_queue.put(mensaje)
