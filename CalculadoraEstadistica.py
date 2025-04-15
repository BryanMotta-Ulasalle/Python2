import tkinter as tk
from tkinter import messagebox
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

# Variable global para almacenar los datos ingresados
datos_global = []

# -------------------- FUNCIONES DE CÁLCULO --------------------

def calcular_tendencia_central(datos):
    media = np.mean(datos)
    mediana = np.median(datos)
    moda_result = stats.mode(datos, keepdims=True)
    moda = moda_result.mode[0] if moda_result.count[0] > 1 else "No tiene moda"
    return {"Media": media, "Mediana": mediana, "Moda": moda}

def calcular_dispersion(datos):
    varianza = np.var(datos, ddof=1)
    desviacion = np.std(datos, ddof=1)
    return {"Varianza": varianza, "Desviación Estándar": desviacion}

def calcular_forma_posicion(datos):
    asimetria = stats.skew(datos)
    curtosis = stats.kurtosis(datos)
    percentiles = {
        "P25": np.percentile(datos, 25),
        "P50": np.percentile(datos, 50),
        "P75": np.percentile(datos, 75)
    }
    cuartiles = {
        "Q1": np.quantile(datos, 0.25),
        "Q2": np.quantile(datos, 0.50),
        "Q3": np.quantile(datos, 0.75)
    }
    return {"Asimetría": asimetria, "Curtosis": curtosis, **percentiles, **cuartiles}

def calcular_tamano_muestra(datos):
    z = 1.96  # 95% de confianza
    e = 0.05  # error esperado
    desviacion = np.std(datos, ddof=1)
    n = ((z * desviacion) / e) ** 2
    return {"Tamaño de Muestra Estimado": int(round(n))}

# -------------------- INTERFAZ --------------------

def mostrar_resultado(nombre_medida, resultados):
    ventana_resultado = tk.Toplevel()
    ventana_resultado.title(f"Resultados - {nombre_medida}")
    
    tk.Label(ventana_resultado, text=f"Resultados de {nombre_medida}", font=("Arial", 14, "bold")).pack(pady=10)
    
    for clave, valor in resultados.items():
        tk.Label(ventana_resultado, text=f"{clave}: {valor}", font=("Arial", 12)).pack()

    # Botón para graficar
    tk.Button(ventana_resultado, text="Graficar Resultados", command=lambda: graficar_resultados(nombre_medida, resultados)).pack(pady=10)

def graficar_resultados(nombre_medida, resultados):
    claves = list(resultados.keys())
    valores = list(resultados.values())

    # Eliminar valores que no sean numéricos (como "No tiene moda")
    claves_filtradas = []
    valores_filtrados = []
    for k, v in zip(claves, valores):
        if isinstance(v, (int, float, np.float64)):
            claves_filtradas.append(k)
            valores_filtrados.append(v)

    if not valores_filtrados:
        messagebox.showinfo("Sin valores numéricos", "No hay datos numéricos para graficar.")
        return

    plt.figure(figsize=(8, 5))
    plt.bar(claves_filtradas, valores_filtrados, color="skyblue")
    plt.title(f"Gráfico - {nombre_medida}")
    plt.ylabel("Valor")
    plt.tight_layout()
    plt.show()

def seleccionar_medida(nombre):
    if not datos_global:
        messagebox.showwarning("Error", "Primero debes ingresar datos.")
        return
    
    datos = np.array(datos_global)
    
    if nombre == "Tendencia Central":
        resultado = calcular_tendencia_central(datos)
    elif nombre == "Dispersión":
        resultado = calcular_dispersion(datos)
    elif nombre == "Forma y Posición":
        resultado = calcular_forma_posicion(datos)
    elif nombre == "Tamaño de Muestra":
        resultado = calcular_tamano_muestra(datos)
    else:
        resultado = {}
    
    mostrar_resultado(nombre, resultado)

def procesar_datos(entrada, ventana):
    global datos_global
    try:
        datos = [float(x) for x in entrada.get().split()]
        if len(datos) < 2:
            raise ValueError("Se requieren al menos 2 datos.")
        datos_global = datos
        ventana.destroy()
        mostrar_menu_medidas()
    except ValueError as e:
        messagebox.showerror("Error", f"Datos inválidos: {e}")

# -------------------- MENÚS --------------------

def mostrar_ventana_datos():
    ventana_datos = tk.Toplevel()
    ventana_datos.title("Ingresar Datos")

    tk.Label(ventana_datos, text="Ingrese los datos separados por espacios:", font=("Arial", 12)).pack(pady=10)
    entrada = tk.Entry(ventana_datos, width=40)
    entrada.pack(pady=5)

    tk.Button(ventana_datos, text="Continuar", command=lambda: procesar_datos(entrada, ventana_datos)).pack(pady=10)

def mostrar_menu_medidas():
    ventana_menu = tk.Toplevel()
    ventana_menu.title("Seleccionar Medida Estadística")

    tk.Label(ventana_menu, text="Selecciona el tipo de medida estadística", font=("Arial", 14, "bold")).pack(pady=15)

    opciones = ["Tendencia Central", "Dispersión", "Forma y Posición", "Tamaño de Muestra"]
    for op in opciones:
        tk.Button(ventana_menu, text=op, width=30, command=lambda op=op: seleccionar_medida(op)).pack(pady=5)

# -------------------- VENTANA PRINCIPAL --------------------

def main():
    raiz = tk.Tk()
    raiz.title("Calculadora Estadística")
    raiz.geometry("400x300")

    tk.Label(raiz, text="Calculadora Estadística", font=("Arial", 16, "bold")).pack(pady=20)

    tk.Button(raiz, text="Ingresar Datos", width=25, command=mostrar_ventana_datos).pack(pady=10)

    tk.Button(raiz, text="Salir", width=25, command=raiz.destroy).pack(pady=10)

    raiz.mainloop()

# -------------------- EJECUTAR --------------------

if __name__ == "__main__":
    main()
