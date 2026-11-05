import math
from config import *
from vectores import *
from matrices import *
from expresion import *
from geometria import *
from elementos import *
from estatica2d import *
from solucionador import *
from guardar import *
from ejemplos import *
_R = {"ok": 0, "fallo": 0, "log": []}
def _chk(nom, cond, extra=""):
    if cond:
        _R["ok"] += 1
    else:
        _R["fallo"] += 1
        _R["log"].append("FALLO: " + nom + (" " + extra if extra else ""))
def _cerca(a, b, tol=1e-6):
    return abs(a - b) <= tol * max(1.0, abs(b))
def t_vectores():
    f = polar(100, 30)
    _chk("polar x", _cerca(f[0], 86.6025403784))
    _chk("polar y", _cerca(f[1], 50.0))
    _chk("polar 270 x=0", f[0] == 0.0 or abs(polar(1, 270)[0]) < 1e-12)
    _chk("dot", _cerca(v_dot((1, 2, 3), (4, -5, 6)), 12.0))
    c = v_cross((1, 0, 0), (0, 1, 0))
    _chk("cruz i x j = k", c == (0, 0, 1))
    c = v_cross((2, 3, 4), (5, 6, 7))
    _chk("cruz general", c == (-3, 6, -3))
    _chk("cruz2", cruz2((3, 0), (0, 2)) == 6)
    _chk("norma", _cerca(v_norm((3, 4)), 5.0))
    _chk("unitario nulo", v_unit((0, 0)) is None)
    _chk("momento +", momento2d((1, 0), (0, 0), (0, 10)) == 10)
    _chk("momento -", momento2d((0, 1), (0, 0), (10, 0)) == -10)
    _chk("momento 3D", momento3d((0, 2, 0), (0, 0, 0), (3, 0, 0)) ==
         (0, 0, -6))
    _chk("ang_de 135", _cerca(ang_de((-1, 1)), 135.0))
    _chk("ang_de 270", _cerca(ang_de((0, -1)), 270.0))
    _chk("ang_entre", _cerca(ang_entre((1, 0), (0, 3)), 90.0))
    _chk("rad/grad", _cerca(grad(rad(37.0)), 37.0))
    pr = proy((3, 4), (1, 0))
    _chk("proyeccion", _cerca(pr[0], 3.0))
def t_matrices():
    A = [[2, 1, -1], [-3, -1, 2], [-2, 1, 2]]
    b = [8, -11, -3]
    g = gauss(A, b)
    _chk("gauss unica", g["estado"] == "unica")
    if g["x"]:
        _chk("gauss x", _cerca(g["x"][0], 2) and _cerca(g["x"][1], 3) and
             _cerca(g["x"][2], -1))
    g = gauss([[1, 2], [2, 4]], [3, 6])
    _chk("gauss infinitas", g["estado"] == "infinitas")
    g = gauss([[1, 2], [2, 4]], [3, 7])
    _chk("gauss incompatible", g["estado"] == "incompatible")
    g = gauss([[0, 1], [1, 0]], [5, 7])
    _chk("pivoteo", g["estado"] == "unica" and _cerca(g["x"][0], 7))
    g = gauss([[1e-14, 1], [1, 1]], [1, 2])
    _chk("pivote pequeno", g["estado"] == "unica" and _cerca(g["x"][0], 1))
    _chk("rango", rango([[1, 2, 3], [2, 4, 6], [1, 0, 1]]) == 2)
    _chk("det", _cerca(det([[1, 2], [3, 4]]), -2.0))
    _chk("det singular", det([[1, 2], [2, 4]]) == 0.0)
    I = inversa([[4, 7], [2, 6]])
    _chk("inversa", I is not None and _cerca(I[0][0], 0.6) and
         _cerca(I[1][0], -0.2))
    _chk("inversa singular", inversa([[1, 2], [2, 4]]) is None)
    g = gauss([[1, 1], [1, -1], [2, 0]], [2, 0, 2])
    _chk("sobredeterminado compatible", g["estado"] == "unica")
    g = gauss([[1, 1], [1, -1], [2, 0]], [2, 0, 5])
    _chk("sobredeterminado incompatible", g["estado"] == "incompatible")
def t_expresion():
    _chk("expr 1", _cerca(evaluar("2+3*4"), 14))
    _chk("expr pot", _cerca(evaluar("2^3^2"), 512))
    _chk("expr neg", _cerca(evaluar("-2^2"), -4))
    _chk("expr trig", _cerca(evaluar("500*cos(60)"), 250))
    _chk("expr sqrt", _cerca(evaluar("sqrt(2)/2"), 0.70710678118))
    _chk("expr implicita", _cerca(evaluar("2pi"), 2 * math.pi))
    _chk("expr sci", _cerca(evaluar("1.5e3"), 1500))
    _chk("expr atan", _cerca(evaluar("atan(1)"), 45))
    try:
        evaluar("2+")
        _chk("expr error", False)
    except ErrorExpr:
        _chk("expr error", True)
    try:
        evaluar("1/0")
        _chk("expr div0", False)
    except ErrorExpr:
        _chk("expr div0", True)
