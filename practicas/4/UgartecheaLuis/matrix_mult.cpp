#include <iostream>
#include <thread>
#include <vector>

void multiply_row(const std::vector<std::vector<int>>& A, const std::vector<std::vector<int>>& B, std::vector<std::vector<int>>& C, int row, int size) {
    for (int j = 0; j < size; j++) {
        C[row][j] = 0;
        for (int k = 0; k < size; k++)
            C[row][j] += A[row][k] * B[k][j];
    }
}

void print_matrix(const std::vector<std::vector<int>>& matrix, int size) {
    for (int i = 0; i < size; i++) {
        for (int j = 0; j < size; j++)
            std::cout << matrix[i][j] << " ";
        std::cout << std::endl;
    }
}

int main() {
    int size;
    std::cout << "Enter the size of the matrices: ";
    std::cin >> size;

    std::vector<std::vector<int>> A(size, std::vector<int>(size));
    std::vector<std::vector<int>> B(size, std::vector<int>(size));
    std::vector<std::vector<int>> C(size, std::vector<int>(size, 0));

    std::cout << "Enter elements of matrix A:\n";
    for (int i = 0; i < size; i++)
        for (int j = 0; j < size; j++)
            std::cin >> A[i][j];

    std::cout << "Enter elements of matrix B:\n";
    for (int i = 0; i < size; i++)
        for (int j = 0; j < size; j++)
            std::cin >> B[i][j];

    std::cout << "Matrix A:\n";
    print_matrix(A, size);

    std::cout << "Matrix B:\n";
    print_matrix(B, size);

    std::vector<std::thread> threads(size);

    for (int i = 0; i < size; i++)
        threads[i] = std::thread(multiply_row, std::ref(A), std::ref(B), std::ref(C), i, size);

    
    for (int i = 0; i < size; i++)
        threads[i].join();


    std::cout << "Result matrix:\n";
    print_matrix(C, size);

    return 0;
}