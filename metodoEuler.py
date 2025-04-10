import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import numpy as np

def euler_method(f, x0, y0, xn, n):
    h = (xn - x0) / n
    x = [x0]
    y = [y0]
    for i in range(n):
        y_new = y[-1] + h * f(x[-1], y[-1])
        x_new = x[-1] + h
        x.append(x_new)
        y.append(y_new)
    return x, y

def parse_function(func_str):
    def f(x, y):
        return eval(func_str, {"x": x, "y": y, "np": np})
    return f

def solve():
    try:
        func_str = entry_func.get()
        x0 = float(entry_x0.get())
        y0 = float(entry_y0.get())
        xn = float(entry_xn.get())
        n = int(entry_n.get())

        f = parse_function(func_str)
        x_vals, y_vals = euler_method(f, x0, y0, xn, n)

        plt.plot(x_vals, y_vals, marker='o', linestyle='-', color='b')
        plt.title('Método de Euler')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.grid(True)
        plt.show()

    except Exception as e:
        messagebox.showerror("Error", f"Hubo un problema: {e}")

root = tk.Tk()
root.title("Método de Euler")

tk.Label(root, text="f(x, y) =").grid(row=0, column=0)
entry_func = tk.Entry(root)
entry_func.insert(0, "(x**2-1)/y**2") 
entry_func.grid(row=0, column=1)

tk.Label(root, text="x0 =").grid(row=1, column=0)
entry_x0 = tk.Entry(root)
entry_x0.insert(0, "0")
entry_x0.grid(row=1, column=1)

tk.Label(root, text="y0 =").grid(row=2, column=0)
entry_y0 = tk.Entry(root)
entry_y0.insert(0, "2")
entry_y0.grid(row=2, column=1)

tk.Label(root, text="xn =").grid(row=3, column=0)
entry_xn = tk.Entry(root)
entry_xn.insert(0, "1")
entry_xn.grid(row=3, column=1)

tk.Label(root, text="Número de pasos =").grid(row=4, column=0)
entry_n = tk.Entry(root)
entry_n.insert(0, "5    ")
entry_n.grid(row=4, column=1)

tk.Button(root, text="Resolver", command=solve).grid(row=5, column=0, columnspan=2)
root.mainloop()
