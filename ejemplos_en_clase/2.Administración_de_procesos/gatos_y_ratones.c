int num_gatos = 2;
int num_ratones = 1;
int num_platos = 2;
struct semaphore mut_plato0;
struct semaphore mut_plato1;
struct semaphore mut_plato2;

struct semaphore mut_cuarto;
int gatos_en_cuarto = 0;
int ratones_en_cuarto = 0;
struct semaphore contador_gatos;
struct semaphore contador_ratones;

int main(void) {
  sema_init(&mut_plato0, 1);
  sema_init(&mut_plato1, 1);
  sema_init(&mut_plato2, 1);
  sema_init(&mut_cuarto, 1);
  sema_init(&contador_gatos, 1);
  sema_init(&contador_ratones, 1);

  for (int i=0; i < num_gatos; i++) {
    thread_new(&gato);
  }

  for (int i=0; i < num_ratones; i++) {
    thread_new(&raton);
  }

  return 0;
}

void come(int plato, int ident) {
  if (plato == 0) sema_down(&mut_plato0);
  else if (plato == 1) sema_down(&mut_plato1);
  else if (plato == 2) sema_down(&mut_plato2);
  if (ident == 0) {
    printf("GATO: Comiendo del plato %d...\n", plato);
  } else {
    printf("RATON: Comiendo del plato %d...\n", plato);
  }
  if (plato == 0) sema_up(&mut_plato0);
  else if (plato == 1) sema_up(&mut_plato1);
  else if (plato == 2) sema_up(&mut_plato2);
}

void duerme(int ident) {
  if (ident == 0) {
    printf("GATO durmiendo...\n");
  } else {
    printf("RATON durmiendo...\n");
  }
}

void gato() {
  int mi_plato = 0;
  int ident = 0;
  while (1) {
    duerme(ident);
    /* Verificamos y obtenemos el apagador */
    sema_down(&contador_gatos);
    gatos_en_cuarto++;
    if (gatos_en_cuarto == 1) {
      sema_down(&mut_cuarto);
      printf("El comedor está reservado para los GATOS\n");
    }
    sema_up(&contador_gatos);

    sema_down(&contador_ratones);
    if (ratones_en_cuarto > 0) {
      printf("¡UN ASQUEROSO RATÓÓÓÓÓÓÓÓÓN!\n");
      printf("Hagamos de cuenta que me lo estoy comiendo :-Þ\n");
    }
    sema_up(&contador_ratones);

    come(mi_plato, ident);
    /* Verificamos y liberamos el apagador */
    sema_down(&contador_gatos);
    gatos_en_cuarto--;
    if (gatos_en_cuarto == 0) {
      sema_up(&mut_cuarto);
      printf("El comedor está libre.\n");
    }
    sema_up(&contador_gatos);

    mi_plato = mi_plato + 1 % num_platos;
  }
}

void raton() {
  int mi_plato = 0;
  int ident = 1;
  while (1) {
    duerme(ident);
    /* Me registro como ratón en el cuarto... */
    sema_down(&contador_ratones);
    ratones_en_cuarto++;
    /* if (ratones_en_cuarto == 1) { */
    /*   sema_down(&mut_cuarto); */
    /*   printf("El comedor está reservado para los RATONES\n"); */
    /* } */
    sema_up(&contador_ratones);

    sema_down(&mut_cuarto);
    come(mi_plato, ident);
    sema_up(&mut_cuarto);
    mi_plato = mi_plato + 1 % num_platos;

    /* Verificamos y liberamos el apagador */
    sema_down(&contador_ratones);
    ratones_en_cuarto--;
    /* if (ratones_en_cuarto == 0) { */
    /*   sema_up(&mut_cuarto); */
    /*   printf("El comedor está libre.\n"); */
    /* } */
    sema_up(&contador_ratones);


  }
}
