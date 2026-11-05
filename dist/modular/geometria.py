import math
from vectores import *
def dist(p, q):
    return math.sqrt((q[0] - p[0]) ** 2 + (q[1] - p[1]) ** 2)
def brazo(punto, direc, ref):
    u = v_unit(direc)
    if u is None:
        return None
    r = (punto[0] - ref[0], punto[1] - ref[1])
    return abs(cruz2(r, u))
def iguales(p, q, tol=1e-9):
    return abs(p[0] - q[0]) <= tol and abs(p[1] - q[1]) <= tol
def caja(puntos):
    if not puntos:
        return (0.0, 0.0, 1.0, 1.0)
    xs = [p[0] for p in puntos]
    ys = [p[1] for p in puntos]
    return (min(xs), min(ys), max(xs), max(ys))
def interp(p, q, t):
    return (p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t)
def carga_lineal(L, w1, w2):
    W = 0.5 * (w1 + w2) * L
    s = w1 + w2
    if abs(s) < 1e-15:
        return (0.0, 0.5 * L)
    xc = L * (w1 + 2.0 * w2) / (3.0 * s)
    return (W, xc)
def colineales(p, q, r, tol=1e-9):
    return abs(cruz2(v_sub(q, p), v_sub(r, p))) <= tol
