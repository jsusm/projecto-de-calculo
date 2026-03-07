import numpy as np
from scipy.interpolate import CubicSpline
from scipy import integrate

def build_splines(nodes: list[tuple[float, float]]):
    P = np.asarray(nodes, float)
    #Obligamos a ser una curva cerrada
    if not np.allclose(P[0], P[-1]):
        P = np.vstack([P, P[0]])  # pyright: ignore[reportConstantRedefinition]

    #Ignoramos cuando otro nodo no esta distante de otro
    d = np.diff(P, axis=0)
    keep = np.r_[True, np.hypot(d[:,0], d[:,1]) > 0]
    P = P[keep]  # pyright: ignore[reportConstantRedefinition]

    # Parametrizamos calculando las distancias acumuladas
    d = np.diff(P, axis=0)
    seg = np.hypot(d[:,0], d[:,1])
    S = np.r_[0.0, np.cumsum(seg)]
    t: list[float] = S / S[-1]

    Sx = CubicSpline(t, P[:,0], bc_type='periodic')
    Sy = CubicSpline(t, P[:,1], bc_type='periodic')
    return Sx, Sy, t

def area_green(Sx, Sy):
    def integrand(u):
        return 0.5 * (Sx(u) * Sy(u, 1) - Sy(u) * Sx(u, 1))
    
    val, _ = integrate.quad(integrand, 0.0, 1.0, epsabs=1e-9, epsrel=1e-9)
    return float(val)

def calculateArea(nodes):
    Sx, Sy, t = build_splines(nodes)
    return area_green(Sx, Sy)

#Callee
def areaBetween(nodes_f, nodes_g):
    return np.abs(calculateArea(nodes_f) - calculateArea(nodes_g))

# Test
# nodes_f = [(0,-2), (2,0), (0,2), (-2,0), (-1.5, -1.5), (1.5, 1.5),(-1.5, 1.5), (1.5, 1.5)]  # Poligon
# nodes_g = [(0,-1), (1,0), (0,1), (-1,0), (0.5,-0.5), (0.5,0.5), (0.5,0.5), (-0.5,0.5)]  # Poligon

# circle1 = [
#     (10.0, 0.0),
#     (8.090169944, 5.877852522),
#     (3.090169944, 9.510565163),
#     (0.0, 10.0),
#     (-3.090169944, 9.510565163),
#     (-8.090169944, 5.877852522),
#     (-10.0, 0.0),
#     (-9.510565163, -3.090169944),
#     (-8.090169944, -5.877852522),
#     (-3.090169944, -9.510565163),
#     (0.0, -10.0),
#     (3.090169944, -9.510565163),
#     (5.877852522, -8.090169944),
#     (9.510565163, -3.090169944)
# ]

# circle2 = [
#     (3.0, 1.0),
#     (2.902113033, 1.618033989),
#     (2.175570505, 2.618033989),
#     (1.0, 3.0),
#     (-0.175570505, 2.618033989),
#     (-0.902113033, 1.618033989),
#     (-1.0, 1.0),
#     (-0.902113033, 0.381966011),
#     (-0.175570505, -0.618033989),
#     (1.0, -1.0),
#     (1.618033989, -0.902113033),
#     (2.175570505, -0.618033989),
#     (2.618033989, -0.175570505),
#     (2.902113033, 0.381966011)
# ]


# print(f"Area entre las curvas = {areaBetween(circle1, circle2)}")
