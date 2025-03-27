/*Autores:
          Nava Benítez David Emilio
          Tavera Castillo David Emmanuel
Tarea 1
SO Gpo: 6
*/         
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <semaphore.h>
#include <unistd.h>
#include <time.h>

#define NUM_AUTOS 5   
#define IZQUIERDA 0
#define DERECHA 1 
#define RECTO 2

sem_t cuadrante[4]; // Un semáforo por cada cuadrante

typedef struct {
    int id;
    int direccion;  // 0: Izquierda, 1: Derecha, 2: Recto
    int entrada;    // 0: Norte, 1: Este, 2: Sur, 3: Oeste
} Auto;

void solicitar_cuadrantes(Auto a);
void liberar_cuadrantes(Auto a);
void* auto_cruza(void* arg);

int main() {
    pthread_t autos[NUM_AUTOS];//arreglo de hilos (autos)
    srand(time(NULL));
    int i;

    // Inicialización de los semáforos de cada cuadrante
    for (i = 0; i < 4; i++) {
        sem_init(&cuadrante[i], 0, 1);
    }

    // Crear los autos (hilos) en memoria dinámica
    for (i = 0; i < NUM_AUTOS; i++) {
        Auto* a = malloc(sizeof(Auto));
        if (!a) {
            perror("Error asignando memoria");
            exit(1);
        }
        a->id = i + 1;
        a->entrada = rand() % 4;     // Entrada aleatoria: Norte, Este, Sur u Oeste
        a->direccion = rand() % 3;   // Dirección aleatoria: Izquierda, Derecha o Recto

        pthread_create(&autos[i], NULL, auto_cruza, a);
        
    }

    for (i = 0; i < NUM_AUTOS; i++) {
        pthread_join(autos[i], NULL);
    }

    for (i = 0; i < 4; i++) {
        sem_destroy(&cuadrante[i]);
    }

    return 0;
}

// Mapea la entrada a los cuadrantes usados en cada dirección
void solicitar_cuadrantes(Auto a) {
    int q1, q2, q3;

    if (a.entrada == 0) {  // Norte
        q1 = 0; q2 = 1; q3 = 2;
    } else if (a.entrada == 1) {  // Este
        q1 = 1; q2 = 2; q3 = 3;
    } else if (a.entrada == 2) {  // Sur
        q1 = 2; q2 = 3; q3 = 0;
    } else {  // Oeste
        q1 = 3; q2 = 0; q3 = 1;
    }

    if (a.direccion == DERECHA) {  // Giro a la derecha (1 cuadrante)
        sem_wait(&cuadrante[q1]);
    } else if (a.direccion == RECTO) {  // Seguir recto (2 cuadrantes)
        sem_wait(&cuadrante[q1]);
        sem_wait(&cuadrante[q2]);
    } else if (a.direccion == IZQUIERDA) {  // Giro a la izquierda (3 cuadrantes)
        sem_wait(&cuadrante[q1]);
        sem_wait(&cuadrante[q2]);
        sem_wait(&cuadrante[q3]);
    }
}

// Libera los cuadrantes en orden inverso para evitar bloqueos y que los autos esperando puedan tomar el semáforo
void liberar_cuadrantes(Auto a) {
    int q1, q2, q3;

    if (a.entrada == 0) {
        q1 = 0; q2 = 1; q3 = 2;
    } else if (a.entrada == 1) {
        q1 = 1; q2 = 2; q3 = 3;
    } else if (a.entrada == 2) {
        q1 = 2; q2 = 3; q3 = 0;
    } else {
        q1 = 3; q2 = 0; q3 = 1;
    }

    if (a.direccion == DERECHA) {
        sem_post(&cuadrante[q1]);
    } else if (a.direccion == RECTO) {
        sem_post(&cuadrante[q2]);
        sem_post(&cuadrante[q1]);
    } else if (a.direccion == IZQUIERDA) {
        sem_post(&cuadrante[q3]);
        sem_post(&cuadrante[q2]);
        sem_post(&cuadrante[q1]);
    }
}

// Simulación de autos cruzando la intersección
void* auto_cruza(void* arg) {
    Auto* a = (Auto*)arg;

    printf("Auto %d llega desde %s y quiere ir %s.\n",
           a->id,
           (a->entrada == 0) ? "Norte" : (a->entrada == 1) ? "Este" : (a->entrada == 2) ? "Sur" : "Oeste",
           (a->direccion == IZQUIERDA) ? "Izquierda" : (a->direccion == DERECHA) ? "Derecha" : "Recto");

    solicitar_cuadrantes(*a);  // Toma los cuadrantes necesarios para el giro

    printf("Auto %d cruzando la interseccion...\n", a->id);
    sleep(1);

    printf("Auto %d ha salido de la interseccion.\n", a->id);
    liberar_cuadrantes(*a);  // Libera los cuadrantes ocupados

    free(a); //liberación de memoria (importante para evitar basura en memoria)
    return NULL;
}