def t_geometria():
    W, xc = carga_lineal(6, 0, 600)
    _chk("triangular W", _cerca(W, 1800))
    _chk("triangular xc", _cerca(xc, 4))
    W, xc = carga_lineal(4, 100, 300)
    _chk("trapecio xc", _cerca(xc, 4 * (100 + 600) / (3 * 400)))
    _chk("brazo", _cerca(brazo((0, 3), (1, 0), (0, 0)), 3))
    _chk("colineales", colineales((0, 0), (1, 1), (3, 3)))
def _resuelve_igual(m, esperado, nombre):
    R = resolver(m)
    if isinstance(esperado, str):
        _chk(nombre + " estado", R["estado"] == esperado, R["estado"])
        return R
    _chk(nombre + " determinado", R["estado"] == "determinado",
         R["estado"] + " " + str(R["msgs"]))
    if R["estado"] != "determinado":
        return R
    for k in esperado:
        v = R["x"].get(k)
        _chk(nombre + " " + k, v is not None and
             abs(v - esperado[k]) <= 1e-4 * max(1.0, abs(esperado[k])),
             str(v) + " != " + str(esperado[k]))
    _chk(nombre + " equilibrio", R["chk"]["ok"])
    return R
def t_ejemplos():
    for nom, f in EJEMPLOS:
        m, e = f()
        R = _resuelve_igual(m, e, nom)
        try:
            P = pasos(m, R)
            _chk(nom + " pasos", len(P) >= 2)
        except Exception as ex:
            _chk(nom + " pasos", False, str(ex))
def _trasladar(m, dx, dy):
    for n in m.nodos:
        n.x += dx
        n.y += dy
def t_invariancia():
    for nom, f in EJEMPLOS:
        m, e = f()
        if isinstance(e, str):
            continue
        _trasladar(m, 7.3, -2.1)
        _resuelve_igual(m, e, nom + " trasl")
    for nom, f in EJEMPLOS[:9]:
        m, e = f()
        for n in m.nodos:
            R = resolver(m, n.nom)
            ok = R["estado"] == "determinado"
            for k in e:
                ok = ok and abs(R["x"][k] - e[k]) <= 1e-4 * max(1, abs(e[k]))
            _chk(nom + " ref " + n.nom, ok)
        R = resolver(m, (3.7, -8.2))
        ok = R["estado"] == "determinado"
        for k in e:
            ok = ok and abs(R["x"][k] - e[k]) <= 1e-4 * max(1, abs(e[k]))
        _chk(nom + " ref arbitraria", ok)
    for th in (30.0, 117.0, 245.0):
        m, e = ej_pluma()
        c = cosd(th)
        s = sind(th)
        for n in m.nodos:
            x, y = n.x, n.y
            n.x = c * x - s * y
            n.y = s * x + c * y
        f = m.fuerzas[0]
        nf = fuerza_polar(f.nom, f.nodo, f.mag, f.ang + th)
        m.fuerzas[0] = nf
        R = resolver(m)
        _chk("rotacion " + str(th) + " T", R["estado"] == "determinado" and
             _cerca(R["x"]["TBC"], 3333.33333, 1e-6))
        if R["estado"] == "determinado":
            RA = math.sqrt(R["x"]["Ax"] ** 2 + R["x"]["Ay"] ** 2)
            _chk("rotacion " + str(th) + " RA", _cerca(RA, 2666.66667, 1e-6))
