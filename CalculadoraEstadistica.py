import numpy as np
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from scipy import stats

# Variables globales
datos_global = []  # Guardamos los datos globalmente

# Funciones estadísticas
def calcular_estadisticas(datos):
    media = np.mean(datos)
    mediana = np.median(datos)
    moda_res = stats.mode(datos)
    moda = moda_res.mode[0] if moda_res.count[0] > 1 else "No tiene moda"
    varianza = np.var(datos)
    desviacion = np.std(datos)
    asimetria = stats.skew(datos)
    curtosis = stats.kurtosis(datos, fisher=False)
    percentiles = np.percentile(datos, [25, 50, 75])
    cuartiles = (percentiles[0], percentiles[2])
    tamano_muestra = len(datos)
    
    return {
        "Media": media,
        "Mediana": mediana,
        "Moda": moda,
        "Varianza": varianza,
        "Desviación Estándar": desviacion,
        "Asimetría": asimetria,
        "Curtosis": curtosis,
        "Percentiles": percentiles,
        "Cuartiles": cuartiles,
        "Tamaño de la Muestra": tamano_muestra
    }

# Función para mostrar los resultados en una nueva ventana
def mostrar_resultados(resultado):
    ventana_resultados = tk.Toplevel(ventana)
    ventana_resultados.title("Resultados Estadísticos")
    ventana_resultados.geometry("400x300")
    tk.Label(ventana_resultados, text=resultado, font=("Arial", 12)).pack(pady=20)

# Función para procesar los datos de entrada
def procesar(entrada_datos):
    try:
        datos = [float(x) for x in entrada_datos.get().split()]
        global datos_global
        datos_global = datos
        messagebox.showinfo("Información", "Datos procesados correctamente.")
    except ValueError:
        messagebox.showerror("Error", "Por favor, introduce solo números separados por espacios.")

# Función para mostrar los resultados según la opción seleccionada
def mostrar_medida(seleccion):
    if not datos_global:
        messagebox.showwarning("Error", "Primero introduce los datos.")
        return
    
    medidas = calcular_estadisticas(np.array(datos_global))
    
    if seleccion not in medidas:
        messagebox.showerror("Error", "Opción no válida.")
        return

    resultado = f"{seleccion}: {medidas[seleccion]}"
    mostrar_resultados(resultado)

# Función para la ventana de estadísticas
def ventana_estadisticas():
    ventana_secundaria = tk.Toplevel(ventana)
    ventana_secundaria.title("Calcular Estadísticas")
    ventana_secundaria.geometry("600x400")

    tk.Label(ventana_secundaria, text="Introduce los datos (separados por espacios):").pack()
    entrada_datos = tk.Entry(ventana_secundaria, width=70)
    entrada_datos.pack(pady=5)

    tk.Button(ventana_secundaria, text="Procesar Datos", command=lambda: procesar(entrada_datos)).pack(pady=10)

    tk.Label(ventana_secundaria, text="Selecciona una medida para mostrar:").pack(pady=5)

    # Botones para las medidas
    botones = [
        ("Media", "Media"),
        ("Mediana", "Mediana"),
        ("Moda", "Moda"),
        ("Varianza", "Varianza"),
        ("Desviación Estándar", "Desviación Estándar"),
        ("Asimetría", "Asimetría"),
        ("Curtosis", "Curtosis"),
        ("Percentiles", "Percentiles"),
        ("Cuartiles", "Cuartiles"),
        ("Tamaño de la Muestra", "Tamaño de la Muestra")
    ]
    
    for texto, medida in botones:
        tk.Button(ventana_secundaria, text=texto, width=30, command=lambda medida=medida: mostrar_medida(medida)).pack(pady=5)

# Función para la ventana de gráficos
def ventana_graficos():
    ventana_secundaria = tk.Toplevel(ventana)
    ventana_secundaria.title("Seleccionar Gráfico")
    ventana_secundaria.geometry("400x300")

    tk.Label(ventana_secundaria, text="Selecciona un gráfico para mostrar:").pack(pady=5)
    opciones_grafico = ["Histograma", "Boxplot", "Barras", "Líneas", "KDE", "Dispersión"]
    combo = ttk.Combobox(ventana_secundaria, values=opciones_grafico)
    combo.pack()

    tk.Button(ventana_secundaria, text="Mostrar Gráfico", command=lambda: mostrar_grafico(combo.get())).pack(pady=10)

# Función para crear el menú principal
def menu_principal():
    ventana.geometry("400x300")
    ventana.title("Menú Principal")

    tk.Label(ventana, text="Bienvenido a la Calculadora Estadística", font=("Arial", 16)).pack(pady=20)

    tk.Button(ventana, text="Calcular Estadísticas", width=30, command=ventana_estadisticas).pack(pady=10)
    tk.Button(ventana, text="Mostrar Gráficos", width=30, command=ventana_graficos).pack(pady=10)

# Configuración de ventana principal
ventana = tk.Tk()
menu_principal()

ventana.mainloop()
