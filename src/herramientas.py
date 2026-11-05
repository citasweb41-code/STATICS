# Engineering Solver - herramientas.py
# Herramientas matematicas independientes, todas con procedimiento.

import math
from config import *
from vectores import *
from matrices import *
from entrada import *


def h_descomp():
    p("Descomposicion de una fuerza")
    i = elegir("Tipo", ["2D: magnitud y angulo", "3D: magnitud y" +
                        " angulos directores", "3D: magnitud y punto" +
                        " (direccion r)"])
    F = leer_num("Magnitud F")
    L = []
    if i == 0:
        a = leer_num("Angulo desde +x (grados)")
        fx, fy = polar(F, a)
        L.append("Fx = F·cosθ = " + fmt(F) + "·cos(" + fmt(a, 2) +
                 "°) = " + fmt(fx))
        L.append("Fy = F·sinθ = " + fmt(F) + "·sin(" + fmt(a, 2) +
                 "°) = " + fmt(fy))
        L.append("Comprobacion: √(Fx²+Fy²) = " +
                 fmt(math.sqrt(fx * fx + fy * fy)))
    elif i == 1:
        al = leer_num("alfa (con x)")
        be = leer_num("beta (con y)")
        ga = leer_num("gamma (con z)")
        s = cosd(al) ** 2 + cosd(be) ** 2 + cosd(ga) ** 2
        L.append("cos²α+cos²β+cos²γ = " + fmt(s, 4))
        if abs(s - 1.0) > 1e-3:
            L.append("ERROR: debe ser 1. Angulos incompatibles.")
        else:
            for nm, g in (("Fx", al), ("Fy", be), ("Fz", ga)):
                L.append(nm + " = F·cos(" + fmt(g, 2) + "°) = " +
                         fmt(F * cosd(g)))
    else:
        r = leer_vec("Vector de direccion r", 3)
        n = v_norm(r)
        if n < 1e-12:
            L.append("ERROR: vector nulo.")
        else:
            u = v_esc(1.0 / n, r)
            L.append("|r| = " + fmt(n))
            L.append("u = r/|r| = " + v_str(u, lambda c: fmt(c, 4)))
            L.append("F = F·u = " + v_str(v_esc(F, u), fmt))
            L.append("Angulos directores: " +
                     v_str(dir_cosenos(u), lambda c: fmt(c, 2)))
    mostrar(L, "Resultado")


def h_resultante():
    p("Resultante de varias fuerzas 2D")
    n = leer_ent("Numero de fuerzas", 1, 20)
    L = []
    sx = 0.0
    sy = 0.0
    for k in range(n):
        i = elegir("F" + str(k + 1), ["Magnitud y angulo", "Componentes"])
        if i == 0:
            F = leer_num("  F" + str(k + 1))
            a = leer_num("  angulo")
            fx, fy = polar(F, a)
            L.append("F" + str(k + 1) + ": " + fmt(F) + "·(cos " +
                     fmt(a, 1) + ", sin " + fmt(a, 1) + ") = (" + fmt(fx) +
                     ", " + fmt(fy) + ")")
        else:
            fx, fy = leer_par("  F" + str(k + 1))
            L.append("F" + str(k + 1) + " = (" + fmt(fx) + ", " + fmt(fy) +
                     ")")
        sx += fx
        sy += fy
    R = math.sqrt(sx * sx + sy * sy)
    L.append("Rx = ΣFx = " + fmt(sx))
    L.append("Ry = ΣFy = " + fmt(sy))
    L.append("R = √(Rx²+Ry²) = " + fmt(R))
    if R > 1e-12:
        L.append("θ = atan2(Ry,Rx) = " + fmt(ang_de((sx, sy)), 3) +
                 "°")
    mostrar(L, "Resultante")


