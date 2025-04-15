import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

# Funciones estadísticas
def calcular_tendencia_central(datos):
    moda_resultado = stats.mode(datos, keepdims=True)
    moda = moda_resultado.mode
    return {
        'Media': np.mean(datos),
        'Mediana': np.median(datos),
        'Moda': moda[0] if len(moda) > 0 else 'No definida'
    }


def calcular_dispersion(datos):
    varianza = np.var(datos, ddof=1)
    desviacion = np.std(datos, ddof=1)
    resultados = {
        'Varianza': varianza,
        'Desviación Estándar': desviacion
    }
    return resultados

def calcular_forma_posicion(datos):
    asimetria = stats.skew(datos)
    curtosis = stats.kurtosis(datos)
    percentil_25 = np.percentile(datos, 25)
    percentil_50 = np.percentile(datos, 50)
    percentil_75 = np.percentile(datos, 75)
    resultados = {
        'Asimetría': asimetria,
        'Curtosis': curtosis,
        'Percentil 25': percentil_25,
        'Percentil 50 (Mediana)': percentil_50,
        'Percentil 75': percentil_75
    }
    return resultados

def calcular_tamano_muestra(N, Z=1.96, p=0.5, e=0.05):
    n = (Z**2 * p * (1 - p)) / (e**2)
    n_ajustada = (n * N) / (n + N - 1)
    return round(n_ajustada)

# Función para graficar los resultados según la medida seleccionada
def graficar_resultados(tipo, resultados):
    plt.figure(figsize=(7, 4))
    if tipo == 'Tendencia Central':
        plt.bar(resultados.keys(), resultados.values(), color='skyblue')
        plt.title('Medidas de Tendencia Central')
    elif tipo == 'Dispersión':
        plt.bar(resultados.keys(), resultados.values(), color='orange')
        plt.title('Medidas de Dispersión')
    elif tipo == 'Forma y Posición':
        sns.barplot(x=list(resultados.keys()), y=list(resultados.values()), palette='magma')
        plt.xticks(rotation=30)
        plt.title('Medidas de Forma y Posición')
    elif tipo == 'Tamaño de Muestra':
        plt.pie([resultados, 100 - resultados], labels=['Muestra', 'Resto'], autopct='%1.1f%%', colors=['#4CAF50', '#FFC107'])
        plt.title('Tamaño de Muestra estimado')
    plt.tight_layout()
    plt.show()

# Función principal que se llama al presionar calcular
def procesar():
    entrada = datos_entry.get()
    opcion = tipo_combo.get()

    if opcion != 'Tamaño de Muestra':
        try:
            datos = np.array(list(map(float, entrada.split(','))))
            if len(datos) < 2:
                raise ValueError("Se requieren al menos dos valores.")
        except Exception as e:
            messagebox.showerror("Error", f"Entrada inválida: {e}")
            return

    if opcion == 'Tendencia Central':
        resultados = calcular_tendencia_central(datos)
    elif opcion == 'Dispersión':
        resultados = calcular_dispersion(datos)
    elif opcion == 'Forma y Posición':
        resultados = calcular_forma_posicion(datos)
    elif opcion == 'Tamaño de Muestra':
        try:
            N = int(tamano_entry.get())
            if N <= 0:
                raise ValueError("El tamaño de población debe ser mayor a 0.")
            resultados = calcular_tamano_muestra(N)
        except Exception as e:
            messagebox.showerror("Error", f"Tamaño inválido: {e}")
            return

    mostrar_resultados(opcion, resultados)

def mostrar_resultados(opcion, resultados):
    resultado_text.config(state=tk.NORMAL)
    resultado_text.delete(1.0, tk.END)
    if isinstance(resultados, dict):
        for clave, valor in resultados.items():
            resultado_text.insert(tk.END, f"{clave}: {valor}\n")
    else:
        resultado_text.insert(tk.END, f"Tamaño de muestra recomendado: {resultados}")
    resultado_text.config(state=tk.DISABLED)

    if graficar_var.get():
        graficar_resultados(opcion, resultados)

# Interfaz gráfica
root = tk.Tk()
root.title("Calculadora Estadística")

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

ttk.Label(frame, text="Seleccione el tipo de medida:").grid(column=0, row=0, sticky=tk.W)
tipo_combo = ttk.Combobox(frame, values=["Tendencia Central", "Dispersión", "Forma y Posición", "Tamaño de Muestra"], state="readonly")
tipo_combo.grid(column=1, row=0, sticky=tk.W)
tipo_combo.set("Tendencia Central")

ttk.Label(frame, text="Ingrese los datos (separados por coma):").grid(column=0, row=1, sticky=tk.W)
datos_entry = ttk.Entry(frame, width=40)
datos_entry.grid(column=1, row=1, sticky=tk.W)

ttk.Label(frame, text="Tamaño de población (solo para tamaño de muestra):").grid(column=0, row=2, sticky=tk.W)
tamano_entry = ttk.Entry(frame, width=15)
tamano_entry.grid(column=1, row=2, sticky=tk.W)

graficar_var = tk.BooleanVar()
graficar_check = ttk.Checkbutton(frame, text="Mostrar gráfica", variable=graficar_var)
graficar_check.grid(column=1, row=3, sticky=tk.W)

calcular_btn = ttk.Button(frame, text="Calcular", command=procesar)
calcular_btn.grid(column=1, row=4, pady=10, sticky=tk.E)

resultado_text = tk.Text(frame, width=50, height=10, state=tk.DISABLED)
resultado_text.grid(column=0, row=5, columnspan=2)

root.mainloop()
