import math
import numpy as np
import scipy.integrate as integrate

#Recibir parametros de la interfaz
def calculate_area(interpolators: list[tuple[float, float]], a: int, b: int):
    # Numero de interpolantes
    n = len(interpolators)

    # Debemos integrar la base de los polinomios en este caso la base canonica
    # para construir el b del sistema de ecuaciones Aw = k
    k = np.empty(n)
    for i in range(n):
        # calculamos la integral desde 'a' hasta 'b' de x^i
        k[i] = (1/(i+1)) * (math.pow(b, i + 1) - math.pow(a, i + 1))

    # Contruimos la matriz de Vandermore
    A = np.empty((n, n))
    for i in range(n):
        for j in range(n):
            # A_{i,j} = x_j^i
            A[i][j] = math.pow(interpolators[j][0], i)

    # Calculamos los w_i
    w = np.linalg.solve(A, k)

    area: float = 0
    for i in range(n):
        area += w[i] * interpolators[i][1]  # pyright: ignore[reportAny]

    return area

print(calculate_area([(0, 0), (1/3, 1/27), (1, 1)], 0, 1))
