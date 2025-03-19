#include <iostream>
#include <thread>
#include <vector>

using namespace std;

void multiplicacion(int a, int b, int &res){
    res=a*b;
}

int main(){
    //declaracion de vectores
    vector<int>resultados(3);
    vector<thread> hilos;
    //llamado a la funcions y realizacion de la multiplicacion
    for(int i = 0; i<3; i++){
        hilos.push_back(thread(multiplicacion, i+2,i+3,ref(resultados[i])));
    }
    //terminacion
    for(auto &hilos:hilos){
        hilos.join();
    }
    //imprimir resultados
    for(int i=0;i<3;i++){
        cout << "Resultado de la primer multiplicacion: " << resultados[i] << endl;
    }
    
    
    return 0;
}
