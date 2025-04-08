from Platos import *

# Heredamos de la clase Thread
class Cliente(threading.Thread):
    # Constructor
    def __init__(self, id, champion, platos):
        super().__init__() # Llamamos al constructor del padre
        self.id = id # Asignamos el id del cliente
        self.champion = champion # Mandamos al champion?
        self.platos = platos # Mandamos el plato
        self.etapa = 0  # 0: no ha pedido, 1: pidió, 2: comió
        self.max_intentos = 3 # Si hace algo mal,puede volver a intentar comprar máximo 3 veces

    # Ejecución del hilo
    def run(self):
        intentos = 0
        # Mientras esté dentro de sus intentos permitidos, ejecutamos
        while intentos < self.max_intentos:
            intentos += 1 # Incrementamos un intento
            print(f"[Cliente {self.id}] Intento #{intentos}")

            # Intento de desorden (Más adelante lo haremos por etapas)
            if random.random() < 0.1: # 10% de probabilidad
                print(f"[Cliente {self.id}] Intentó hacer trampa (desorden). Rechazado.")
                self.esperarReintento() # Mandar a esperar un reintento
                continue

            # Paso 1: Pedir
            self.champion.servir_tacos(self.id)

            # Paso 2: Comer
            print(f"[Cliente {self.id}] Esperando un plato...")
            self.platos.tomar(self.id) # Tomamos un plato
            print(f"[Cliente {self.id}] Comiendo tacos.")
            time.sleep(random.uniform(0.3, 0.6))
            self.platos.devolver() # Devolvemos el plato

            # Paso 3: Pagar (quizá mal)
            pago_correcto = random.random() > 0.15 # 85% de probabilidad de pagar la cantidad correcta
            pago_aceptado = self.champion.cobrar(self.id, pago_correcto)

            # Condicional para el pago
            if pago_aceptado:
                print(f"[Cliente {self.id}] Completó su visita con éxito. ✅\n")
                break
            else:
                self.esperarReintento() # Enviar a reintento

        # Si llegamos a la cantidad máxima, el hilo se detiene
        if intentos == self.max_intentos:
            print(f"[Cliente {self.id}] Fue expulsado por intentos fallidos. ❌")

    def esperarReintento(self):
        wait_time = random.uniform(0.5, 1.0)
        print(f"[Cliente {self.id}] Esperando {wait_time:.2f}s para reintentar...\n")
        time.sleep(wait_time)
            