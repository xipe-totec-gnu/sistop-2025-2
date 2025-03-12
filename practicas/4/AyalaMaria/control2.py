contador = 10

with open("resultado.txt", "w") as archivo:
    while contador <= 10 and contador >= 1:
        archivo.write(f"Numero {contador}\n")
        contador -= 1
    archivo.write("Fin del ciclo\n")

print("El resultado se ha guardado en resultado.txt")




