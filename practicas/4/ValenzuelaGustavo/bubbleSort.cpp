#include <iostream>
#include <vector>

void bubbleSort(std::vector<int>& arr) {
    int n = arr.size();
    bool cambiados;

    for (int i = 0; i < n - 1; ++i) {
        cambiados = false;
        for(int j=i; j<n-1; j++){
            if(arr[j] > arr[j + 1]){
                std::swap(arr[j],arr[j+1]);
            }
        }
    }
}

int main() {
    std::vector<int> arr;
    int n;

    std::cout<<"Ingresa el tamaño del  arreglo: ";
    std::cin>>n;
    std::cout<<"Ingresa el arreglo\n";
    for(int i=0; i<n; i++){\
        int tmp; std::cin>>tmp;
        arr.push_back(tmp);
    }

    bubbleSort(arr);

    std::cout << "Arreglo ordenado: ";
    for (int num : arr) {
        std::cout << num << " ";
    }
    std::cout << "\n";

    return 0;
}
