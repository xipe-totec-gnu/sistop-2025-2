#include <stdio.h>

void main() {
  char valores[12];
  for (int i=0; i<12; i++)
    valores[i] = 65 + i;
  valores[9] = 0;
  printf("Los valores que hay en el arreglo son:\n%s\n", valores);
}
