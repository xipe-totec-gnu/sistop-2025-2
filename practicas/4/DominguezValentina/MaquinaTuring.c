 #include <stdio.h> 
#include <stdlib.h> 
#include <string.h> 
#define MAX_LENGTH 100 
typedef enum { 
Q0, Q1, Q2, Q3, Q4 
} State; 
typedef enum { 
ONE, ZERO, BLANK, X, Y, C 
} Symbol; 
typedef enum { 
LEFT, RIGHT 
} Direction; 
typedef struct { 
State current_state; 
Symbol read_symbol; 
State next_state; 
Symbol write_symbol; 
Direction move_direction; 
} Transition; 
void runTuringMachine(int num1, int num2, char tape1[MAX_LENGTH], char 
tape2[MAX_LENGTH], Transition transitions[], int num_transitions, int aux) { 
int tape2_ = aux; 
State current_state = Q0; 
int tape1_head = 0; 
int tape2_head = 0; 
while (1) { 
Symbol current_symbol = tape1[tape1_head]; 
        int i; 
        int found = 0;  
        for (i = 0; i < num_transitions; ++i) { 
            if (transitions[i].current_state == current_state && 
                transitions[i].read_symbol == current_symbol) { 
                tape1[tape1_head] = transitions[i].write_symbol; 
                current_state = transitions[i].next_state; 
                if (transitions[i].move_direction == LEFT) { 
                    tape1_head--; 
                } else { 
                    tape1_head++; 
                } 
                if (transitions[i].write_symbol == 'x') { 
                    tape2[tape2_head] = '1'; 
                    tape2_head++; 
                } else if (transitions[i].write_symbol == 'y') { 
                    tape2[tape2_head] = 'B'; 
                    tape2_head++; 
                } 
                found = 1; 
                break; 
            } 
        } 
        if (!found) { 
            break; 
        } 
    } 
    while (tape2_head < MAX_LENGTH) { 
        tape2[tape2_head] = 'B'; 
        tape2_head++; 
    } 
    printf("%d x %d = %d\n",num1, num2, tape2_); 
} 
 
char *generarCadena(int num1, int num2) { 
    int longitudTotal = num1 + num2 + 7; 
    char *cadena = (char *)malloc((longitudTotal + 1) * sizeof(char)); 
    if (cadena == NULL) { 
        fprintf(stderr, "Error: No se pudo asignar memoria.\n"); 
        exit(EXIT_FAILURE); 
    } 
    cadena[0] = 'B'; 
    if (num1 == 0) { 
        cadena[1] = 'C'; 
        cadena[2] = '0'; 
        int indice = 2; 
        int aux; 
        if(num2 == 0){ 
            cadena[3] = 'C'; 
            cadena[4] = 'B'; 
            cadena[5] = '\0'; 
        } 
        for (int i = 1; i < num2+2; ++i){ 
            cadena[indice+i] = '1'; 
            aux = indice +i; 
        } 
        cadena[aux++] = 'B'; 
        cadena[aux] = '\0'; 
    } else if (num2 == 0) { 
        int indice = 0; 
        int aux; 
        for (int i = 1; i < num1+1; ++i) { 
            cadena[indice+i] = '1'; 
            aux = indice+i; 
        } 
        cadena[aux+1] = '0'; 
        cadena[aux+2] = 'C'; 
        cadena[aux+3] = 'B'; 
        cadena[aux+4] = '\0'; 
    } else{ 
        int aux; 
        for (int i = 0; i < num1; ++i) { 
            cadena[i + 1] = '1'; 
            aux = i+1; 
        } 
        cadena[aux + 1] = '0'; 
        int aux2; 
        for (int i = 0; i < num2; ++i) { 
            cadena[i + num1 + 2] = '1'; 
            aux2 = i+num1+2; 
        } 
        cadena[aux2+1] = 'B'; 
        cadena[aux2 + 2] = '\0'; 
    } 
    if(num1 ==0 && num2 ==0){ 
        cadena[0] = 'B'; 
        cadena[1] = 'C'; 
        cadena[2] = '0'; 
        cadena[3] = 'C'; 
        cadena[4] = 'B'; 
        cadena[5] = '\0'; 
    } 
    return cadena; 
} 
int main() { 
    int num1, num2; 
     int input1_valid = 0, input2_valid = 0; 
    do { 
        printf("Ingrese el primer numero: "); 
        if (scanf("%d", &num1) == 1) { 
            input1_valid = 1; 
        } else { 
            while (getchar() != '\n'); 
            printf("Error: Ingrese un numero entero.\n"); 
        } 
    } while (!input1_valid); 
    do { 
        printf("Ingrese el segundo numero: "); 
        if (scanf("%d", &num2) == 1) { 
            input2_valid = 1; 
        } else { 
            while (getchar() != '\n'); 
            printf("Error: Ingrese un numero entero.\n"); 
        } 
    } while (!input2_valid); 
    int tape2_aux = 0; 
    int i; 
    for(i=0;i<num2;i++){ 
        tape2_aux += num1; 
    } 
    char *cadena_a_trabajar = generarCadena(num1, num2); 
    printf("Cadena a trabajar: %s\n", cadena_a_trabajar); 
    char tape1[MAX_LENGTH]; 
    char tape2[MAX_LENGTH]; 
    strcpy(tape1,cadena_a_trabajar);  
    strcpy(tape2, "B");           
    Transition transitions[] = { 
        {Q0, 'B', Q1, 'B', RIGHT}, {Q1, 'B', Q1, 'B', RIGHT}, 
        {Q1, '1', Q1, 'x', RIGHT}, {Q1, '0', Q2, '0', RIGHT}, 
        {Q1, 'x', Q1, 'x', RIGHT}, {Q1, 'C', Q1, 'C', RIGHT}, 
        {Q2, '1', Q3, 'y', LEFT}, {Q2, 'B', Q4, 'B', RIGHT}, 
        {Q2, 'y', Q2, 'y', RIGHT}, {Q2, 'C', Q2, 'C', RIGHT}, 
        {Q3, '0', Q3, '0', LEFT}, {Q3, 'B', Q1, 'B', RIGHT}, 
        {Q3, 'x', Q3, 'x', LEFT}, {Q3, 'y', Q3, 'y', LEFT}, 
    }; 
    runTuringMachine(num1, num2, tape1, tape2, transitions, sizeof(transitions) / 
sizeof(Transition),tape2_aux); 
 
    system("pause"); 
    return 0; 
    system("pause"); 
    free(cadena_a_trabajar); 
} 
