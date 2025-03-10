#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>
#include <time.h>

void *thread_function(void *arg) {
    sleep(1);
    int pid = getpid();
    pthread_t tid = pthread_self();
    printf("Hello from pid %d and tid %lu at %ld\n", pid, tid, time(NULL));
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        printf("Usage: %s <number of threads>\n", argv[0]);
        return 1;
    }

    int thread_num = atoi(argv[1]);

    printf("Initial time: %ld\n", time(NULL));

    pthread_t threads[thread_num];
    for (int i = 0; i < thread_num; i++) {
        pthread_create(&threads[i], NULL, thread_function, NULL);
    }

    for (int i = 0; i < thread_num; i++) {
        pthread_join(threads[i], NULL);
    }

    printf("Final time: %ld\n", time(NULL));
    return 0;
}