#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <cstdint>
#include <algorithm>

using namespace std;

// Estructura para representar una coincidencia encontrada
struct Coincidencia{
    int desplazamiento; // Desplazamiento de la cadena desde la referencia a la original
    int longitud; // Longitud de la subcadena
};

// Función para encontrar la mejor coincidencia de una subcadena en la ventana de búsqueda
Coincidencia encontrarCoincidencia(const string& entrada, int pos, int tamVentana){
    Coincidencia mejor = {0, 0}; // Guardamos la mejor coincidencia encontrada: {distancia, longitud}
    int maxLookahead = 18; // Máximo número de caracteres para coincidir (longitud máxima del lookahead)

    // Buscamos en la ventana anterior a la posición actual
    for(int i = max(0, pos - tamVentana); i < pos; ++i){
        int longitud = 0; // Longitud actual de coincidencia

        // Comparar mientras no salgamos del texto y los caracteres coincidan
        while(pos + longitud < entrada.size() && entrada[i + longitud] == entrada[pos + longitud]){
            ++longitud;
            if(longitud >= maxLookahead) break; // Límite del lookahead alcanzado
        }

        // Si esta coincidencia es mejor que la anterior, la guardamos
        if(longitud > mejor.longitud){
            mejor = {pos - i, longitud}; // Distancia desde la posición actual, longitud de coincidencia
        }
    }

    // Retornar la mejor coincidencia encontrada
    return mejor;
}

// Función para comprimir
string comprimirLZNT1(const string& entrada){
    string comprimido; // Cadena de salida que contendrá el texto comprimido
    int pos = 0; // Puntero actual en la cadena de entrada

    // Procesamos la entrada hasta recorrer toda la cadena
    while(pos < entrada.size()){
        uint8_t banderas = 0; // Byte de bandera que indica si cada uno de los 8 tokens es un literal (0) o una referencia (1)
        string tokens; // Acumula los 8 tokens (literales o referencias) de este bloque
        int cnt = 0; // Contador de tokens en el bloque actual (máximo 8)

        // Procesamos un bloque de hasta 8 elementos (tokens)
        while(cnt < 8 && pos < entrada.size()){
            // Buscar la mejor coincidencia en los últimos 4096 caracteres
            Coincidencia coincidencia = encontrarCoincidencia(entrada, pos, 4096);

            // Si la coincidencia tiene longitud suficiente, se comprime como una referencia
            if(coincidencia.longitud >= 3){
                // Establecemos el bit correspondiente en el byte de banderas
                banderas |= (1 << cnt);

                // Creamos el token de 2 bytes:
                // Bits 15-4: desplazamiento (12 bits)
                // Bits 3-0 : longitud - 3 (4 bits)
                uint16_t token = ((coincidencia.desplazamiento & 0xFFF) << 4) | ((coincidencia.longitud - 3) & 0xF);

                // Guardamos el token en orden big-endian (MSB primero)
                tokens += (char)(token >> 8);      // Byte alto
                tokens += (char)(token & 0xFF);    // Byte bajo

                // Avanzamos la posición actual según la longitud de la coincidencia
                pos += coincidencia.longitud;
            } else {
                // Si no hay coincidencia suficiente, guardamos el carácter literal tal cual
                tokens += entrada[pos++];
            }

            cnt++; // Aumentamos el contador de tokens en este bloque
        }

        // Guardamos el byte de banderas seguido de los tokens comprimidos
        comprimido += (char)banderas;
        comprimido += tokens;
    }

    return comprimido; // Retornamos la cadena comprimida
}

// Función para descomprimir
string descomprimirLZNT1(const string& comprimido){
    string salida; // Cadena resultante descomprimida
    int pos = 0;   // Posición actual en la cadena comprimida

    // Iteramos hasta recorrer toda la entrada comprimida
    while(pos < comprimido.size()){
        uint8_t banderas = comprimido[pos++]; // Leemos el byte de banderas que indica el tipo de cada uno de los próximos 8 tokens

        // Procesamos hasta 8 tokens (literales o referencias)
        for(int i = 0; i < 8 && pos < comprimido.size(); ++i){
            bool esReferencia = (banderas >> i) & 1; // Verificamos si el bit i-ésimo indica una referencia

            if(esReferencia){
                // Nos aseguramos de que hay al menos 2 bytes disponibles para el token
                if(pos + 1 >= comprimido.size()) break;

                // Leemos los 2 bytes que componen el token de referencia (en orden big-endian)
                uint16_t token = (uint8_t)comprimido[pos] << 8 | (uint8_t)comprimido[pos + 1];
                pos += 2;

                // Extraemos el desplazamiento y la longitud
                int desplazamiento = (token >> 4) & 0xFFF; // 12 bits superiores
                int longitud = (token & 0xF) + 3;           // 4 bits inferiores + 3

                // Calculamos la posición de inicio de la copia en la salida
                int inicio = salida.size() - desplazamiento;

                // Copiamos la subcadena desde 'inicio' con 'longitud' caracteres
                for(int j = 0; j < longitud; ++j) {
                    salida += salida[inicio + j];
                }
            } else {
                // Si es literal, simplemente copiamos el carácter directamente
                salida += comprimido[pos++];
            }
        }
    }

    return salida; // Retornamos la cadena descomprimida
}


int main(){
    // Leer el archivo original
    ifstream entrada("por_comprimir.txt", ios::in | ios::binary);
    if(!entrada){
        cerr << "Error al abrir el archivo por_comprimir.txt\n";
        return 1;
    }

    // Leer todo el contenido en memoria
    string original((istreambuf_iterator<char>(entrada)), istreambuf_iterator<char>());
    entrada.close();

    // Comprimir
    string comprimido = comprimirLZNT1(original);

    // Escribir el archivo comprimido
    ofstream salida("por_comprimir_comprimido.txt", ios::out | ios::binary);
    if(!salida){
        cerr << "Error al escribir por_comprimir_comprimido.txt\n";
        return 1;
    }
    salida.write(comprimido.data(), comprimido.size());
    salida.close();

    // Descomprimir para verificar
    string descomprimido = descomprimirLZNT1(comprimido);
    ofstream salida2("descomprimido.txt", ios::out | ios::binary);
    salida2.write(descomprimido.data(), descomprimido.size());
    salida2.close();

    cout << "Compresión terminada. Archivos generados:\n";
    cout << "- por_comprimir_comprimido.txt\n";
    cout << "- descomprimido.txt (verificación)\n";

    return 0;
}
