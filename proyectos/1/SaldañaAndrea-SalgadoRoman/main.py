import tkinter as tk
from sistema_reservas import SistemaReservas
from usuario import Usuario
from gui import ReservaGUI

def main():
    # Definimos un sistema con 4 canchas y 6 horarios
    sistema = SistemaReservas(num_canchas=4, num_horarios=6)

    # Creamos varios usuarios; unos VIP (prio=2) y otros normales (prio=1)
    users_info = [
        (1, 2), (2, 1), (3, 2), (4, 1),
        (5, 2), (6, 1), (7, 1), (8, 2),
    ]

    hilos = []
    for uid, prio in users_info:
        t = Usuario(user_id=uid, priority=prio, sistema=sistema, num_acciones=20)
        hilos.append(t)
        t.start()

    root = tk.Tk()
    app = ReservaGUI(root, sistema, update_interval=1000)
    root.mainloop()

    for t in hilos:
        t.join()

    print("Todos los hilos han finalizado. Revisa 'acciones.log' para ver el registro de acciones :).")

if __name__ == "__main__":
    main()
