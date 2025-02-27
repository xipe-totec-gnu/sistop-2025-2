#include <stdio.h>

int main()
{
    char test[10]; 
    printf("Hola! Ingresa tu nombre: ");
    scanf("%s", &test);
    
    printf("\nHola %s, buen día", test);
    return 0;
}