def h_momento():
    p("Momento de una fuerza")
    i = elegir("Tipo", ["2D (escalar)", "3D (vector r x F)"])
    L = []
    if i == 0:
        P = leer_par("Punto de aplicacion P")
        O = leer_par("Punto de referencia O")
        j = elegir("Fuerza", ["Magnitud y angulo", "Componentes"])
        if j == 0:
            F = leer_num("F")
            a = leer_num("angulo")
            Fv = polar(F, a)
        else:
            Fv = leer_par("F")
        rx = P[0] - O[0]
        ry = P[1] - O[1]
        M = rx * Fv[1] - ry * Fv[0]
        L.append("r = P - O = (" + fmt(rx) + ", " + fmt(ry) + ")")
        L.append("F = (" + fmt(Fv[0]) + ", " + fmt(Fv[1]) + ")")
        L.append("M = rx·Fy - ry·Fx")
        L.append("  = (" + fmt(rx) + ")(" + fmt(Fv[1]) + ") - (" + fmt(ry) +
                 ")(" + fmt(Fv[0]) + ")")
        L.append("  = " + fmt(M) + (" antihorario" if M > 0 else
                                    (" horario" if M < 0 else "")))
        Fm = v_norm(Fv)
        if Fm > 1e-12:
            L.append("Brazo d = |M|/|F| = " + fmt(abs(M) / Fm))
    else:
        r = leer_vec("r (de O a P)", 3)
        F = leer_vec("F", 3)
        L += _cruz_txt(r, F, "M = r x F")
        L.append("|M| = " + fmt(v_norm(v_cross(r, F))))
    mostrar(L, "Momento")


def _cruz_txt(a, b, nom):
    c = v_cross(a, b)
    return [nom + " = |i j k; a; b|",
            "i: (" + fmt(a[1]) + ")(" + fmt(b[2]) + ")-(" + fmt(a[2]) + ")(" +
            fmt(b[1]) + ") = " + fmt(c[0]),
            "j: (" + fmt(a[2]) + ")(" + fmt(b[0]) + ")-(" + fmt(a[0]) + ")(" +
            fmt(b[2]) + ") = " + fmt(c[1]),
            "k: (" + fmt(a[0]) + ")(" + fmt(b[1]) + ")-(" + fmt(a[1]) + ")(" +
            fmt(b[0]) + ") = " + fmt(c[2]),
            nom.split("=")[0].strip() + " = " + v_str(c, fmt)]


def h_vectores():
    while True:
        k = menu("Vectores 2D/3D", ["Suma y resta", "Producto punto y" +
                                    " angulo", "Producto cruz", "Modulo y" +
                                    " unitario", "Proyeccion de a sobre b"])
        if k == 0:
            return
        try:
            d = 3 if elegir("Dimension", ["2D", "3D"]) == 1 else 2
            a = leer_vec("a", d)
            L = []
            if k in (1, 2, 3, 5):
                b = leer_vec("b", d)
            if k == 1:
                L.append("a + b = " + v_str(v_add(a, b), fmt))
                L.append("a - b = " + v_str(v_sub(a, b), fmt))
            elif k == 2:
                pp = v_dot(a, b)
                L.append("a·b = " + " + ".join(["(" + fmt(a[i]) + ")(" +
                                                    fmt(b[i]) + ")"
                                                    for i in range(d)]))
                L.append("    = " + fmt(pp))
                g = ang_entre(a, b)
                if g is not None:
                    L.append("cosθ = a·b/(|a||b|) = " + fmt(pp) + "/(" +
                             fmt(v_norm(a)) + "·" + fmt(v_norm(b)) + ")")
                    L.append("θ = " + fmt(g, 3) + "°")
            elif k == 3:
                L += _cruz_txt(a, b, "a x b")
                if d == 2:
                    L.append("(En 2D solo existe la componente k)")
            elif k == 4:
                n = v_norm(a)
                L.append("|a| = √(" + " + ".join([fmt(c) + "²"
                                                     for c in a]) + ")")
                L.append("    = " + fmt(n))
                u = v_unit(a)
                if u is None:
                    L.append("Vector nulo: no tiene unitario.")
                else:
                    L.append("u = a/|a| = " + v_str(u, lambda c: fmt(c, 4)))
            elif k == 5:
                r = proy(a, b)
                if r is None:
                    L.append("b es nulo.")
                else:
                    L.append("comp_b a = a·b/|b| = " + fmt(r[0]))
                    L.append("proy_b a = " + v_str(r[1], fmt))
            mostrar(L, "Resultado")
        except Cancelar:
            pass


