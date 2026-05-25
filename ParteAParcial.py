# PARTE A - ANALISIS EXPLORATORIO
# GRAFICA DE IMPEDANCIA VS FRECUENCIA

# Este código:
#
# 1. Grafica los puntos experimentales
# 2. Construye un spline cúbico
# 3. Muestra la curva suave
# 4. Encuentra el mínimo local aproximado
# 5. Marca el mínimo en la gráfica

import numpy as np
import matplotlib.pyplot as plt
from  scipy.interpolate import CubicSpline

# DATOS EXPERIMENTALES

frecuencia = [100, 120, 145, 170, 200, 235, 270, 310, 355, 405, 460, 520, 585, 655, 730, 810, 895, 985, 1080, 1180, 1290, 1410, 1540, 1680, 1830, 1990, 2160, 2340, 2530, 2730]

impedancia = [152.3, 149.1, 146.8, 144.9, 142.0, 139.5, 137.9, 136.1, 134.8, 133.6, 132.7, 131.9, 131.4, 131.1, 130.9, 131.0, 131.3, 131.9, 132.7, 133.8, 135.2, 136.9, 138.9, 141.1, 143.5, 146.1, 149.0, 152.2, 155.6, 159.2]

# CREAR SPLINE CÚBICO
spline = CubicSpline(frecuencia, impedancia)

# GENERAR MUCHOS PUNTOS (esto hace que la curva salga suave)
f_suave = np.linspace(
    min(frecuencia),
    max(frecuencia),
    1000
)

# EVALUAR EL SPLINE
z_suave = spline(f_suave)

# ENCONTRAR EL MÍNIMO LOCAL APROXIMADO
indice_min = np.argmin(z_suave)

f_min = f_suave[indice_min]

z_min = z_suave[indice_min]

# MOSTRAR RESULTADOS
print("\n===================================")
print(" ANALISIS EXPLORATORIO")
print("===================================")

print(f"\nFrecuencia aproximada del mínimo:")

print(f"f ≈ {f_min:.2f} Hz")

print(f"\nImpedancia mínima aproximada:")

print(f"|Z| ≈ {z_min:.2f}")

# GRAFICAR
plt.figure(figsize=(10,6))

# PUNTOS EXPERIMENTALES
plt.scatter(
    frecuencia,
    impedancia,
    label="Datos experimentales"
)

# CURVA SPLINE
plt.plot(
    f_suave,
    z_suave,
    label="Spline cúbico"
)

# MARCAR EL MÍNIMO
plt.scatter(
    f_min,
    z_min,
    s=100,
    label="Mínimo local"
)

# TITULOS Y DETALLES
plt.title("Impedancia vs Frecuencia")

plt.xlabel("Frecuencia (Hz)")

plt.ylabel("|Z|")

plt.grid(True)

plt.legend()

# MOSTRAR GRAFICA
plt.show()

# FIN DEL PROGRAMA