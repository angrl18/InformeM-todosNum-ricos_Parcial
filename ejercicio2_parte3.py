# PARTE 3 — RAICES POR CAMBIO DE SIGNO Y BISECCION
# CON SPLINE CUBICO NATURAL
# LIBRERIAS
import numpy as np
import matplotlib.pyplot as plt

from scipy.interpolate import CubicSpline
from scipy.optimize import bisect
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

# CONSTRUCCION DEL SPLINE CUBICO NATURAL

spline = CubicSpline(f, V, bc_type='natural')

# FUNCION DE BISECCION MANUAL

def biseccion(func, a, b, tol=1e-8, max_iter=100):

    if func(a) * func(b) > 0:
        raise ValueError("No existe cambio de signo.")

    for i in range(max_iter):

        c = (a + b) / 2

        # Verificacion de tolerancia
        if abs(func(c)) < tol:
            return c

        # Cambio de intervalo
        if func(a) * func(c) < 0:
            b = c
        else:
            a = c

    return c

# BUSQUEDA DE CAMBIOS DE SIGNO
print("================================================")
print("CAMBIOS DE SIGNO ENCONTRADOS")
print("================================================\n")

intervalos = []

for i in range(len(V)-1):

    if V[i] * V[i+1] < 0:

        a = f[i]
        b = f[i+1]

        intervalos.append((a, b))

        print(f"Cambio de signo entre:")
        print(f"{a} kHz  y  {b} kHz\n")

# RAICES POR BISECCION

print("================================================")
print("RAICES POR BISECCION")
print("================================================\n")

raices_biseccion = []

for a, b in intervalos:

    raiz = biseccion(spline, a, b)

    raices_biseccion.append(raiz)

    print(f"Intervalo [{a}, {b}]")
    print(f"Raiz ≈ {raiz:.4f} kHz\n")

# RAICES USANDO FUNCION BISECT DE SCIPY

print("================================================")
print("RAICES REFINADAS CON SCIPY")
print("================================================\n")

raices_scipy = []

for a, b in intervalos:

    raiz = bisect(spline, a, b)

    raices_scipy.append(raiz)

    print(f"Intervalo [{a}, {b}]")
    print(f"Raiz refinada ≈ {raiz:.4f} kHz\n")

# COMPARACION

print("================================================")
print("COMPARACION DE RESULTADOS")
print("================================================\n")

for i in range(len(raices_biseccion)):

    diferencia = abs(raices_biseccion[i] - raices_scipy[i])

    print(f"Raiz {i+1}")

    print(f"Biseccion manual : {raices_biseccion[i]:.4f} kHz")

    print(f"SciPy bisect     : {raices_scipy[i]:.4f} kHz")

    print(f"Diferencia       : {diferencia:.4f}\n")

# GRAFICA
# Malla fina
f_fina = np.linspace(min(f), max(f), 2000)

# Evaluacion spline
V_fina = spline(f_fina)

plt.figure(figsize=(12,6))

# Datos experimentales
plt.plot(
    f,
    V,
    'bo',
    label='Datos experimentales'
)

# Spline cubico
plt.plot(
    f_fina,
    V_fina,
    'r-',
    linewidth=2,
    label='Spline Cubico Natural'
)

# Linea y = 0
plt.axhline(
    0,
    color='black',
    linestyle='--'
)

# Mostrar raices
for raiz in raices_scipy:

    plt.plot(
        raiz,
        0,
        'ks',
        markersize=8
    )

    plt.axvline(
        raiz,
        color='green',
        linestyle=':'
    )

# Etiquetas
plt.title('Raices de V(f) usando Biseccion y Spline')
plt.xlabel('Frecuencia (kHz)')
plt.ylabel('Voltaje V(f)')

plt.grid(True)
plt.legend()

plt.show()

# INTERPRETACION FISICA
print("================================================")
print("INTERPRETACION FISICA")
print("================================================\n")

print("Las raices representan frecuencias criticas")
print("donde el voltaje cambia de signo.")
print("\nEn estas frecuencias el circuito de decision")
print("puede activar la alarma digital.")
print("\nEl spline cubico proporciona una aproximacion")
print("mas suave y continua del comportamiento fisico")
print("del sistema respecto a la interpolacion discreta.")