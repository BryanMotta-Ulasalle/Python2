import tkinter as tk

def saludar():
    etiqueta.config(text="¡Hola, mundo!")  # Cambia el texto cuando presionas el botón

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Mi primera GUI")
ventana.geometry("300x200")

# Crear etiqueta (inicialmente vacía o con texto inicial)
etiqueta = tk.Label(ventana, text="Presiona el botón")
etiqueta.pack(pady=10)

# Crear el botón
boton = tk.Button(ventana, text="Saludar", command=saludar)
boton.pack(pady=10)

# Mantener la ventana abierta
ventana.mainloop()

