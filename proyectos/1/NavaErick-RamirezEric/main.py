from queue import PriorityQueue
from Gato import Gato, TipoGato
from Plato import Plato 
from Dispensador import Dispensador
import threading

def main():
    #creando par de platos
    plato1 = Plato(1)
    plato2 = Plato(2)
    listaPlatos = [plato1, plato2]
    #cola para entrar a los platos
    colaGatos = PriorityQueue()
    print("Hola")
    #instanciando los gatos
    gatoMacho   = Gato("Kermit", TipoGato.MACHO     ,list(listaPlatos),colaGatos)
    gata1       = Gato("Violeta", TipoGato.HEMBRA  ,list(listaPlatos),colaGatos)
    gata2       = Gato("Luna", TipoGato.HEMBRA     ,list(listaPlatos),colaGatos  )
    gata3       = Gato("Zule", TipoGato.HEMBRA  ,list(listaPlatos),colaGatos)
    gata4       = Gato("Suiza", TipoGato.HEMBRA    ,list(listaPlatos),colaGatos)
    gatoInvasor = Gato("GatoInvasor", TipoGato.INVASOR,list(listaPlatos),colaGatos)
    gatos = [gatoMacho, gata1, gata2, gata3, gata4, gatoInvasor]
    print("hola")
    
    
    #instanciando el dispensador con los platos
    dispensador = Dispensador(listaPlatos, gatos, colaGatos)
    #el dispensador ocupa dos hilo durante la ejecución del programa
    threading.Thread(target=dispensador.gestion, daemon=True).start()
    threading.Thread(target=dispensador.run, daemon=True).start()
    #hilo para el metodo gestion y deamon para que se detenga al finalizar el programa
    print("Hola")
    #iniciando los gatos
    for gato in gatos:
        gato.start()
        
main()