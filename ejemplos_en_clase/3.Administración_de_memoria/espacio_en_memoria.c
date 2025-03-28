/* #include <stdio.h> */
/* #include <stdlib.h> */
char *cadena;
int ejemplo = 10;

/* Este programa es para ilustrar qué tipo de datos van a parar a cuál de las
   secciones de memoria. pueden ver que hay algunas instrucciones comentadas,
   esto es porque ilustré el funcionamiento utilizando _progvis_
   (https://storm-lang.org/Programs/Progvis.html), que es un simulador basado en
   un subconjunto de C. Si quieres compilar este código para C _real_, hay que
   activar los #includes (arriba), y cambiar los "print" por los "printf". ¡Ah!
   Y reemplazar la llamada a thread_new() por _otra cosa_ ;-)

   cadena y ejemplo son declarados globalmente, su asignación forma parte de la
   sección de _datos_

   La cadena "%d" que aparece en main() también forma parte de la sección de
   datos

   La función "func2" se compila, y el punto de inicio de su ejecución forma
   también parte de la sección de datos. */

int func2(int *var) {
  return *var = 25;
}

void un_hilo(int num) {
  /* un_hilo es llamado con thread_new. Cada hilo “constituye” su propio
     stack. */

  print(num);
}

void main() {
  int var1 = 100;
  int var2 = 100;
  int arr1[5] = {1,2,3,4,5};
  /* Todas las variables definidas dentro de una función forman parte de su
     stack */

  int *var3 = malloc(5 * sizeof(int));
  free(var3);
  var3 = malloc(10 * sizeof(int));
  free(var3);
  var3 = malloc(sizeof(int));
  /* var3 es un apuntador a entero. var3 mismo está en el stack de main(), pero
     el valor apuntado está en libres (heap). */

  func2(var3);
  /* printf("%016x: %d\n",var3, *var3); */
  print(*var3);
  free(var3);
  /* printf("%016x: %d\n",var3, *var3); */


  for (int i = 0; i < 5; i++)
    thread_new(&un_hilo, i);
}

