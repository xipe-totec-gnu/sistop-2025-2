#include <stdio.h>
#include <pthread.h>
#include <semaphore.h>

int num_hackers=2;
int num_serfs=2;

//struct semaphore barrera;			//barrera que contara que solo haya 4 pasajeros
//int num_hilos=4;
//int contador;
//struct semaphore mutexbarrera;		//mutex para el contador

int nhacker=0;
int nserf=0;

struct semaphore mutex;				//mutex
struct semaphore colahacker;		//cola para contar el numero de hackers en el barco
struct semaphore colaserf;			//cola para contar el numero de serfs en el barco


void hacker(){
	
	int id=0;
	sema_down(&mutex);
	nhacker++;	
	
	if(nhacker ==4){
		sema_up(&colahacker);
		sema_up(&colahacker);
		sema_up(&colahacker);
		sema_up(&colahacker);
		bote();
		nhacker=0;
	}else if (nhacker==2 && nserf>=2){
		sema_up(&colahacker);
		sema_up(&colahacker);
		sema_up(&colaserf);
		sema_up(&colaserf);
		bote();
		nhacker=0;
		nserf-=2;
	}else{
		sema_up(&mutex);
		sema_down(&colahacker);
	}
	
	sema_up(&mutex);
	
}	

void serf(){
	
	int id=1;
	sema_down(&mutex);
	nserf++;	
	
	if(nserf ==4){
		sema_up(&colaserf);
		sema_up(&colaserf);
		sema_up(&colaserf);
		sema_up(&colaserf);
		nserf=0;
		bote();
	}else if (nserf==2 && nhacker>=2){
		sema_up(&colaserf);
		sema_up(&colaserf);
		sema_up(&colahacker);
		sema_up(&colahacker);
		bote();
		nserf=0;
		nhacker-=2;
	}else{
		sema_up(&mutex);
		sema_down(&colaserf);
	}
	
	abordar();
	sema_up(&mutex);
}

void abordar(int id){
	if(id==0){
		printf("hola soy un hacker en el bote.:p\n");
	}else{
		printf("hola soy un serf en el bote.:>\n");
	}
}

void bote(){
	printf("nos vamos. :):):):)");
}

int main(void){

	sema_init(&mutex,1);
	sema_init(&colahacker,0);
	sema_init(&colaserf,0);
	
	for (int i= 0; i<num_hackers;i++){		//creamos hackers
		thread_new(&hacker);
	}
	for (int i=0; i<num_serfs; i++){		//creamos serfs
		thread_new(&serf);
	}
		
	return 0;
}


