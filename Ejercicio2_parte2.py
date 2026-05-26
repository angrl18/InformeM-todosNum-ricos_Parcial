# PARTE 2 — DERIVACION NUMERICA
# LIBRERIAS
import numpy as np
import matplotlib.pyplot as plt
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

# ESPACIAMIENTO ENTRE DATOS
h = 2.5  # kHz

# FUNCIONES DE DERIVACION NUMERICA

# DIFERENCIA CENTRADA ORDEN 2

def derivada_centrada_orden2(y_menos, y_mas, h):

    return (y_mas - y_menos) / (2*h)

# DIFERENCIA CENTRADA ORDEN 4

def derivada_centrada_orden4(y_menos2, y_menos1,
                             y_mas1, y_mas2, h):

    return (
        -y_mas2
        + 8*y_mas1
        - 8*y_menos1
        + y_menos2
    ) / (12*h)

# DIFERENCIA PROGRESIVA ORDEN 2

def derivada_progresiva_orden2(y0, y1, y2, h):

    return (-3*y0 + 4*y1 - y2) / (2*h)

# SPLINE CUBICO NATURAL

spline = CubicSpline(f, V, bc_type='natural')

# Derivada del spline
spline_derivada = spline.derivative()

# FRECUENCIAS PEDIDAS

frecuencias = [40.0, 70.0, 100.0]

# RESULTADOS

print("================================================")
print("PARTE 2 — DERIVACION NUMERICA")
print("================================================\n")

# DERIVADAS EN 40, 70 y 100 kHz

for freq in frecuencias:

    # Buscar indice correspondiente
    i = np.where(f == freq)[0][0]

    print(f"============== f = {freq} kHz ==============\n")

    # DIFERENCIA CENTRADA ORDEN 2

    derivada_o2 = derivada_centrada_orden2(
        V[i-1],
        V[i+1],
        h
    )

    print("Diferencia centrada orden 2:")
    print(f"dV/df = {derivada_o2:.6f} V/kHz\n")

    # DIFERENCIA CENTRADA ORDEN 4

    if i >= 2 and i <= len(V)-3:

        derivada_o4 = derivada_centrada_orden4(
            V[i-2],
            V[i-1],
            V[i+1],
            V[i+2],
            h
        )

        print("Diferencia centrada orden 4:")
        print(f"dV/df = {derivada_o4:.6f} V/kHz\n")

    else:

        print("Diferencia centrada orden 4:")
        print("No hay suficientes puntos.\n")

    # DERIVADA DEL SPLINE

    derivada_spline = spline_derivada(freq)

    print("Derivada usando spline:")
    print(f"dV/df = {derivada_spline:.6f} V/kHz\n")

# DERIVADA EN EL EXTREMO INFERIOR

print("================================================")
print("DERIVADA EN f = 10 kHz")
print("================================================\n")

derivada_extremo = derivada_progresiva_orden2(
    V[0],
    V[1],
    V[2],
    h
)

print("Diferencia progresiva orden 2:")
print(f"dV/df = {derivada_extremo:.6f} V/kHz\n")

# Comparacion con spline
derivada_spline_10 = spline_derivada(10.0)

print("Derivada usando spline:")
print(f"dV/df = {derivada_spline_10:.6f} V/kHz\n")

# GRAFICA DE DERIVADA DEL SPLINE

f_fina = np.linspace(min(f), max(f), 1000)

derivada_fina = spline_derivada(f_fina)

plt.figure(figsize=(12,6))

plt.plot(
    f_fina,
    derivada_fina,
    'r',
    linewidth=2,
    label='dV/df usando spline'
)

plt.axhline(
    0,
    color='black',
    linestyle='--'
)

plt.xlabel('Frecuencia (kHz)')
plt.ylabel('dV/df (V/kHz)')
plt.title('Derivada del Voltaje respecto a la Frecuencia')

plt.grid(True)
plt.legend()

plt.show()

# INTERPRETACION AUTOMATICA
print("================================================")
print("INTERPRETACION FISICA")
print("================================================\n")

for freq in frecuencias:

    valor = spline_derivada(freq)

    print(f"Frecuencia: {freq} kHz")

    if valor > 0:

        print("La derivada es positiva.")
        print("El voltaje aumenta con la frecuencia.")

    else:

        print("La derivada es negativa.")
        print("El voltaje disminuye con la frecuencia.")

    if abs(valor) > 0.05:

        print("Alta sensibilidad del sistema.\n")

    else:

        print("Sensibilidad moderada del sistema.\n")