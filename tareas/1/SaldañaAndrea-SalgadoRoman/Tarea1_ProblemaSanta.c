#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <semaphore.h>
#include <unistd.h>



int num_Elfos = 10;
int num_Renos = 9;
int termino_la_navidad = 0;

struct semaphore santa_duerme;
struct semaphore elfos_esperan;
struct semaphore renos_esperan;
struct semaphore mutex_santa_ayudando;


int Elfos_en_espera = 0;
int renos_que_han_llegado = 0;

struct semaphore contador_elfos;
struct semaphore contador_renos;

int main(void) {
    sema_init(&santa_duerme, 1);
    sema_init(&elfos_esperan, 1);
    sema_init(&renos_esperan, 1);
    sema_init(&mutex_santa_ayudando, 1);
    sema_init(&contador_elfos, 1);
    sema_init(&contador_renos, 1);
    // creamos hilo de santa       
    thread_new(&santa);
    // Creamos los hilos de renos y elfos
    for (int i=0; i < num_Renos; i++) {
        thread_new(&reno);
    }

    for (int i=0; i < num_Elfos; i++) {
        thread_new(&elfo);
    }
    
    return 0;
}


void santa() { 
    while (1) {
        printf("Shhh, Santa está descansando 😴😴😴\n");
        sema_down(&elfos_esperan); 
        sema_down(&mutex_santa_ayudando);
        printf("Santa está ayudando a 3 elfos que están en aprietos!\n");
        Elfos_en_espera -= 3;
        sema_up(&mutex_santa_ayudando); 
        sema_up(&contador_elfos);

        if (renos_que_han_llegado == num_Renos) {
            printf("¡Los renos han llegado! Santa está listo para el viaje.\n");
        }
    }
}


void elfo() {
    while (1) {
        sema_down(&contador_elfos); 
        Elfos_en_espera++;

        if (Elfos_en_espera == 3) {
            printf("¡Tres elfos están pidiendo ayuda a Santa!\n");
            sema_up(&elfos_esperan);
            sema_down(&mutex_santa_ayudando);
            printf("Santa está ayudando a 3 elfos que están en aprietos!\n");
            Elfos_en_espera -= 3;
            sema_up(&contador_elfos);
        } else {
            sema_up(&contador_elfos);
        }
    }
}


void reno() {
    while (1) {
        sema_down(&contador_renos); 
        renos_que_han_llegado++;

        if (renos_que_han_llegado == num_Renos) {
            printf("¡Todos los renos han llegado! Santa está listo para el viaje.\n");
            sema_up(&santa_duerme);
        } else {
            sema_up(&contador_renos);
        }

        sleep(1);
    }
}
