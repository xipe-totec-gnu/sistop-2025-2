#include <stdio.h>

int main()
{
    char nombre[100];
    printf("Ingresa tu nombre\n");  
    if (fgets(nombre, sizeof(nombre), stdin) != NULL) { 
        printf("Hola %s¿Cómo estas?\n", nombre); 
    } else { 
        printf("\n"); 
    }

    return 0;
}
