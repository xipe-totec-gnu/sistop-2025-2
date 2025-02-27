#include <stdio.h>
#include <string.h>

int main(int argc, char *argv[]) {
  if (argc > 1) {
    printf("Hola, %s!\n", argv[1]);
  } else {
    printf("Hola, Mundo!\n");
  }
  return 0;
}


