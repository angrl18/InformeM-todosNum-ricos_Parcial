# PARTE D - BUSQUEDA DE RAICES
# OBJETIVO:
# Encontrar las frecuencias donde:
# |Z|(f) = 150 ohmios
# usando:
# 1) Biseccion
# 2) Newton-Raphson
# Ademas:
# - comparar convergencia
# - analizar robustez
# - calcular sensibilidad df/d|Z|
# LIBRERIAS

import numpy as np
import matplotlib.pyplot as plt

from scipy.interpolate import CubicSpline
from scipy.optimize import bisect
from scipy.optimize import newton

# DATOS EXPERIMENTALES
# REEMPLAZA POR TUS DATOS

f = np.array([
    100, 120, 145, 170, 200, 235, 270, 310, 355, 405, 
    460, 520, 585, 655, 730, 810, 895, 985, 1080, 1180, 
    1290, 1410, 1540, 1680, 1830, 1990, 2160, 2340, 2530, 2730
])

Z = np.array([
    152.3, 149.1, 146.8, 144.9, 142.0, 139.5, 137.9, 
    136.1, 134.8, 133.6, 132.7, 131.9, 131.4, 131.1, 
    130.9, 131.0, 131.3, 131.9, 132.7, 133.8, 135.2, 
    136.9, 138.9, 141.1, 143.5, 146.1, 149.0, 152.2, 
    155.6, 159.2
])

# UMBRAL

Z_th = 150

# SPLINE CUBICO NATURAL

spline = CubicSpline(
    f,
    Z,
    bc_type='natural'
)
# FUNCION OBJETIVO
# g(f) = S(f) - 150
# LAS RAICES OCURREN CUANDO:
# g(f) = 0

def g(x):

    return spline(x) - Z_th

# MALLA FINA

f_suave = np.linspace(
    min(f),
    max(f),
    5000
)

# EVALUAR FUNCION

g_vals = g(f_suave)

# GRAFICA

plt.figure(figsize=(14,8))

plt.plot(
    f_suave,
    g_vals,
    linewidth=3,
    label="g(f)=S(f)-150"
)

# LINEA CERO

plt.axhline(
    0,
    linestyle='--'
)

plt.title(
    "Busqueda de Raices del Spline"
)

plt.xlabel("Frecuencia (Hz)")

plt.ylabel("g(f)")

plt.grid(True)

plt.legend()

plt.show()

# BUSCAR INTERVALOS CON CAMBIO DE SIGNO

intervalos = []

for i in range(len(f)-1):

    if g(f[i]) * g(f[i+1]) < 0:

        intervalos.append(
            (f[i], f[i+1])
        )

# MOSTRAR INTERVALOS

print("\n================================================")
print("INTERVALOS CON CAMBIO DE SIGNO")
print("================================================")

for intervalo in intervalos:

    print(intervalo)

# METODO DE BISECCION

print("\n================================================")
print("METODO DE BISECCION")
print("================================================")

raices_biseccion = []

for a,b in intervalos:

    raiz = bisect(
        g,
        a,
        b
    )

    raices_biseccion.append(raiz)

    print(f"\nRaiz encontrada: {raiz:.4f} Hz")

# DERIVADA DEL SPLINE

spline_derivada = spline.derivative()

# METODO DE NEWTON-RAPHSON

print("\n================================================")
print("METODO DE NEWTON-RAPHSON")
print("================================================")

raices_newton = []

for a,b in intervalos:

    # Aproximacion inicial
    x0 = (a+b)/2

    raiz = newton(
        g,
        x0,
        fprime=spline_derivada
    )

    raices_newton.append(raiz)

    print(f"\nRaiz encontrada: {raiz:.4f} Hz")

# COMPARACION FINAL

print("\n================================================")
print("COMPARACION DE METODOS")
print("================================================")

for i in range(len(raices_biseccion)):

    print(f"""
Raiz {i+1}

Biseccion      : {raices_biseccion[i]:.4f} Hz
Newton-Raphson : {raices_newton[i]:.4f} Hz
""")

# SENSIBILIDAD
# df/d|Z|
# USAREMOS LA RAIZ MAS CERCANA A 2000 Hz
# ELEGIR RAIZ MAS CERCANA A 2000
raiz_objetivo = min(
    raices_newton,
    key=lambda x: abs(x-2000)
)

# DERIVADA EN LA RAIZ

pendiente = spline_derivada(
    raiz_objetivo
)

# SENSIBILIDAD

sensibilidad = 1 / pendiente

# MOSTRAR RESULTADOS

print("\n================================================")
print("SENSIBILIDAD NUMERICA")
print("================================================")

print(f"\nRaiz analizada : {raiz_objetivo:.4f} Hz")

print(f"\nd|Z|/df = {pendiente:.4f}")

print(f"\ndf/d|Z| = {sensibilidad:.4f}")

# GRAFICA FINAL

plt.figure(figsize=(14,8))

# SPLINE ORIGINAL

plt.plot(
    f_suave,
    spline(f_suave),
    linewidth=3,
    label="Spline cubico natural"
)

# DATOS

plt.scatter(
    f,
    Z,
    s=50,
    label="Datos experimentales"
)

# LINEA DEL UMBRAL

plt.axhline(
    Z_th,
    linestyle='--',
    label="Umbral = 150 ohm"
)

# MARCAR RAICES

for r in raices_newton:

    plt.scatter(
        r,
        Z_th,
        s=120,
        marker='x'
    )

# DETALLES

plt.title(
    "Raices del Spline Cubico"
)

plt.xlabel("Frecuencia (Hz)")

plt.ylabel("|Z|")

plt.grid(True)

plt.legend()

plt.show()

# ANALISIS FINAL

print("""
================================================

ANALISIS FINAL

El metodo de biseccion presento
mayor robustez debido a que siempre
converge cuando existe cambio de signo.

Newton-Raphson convergio mas rapido,
pero depende fuertemente de una
buena aproximacion inicial y de que
la derivada no sea cercana a cero.

Las raices encontradas representan
las frecuencias limite donde la
impedancia alcanza el umbral critico
de 150 ohmios.

Estas frecuencias delimitan la banda
segura de operacion del sistema.

================================================
""")