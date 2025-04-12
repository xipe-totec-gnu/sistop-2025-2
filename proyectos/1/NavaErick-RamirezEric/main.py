from queue import PriorityQueue
from Gato import Gato, TipoGato
from Plato import Plato 
from Dispensador import Dispensador
from threading import Lock
def main():
    #creando par de platos
    plato1 = Plato(1)
    plato2 = Plato(2)
    listaPlatos = [plato1, plato2]
    
    #instanciando los gatos
    gatoMacho = Gato("Kermit", TipoGato.MACHO)
    gata1 = Gato("Violeta", TipoGato.HEMBRA)
    gata2 = Gato("Luna", TipoGato.HEMBRA)
    gata3 = Gato("Violeta", TipoGato.HEMBRA)
    gata4 = Gato("Suiza", TipoGato.HEMBRA)
    gatoInvasor = Gato("GatoInvasor", TipoGato.INVASOR)
    gatos = [gatoMacho, gata1, gata2, gata3, gata4, gatoInvasor]
    
    #cola para entrar a los platos
    colaGatos = PriorityQueue()
    
    #instanciando el dispensador con los platos
    dispensador = Dispensador(listaPlatos, gatos, colaGatos)
    
    #iniciando los gatos
    for gato in gatos:
        gato.start()
        
main()