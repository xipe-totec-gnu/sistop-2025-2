import tkinter as tk
from datetime import datetime

def print_time():
    nombre = input("¿Cuál es tu nombre? ")
    current_time = datetime.now().strftime("%H:%M:%S")
    print(nombre," la hora es:", current_time)
    

root = tk.Tk()
root.title("Print Time Button")

print_time_button = tk.Button(root, text="Print Time", command=print_time)
print_time_button.pack(pady=100)

root.mainloop()