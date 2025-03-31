/*Autores:
	Nava Benítez David Emilio
	Tavera Castillo David Emmanuel
Proyecto 1
SO		Gpo: 6
*/
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <semaphore.h>
#include <unistd.h>
#include <time.h>

#define TOTAL_IMPRESORAS 8
#define IMPRESORAS_DISPONIBLES 5

sem_t impresora;

void *tarea(void *arg) {
    int id = *(int *)arg;
    free(arg);
    printf("Usuario %d esperando su turno...\n", id);
    sem_wait(&impresora);

    unsigned int seed = time(NULL) + id * 31; // Semilla más variable
    srand(seed);
    int accion = rand() % 3;
    switch (accion) {
        case 0:
            printf("Usuario %d esta imprimiendo...\n", id);
            sleep(2);
            break;
        case 1:
            printf("Usuario %d esta sacando copias...\n", id);
            sleep(3);
            break;
        case 2:
            printf("Usuario %d esta escaneando...\n", id);
            sleep(4);
            break;
    }
    
    printf("Usuario %d ha terminado su tarea.\n", id);
    sem_post(&impresora);
    return NULL;
}

int main() {
    pthread_t usuarios[10];
    sem_init(&impresora, 0, IMPRESORAS_DISPONIBLES);
    int i;
    for ( i = 0; i < 10; i++) {
        int *id = malloc(sizeof(int));
        *id = i + 1;
        pthread_create(&usuarios[i], NULL, tarea, id);
        usleep(100000);
    }
    
    for ( i = 0; i < 10; i++) {
        pthread_join(usuarios[i], NULL);
    }
    
    sem_destroy(&impresora);
    return 0;
}
