#include <stdio.h>

int main () {
    int n;
    printf("Ingresa el tamaño de la piramide: ");
    scanf("%d", &n);

    printf("Hola.\n");
    for(int i = 0; i < n; i++) {
        for(int j = i; j >= 0; j--) {

            printf("o");
        }
        printf("\n");
    }
}