def h_sistema():
    p("Sistema lineal A x = b (Gauss con pivoteo parcial)")
    m = leer_ent("Numero de ecuaciones", 1, 8)
    n = leer_ent("Numero de incognitas", 1, 8)
    A = []
    b = []
    for i in range(m):
        p("Ecuacion " + str(i + 1) + ": coeficientes y termino b")
        f = []
        for j in range(n):
            f.append(leer_num("  a" + str(i + 1) + str(j + 1)))
        A.append(f)
        b.append(leer_num("  b" + str(i + 1)))
    log = []
    g = gauss(A, b, None, log)
    L = ["Matriz aumentada [A|b]:"] + mat_lineas(A, b)
    L.append("Operaciones de fila:")
    L += ["  " + s for s in log]
    L.append("Matriz reducida:")
    M = g["M"]
    L += mat_lineas([f[:-1] for f in M], [f[-1] for f in M])
    L.append("rango(A)=" + str(g["rango"]) + " rango([A|b])=" +
             str(g["rango_aum"]))
    if g["estado"] == "unica":
        L.append("SOLUCION UNICA:")
        for j in range(n):
            L.append("  x" + str(j + 1) + " = " + fmt(g["x"][j]))
        L.append("Residuo max |Ax-b| = " + fmte(residuo(A, g["x"], b)))
        if m == n:
            L.append("det(A) = " + fmt(det(A)))
    elif g["estado"] == "infinitas":
        L.append("INFINITAS SOLUCIONES (sistema indeterminado).")
        L.append("Variables libres: " + ", ".join(["x" + str(j + 1)
                                                   for j in g["libres"]]))
    else:
        L.append("SIN SOLUCION (sistema incompatible).")
    mostrar(L, "Sistema")


# ---------------- conversion de unidades ----------------
_UNI = [
    ("Fuerza", [("N", 1.0), ("kN", 1000.0), ("lb", 4.4482216152605),
                ("kip", 4448.2216152605), ("kgf", 9.80665),
                ("dina", 1e-5)]),
    ("Longitud", [("m", 1.0), ("cm", 0.01), ("mm", 0.001),
                  ("ft", 0.3048), ("in", 0.0254), ("km", 1000.0)]),
    ("Momento", [("N·m", 1.0), ("kN·m", 1000.0),
                 ("lb·ft", 1.3558179483314), ("lb·in", 0.112984829),
                 ("kip·ft", 1355.8179483314)]),
    ("Carga distr.", [("N/m", 1.0), ("kN/m", 1000.0),
                      ("lb/ft", 14.593902937), ("kip/ft", 14593.902937),
                      ("lb/in", 175.12683524)]),
    ("Presion/esfuerzo", [("Pa", 1.0), ("kPa", 1e3), ("MPa", 1e6),
                          ("psi", 6894.7572932), ("ksi", 6894757.2932),
                          ("bar", 1e5)]),
    ("Masa", [("kg", 1.0), ("g", 0.001), ("lbm", 0.45359237),
              ("slug", 14.593902937)]),
]


def convertir(v, f1, f2):
    return v * f1 / f2


def h_unidades():
    while True:
        k = menu("Conversion de unidades", [u[0] for u in _UNI] +
                 ["Angulos (grados/rad)"])
        if k == 0:
            return
        try:
            if k == len(_UNI) + 1:
                i = elegir("De", ["grados -> rad", "rad -> grados"])
                v = leer_num("Valor")
                if i == 0:
                    mostrar([fmt(v) + "° = " + fmt(v, 2) + "·π/180" +
                             " = " + fmt(rad(v), 6) + " rad"])
                else:
                    mostrar([fmt(v) + " rad = " + fmt(v) + "·180/π" +
                             " = " + fmt(grad(v), 6) + "°"])
                continue
            nom, us = _UNI[k - 1]
            a = elegir("Unidad origen", [u[0] for u in us])
            b = elegir("Unidad destino", [u[0] for u in us])
            v = leer_num("Valor")
            r = convertir(v, us[a][1], us[b][1])
            mostrar([fmt(v, 6) + " " + us[a][0] + " = " + fmt(r, 6) + " " +
                     us[b][0], "(factor " + fmt(us[a][1] / us[b][1], 8) +
                     ")"])
        except Cancelar:
            pass


def menu_herramientas():
    while True:
        k = menu("HERRAMIENTAS", ["Descomposicion vectorial",
                                  "Resultante de fuerzas",
                                  "Momento de una fuerza",
                                  "Producto cruz",
                                  "Sistema de ecuaciones",
                                  "Conversion de unidades",
                                  "Vectores 2D y 3D"])
        if k == 0:
            return
        try:
            if k == 1:
                h_descomp()
            elif k == 2:
                h_resultante()
            elif k == 3:
                h_momento()
            elif k == 4:
                d = 3 if elegir("Dimension", ["2D", "3D"]) == 1 else 2
                a = leer_vec("a", d)
                b = leer_vec("b", d)
                mostrar(_cruz_txt(a, b, "a x b"), "Producto cruz")
            elif k == 5:
                h_sistema()
            elif k == 6:
                h_unidades()
            elif k == 7:
                h_vectores()
        except Cancelar:
            p("(cancelado)")
