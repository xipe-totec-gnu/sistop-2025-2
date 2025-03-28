#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <semaphore.h>
#include <unistd.h>

int numRenos = 9;
int renosEsperando = 0;
int numElfos = 30;
int elfosEsperando = 0;

sem_t mutRen;
sem_t mutElf;
sem_t barreraElfos;
sem_t barreraRenos;

void actividad(int ident) {
    if (ident == 0) {
        printf("El reno se va de vacaciones a la playa asifonyuuuuu...\n");
    } else {
        printf("El elfo se pone a armar juguetes....\n");
    }
}

// Función que ejecuta cada hilo de reno
void *reno(void *arg) {
    int ident = 0;
    while (1) {
        actividad(ident);
        // Los renos regresan de sus vacaciones y esperan en la habitación de Santa
        sem_wait(&mutRen);
        printf("El reno ya regresó.....\n");
        renosEsperando++;
        printf("El número de renos esperando afuera de la habitación de Santa son: %d\n", renosEsperando);

        if (renosEsperando == numRenos) {
            sem_post(&barreraRenos);  // Desbloquea la barrera
            printf("Santa ha ido a entregar juguetes, ¡FELIZ NAVIDAD!\n");
            renosEsperando = 0;
        }
        sem_post(&mutRen);
        sleep(1);
    }
    return NULL;
}

// Función que ejecuta cada hilo de elfo
void *elfo(void *arg) {
    int ident = 1;
    while (1) {
        actividad(ident);
        // Los elfos esperan su turno para hablar con Santa
        sem_wait(&mutElf);
        elfosEsperando++;
        printf("El número de elfos que requieren ayuda de Santa son: %d\n", elfosEsperando);

        // Los elfos esperan hasta que haya al menos 3 y que los renos sean menores de 9
        if (elfosEsperando == 3 && renosEsperando < 9) {
            sem_post(&barreraElfos); // Desbloquea a los elfos
            printf("Los 3 elfos recibieron ayuda de Santa....\n");
            elfosEsperando = 0;
        } else {
            printf("Santa no está disponible....\n");
        }
        sem_post(&mutElf);
        sleep(1); // Simula la espera entre acciones
    }
    return NULL;
}

int main(void) {
    pthread_t hilosRenos[numRenos];
    pthread_t hilosElfos[numElfos];
    

    // Inicialización de semáforos
    sem_init(&mutElf, 0, 1);
    sem_init(&mutRen, 0, 1);
    sem_init(&barreraElfos, 0, 0);
    sem_init(&barreraRenos, 0, 0);

    // Crear los hilos para los renos
    for (int i = 0; i < numRenos; i++) {
        if (pthread_create(&hilosRenos[i], NULL, reno, NULL) != 0) {
            perror("Error al crear hilo de reno");
            exit(1);
        }
    }

    // Crear los hilos para los elfos
    for (int i = 0; i < numElfos; i++) {
        if (pthread_create(&hilosElfos[i], NULL, elfo, NULL) != 0) {
            perror("Error al crear hilo de elfo");
            exit(1);
  
        }
    }

    // Esperar que todos los hilos de renos terminen
    for (int i = 0; i < numRenos; i++) {
        pthread_join(hilosRenos[i], NULL);
    }

    // Esperar que todos los hilos de elfos terminen
    for (int i = 0; i < numElfos; i++) {
        pthread_join(hilosElfos[i], NULL);
    }

    // Liberar los semáforos al final
    sem_destroy(&mutElf);
    sem_destroy(&mutRen);
    sem_destroy(&barreraElfos);
    sem_destroy(&barreraRenos);

    return 0;
}

