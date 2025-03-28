#include <stdio.h>

void main() {
  int a = 1;
  for (int i=0; i<=100; i++)
    a += a;
  printf("El valor final de a es: %d\n", a);
}
