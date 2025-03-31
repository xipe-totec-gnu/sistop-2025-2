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
//Semaforo para controlar el acceso a una impresora

sem_t impresora;
int impresoras_funcionales;

void *tarea(void *arg);
int obtenerEntero(char *mensaje, int min, int max);
int main() {
    pthread_t usuarios[10];//10 hilos que es la cantidad de usuarios
    int num_impresoras, i;
    
    num_impresoras = obtenerEntero("Ingrese el numero total de copiadoras: ", 1, TOTAL_IMPRESORAS);
    impresoras_funcionales = obtenerEntero("Ingrese el numero de copiadoras funcionales: ", 1, num_impresoras);
    
    sem_init(&impresora, 0, impresoras_funcionales);
    srand(time(NULL));
    
    for (i = 0; i < 10; i++) {
        int *id = malloc(sizeof(int));
        *id = i + 1;
        pthread_create(&usuarios[i], NULL, tarea, id);
        usleep(100000);
    }
    
    for (i = 0; i < 10; i++) {
        pthread_join(usuarios[i], NULL);
    }
    
    sem_destroy(&impresora);
    return 0;
}

void *tarea(void *arg){
    int id = *(int *)arg;
    free(arg);
    printf("Usuario %d esperando su turno...\n", id);
    sem_wait(&impresora);

    unsigned int seed = time(NULL) + id * 31; 
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

//validación de entradas 
int obtenerEntero(char *mensaje, int min, int max) {
    int valor;
    char c;
    while (1) {
        printf("%s", mensaje);
        if (scanf("%d", &valor) != 1) {
            printf("Entrada invalida. Intente nuevamente.\n");
            while ((c = getchar()) != '\n' && c != EOF); // Limpiar buffer
        } else if (valor < min || valor > max) {
            printf("Numero fuera de rango. Intente nuevamente.\n");
        } else {
            return valor;
        }
    }
}

