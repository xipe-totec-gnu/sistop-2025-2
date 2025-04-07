#Este programa simula la conexión de varios jugadores a un servidor.
#Al principio, se generan 24 jugadores, los cuales intentan entrar a un servidor de máximo 12 jugadores.
#Cada 20 segundos, entra un nuevo jugados a la cola de jugadores que quieren entrar al servidor.
#Entrando ya al servidor, los jugadores permanecen de 10 a 30 segundos.
#En lo que permanecen en el servidor, los jugadores acumulan kills or muertes.
#Si su KD actual es mayor a 2.0, reciben una recompenza de 100 monedas por cada kill.
#La ventana muestra una sección con los jugadores en la cola de espera, los que se encuentran jugando, y el historial de eventos.

#Por arreglar:
#Errores en la implementación del semaforo. En ocasiones se muestran más de 12 jugadores conectados en el servidor.
#Reducir el número de eventos que aparecen en el historial, es dificil de interpretar lo que está sucediendo.
#Balancear tasa de nuevos jugadores contra jugadores que se salen del servidor. Se acaban muy rápido los jugadores.
#Mejorar la estética de la ventana.
#Comentar código.

from tkinter import Tk
from servidor import Servidor
from ui import Interfaz

if __name__ == "__main__":
    root = Tk()
    servidor = Servidor()
    app = Interfaz(root, servidor)
    root.mainloop()

