# PARTE B1 y B2 - INTERPOLACION POLINOMICA
# Este programa realiza:
# 1. Interpolación polinómica global
# 2. Método matricial (Vandermonde)
# 3. Interpolación de Lagrange
# 4. Comparación entre grados:
#       5, 10, 15 y 29
# 5. Evidencia del fenómeno de Runge
# 6. Validacion Leave-One-Out (LOO)
# 7. Interpolacion por Spline Cubico Natural
# 8. Comparacion entre Spline Cubico y Polinomio Global
# LIBRERIAS

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import lagrange

# DATOS EXPERIMENTALES

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

# MALLA FINA PARA GRAFICAS
f_suave = np.linspace(min(f), max(f), 5000)

# GRADOS A COMPARAR
grados = [5, 10, 15, 29]

# DICCIONARIO PARA GUARDAR POLINOMIOS
polinomios = {}

# GRAFICA GENERAL
plt.figure(figsize=(14,8))

# DATOS ORIGINALES
plt.scatter(
    f,
    Z,
    s=50,
    label="Datos experimentales"
)

# INTERPOLACION POLINOMICA
for grado in grados:

    # METODO MATRICIAL (VANDERMONDE)
    # polyfit usa algebra matricial internamente

    coeficientes = np.polyfit(f, Z, grado)

    # CREAR POLINOMIO GLOBAL
    Pn = np.poly1d(coeficientes)

    # GUARDAR POLINOMIO
    polinomios[grado] = Pn

    # EVALUAR POLINOMIO
    Z_suave = Pn(f_suave)

    # GRAFICAR
    plt.plot(
        f_suave,
        Z_suave,
        linewidth=2,
        label=f"Polinomio grado {grado}"
    )

# TITULOS
plt.title(
    "Comparacion de Polinomios Interpolantes"
)
plt.xlabel("Frecuencia (Hz)")

plt.ylabel("|Z|")

plt.grid(True)

plt.legend()
# MOSTRAR GRAFICA
plt.show()
# MOSTRAR POLINOMIOS HALLADOS
print("\n====================================================")
print(" POLINOMIOS GLOBALES - METODO MATRICIAL")
print("====================================================")

for grado in grados:

    print(f"\n\nPOLINOMIO DE GRADO {grado}")

    print("\n")

    print(polinomios[grado])

# INTERPOLACION DE LAGRANGE
# IMPORTANTE:
# Lagrange completo con 30 puntos y grado 29
# es muy inestable y algebraicamente enorme.
# Aqui se muestra un ejemplo representativo
# usando algunos puntos.
print("\n====================================================")
print(" INTERPOLACION DE LAGRANGE")
print("====================================================")
# TOMAR ALGUNOS PUNTOS
f_lagrange = f[:6]

Z_lagrange = Z[:6]

# CONSTRUIR POLINOMIO DE LAGRANGE
P_lagrange = lagrange(
    f_lagrange,
    Z_lagrange
)
# MOSTRAR POLINOMIO
print("\nPolinomio de Lagrange:")

print("\n")

print(P_lagrange)
# GRAFICA LAGRANGE
plt.figure(figsize=(12,6))
# PUNTOS
plt.scatter(
    f_lagrange,
    Z_lagrange,
    s=60,
    label="Puntos usados"
)
# EVALUAR LAGRANGE
f_lag_suave = np.linspace(
    min(f_lagrange),
    max(f_lagrange),
    1000
)

Z_lag_suave = P_lagrange(f_lag_suave)
# GRAFICAR LAGRANGE
plt.plot(
    f_lag_suave,
    Z_lag_suave,
    linewidth=2,
    label="Polinomio de Lagrange"
)

# TITULOS
plt.title("Interpolacion de Lagrange")

plt.xlabel("Frecuencia (Hz)")

plt.ylabel("|Z|")

plt.grid(True)

plt.legend()

# MOSTRAR
plt.show()

# ANALISIS DE RUNGE

print("\n====================================================")
print(" ANALISIS DEL FENOMENO DE RUNGE")
print("====================================================")

print("""
Al aumentar el grado del polinomio global,
especialmente en grado 29, pueden aparecer
oscilaciones artificiales cerca de los extremos
del intervalo.

Este comportamiento se conoce como:
FENOMENO DE RUNGE.

Los polinomios de grado moderado suelen ser
mas estables y fisicamente razonables.
""")

# VALIDACION LEAVE-ONE-OUT (LOO)
print("\n====================================================")
print(" VALIDACION LEAVE-ONE-OUT (LOO)")
print("====================================================")

