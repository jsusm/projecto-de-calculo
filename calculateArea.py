import numpy as np
import scipy.integrate as integrate

#Recibir parametros de la interfaz
def calculate_area(f_points, g_points, x1, x2):
    print("Calculando area con puntos f:", f_points)
    print("Calculando area con puntos g:", g_points)
    print("Subintervalos en x:", x1, x2)