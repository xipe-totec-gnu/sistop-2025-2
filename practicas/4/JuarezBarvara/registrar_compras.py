def registrar_compras():
    with open("compras.txt", "w", encoding="utf-8") as archivo:
        print("Registro de compras")
        print("===================")

        while True:
            nombre = input("Ingrese el nombre del producto: ")
            precio = input("Ingrese el precio del producto: ")

            archivo.write(f"Producto: {nombre} - Precio: {precio}\n")

            continuar = input("¿Desea agregar otro producto? (s/n): ").strip().lower()
            if continuar != 's':
                break

    print("Los datos han sido guardados en compras.txt.")

if __name__ == "__main__":
    registrar_compras()
