nombre = input("Ingresa tu nombre completo: ")
print(f"¡Hola, {nombre}!")

def mostrar_menu():
    print("\nOpciones:")
    print("1. Saludar")
    print("2. Mostrar la cantidad de letras en tu nombre")
    print("3. Repetir tu nombre 3 veces")
    print("4. Salir")

def main():
    nombre = input("Ingresa tu nombre: ").strip()
    
    while True:
        mostrar_menu()
        opcion = input("Elige una opción (1-4): ")
        
        if opcion == "1":
            print(f"¡Hola, {nombre}! Espero que tengas un gran día. 😊")
        elif opcion == "2":
            print(f"Tu nombre tiene {len(nombre)} letras.")
        elif opcion == "3":
            print(f"{nombre} " * 3)
        elif opcion == "4":
            print("¡Hasta luego! 👋")
            break
        else:
            print("Opción no válida. Inténtalo de nuevo.")

if __name__ == "__main__":
    main()
