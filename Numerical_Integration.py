import math
import matplotlib.pyplot as plt

# Método del Trapecio
def trapezoidal_rule(f, a, b, n):
    h = (b - a) / n  # Calcula el ancho de cada subintervalo
    integral = (f(a) + f(b)) / 2.0  # Inicializa la integral con los valores en los extremos
    print(f"Trapecio - Inicial integral value: {integral}")
    for i in range(1, n):
        x_i = a + i * h  # Calcula el valor de x en el subintervalo i
        f_x_i = f(x_i)  # Calcula el valor de la función en x_i
        integral += f_x_i  # Suma el valor de la función a la integral
        print(f"Trapecio - Step {i}, x = {x_i}, f(x) = {f_x_i}, integral = {integral}")
    integral *= h  # Multiplica la suma por el ancho del subintervalo
    print(f"Trapecio - Final integral value after multiplying by h: {integral}")
    return integral

# Método de Simpson
def simpson_rule(f, a, b, n):
    if n % 2 == 1:
        n += 1  # Asegura que n sea par
    h = (b - a) / n  # Calcula el ancho de cada subintervalo
    integral = f(a) + f(b)  # Inicializa la integral con los valores en los extremos
    print(f"Simpson - Initial integral value: {integral}")
    for i in range(1, n, 2):
        x_i = a + i * h  # Calcula el valor de x en el subintervalo impar i
        f_x_i = f(x_i)  # Calcula el valor de la función en x_i
        integral += 4 * f_x_i  # Suma cuatro veces el valor de la función a la integral
        print(f"Simpson - Step {i}, x = {x_i}, 4*f(x) = {4 * f_x_i}, integral = {integral}")
    for i in range(2, n, 2):
        x_i = a + i * h  # Calcula el valor de x en el subintervalo par i
        f_x_i = f(x_i)  # Calcula el valor de la función en x_i
        integral += 2 * f_x_i  # Suma dos veces el valor de la función a la integral
        print(f"Simpson - Step {i}, x = {x_i}, 2*f(x) = {2 * f_x_i}, integral = {integral}")
    integral *= h / 3  # Multiplica la suma por h/3
    print(f"Simpson - Final integral value after multiplying by h/3: {integral}")
    return integral

# Método de Romberg
def romberg_integration(f, a, b, tol=1e-6):
    R = [[0.5 * (b - a) * (f(a) + f(b))]]  # Inicializa R[0][0] con el método del trapecio básico
    print(f"Romberg - R[0][0] = {R[0][0]}")
    n = 1
    iteration = 0
    while True:
        iteration += 1
        n *= 2  # Duplica el número de subintervalos en cada iteración
        h = (b - a) / n  # Calcula el ancho de cada subintervalo
        sum_f = sum(f(a + (k - 0.5) * h) for k in range(1, n + 1))  # Suma los valores medios de los subintervalos
        R.append([0.5 * R[-1][0] + sum_f * h])  # Calcula R[iteration][0] usando el método del trapecio refinado
        print(f"Romberg - Iteration {iteration}, R[{iteration}][0] = {R[-1][0]}")
        for j in range(1, iteration + 1):  # Calcula las extrapolaciones de Richardson para mejorar la precisión
            R[-1].append((4*j * R[-1][j-1] - R[-2][j-1]) / (4*j - 1))
            print(f"Romberg - R[{iteration}][{j}] = {R[-1][j]}")
        if iteration > 1 and abs(R[-1][-1] - R[-2][-2]) < tol:  # Verifica si la diferencia entre las últimas dos estimaciones es menor que la tolerancia
            return R[-1][-1]

# Ejemplo de uso
# Define tu función aquí. Puedes cambiar esta función a cualquier otra ecuación que desees integrar.
def f(x):
    return x**2  # Ejemplo con x^2

# Define el intervalo de integración [a, b]
a = 0          # Límite inferior del intervalo
b = 1          # Límite superior del intervalo

# Define el número inicial y máximo de subintervalos (n)
n_initial = 2
n_max = 128

# Almacenar los resultados
n_values = []
trapezoidal_values = []
simpson_values = []
romberg_values = []

# Calcular las integrales para diferentes números de subintervalos
n = n_initial
while n <= n_max:
    n_values.append(n)
    print(f"\nNúmero de subintervalos: {n}")
    trapezoidal_values.append(trapezoidal_rule(f, a, b, n))
    simpson_values.append(simpson_rule(f, a, b, n))
    romberg_values.append(romberg_integration(f, a, b))
    n *= 2

# Graficar los resultados
fig, axs = plt.subplots(3, 2, figsize=(14, 18))

# Gráfica para los valores de la integral
axs[0, 0].plot(n_values, trapezoidal_values, label="Trapecio", marker='o')
axs[0, 0].set_xscale('log')
axs[0, 0].set_xlabel("Número de subintervalos (n)")
axs[0, 0].set_ylabel("Valor de la integral")
axs[0, 0].set_title("Valores de la Integral - Método del Trapecio")
axs[0, 0].legend()

axs[1, 0].plot(n_values, simpson_values, label="Simpson", marker='x')
axs[1, 0].set_xscale('log')
axs[1, 0].set_xlabel("Número de subintervalos (n)")
axs[1, 0].set_ylabel("Valor de la integral")
axs[1, 0].set_title("Valores de la Integral - Método de Simpson")
axs[1, 0].legend()

axs[2, 0].plot(n_values, romberg_values, label="Romberg", marker='s')
axs[2, 0].set_xscale('log')
axs[2, 0].set_xlabel("Número de subintervalos (n)")
axs[2, 0].set_ylabel("Valor de la integral")
axs[2, 0].set_title("Valores de la Integral - Método de Romberg")
axs[2, 0].legend()

# Calcular errores relativos
exact_value = 1/3  # Valor exacto de la integral de x^2 de 0 a 1
trapezoidal_errors = [abs(tv - exact_value) for tv in trapezoidal_values]
simpson_errors = [abs(sv - exact_value) for sv in simpson_values]
romberg_errors = [abs(rv - exact_value) for rv in romberg_values]

# Gráfica para los errores relativos
axs[0, 1].plot(n_values, trapezoidal_errors, label="Trapecio", marker='o')
axs[0, 1].set_xscale('log')
axs[0, 1].set_yscale('log')
axs[0, 1].set_xlabel("Número de subintervalos (n)")
axs[0, 1].set_ylabel("Error relativo")
axs[0, 1].set_title("Errores Relativos - Método del Trapecio")
axs[0, 1].legend()

axs[1, 1].plot(n_values, simpson_errors, label="Simpson", marker='x')
axs[1, 1].set_xscale('log')
axs[1, 1].set_yscale('log')
axs[1, 1].set_xlabel("Número de subintervalos (n)")
axs[1, 1].set_ylabel("Error relativo")
axs[1, 1].set_title("Errores Relativos - Método de Simpson")
axs[1, 1].legend()

axs[2, 1].plot(n_values, romberg_errors, label="Romberg", marker='s')
axs[2, 1].set_xscale('log')
axs[2, 1].set_yscale('log')
axs[2, 1].set_xlabel("Número de subintervalos (n)")
axs[2, 1].set_ylabel("Error relativo")
axs[2, 1].set_title("Errores Relativos - Método de Romberg")
axs[2, 1].legend()

plt.tight_layout()
plt.show()