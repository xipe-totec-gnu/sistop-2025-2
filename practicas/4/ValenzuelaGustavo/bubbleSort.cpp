#include <iostream>
#include <vector>
#include <thread>
#include <mutex>
#include <atomic>

std::mutex mtx;

void deboIntercambiar(std::vector<int>& arr, int i, std::atomic<bool>& cambiados) {
    if (arr[i] > arr[i + 1]) {
        std::lock_guard<std::mutex> lock(mtx);
        std::swap(arr[i], arr[i + 1]);
        cambiados = true;
    }
}

void bubbleSortParalelo(std::vector<int>& arr) {
    int n = arr.size();

    bool huboCambios;
    do {
        huboCambios = false;
        std::atomic<bool> cambiados(false);
        std::vector<std::thread> hilos;

        for (int j = 0; j < n - 1; j += 2) {
            hilos.emplace_back(deboIntercambiar, std::ref(arr), j, std::ref(cambiados));
        }
        for (auto& hilo : hilos) {
            hilo.join();
        }

        if (cambiados) huboCambios = true;
        cambiados = false;
        hilos.clear();

        for (int j = 1; j < n - 1; j += 2) {
            hilos.emplace_back(deboIntercambiar, std::ref(arr), j, std::ref(cambiados));
        }
        for (auto& hilo : hilos) {
            hilo.join();
        }

        if (cambiados) huboCambios = true;

    } while (huboCambios);
}

int main() {
    std::vector<int> arr;
    int n;

    std::cout << "Ingresa el tamaño del arreglo: ";
    std::cin >> n;
    std::cout << "Ingresa el arreglo:\n";
    for (int i = 0; i < n; i++) {
        int tmp;
        std::cin >> tmp;
        arr.push_back(tmp);
    }

    bubbleSortParalelo(arr);

    std::cout << "Arreglo ordenado: ";
    for (int num : arr) {
        std::cout << num << " ";
    }
    std::cout << "\n";

    return 0;
}
