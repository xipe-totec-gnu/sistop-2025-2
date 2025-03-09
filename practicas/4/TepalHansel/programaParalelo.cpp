#include <iostream>
#include <vector>
#include <thread>
#include <algorithm>

void merge(std::vector<int>& arr, int left, int right, int mid){
    int n1 = mid - left + 1;
    int n2 = right - mid;
    std::vector<int> L(n1), R(n2);

    for(int i = 0; i < n1; i++){
        L[i] = arr[left + i];
    }
    for(int i = 0; i < n2; i++){
        R[i] = arr[mid + 1 + i];
    }

    int i = 0, j = 0, k = left;
    while(i < n1 && j < n2){
        if(L[i] <= R[j]){
            arr[k] = L[i];
            i++;
        }else{
            arr[k] = R[j];
            j++;
        }
        k++;
    }
    while(i < n1){
        arr[k] = L[i];
        i++;
        k++;
    }
    while(j < n2){
        arr[k] = R[j];
        j++;
        k++;
    }
}

void merge_sort_parallel(std::vector<int>& arr, int left, int right){
    if(left < right){
        int mid = left + (right - left) / 2;

        std::thread t1(merge_sort_parallel, std::ref(arr),left, mid);
        std::thread t2(merge_sort_parallel, std::ref(arr), mid + 1, right);

        t1.join();
        t2.join();

        merge(arr, left, right, mid);
    }
}

int main(){
    std::vector<int> arr = {64, 34, 25, 12, 22, 11, 90};
    std::cout << "Array original: "<< std::endl;
    for(int i = 0; i < arr.size(); i++){
        std::cout << arr[i] << " ";
    }
    std::cout << std::endl;
    merge_sort_parallel(arr, 0, arr.size() - 1);
    std::cout << "Array ordenado: "<< std::endl;
    for(int i = 0; i < arr.size(); i++){
        std::cout << arr[i] << " ";
    }
    std::cout << std::endl;

    return 0;
}