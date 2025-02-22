#include <stdio.h>

int main () {
    int n = 6;

    printf("Hola.\n");
    for(int i = 0; i < n; i++) {
        for(int j = i; j >= 0; j--) {

            printf("o");
        }
        printf("\n");
    }
}