# ESCOGER 5 INDICES ALEATORIOS
indices_aleatorios = np.random.choice(
    len(f),
    5,
    replace=False
)

# LISTA PARA GUARDAR ERRORES
errores = []

# RECORRER LOS PUNTOS SELECCIONADOS
for indice in indices_aleatorios:

    # PUNTO ELIMINADO
    f_test = f[indice]

    Z_real = Z[indice]

    # DATOS DE ENTRENAMIENTO
    f_train = np.delete(f, indice)

    Z_train = np.delete(Z, indice)

    # RECONSTRUIR POLINOMIO GRADO 10
    coef_LOO = np.polyfit(
        f_train,
        Z_train,
        10
    )

    P_LOO = np.poly1d(coef_LOO)

    # PREDECIR EL PUNTO ELIMINADO
    Z_pred = P_LOO(f_test)

    # ERROR RELATIVO
    error_relativo = abs(
        (Z_real - Z_pred) / Z_real
    ) * 100

    # GUARDAR ERROR
    errores.append(error_relativo)

    # MOSTRAR RESULTADOS
    print("\n----------------------------------------")

    print(f"Frecuencia eliminada: {f_test} Hz")

    print(f"Valor real      : {Z_real:.6f}")

    print(f"Valor predicho  : {Z_pred:.6f}")

    print(f"Error relativo  : {error_relativo:.4f} %")
# ERROR PROMEDIO
error_promedio = np.mean(errores)
print("\n====================================================")
print(f"ERROR RELATIVO PROMEDIO: {error_promedio:.4f} %")
print("====================================================")
# CONCLUSION AUTOMATICA
if error_promedio < 5:

    print("""
El polinomio de grado 10 presenta
una buena capacidad predictiva y
un comportamiento numericamente estable.
""") 
else:

    print("""
El modelo presenta errores relativamente altos.
Podria evaluarse otro grado polinomico.
""")
# VALOR INTERPOLADO EN 1000 Hz
print("\n========================================")
print(" VALOR INTERPOLADO EN 1000 Hz")
print("========================================")
Z_1000 = polinomios[10](1000)
print(f"\nP10(1000) = {Z_1000:.6f}")
# B2 - SPLINE CUBICO NATURAL
from scipy.interpolate import CubicSpline
# CONSTRUIR SPLINE CUBICO NATURAL
spline = CubicSpline(
    f,
    Z,
    bc_type='natural'
)
# EVALUAR SPLINE EN MALLA FINA
Z_spline = spline(f_suave)
# POLINOMIO SELECCIONADO (grado 10)
Z_polinomio = polinomios[10](f_suave)
# GRAFICA COMPARATIVA
plt.figure(figsize=(14,8))

# DATOS ORIGINALES
plt.scatter(
    f,
    Z,
    s=50,
    label="Datos experimentales"
)
# SPLINE CUBICO
plt.plot(
    f_suave,
    Z_spline,
    linewidth=3,
    label="Spline cubico natural"
)
# POLINOMIO GRADO 10
plt.plot(
    f_suave,
    Z_polinomio,
    linewidth=2,
    linestyle='--',
    label="Polinomio grado 10"
)
# TITULOS
plt.title(
    "Comparacion: Spline Cubico vs Polinomio Global"
)

plt.xlabel("Frecuencia (Hz)")

plt.ylabel("|Z|")

plt.grid(True)

plt.legend()

# MOSTRAR GRAFICA
plt.show()

# EVALUAR EN 1000 Hz
print("\n====================================================")
print(" COMPARACION EN 1000 Hz")
print("====================================================")

# SPLINE
Z_spline_1000 = spline(1000)

# POLINOMIO
Z_poly_1000 = polinomios[10](1000)

# MOSTRAR RESULTADOS
print(f"\nSpline cubico      : {Z_spline_1000:.6f}")

print(f"Polinomio grado 10 : {Z_poly_1000:.6f}")

# DIFERENCIA
diferencia = abs(
    Z_spline_1000 - Z_poly_1000
)

print(f"\nDiferencia absoluta: {diferencia:.6f}")

# ANALISIS FINAL
print("""
====================================================
ANALISIS:
El spline cubico natural presenta un comportamiento
mas suave y estable que el polinomio global.
Debido a que los splines trabajan localmente,
evitan las oscilaciones excesivas asociadas
al fenomeno de Runge.
En aplicaciones biomedicas, donde las mediciones
fisicas suelen variar suavemente, el spline
cubico resulta generalmente mas confiable
para interpolacion y prediccion.
====================================================
""")