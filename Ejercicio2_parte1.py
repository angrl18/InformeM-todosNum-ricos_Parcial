# PARTE 1 — INTERPOLACION
# Lagrange grado 2 y Spline Cubico Natural
# LIBRERIAS
import numpy as np
import matplotlib.pyplot as plt

from scipy.interpolate import lagrange
from scipy.interpolate import CubicSpline

plt.ion()

# DATOS EXPERIMENTALES
# Frecuencia (kHz)
f = np.array([
10.0,12.5,15.0,17.5,20.0,22.5,25.0,27.5,30.0,32.5,
35.0,37.5,40.0,42.5,45.0,47.5,50.0,52.5,55.0,57.5,
60.0,62.5,65.0,67.5,70.0,72.5,75.0,77.5,80.0,82.5,
85.0,87.5,90.0,92.5,95.0,97.5,100.0,102.5,105.0,107.5
])

# Voltaje V(f)
V = np.array([
0.842,0.911,0.986,1.062,1.143,1.227,1.314,1.401,1.482,1.551,
1.216,1.048,0.866,0.689,0.521,0.364,0.223,0.103,0.012,-0.041,
-0.057,-0.034,0.018,0.096,0.197,0.318,0.452,0.579,0.700,0.809,
0.611,0.688,0.756,0.811,0.856,0.894,0.926,0.954,0.980,1.004
])

# Impedancia |Z|(f)
Z = np.array([
182.4,178.9,175.1,171.0,166.8,162.7,158.9,155.4,152.0,149.0,
146.1,145.2,145.8,147.3,149.9,153.5,158.0,163.2,168.9,174.8,
180.5,186.2,191.5,196.2,200.1,203.1,205.2,206.3,206.1,204.7,
198.0,194.4,190.9,187.8,185.1,183.0,181.6,180.8,180.6,180.9
])

# FUNCION PARA LAGRANGE GRADO 2
def lagrange_grado2(x_datos, y_datos, x_interp):

    # Buscar los 3 puntos mas cercanos
    distancias = np.abs(x_datos - x_interp)

    indices = np.argsort(distancias)[:3]

    # Ordenar
    indices = np.sort(indices)

    x = x_datos[indices]
    y = y_datos[indices]

    # Construir polinomio
    polinomio = lagrange(x, y)

    # Evaluar
    y_interp = polinomio(x_interp)

    return y_interp, polinomio

# SPLINES CUBICOS NATURALES

spline_V = CubicSpline(f, V, bc_type='natural')

spline_Z = CubicSpline(f, Z, bc_type='natural')

# FRECUENCIAS A INTERPOLAR

frecuencias_interp = [41.0, 73.0]

# RESULTADOS

print("==============================================")
print("INTERPOLACION CON LAGRANGE Y SPLINE CUBICO")
print("==============================================\n")

for freq in frecuencias_interp:

    print(f"============== f = {freq} kHz ==============\n")

    # VOLTAJE V(f)

    V_lagrange, pol_V = lagrange_grado2(f, V, freq)

    V_spline = spline_V(freq)

    print("Voltaje V(f)\n")

    print(f"Lagrange grado 2:")
    print(f"V({freq}) = {V_lagrange:.6f} V")

    print(f"Spline Cubico:")
    print(f"V({freq}) = {V_spline:.6f} V")

    diferencia_V = abs(V_lagrange - V_spline)

    print(f"Diferencia:")
    print(f"|Spline - Lagrange| = {diferencia_V:.8f}\n")

    # IMPEDANCIA |Z|(f)

    Z_lagrange, pol_Z = lagrange_grado2(f, Z, freq)

    Z_spline = spline_Z(freq)

    print("Impedancia |Z|(f)\n")

    print(f"Lagrange grado 2:")
    print(f"|Z|({freq}) = {Z_lagrange:.6f} Ohm")

    print(f"Spline Cubico:")
    print(f"|Z|({freq}) = {Z_spline:.6f} Ohm")

    diferencia_Z = abs(Z_lagrange - Z_spline)

    print(f"Diferencia:")
    print(f"|Spline - Lagrange| = {diferencia_Z:.8f}\n")

# GRAFICAS

# Malla fina
f_fina = np.linspace(min(f), max(f), 1000)

# Evaluacion splines
V_fina = spline_V(f_fina)
Z_fina = spline_Z(f_fina)

# GRAFICA V(f)

plt.figure(figsize=(12,6))

plt.plot(f, V, 'bo', label='Datos experimentales')

plt.plot(
    f_fina,
    V_fina,
    'r-',
    linewidth=2,
    label='Spline Cubico'
)

plt.title('Interpolacion de Voltaje V(f)')
plt.xlabel('Frecuencia (kHz)')
plt.ylabel('Voltaje (V)')
plt.grid(True)
plt.legend()

plt.show()

# GRAFICA |Z|(f)

plt.figure(figsize=(12,6))

plt.plot(f, Z, 'go', label='Datos experimentales')

plt.plot(
    f_fina,
    Z_fina,
    'm-',
    linewidth=2,
    label='Spline Cubico'
)

plt.title('Interpolacion de Impedancia |Z|(f)')
plt.xlabel('Frecuencia (kHz)')
plt.ylabel('Impedancia (Ohm)')
plt.grid(True)
plt.legend()

plt.show()