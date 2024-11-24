import math

# Método del Trapecio
def trapezoidal_rule(f, a, b, n):
    h = (b - a) / n  # Calcula el ancho de cada subintervalo
    integral = (f(a) + f(b)) / 2.0  # Inicializa la integral con los valores en los extremos
    print(f"Initial integral value: {integral}")
    for i in range(1, n):
        x_i = a + i * h  # Calcula el valor de x en el subintervalo i
        f_x_i = f(x_i)  # Calcula el valor de la función en x_i
        integral += f_x_i  # Suma el valor de la función a la integral
        print(f"Step {i}, x = {x_i}, f(x) = {f_x_i}, integral = {integral}")
    integral *= h  # Multiplica la suma por el ancho del subintervalo
    print(f"Final integral value after multiplying by h: {integral}")
    return integral

# Método de Simpson
def simpson_rule(f, a, b, n):
    if n % 2 == 1:
        n += 1  # Asegura que n sea par
    h = (b - a) / n  # Calcula el ancho de cada subintervalo
    integral = f(a) + f(b)  # Inicializa la integral con los valores en los extremos
    print(f"Initial integral value: {integral}")
    for i in range(1, n, 2):
        x_i = a + i * h  # Calcula el valor de x en el subintervalo impar i
        f_x_i = f(x_i)  # Calcula el valor de la función en x_i
        integral += 4 * f_x_i  # Suma cuatro veces el valor de la función a la integral
        print(f"Step {i}, x = {x_i}, 4*f(x) = {4 * f_x_i}, integral = {integral}")
    for i in range(2, n-1, 2):
        x_i = a + i * h  # Calcula el valor de x en el subintervalo par i
        f_x_i = f(x_i)  # Calcula el valor de la función en x_i
        integral += 2 * f_x_i  # Suma dos veces el valor de la función a la integral
        print(f"Step {i}, x = {x_i}, 2*f(x) = {2 * f_x_i}, integral = {integral}")
    integral *= h / 3  # Multiplica la suma por h/3
    print(f"Final integral value after multiplying by h/3: {integral}")
    return integral

# Método de Romberg
def romberg_integration(f, a, b, tol=1e-6):
    R = [[0.5 * (b - a) * (f(a) + f(b))]]  # Inicializa R[0][0] con el método del trapecio básico
    print(f"R[0][0] = {R[0][0]}")
    n = 1
    iteration = 0
    while True:
        iteration += 1
        n *= 2  # Duplica el número de subintervalos en cada iteración
        h = (b - a) / n  # Calcula el ancho de cada subintervalo
        sum_f = sum(f(a + (k - 0.5) * h) for k in range(1, n + 1))  # Suma los valores medios de los subintervalos
        R.append([0.5 * R[-1][0] + sum_f * h])  # Calcula R[iteration][0] usando el método del trapecio refinado
        print(f"Iteration {iteration}, R[{iteration}][0] = {R[-1][0]}")
        for j in range(1, iteration + 1):  # Calcula las extrapolaciones de Richardson para mejorar la precisión
            R[-1].append((4**j * R[-1][j-1] - R[-2][j-1]) / (4**j - 1))
            print(f"R[{iteration}][{j}] = {R[-1][j]}")
        if iteration > 1 and abs(R[-1][-1] - R[-2][-2]) < tol:  # Verifica si la diferencia entre las últimas dos estimaciones es menor que la tolerancia
            return R[-1][-1]

# Ejemplo de uso
# Define tu función aquí. Puedes cambiar esta función a cualquier otra ecuación que desees integrar.
def f(x):
    return x**2  # Ejemplo con x^2

# Define el intervalo de integración [a, b]
a = 0          # Límite inferior del intervalo
b = 1          # Límite superior del intervalo

# Define el número de subintervalos (n)
n = 10         # Número de subintervalos. Puedes ajustar este valor según la precisión que necesites.

print("Método del Trapecio:")
trapezoidal_rule(f, a, b, n)

print("\nMétodo de Simpson:")
simpson_rule(f, a, b, n)

print("\nMétodo de Romberg:")
romberg_integration(f, a, b)