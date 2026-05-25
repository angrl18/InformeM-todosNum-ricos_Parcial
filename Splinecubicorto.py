# SPLINE CÚBICO - VERSIÓN SIMPLE Y DETALLADA
# Este programa:
# 1. Construye un spline cúbico
# 2. Muestra las ecuaciones cúbicas
# 3. Reemplaza los coeficientes numéricamente
# 4. Grafica la interpolación
# Instalar librerías:
# pip install numpy matplotlib scipy
# IMPORTAR LIBRERÍAS

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline

# DATOS
# Puedes cambiar los datos libremente

x = [0, 1, 2, 3, 4, 5]

y = [0, 3, 8, 15, 24, 36]

# CREAR SPLINE CÚBICO

spline = CubicSpline(x, y, bc_type='natural')

# GENERAR PUNTOS SUAVES PARA LA CURVA

x_suave = np.linspace(min(x), max(x), 1000)

y_suave = spline(x_suave)

# MOSTRAR ECUACIONES DEL SPLINE

print("\n================================================")
print(" ECUACIONES DEL SPLINE CÚBICO")
print("================================================")

for i in range(len(x)-1):

    # COEFICIENTES

    a = spline.c[0][i]
    b = spline.c[1][i]
    c = spline.c[2][i]
    d = spline.c[3][i]

    # MOSTRAR ECUACIÓN GENERAL

    print(f"\nINTERVALO [{x[i]}, {x[i+1]}]")

    print("\nEcuación general:")

    print(
        f"S{i}(x)=a(x-{x[i]})³ + "
        f"b(x-{x[i]})² + "
        f"c(x-{x[i]}) + d"
    )

    # ECUACIÓN CON COEFICIENTES REEMPLAZADOS

    print("\nEcuación reemplazando coeficientes:")

    print(
        f"S{i}(x)= "
        f"{a:.6f}(x-{x[i]})³ + "
        f"{b:.6f}(x-{x[i]})² + "
        f"{c:.6f}(x-{x[i]}) + "
        f"{d:.6f}"
    )

# GRÁFICA

plt.figure(figsize=(10,6))

# CURVA SPLINE

plt.plot(
    x_suave,
    y_suave,
    label="Spline cúbico"
)

# PUNTOS ORIGINALES

plt.scatter(
    x,
    y,
    label="Datos originales"
)

# DETALLES DE LA GRÁFICA

plt.title("Interpolación por Spline Cúbico")

plt.xlabel("x")

plt.ylabel("y")

plt.grid(True)

plt.legend()

# MOSTRAR GRÁFICA
plt.show()
# FIN DEL PROGRAMA