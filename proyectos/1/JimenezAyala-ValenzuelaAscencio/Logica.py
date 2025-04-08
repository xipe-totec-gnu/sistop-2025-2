from Cliente import *

if __name__ == "__main__":
    NUM_CLIENTES = 10
    NUM_PLATOS = 3

    champion = Champion()
    platos = Platos(NUM_PLATOS)

    clientes = [Cliente(i, champion, platos) for i in range(NUM_CLIENTES)]

    for c in clientes:
        c.start()
    for c in clientes:
        c.join()

    print("FIN.")



