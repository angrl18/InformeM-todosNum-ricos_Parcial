# PARTE C - DERIVACION NUMERICA CON SPLINE CUBICO

# LIBRERIAS

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline

# DATOS EXPERIMENTALES
#
# REEMPLAZA ESTOS DATOS POR LOS TUYOS

f = np.array([
    100, 120, 145, 170, 200, 235, 270, 310, 355, 405, 
    460, 520, 585, 655, 730, 810, 895, 985, 1080, 1180, 
    1290, 1410, 1540, 1680, 1830, 1990, 2160, 2340, 2530, 2730])

Z = np.array([
    152.3, 149.1, 146.8, 144.9, 142.0, 139.5, 137.9, 
    136.1, 134.8, 133.6, 132.7, 131.9, 131.4, 131.1, 
    130.9, 131.0, 131.3, 131.9, 132.7, 133.8, 135.2, 
    136.9, 138.9, 141.1, 143.5, 146.1, 149.0, 152.2, 
    155.6, 159.2
])

# CONSTRUCCION DEL SPLINE CUBICO NATURAL

spline = CubicSpline(
    f,
    Z,
    bc_type='natural'
)

# MALLA FINA PARA GRAFICAS

f_suave = np.linspace(
    min(f),
    max(f),
    2000
)

# EVALUAR SPLINE

Z_spline = spline(f_suave)

# PRIMERA DERIVADA DEL SPLINE

primera_derivada = spline.derivative()

# EVALUAR PRIMERA DERIVADA

dZ_df = primera_derivada(f_suave)

# GRAFICA DE LA DERIVADA

plt.figure(figsize=(14,8))

plt.plot(
    f_suave,
    dZ_df,
    linewidth=3,
    label="d|Z|/df"
)

# LINEA HORIZONTAL EN CERO

plt.axhline(
    0,
    linestyle='--'
)

plt.title(
    "Primera Derivada de la Impedancia"
)

plt.xlabel("Frecuencia (Hz)")

plt.ylabel("d|Z|/df")

plt.grid(True)

plt.legend()

plt.show()

# BUSCAR EL MINIMO
#
# EL MINIMO OCURRE DONDE:
#
# d|Z|/df = 0

indice_minimo = np.argmin(
    np.abs(dZ_df)
)

# FRECUENCIA DEL MINIMO

f_min = f_suave[indice_minimo]

# VALOR MINIMO DE IMPEDANCIA

Z_min = spline(f_min)

# MOSTRAR RESULTADOS

print("\n================================================")
print(" MINIMO DE LA CURVA")
print("================================================")

print(f"\nFrecuencia del minimo : {f_min:.4f} Hz")

print(f"Impedancia minima     : {Z_min:.4f}")

# SEGUNDA DERIVADA DEL SPLINE

segunda_derivada = spline.derivative(2)

# EVALUAR SEGUNDA DERIVADA EN EL MINIMO

d2Z_df2 = segunda_derivada(f_min)

# MOSTRAR SEGUNDA DERIVADA

print("\n================================================")
print(" SEGUNDA DERIVADA")
print("================================================")

print(f"\nd²|Z|/df² = {d2Z_df2:.8f}")

# ANALISIS DE ESTABILIDAD

if d2Z_df2 > 0:

    print("""
El signo de la segunda derivada es POSITIVO.

La curva es concava hacia arriba.

Por lo tanto:
EL PUNTO ES UN MINIMO ESTABLE.
""")

elif d2Z_df2 < 0:

    print("""
El signo de la segunda derivada es NEGATIVO.

La curva es concava hacia abajo.

Por lo tanto:
EL PUNTO ES UN MAXIMO.
""")

else:

    print("""
La segunda derivada es cercana a cero.

No puede determinarse claramente
la estabilidad del punto.
""")

# GRAFICA FINAL DEL SPLINE Y MINIMO

plt.figure(figsize=(14,8))

# DATOS EXPERIMENTALES

plt.scatter(
    f,
    Z,
    s=50,
    label="Datos experimentales"
)

# SPLINE

plt.plot(
    f_suave,
    Z_spline,
    linewidth=3,
    label="Spline cubico natural"
)

# PUNTO MINIMO

plt.scatter(
    f_min,
    Z_min,
    s=120,
    marker='x',
    label="Minimo encontrado"
)

plt.title(
    "Spline Cubico Natural y Punto Minimo"
)

plt.xlabel("Frecuencia (Hz)")

plt.ylabel("|Z|")

plt.grid(True)

plt.legend()

plt.show()

# ANALISIS FINAL

print("""
================================================

ANALISIS NUMERICO

La derivacion mediante spline cubico permite
obtener derivadas suaves y estables,
evitando el ruido asociado a diferencias finitas.

El minimo de la curva ocurre cuando
la primera derivada cambia de negativa
a positiva.

La segunda derivada positiva confirma
que el minimo es estable.

================================================

ERROR Y ESPACIAMIENTO

El error de derivacion depende del
espaciamiento entre datos.

Si los puntos experimentales estan
muy separados:

- aumenta el error,
- disminuye la precision local,
- empeora la estimacion de derivadas.

================================================

MEJORA EXPERIMENTAL

Para reducir el error se recomienda:

- aumentar la cantidad de datos,
- usar menor espaciamiento en frecuencia,
- tomar mas muestras cerca del minimo,
- reducir ruido experimental.

================================================
""")