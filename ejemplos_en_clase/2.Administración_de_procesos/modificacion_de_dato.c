#include <stdio.h>

void main() {
  int uno = 1;
  int dos = 2;
  int tres;

  tres = uno + dos;

  printf("%d mas %d es igual a %d\n", uno, dos, tres);

  uno++;
  tres = uno + dos;
  printf("Pero ahora, %d mas %d es igual a %d\n", uno, dos,tres);
}
