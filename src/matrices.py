# Engineering Solver - matrices.py
# Algebra matricial: eliminacion de Gauss con pivoteo parcial,
# rango, deteccion de singularidad, determinante e inversa.
# Matrices como listas de listas (filas). Dimension arbitraria.

from config import *


def mat_cero(m, n):
    return [[0.0] * n for _ in range(m)]


def mat_id(n):
    M = mat_cero(n, n)
    for i in range(n):
        M[i][i] = 1.0
    return M


def mat_copia(A):
    return [list(f) for f in A]


def mat_t(A):
    if not A:
        return []
    return [[A[i][j] for i in range(len(A))] for j in range(len(A[0]))]


def mat_mul(A, B):
    m = len(A)
    n = len(B[0])
    p = len(B)
    C = mat_cero(m, n)
    for i in range(m):
        for j in range(n):
            s = 0.0
            for k in range(p):
                s += A[i][k] * B[k][j]
            C[i][j] = s
    return C


def mat_vec(A, x):
    return [sum([A[i][j] * x[j] for j in range(len(x))]) for i in range(len(A))]


def escala_mat(A):
    s = 0.0
    for f in A:
        for v in f:
            if abs(v) > s:
                s = abs(v)
    if s == 0.0:
        s = 1.0
    return s


def _fila_txt(f, w=8):
    return " ".join([padl(fmt(v, 2), w) for v in f])


def mat_lineas(A, b=None, w=8):
    """Lineas de texto para mostrar [A | b]."""
    L = []
    for i in range(len(A)):
        s = "[" + _fila_txt(A[i], w)
        if b is not None:
            s += " |" + padl(fmt(b[i], 2), w)
        L.append(s + "]")
    return L


def gauss(A, b, tol=None, log=None, nombres=None):
    """Resuelve A x = b (m x n, cualquier forma) por eliminacion de
    Gauss-Jordan con pivoteo parcial.
    Devuelve dict:
      estado: 'unica' | 'infinitas' | 'incompatible' | 'vacia'
      x: solucion (si unica), rango, rango_aum, libres, piv
    Si 'log' es una lista, agrega la descripcion de cada operacion."""
    if tol is None:
        tol = CFG["tol"]
    m = len(A)
    n = len(A[0]) if m else 0
    if n == 0:
        inc = False
        for v in b:
            if abs(v) > 1e-9:
                inc = True
        return {"estado": "incompatible" if inc else "vacia", "x": [],
                "rango": 0, "rango_aum": 1 if inc else 0, "libres": [],
                "piv": []}
    M = [list(A[i]) + [b[i]] for i in range(m)]
    eps = tol * escala_mat(A) * 1e3
    if eps < 1e-12:
        eps = 1e-12
    fila = 0
    piv = []
    for col in range(n):
        if fila >= m:
            break
        # pivoteo parcial
        mejor = fila
        for i in range(fila + 1, m):
            if abs(M[i][col]) > abs(M[mejor][col]):
                mejor = i
        if abs(M[mejor][col]) <= eps:
            if log is not None:
                nm = nombres[col] if nombres else "x" + str(col + 1)
                log.append("Col " + nm + ": sin pivote (0)")
            continue
        if mejor != fila:
            M[fila], M[mejor] = M[mejor], M[fila]
            if log is not None:
                log.append("F" + str(fila + 1) + " <-> F" + str(mejor + 1))
        p = M[fila][col]
        if abs(p - 1.0) > 1e-15:
            for j in range(col, n + 1):
                M[fila][j] = M[fila][j] / p
            if log is not None:
                log.append("F" + str(fila + 1) + " <- F" + str(fila + 1) +
                           " / (" + fmt(p) + ")")
        for i in range(m):
            if i == fila:
                continue
            k = M[i][col]
            if abs(k) > 0.0:
                for j in range(col, n + 1):
                    M[i][j] = M[i][j] - k * M[fila][j]
                M[i][col] = 0.0
                if log is not None:
                    log.append("F" + str(i + 1) + " <- F" + str(i + 1) +
                               " - (" + fmt(k) + ")F" + str(fila + 1))
        piv.append(col)
        fila += 1
    rango = len(piv)
    # limpieza de ruido
    for i in range(m):
        for j in range(n + 1):
            if abs(M[i][j]) <= eps:
                M[i][j] = 0.0
    rango_aum = rango
    epsb = tol * max(escala_mat(A), max([abs(v) for v in b] + [1.0])) * 1e3
    for i in range(rango, m):
        if abs(M[i][n]) > epsb:
            rango_aum = rango + 1
            break
    libres = [j for j in range(n) if j not in piv]
    res = {"rango": rango, "rango_aum": rango_aum, "libres": libres,
           "piv": piv, "x": None, "M": M}
    if rango_aum > rango:
        res["estado"] = "incompatible"
    elif rango < n:
        res["estado"] = "infinitas"
    else:
        res["estado"] = "unica"
        x = [0.0] * n
        for i in range(rango):
            x[piv[i]] = M[i][n]
        res["x"] = x
    return res


def rango(A, tol=None):
    if not A:
        return 0
    return gauss(A, [0.0] * len(A), tol)["rango"]


def det(A, tol=None):
    """Determinante por eliminacion con pivoteo parcial (matriz cuadrada)."""
    n = len(A)
    M = mat_copia(A)
    d = 1.0
    eps = (tol if tol is not None else CFG["tol"]) * escala_mat(A) * 1e3
    for c in range(n):
        p = c
        for i in range(c + 1, n):
            if abs(M[i][c]) > abs(M[p][c]):
                p = i
        if abs(M[p][c]) <= eps:
            return 0.0
        if p != c:
            M[p], M[c] = M[c], M[p]
            d = -d
        d *= M[c][c]
        for i in range(c + 1, n):
            k = M[i][c] / M[c][c]
            for j in range(c, n):
                M[i][j] -= k * M[c][j]
    return d


def inversa(A, tol=None):
    """Inversa por Gauss-Jordan. Devuelve None si es singular."""
    n = len(A)
    cols = []
    for j in range(n):
        e = [0.0] * n
        e[j] = 1.0
        r = gauss(A, e, tol)
        if r["estado"] != "unica":
            return None
        cols.append(r["x"])
    return mat_t(cols)


def residuo(A, x, b):
    """max |A x - b|"""
    r = 0.0
    Ax = mat_vec(A, x)
    for i in range(len(b)):
        e = abs(Ax[i] - b[i])
        if e > r:
            r = e
    return r