def t_validacion():
    m = Modelo()
    m.nodos.append(Nodo("A", 0, 0))
    m.nodos.append(Nodo("B", 0, 0))
    _chk("nodos coincidentes", resolver(m)["estado"] == "invalido")
    m = Modelo()
    m.nuevo_nodo(0, 0)
    m.add_miembro("viga", "A", "A")
    _chk("miembro longitud 0", resolver(m)["estado"] == "invalido")
    m = Modelo()
    m.nuevo_nodo(0, 0)
    m.add_apoyo("cab", "A", 0, "A")
    _chk("cable longitud 0", resolver(m)["estado"] == "invalido")
    m = Modelo("particula")
    m.nuevo_nodo(0, 0)
    m.nuevo_nodo(1, 0)
    m.add_fuerza_comp("A", 1, 0)
    m.add_fuerza_comp("B", -1, 0)
    _chk("particula no concurrente", resolver(m)["estado"] == "invalido")
    m = Modelo()
    _chk("modelo vacio", resolver(m)["estado"] == "invalido")
    m = Modelo()
    m.nuevo_nodo(0, 0)
    m.nuevo_nodo(2, 0)
    m.add_carga("A", "B", 100, -100)
    _chk("carga signos mixtos", resolver(m)["estado"] == "invalido")
    m = Modelo()
    m.nuevo_nodo(0, 0)
    m.nuevo_nodo(4, 0)
    m.add_miembro("viga", "A", "B")
    m.add_apoyo("pin", "A")
    m.add_apoyo("rod", "B", 180)
    m.add_fuerza_pol("B", 100, 270)
    R = resolver(m)
    _chk("concurrentes incompatible", R["estado"] == "incompatible",
         R["estado"])
    m = Modelo()
    for x in (0, 2, 4):
        m.nuevo_nodo(x, 0)
    m.add_apoyo("rod", "A", 90)
    m.add_apoyo("rod", "B", 90)
    m.add_apoyo("rod", "C", 90)
    m.add_fuerza_pol("B", 100, 270)
    R = resolver(m)
    _chk("paralelos indeterminado", R["estado"] == "indeterminado")
    m = Modelo()
    m.nuevo_nodo(0, 0)
    m.nuevo_nodo(4, 0)
    m.nuevo_nodo(0, 3)
    m.add_miembro("viga", "A", "B")
    m.add_apoyo("pin", "A")
    m.add_apoyo("cab", "B", 0, "C")
    m.add_fuerza_pol("B", 2000, 90)
    R = resolver(m)
    _chk("aviso cable compresion", R["estado"] == "determinado" and
         len([a for a in R["avisos"] if "COMPRESION" in a]) == 1)
    m = Modelo()
    m.nuevo_nodo(0, 0)
    m.add_fuerza_comp("A", 5, 0)
    m.add_fuerza_comp("A", -5, 0)
    _chk("equilibrio sin incognitas", resolver(m)["estado"] == "equilibrio")
    m = Modelo("particula")
    m.nuevo_nodo(0, 0, "P")
    for x, y in ((-1, 1), (0, 1), (1, 1)):
        m.nuevo_nodo(x, y)
    for n in m.nodos[1:]:
        m.add_apoyo("cab", "P", 0, n.nom)
    m.add_fuerza_pol("P", 10, 270)
    _chk("particula 3 cables", resolver(m)["estado"] == "indeterminado")
def t_particula_libre():
    m = Modelo("particula")
    m.nuevo_nodo(0, 0, "P")
    m.add_fuerza_pol("P", 100, 30)
    m.add_fuerza_pol("P", 50, 135)
    m.add_fdesc("P", "libre")
    R = resolver(m)
    fx = -(100 * cosd(30) + 50 * cosd(135))
    fy = -(100 * sind(30) + 50 * sind(135))
    _chk("particula P libre", R["estado"] == "determinado" and
         _cerca(R["x"]["P1x"], fx) and _cerca(R["x"]["P1y"], fy))
    m = Modelo("particula")
    m.nuevo_nodo(0, 0, "P")
    m.add_fuerza_pol("P", 100, 270)
    m.add_fdesc("P", "dir", 90)
    R = resolver(m)
    _chk("particula P dir", R["estado"] == "determinado" and
         _cerca(R["x"]["P1"], 100))
def t_internas():
    m, e = ej_viga_simple()
    R = resolver(m)
    N, V, M, d = internas(m, R, 1.0)
    _chk("V(1)=Ay", _cerca(V, 800))
    _chk("M(1)=800", _cerca(M, 800))
    N, V, M, d = internas(m, R, 2.0 + 1e-6)
    _chk("V tras carga", _cerca(V, -400, 1e-4))
    _chk("M max = Pab/L", _cerca(M, 1200 * 2 * 4 / 6.0, 1e-4))
    m, e = ej_triangular()
    R = resolver(m)
    x = 3.0
    N, V, M, d = internas(m, R, x)
    _chk("M triangular", _cerca(M, 600 * x - 600 * x ** 3 / 36.0))
    _chk("V triangular", _cerca(V, 600 - 600 * x * x / 12.0))
    m, e = ej_voladizo()
    R = resolver(m)
    N, V, M, d = internas(m, R, 1e-7)
    _chk("voladizo M empotr", _cerca(M, -10.5, 1e-4))
def t_guardar():
    for nom, f in EJEMPLOS:
        m, e = f()
        R1 = resolver(m)
        m2 = decodificar(codificar(m))
        R2 = resolver(m2)
        ok = R1["estado"] == R2["estado"]
        for k in R1["x"]:
            ok = ok and k in R2["x"] and _cerca(R1["x"][k], R2["x"][k])
        _chk("guardar " + nom, ok)
def correr():
    _R["ok"] = 0
    _R["fallo"] = 0
    _R["log"] = []
    for t in (t_vectores, t_matrices, t_expresion, t_geometria, t_ejemplos,
              t_invariancia, t_validacion, t_particula_libre, t_internas,
              t_guardar):
        try:
            t()
        except Exception as ex:
            _R["fallo"] += 1
            _R["log"].append("EXCEPCION en prueba: " + str(ex))
    return _R["ok"], _R["fallo"], list(_R["log"])
