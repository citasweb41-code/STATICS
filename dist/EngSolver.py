# ENGINEERING SOLVER v1.0 - TI-Nspire CX II CAS (Python)
# Archivo generado por tools/build.py a partir de src/.
# Estatica 2D paso a paso. Ejecutar con ctrl+R.
# ---- config ----
VERSION = "1.0"
CFG = {
    "dec": 3,
    "uni": 0,
    "ascii": 0,
    "lineas": 10,
    "ancho": 32,
    "grid": 0.5,
    "gfxin": 1,
    "tol": 1e-9,
}
SIS_UNI = [
    ("N", "m", "N\u00b7m", "N/m"),
    ("kN", "m", "kN\u00b7m", "kN/m"),
    ("lb", "ft", "lb\u00b7ft", "lb/ft"),
    ("kip", "ft", "kip\u00b7ft", "kip/ft"),
    ("lb", "in", "lb\u00b7in", "lb/in"),
]
def uF():
    return SIS_UNI[CFG["uni"]][0]
def uL():
    return SIS_UNI[CFG["uni"]][1]
def uM():
    return SIS_UNI[CFG["uni"]][2]
def uW():
    return SIS_UNI[CFG["uni"]][3]
_ASCII_MAP = [
    ("Σ", "Sum"), ("°", "deg"), ("·", "*"),
    ("θ", "th"), ("→", "->"), ("≈", "~"),
    ("≠", "!="), ("≤", "<="), ("≥", ">="),
    ("×", "x"), ("√", "sqrt"), ("∑", "Sum"),
]
def tx(s):
    if CFG["ascii"]:
        for a, b in _ASCII_MAP:
            if a in s:
                s = s.replace(a, b)
    return s
def fmt(v, d=None):
    if d is None:
        d = CFG["dec"]
    try:
        v = float(v)
    except Exception:
        return str(v)
    if v != v:
        return "nan"
    a = abs(v)
    if a >= 1e7:
        return ("%." + str(d) + "e") % v
    lim = 0.5 * (10 ** (-d))
    if a < lim:
        return ("%." + str(d) + "f") % 0.0
    return ("%." + str(d) + "f") % v
def fmts(v, d=None):
    s = fmt(v, d)
    if s[0] != "-":
        s = "+" + s
    return s
def fmte(v):
    return "%.2e" % v
def pad(s, n):
    s = str(s)
    if len(s) < n:
        s = s + " " * (n - len(s))
    return s
def padl(s, n):
    s = str(s)
    if len(s) < n:
        s = " " * (n - len(s)) + s
    return s
def wrap(s, w=None):
    if w is None:
        w = CFG["ancho"]
    if w < 12:
        w = 12
    out = []
    for par in s.split("\n"):
        k = 0
        while k < len(par) and par[k] == " ":
            k += 1
        ind = " " * min(k, 4)
        words = par.split(" ")
        line = ""
        for wd in words:
            if wd == "":
                continue
            if line == "":
                cand = ind + wd
            else:
                cand = line + " " + wd
            if len(cand) <= w or line == "":
                line = cand
            else:
                out.append(line)
                line = ind + "  " + wd
            while len(line) > w:
                out.append(line[:w])
                line = ind + "  " + line[w:]
        out.append(line)
    return out

# ---- vectores ----
import math
PI = math.pi
def rad(g):
    return g * PI / 180.0
def grad(r):
    return r * 180.0 / PI
def sind(g):
    return math.sin(rad(g))
def cosd(g):
    return math.cos(rad(g))
def limpia(v, eps=1e-12):
    if abs(v) < eps:
        return 0.0
    return v
def cosd_l(g):
    return limpia(cosd(g))
def sind_l(g):
    return limpia(sind(g))
def v_add(a, b):
    return tuple([a[i] + b[i] for i in range(len(a))])
def v_sub(a, b):
    return tuple([a[i] - b[i] for i in range(len(a))])
def v_esc(k, a):
    return tuple([k * a[i] for i in range(len(a))])
def v_dot(a, b):
    s = 0.0
    for i in range(len(a)):
        s += a[i] * b[i]
    return s
def v_norm(a):
    return math.sqrt(v_dot(a, a))
def v_unit(a, tol=1e-12):
    n = v_norm(a)
    if n < tol:
        return None
    return v_esc(1.0 / n, a)
def v_cross(a, b):
    a3 = to3(a)
    b3 = to3(b)
    return (a3[1] * b3[2] - a3[2] * b3[1],
            a3[2] * b3[0] - a3[0] * b3[2],
            a3[0] * b3[1] - a3[1] * b3[0])
def cruz2(a, b):
    return a[0] * b[1] - a[1] * b[0]
def to3(a):
    if len(a) >= 3:
        return (a[0], a[1], a[2])
    return (a[0], a[1], 0.0)
def v_sum(lista):
    if not lista:
        return (0.0, 0.0)
    s = [0.0] * len(lista[0])
    for v in lista:
        for i in range(len(v)):
            s[i] += v[i]
    return tuple(s)
def polar(mag, ang_g):
    return (limpia(mag * cosd(ang_g)), limpia(mag * sind(ang_g)))
def ang_de(v):
    a = grad(math.atan2(v[1], v[0]))
    if a < 0:
        a += 360.0
    if a >= 360.0 - 1e-10:
        a = 0.0
    return a
def ang_entre(a, b):
    na = v_norm(a)
    nb = v_norm(b)
    if na < 1e-12 or nb < 1e-12:
        return None
    c = v_dot(a, b) / (na * nb)
    if c > 1.0:
        c = 1.0
    if c < -1.0:
        c = -1.0
    return grad(math.acos(c))
def proy(a, b):
    u = v_unit(b)
    if u is None:
        return None
    s = v_dot(a, u)
    return (s, v_esc(s, u))
def momento2d(punto, ref, F):
    rx = punto[0] - ref[0]
    ry = punto[1] - ref[1]
    return rx * F[1] - ry * F[0]
def momento3d(punto, ref, F):
    r = v_sub(to3(punto), to3(ref))
    return v_cross(r, to3(F))
def dir_cosenos(v):
    n = v_norm(v)
    if n < 1e-12:
        return None
    r = []
    for c in to3(v):
        x = c / n
        if x > 1.0:
            x = 1.0
        if x < -1.0:
            x = -1.0
        r.append(grad(math.acos(x)))
    return tuple(r)
def v_str(v, f=None):
    if f is None:
        f = str
    return "(" + ", ".join([f(c) for c in v]) + ")"

# ---- matrices ----
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
    L = []
    for i in range(len(A)):
        s = "[" + _fila_txt(A[i], w)
        if b is not None:
            s += " |" + padl(fmt(b[i], 2), w)
        L.append(s + "]")
    return L
def gauss(A, b, tol=None, log=None, nombres=None):
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
    r = 0.0
    Ax = mat_vec(A, x)
    for i in range(len(b)):
        e = abs(Ax[i] - b[i])
        if e > r:
            r = e
    return r

# ---- expresion ----
import math
_FUN = {
    "sin": lambda g: math.sin(rad(g)),
    "cos": lambda g: math.cos(rad(g)),
    "tan": lambda g: math.tan(rad(g)),
    "asin": lambda v: grad(math.asin(v)),
    "acos": lambda v: grad(math.acos(v)),
    "atan": lambda v: grad(math.atan(v)),
    "sqrt": math.sqrt,
    "abs": abs,
    "ln": math.log,
    "log": lambda v: math.log(v) / math.log(10.0),
    "exp": math.exp,
}
_CONST = {"pi": math.pi, "e": math.e}
class ErrorExpr(Exception):
    pass
class _Parser:
    def __init__(self, s):
        s = s.replace(" ", "").replace("−", "-").replace("**", "^")
        s = s.replace("·", "*").replace("×", "*")
        s = s.replace("π", "pi").replace("√", "sqrt")
        self.s = s.lower()
        self.i = 0
    def ver(self):
        if self.i < len(self.s):
            return self.s[self.i]
        return ""
    def tomar(self, c):
        if self.ver() == c:
            self.i += 1
            return True
        return False
    def expr(self):
        v = self.term()
        while True:
            if self.tomar("+"):
                v = v + self.term()
            elif self.tomar("-"):
                v = v - self.term()
            else:
                return v
    def term(self):
        v = self.unario()
        while True:
            if self.tomar("*"):
                v = v * self.unario()
            elif self.tomar("/"):
                d = self.unario()
                if d == 0:
                    raise ErrorExpr("division por cero")
                v = v / d
            else:
                c = self.ver()
                if c != "" and (c == "(" or c.isalpha()):
                    v = v * self.unario()
                else:
                    return v
    def unario(self):
        if self.tomar("-"):
            return -self.unario()
        if self.tomar("+"):
            return self.unario()
        return self.potencia()
    def potencia(self):
        b = self.atomo()
        if self.tomar("^"):
            e = self.unario()
            return b ** e
        return b
    def atomo(self):
        c = self.ver()
        if c == "(":
            self.i += 1
            v = self.expr()
            if not self.tomar(")"):
                raise ErrorExpr("falta ')'")
            return v
        if c.isdigit() or c == ".":
            j = self.i
            while self.i < len(self.s) and (self.s[self.i].isdigit() or
                                            self.s[self.i] == "."):
                self.i += 1
            if self.i < len(self.s) and self.s[self.i] == "e":
                k = self.i + 1
                if k < len(self.s) and self.s[k] in "+-":
                    k += 1
                if k < len(self.s) and self.s[k].isdigit():
                    self.i = k
                    while self.i < len(self.s) and self.s[self.i].isdigit():
                        self.i += 1
            try:
                return float(self.s[j:self.i])
            except Exception:
                raise ErrorExpr("numero invalido")
        if c.isalpha():
            j = self.i
            while self.i < len(self.s) and self.s[self.i].isalpha():
                self.i += 1
            nom = self.s[j:self.i]
            if nom in _FUN:
                if not self.tomar("("):
                    raise ErrorExpr("falta '(' tras " + nom)
                a = self.expr()
                if not self.tomar(")"):
                    raise ErrorExpr("falta ')'")
                try:
                    return float(_FUN[nom](a))
                except ErrorExpr:
                    raise
                except Exception:
                    raise ErrorExpr("dominio invalido en " + nom)
            if nom in _CONST:
                return _CONST[nom]
            raise ErrorExpr("desconocido: " + nom)
        raise ErrorExpr("expresion incompleta")
def evaluar(s):
    p = _Parser(s)
    if p.s == "":
        raise ErrorExpr("vacio")
    v = p.expr()
    if p.i != len(p.s):
        raise ErrorExpr("caracter inesperado '" + p.s[p.i] + "'")
    return v

# ---- geometria ----
import math
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

# ---- elementos ----
T_MIEMBRO = ["viga", "barra", "cuerpo"]
N_MIEMBRO = {"viga": "Viga", "barra": "Barra", "cuerpo": "Cuerpo rigido"}
T_APOYO = ["pin", "rod", "emp", "cab", "bie"]
N_APOYO = {
    "pin": "Articulacion (pasador)",
    "rod": "Rodillo / apoyo simple",
    "emp": "Empotramiento",
    "cab": "Cable / tensor",
    "bie": "Biela (barra 2 fuerzas)",
}
C_APOYO = {
    "pin": "2 incognitas: Rx, Ry",
    "rod": "1 incognita: N normal a la superficie",
    "emp": "3 incognitas: Rx, Ry, M",
    "cab": "1 incognita: T (solo traccion)",
    "bie": "1 incognita: F a lo largo de la biela",
}
def nombre_letra(k):
    L = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if k < 26:
        return L[k]
    return L[k % 26] + str(k // 26)
class Nodo:
    def __init__(self, nom, x, y):
        self.nom = nom
        self.x = float(x)
        self.y = float(y)
    def p(self):
        return (self.x, self.y)
class Miembro:
    def __init__(self, tipo, a, b):
        self.tipo = tipo
        self.a = a
        self.b = b
class Apoyo:
    def __init__(self, tipo, nodo, ang=90.0, ref=None):
        self.tipo = tipo
        self.nodo = nodo
        self.ang = float(ang)
        self.ref = ref
class Fuerza:
    def __init__(self, nom, nodo, fx, fy, modo="comp", mag=0.0, ang=0.0):
        self.nom = nom
        self.nodo = nodo
        self.fx = float(fx)
        self.fy = float(fy)
        self.modo = modo
        self.mag = float(mag)
        self.ang = float(ang)
    def F(self):
        return (self.fx, self.fy)
def fuerza_polar(nom, nodo, mag, ang):
    fx, fy = polar(mag, ang)
    return Fuerza(nom, nodo, fx, fy, "pol", mag, ang)
class Momento:
    def __init__(self, nom, nodo, M):
        self.nom = nom
        self.nodo = nodo
        self.M = float(M)
class CargaD:
    def __init__(self, nom, a, b, w1, w2, ang=270.0):
        self.nom = nom
        self.a = a
        self.b = b
        self.w1 = float(w1)
        self.w2 = float(w2)
        self.ang = float(ang)
class FDesc:
    def __init__(self, nom, nodo, modo="libre", ang=0.0):
        self.nom = nom
        self.nodo = nodo
        self.modo = modo
        self.ang = float(ang)
class Incog:
    def __init__(self, nom, tipo, pt, u, nodo, origen, signo=None):
        self.nom = nom
        self.tipo = tipo
        self.pt = pt
        self.u = u
        self.nodo = nodo
        self.origen = origen
        self.signo = signo
class Conocida:
    def __init__(self, nom, tipo, pt, F, M, nodo, desc, fuente):
        self.nom = nom
        self.tipo = tipo
        self.pt = pt
        self.F = F
        self.M = M
        self.nodo = nodo
        self.desc = desc
        self.fuente = fuente
class Modelo:
    def __init__(self, tipo="rigido", titulo="Problema"):
        self.tipo = tipo
        self.titulo = titulo
        self.nodos = []
        self.miembros = []
        self.apoyos = []
        self.fuerzas = []
        self.momentos = []
        self.cargas = []
        self.fdesc = []
        self.sol = None
        self.ref = None
        self._k = 0
    def nodo(self, nom):
        if nom is None:
            return None
        nom = nom.upper()
        for n in self.nodos:
            if n.nom == nom:
                return n
        return None
    def pos(self, nom):
        n = self.nodo(nom)
        if n is None:
            return None
        return n.p()
    def nodo_en(self, x, y, tol=1e-9):
        for n in self.nodos:
            if abs(n.x - x) <= tol and abs(n.y - y) <= tol:
                return n
        return None
    def nuevo_nodo(self, x, y, nom=None):
        n = self.nodo_en(x, y)
        if n is not None:
            return n
        if nom is None:
            while True:
                nom = nombre_letra(self._k)
                self._k += 1
                if self.nodo(nom) is None:
                    break
        n = Nodo(nom.upper(), x, y)
        self.nodos.append(n)
        self.invalidar()
        return n
    def mover_nodo(self, nom, x, y):
        n = self.nodo(nom)
        if n is not None:
            n.x = float(x)
            n.y = float(y)
            self.invalidar()
    def borrar_nodo(self, nom):
        nom = nom.upper()
        self.nodos = [n for n in self.nodos if n.nom != nom]
        self.miembros = [m for m in self.miembros if m.a != nom and m.b != nom]
        self.apoyos = [a for a in self.apoyos
                       if a.nodo != nom and a.ref != nom]
        self.fuerzas = [f for f in self.fuerzas if f.nodo != nom]
        self.momentos = [m for m in self.momentos if m.nodo != nom]
        self.cargas = [c for c in self.cargas if c.a != nom and c.b != nom]
        self.fdesc = [f for f in self.fdesc if f.nodo != nom]
        if self.ref == nom:
            self.ref = None
        self.invalidar()
    def invalidar(self):
        self.sol = None
    def _nom_libre(self, pref, lista):
        k = 1
        usados = [e.nom for e in lista]
        while pref + str(k) in usados:
            k += 1
        return pref + str(k)
    def add_miembro(self, tipo, a, b):
        m = Miembro(tipo, a.upper(), b.upper())
        self.miembros.append(m)
        self.invalidar()
        return m
    def add_apoyo(self, tipo, nodo, ang=90.0, ref=None):
        if ref is not None:
            ref = ref.upper()
        a = Apoyo(tipo, nodo.upper(), ang, ref)
        self.apoyos.append(a)
        self.invalidar()
        return a
    def add_fuerza_pol(self, nodo, mag, ang):
        f = fuerza_polar(self._nom_libre("F", self.fuerzas), nodo.upper(),
                         mag, ang)
        self.fuerzas.append(f)
        self.invalidar()
        return f
    def add_fuerza_comp(self, nodo, fx, fy):
        f = Fuerza(self._nom_libre("F", self.fuerzas), nodo.upper(), fx, fy)
        self.fuerzas.append(f)
        self.invalidar()
        return f
    def add_momento(self, nodo, M):
        m = Momento(self._nom_libre("M", self.momentos), nodo.upper(), M)
        self.momentos.append(m)
        self.invalidar()
        return m
    def add_carga(self, a, b, w1, w2, ang=270.0):
        c = CargaD(self._nom_libre("w", self.cargas), a.upper(), b.upper(),
                   w1, w2, ang)
        self.cargas.append(c)
        self.invalidar()
        return c
    def add_fdesc(self, nodo, modo="libre", ang=0.0):
        f = FDesc(self._nom_libre("P", self.fdesc), nodo.upper(), modo, ang)
        self.fdesc.append(f)
        self.invalidar()
        return f
    def elementos_en(self, nom):
        r = []
        for a in self.apoyos:
            if a.nodo == nom:
                r.append(("Apoyo " + N_APOYO[a.tipo], self.apoyos, a))
        for f in self.fuerzas:
            if f.nodo == nom:
                r.append(("Fuerza " + f.nom, self.fuerzas, f))
        for m in self.momentos:
            if m.nodo == nom:
                r.append(("Momento " + m.nom, self.momentos, m))
        for f in self.fdesc:
            if f.nodo == nom:
                r.append(("F. desconocida " + f.nom, self.fdesc, f))
        for m in self.miembros:
            if m.a == nom or m.b == nom:
                r.append((N_MIEMBRO[m.tipo] + " " + m.a + "-" + m.b,
                          self.miembros, m))
        for c in self.cargas:
            if c.a == nom or c.b == nom:
                r.append(("Carga distr. " + c.nom, self.cargas, c))
        return r
    def quitar(self, lista, obj):
        for i in range(len(lista)):
            if lista[i] is obj:
                lista.pop(i)
                break
        self.invalidar()
    def dir_apoyo(self, a):
        if a.tipo in ("cab", "bie") and a.ref is not None:
            p = self.pos(a.nodo)
            q = self.pos(a.ref)
            if p is None or q is None:
                return None
            return v_unit(v_sub(q, p))
        return (cosd_l(a.ang), sind_l(a.ang))
    def ang_apoyo(self, a):
        u = self.dir_apoyo(a)
        if u is None:
            return a.ang
        return ang_de(u)
    def incognitas(self):
        L = []
        usados = []
        def nombre(s):
            b = s
            k = 2
            while s in usados:
                s = b + "_" + str(k)
                k += 1
            usados.append(s)
            return s
        for a in self.apoyos:
            p = self.pos(a.nodo)
            if p is None:
                continue
            n = a.nodo
            if a.tipo in ("pin", "emp"):
                L.append(Incog(nombre(n + "x"), "F", p, (1.0, 0.0), n, a))
                L.append(Incog(nombre(n + "y"), "F", p, (0.0, 1.0), n, a))
                if a.tipo == "emp":
                    L.append(Incog(nombre("M" + n), "M", p, None, n, a))
            elif a.tipo == "rod":
                u = self.dir_apoyo(a)
                g = a.ang % 360.0
                if abs(g - 90) < 1e-9 or abs(g - 270) < 1e-9:
                    s = n + "y"
                elif abs(g) < 1e-9 or abs(g - 180) < 1e-9:
                    s = n + "x"
                else:
                    s = "N" + n
                L.append(Incog(nombre(s), "F", p, u, n, a, "C"))
            elif a.tipo == "cab":
                u = self.dir_apoyo(a)
                s = "T" + n + (a.ref if a.ref else "")
                L.append(Incog(nombre(s), "F", p, u, n, a, "T"))
            elif a.tipo == "bie":
                u = self.dir_apoyo(a)
                s = "F" + n + (a.ref if a.ref else "")
                L.append(Incog(nombre(s), "F", p, u, n, a))
        for f in self.fdesc:
            p = self.pos(f.nodo)
            if p is None:
                continue
            if f.modo == "dir":
                L.append(Incog(nombre(f.nom), "F", p,
                               (cosd_l(f.ang), sind_l(f.ang)), f.nodo, f))
            else:
                L.append(Incog(nombre(f.nom + "x"), "F", p, (1.0, 0.0),
                               f.nodo, f))
                L.append(Incog(nombre(f.nom + "y"), "F", p, (0.0, 1.0),
                               f.nodo, f))
        return L
    def conocidas(self):
        L = []
        for f in self.fuerzas:
            p = self.pos(f.nodo)
            if p is None:
                continue
            L.append(Conocida(f.nom, "F", p, f.F(), 0.0, f.nodo, "", f))
        for c in self.cargas:
            pa = self.pos(c.a)
            pb = self.pos(c.b)
            if pa is None or pb is None:
                continue
            Lm = dist(pa, pb)
            if Lm < 1e-12:
                continue
            W, xc = carga_lineal(Lm, c.w1, c.w2)
            pt = interp(pa, pb, xc / Lm)
            F = polar(W, c.ang)
            L.append(Conocida("W" + c.nom[1:], "F", pt, F, 0.0, None,
                              "resultante de " + c.nom, c))
        for m in self.momentos:
            p = self.pos(m.nodo)
            if p is None:
                continue
            L.append(Conocida(m.nom, "M", p, None, m.M, m.nodo, "", m))
        return L
    def puntos(self):
        return [n.p() for n in self.nodos]
    def vacio(self):
        return len(self.nodos) == 0
    def validar(self):
        R = []
        if not self.nodos:
            R.append(("E", "No hay nodos definidos."))
            return R
        for i in range(len(self.nodos)):
            for j in range(i + 1, len(self.nodos)):
                if iguales(self.nodos[i].p(), self.nodos[j].p()):
                    R.append(("E", "Nodos " + self.nodos[i].nom + " y " +
                              self.nodos[j].nom + " coinciden."))
        for m in self.miembros:
            if self.nodo(m.a) is None or self.nodo(m.b) is None:
                R.append(("E", "Miembro con nodo inexistente."))
            elif m.a == m.b or dist(self.pos(m.a), self.pos(m.b)) < 1e-9:
                R.append(("E", "Miembro " + m.a + "-" + m.b +
                          " de longitud cero."))
        for a in self.apoyos:
            if self.nodo(a.nodo) is None:
                R.append(("E", "Apoyo en nodo inexistente " + a.nodo))
                continue
            if a.tipo in ("cab", "bie") and a.ref is not None:
                if self.nodo(a.ref) is None:
                    R.append(("E", "Cable/biela hacia nodo inexistente."))
                elif a.ref == a.nodo or self.dir_apoyo(a) is None:
                    R.append(("E", "Cable/biela " + a.nodo +
                              " de longitud cero."))
        for c in self.cargas:
            pa = self.pos(c.a)
            pb = self.pos(c.b)
            if pa is None or pb is None:
                R.append(("E", "Carga " + c.nom + " en nodo inexistente."))
            elif dist(pa, pb) < 1e-9:
                R.append(("E", "Carga " + c.nom + " sobre longitud cero."))
            elif c.w1 * c.w2 < 0:
                R.append(("E", "Carga " + c.nom + ": w1 y w2 deben tener" +
                          " el mismo signo (divida la carga)."))
        for f in self.fuerzas:
            if self.nodo(f.nodo) is None:
                R.append(("E", "Fuerza " + f.nom + " en nodo inexistente."))
        for f in self.fdesc:
            if self.nodo(f.nodo) is None:
                R.append(("E", f.nom + " en nodo inexistente."))
        for m in self.momentos:
            if self.nodo(m.nodo) is None:
                R.append(("E", m.nom + " en nodo inexistente."))
        if self.tipo == "particula":
            if self.momentos:
                R.append(("A", "Una particula no admite momentos: se" +
                          " ignoran."))
            if self.cargas:
                R.append(("A", "Cargas distribuidas no aplican a una" +
                          " particula: se ignoran."))
            ps = set()
            for f in self.fuerzas:
                ps.add(f.nodo)
            for f in self.fdesc:
                ps.add(f.nodo)
            for a in self.apoyos:
                ps.add(a.nodo)
                if a.tipo in ("pin", "emp", "rod"):
                    pass
            if len(ps) > 1:
                R.append(("E", "En una particula todas las fuerzas deben" +
                          " actuar en el mismo punto (nodos: " +
                          ",".join(sorted(list(ps))) + ")."))
            for a in self.apoyos:
                if a.tipo == "emp":
                    R.append(("A", "Empotramiento en particula: su" +
                              " momento se ignora."))
        if not self.apoyos and not self.fdesc:
            R.append(("A", "No hay apoyos ni incognitas: solo se" +
                      " comprobara el equilibrio."))
        return R

# ---- estatica2d ----
class Ec:
    def __init__(self, nom, n):
        self.nom = nom
        self.coef = [0.0] * n
        self.cte = 0.0
        self.terms = []
def limpia_tol(v, s):
    if abs(v) <= 1e-11 * max(1.0, s):
        return 0.0
    return v
def punto_ref(modelo, ref):
    if ref is None:
        return None
    if type(ref) is tuple:
        return ("O(" + fmt(ref[0], 2) + "," + fmt(ref[1], 2) + ")", ref)
    p = modelo.pos(ref)
    if p is None:
        return None
    return (ref.upper(), p)
def elegir_ref(modelo, inc):
    cands = []
    for n in modelo.nodos:
        cands.append((n.nom, n.p()))
    mejor = None
    mejor_s = -1
    for nom, p in cands:
        s = 0
        for u in inc:
            if u.tipo == "F" and u.u is not None:
                r = v_sub(u.pt, p)
                if abs(cruz2(r, u.u)) < 1e-9:
                    s += 1
        bonus = 0
        for a in modelo.apoyos:
            if a.nodo == nom:
                bonus = 0.5
        if s + bonus > mejor_s:
            mejor_s = s + bonus
            mejor = (nom, p, s)
    if mejor is None:
        return ("O", (0.0, 0.0), 0)
    return mejor
def plantear(modelo, ref=None):
    part = modelo.tipo == "particula"
    inc = modelo.incognitas()
    kn = modelo.conocidas()
    if part:
        inc = [u for u in inc if u.tipo != "M"]
        kn = [k for k in kn if k.tipo == "F" and not isinstance(k.fuente,
                                                                CargaD)]
    n = len(inc)
    if part:
        refi = None
    else:
        r = punto_ref(modelo, ref if ref is not None else modelo.ref)
        if r is None:
            a = elegir_ref(modelo, inc)
            refi = (a[0], a[1])
        else:
            refi = r
    ecx = Ec("ΣFx", n)
    ecy = Ec("ΣFy", n)
    ecs = [ecx, ecy]
    ecm = None
    if not part:
        ecm = Ec("ΣM" + refi[0], n)
        ecs.append(ecm)
    O = refi[1] if refi else (0.0, 0.0)
    for k in kn:
        if k.tipo == "F":
            ecx.cte += k.F[0]
            ecx.terms.append({"n": k.nom, "j": -1, "v": k.F[0]})
            ecy.cte += k.F[1]
            ecy.terms.append({"n": k.nom, "j": -1, "v": k.F[1]})
            if ecm is not None:
                rx = k.pt[0] - O[0]
                ry = k.pt[1] - O[1]
                M = rx * k.F[1] - ry * k.F[0]
                ecm.cte += M
                ecm.terms.append({"n": k.nom, "j": -1, "v": M, "rx": rx,
                                  "ry": ry, "Fx": k.F[0], "Fy": k.F[1]})
        else:
            if ecm is not None:
                ecm.cte += k.M
                ecm.terms.append({"n": k.nom, "j": -1, "v": k.M, "par": 1})
    for j in range(n):
        u = inc[j]
        if u.tipo == "F":
            ecx.coef[j] = u.u[0]
            ecy.coef[j] = u.u[1]
            if u.u[0] != 0.0:
                ecx.terms.append({"n": u.nom, "j": j, "v": u.u[0]})
            if u.u[1] != 0.0:
                ecy.terms.append({"n": u.nom, "j": j, "v": u.u[1]})
            if ecm is not None:
                rx = u.pt[0] - O[0]
                ry = u.pt[1] - O[1]
                c = limpia(rx * u.u[1] - ry * u.u[0], 1e-12)
                ecm.coef[j] = c
                ecm.terms.append({"n": u.nom, "j": j, "v": c, "rx": rx,
                                  "ry": ry, "Fx": u.u[0], "Fy": u.u[1]})
        else:
            if ecm is not None:
                ecm.coef[j] = 1.0
                ecm.terms.append({"n": u.nom, "j": j, "v": 1.0, "par": 1})
    return inc, kn, ecs, refi
def _determinadas(A, g, n):
    r0 = g["rango"]
    det_ = []
    for j in range(n):
        e = [0.0] * n
        e[j] = 1.0
        if rango(A + [e]) == r0:
            det_.append(j)
    return det_
def resolver(modelo, ref=None):
    R = {"estado": "", "msgs": [], "avisos": [], "x": {}, "xv": None}
    val = modelo.validar()
    errs = [m for (lv, m) in val if lv == "E"]
    R["avisos"] = [m for (lv, m) in val if lv == "A"]
    if errs:
        R["estado"] = "invalido"
        R["msgs"] = errs
        modelo.sol = R
        return R
    inc, kn, ecs, refi = plantear(modelo, ref)
    n = len(inc)
    neq = len(ecs)
    R["inc"] = inc
    R["kn"] = kn
    R["ecs"] = ecs
    R["ref"] = refi
    A = [list(e.coef) for e in ecs]
    b = [-e.cte for e in ecs]
    R["A"] = A
    R["b"] = b
    escala = max(escala_mat(A), max([abs(v) for v in b] + [1.0]))
    if n == 0:
        bad = [e.nom for e in ecs if abs(e.cte) > 1e-9 * escala]
        if bad:
            R["estado"] = "incompatible"
            R["msgs"].append("Sin incognitas y las cargas no estan en" +
                             " equilibrio (" + ", ".join(bad) + " != 0).")
        else:
            R["estado"] = "equilibrio"
            R["msgs"].append("Sin incognitas: las cargas ya estan en" +
                             " equilibrio.")
        R["xv"] = []
        modelo.sol = R
        return R
    g = gauss(A, b)
    R["g"] = g
    nom = [u.nom for u in inc]
    if g["estado"] == "unica":
        R["estado"] = "determinado"
        x = g["x"]
        x = [limpia_tol(v, escala) for v in x]
        R["xv"] = x
        for j in range(n):
            R["x"][nom[j]] = x[j]
        if g["rango"] < neq:
            R["msgs"].append("Apoyos insuficientes (" + str(n) + " incog. <" +
                             " " + str(neq) + " ec.). El equilibrio solo es" +
                             " posible para ESTA carga: cuerpo parcialmente" +
                             " restringido.")
        else:
            R["msgs"].append("Sistema estaticamente determinado" +
                             " (isostatico): " + str(n) + " incognitas, " +
                             str(neq) + " ecuaciones independientes.")
        _avisos_fisicos(R, inc, x)
        R["chk"] = comprobar(modelo, R)
    elif g["estado"] == "infinitas":
        R["estado"] = "indeterminado"
        gr = n - g["rango"]
        R["grado"] = gr
        R["msgs"].append("Sistema estaticamente INDETERMINADO: " + str(n) +
                         " incognitas y solo " + str(g["rango"]) +
                         " ecuaciones independientes. Grado de" +
                         " indeterminacion = " + str(gr) + ".")
        if g["rango"] < neq:
            R["msgs"].append("Ademas las restricciones son impropias" +
                             " (reacciones concurrentes o paralelas).")
        R["msgs"].append("La estatica no da solucion unica: se requieren" +
                         " ecuaciones de deformacion (Resistencia de" +
                         " Materiales). No se inventa una solucion.")
        dets = _determinadas(A, g, n)
        if dets:
            xp = [0.0] * n
            M = g["M"]
            for i in range(g["rango"]):
                xp[g["piv"][i]] = M[i][n]
            R["parcial"] = [(nom[j], limpia_tol(xp[j], escala))
                            for j in dets]
            R["msgs"].append("Aun asi quedan determinadas: " +
                             ", ".join([nom[j] for j in dets]) + ".")
    else:
        R["estado"] = "incompatible"
        R["msgs"].append("Sistema INCOMPATIBLE: ninguna combinacion de" +
                         " reacciones equilibra las cargas.")
        if g["rango"] < neq:
            R["msgs"].append("Causa probable: restricciones impropias" +
                             " (todas las reacciones son paralelas o" +
                             " concurren en un punto) o apoyos" +
                             " insuficientes: el cuerpo es un mecanismo.")
    modelo.sol = R
    return R
def _avisos_fisicos(R, inc, x):
    for j in range(len(inc)):
        u = inc[j]
        if u.signo == "T" and x[j] < -1e-9:
            R["avisos"].append("El cable " + u.nom + " resulta en" +
                               " COMPRESION: solucion no fisica, un cable" +
                               " solo puede tirar. Revise la geometria.")
        if u.signo == "C" and x[j] < -1e-9:
            R["avisos"].append("El rodillo " + u.nom + " tendria que tirar" +
                               " del cuerpo: si es apoyo simple se" +
                               " despegaria (valido solo si esta guiado).")
def fuerzas_totales(modelo, R):
    L = []
    for k in R.get("kn", []):
        L.append((k.nom, k.tipo, k.pt, k.F, k.M))
    if R.get("xv") is not None:
        inc = R["inc"]
        for j in range(len(inc)):
            u = inc[j]
            v = R["xv"][j]
            if u.tipo == "F":
                L.append((u.nom, "F", u.pt, v_esc(v, u.u), 0.0))
            else:
                L.append((u.nom, "M", u.pt, None, v))
    return L
def momento_en(modelo, R, pt):
    det_ = []
    tot = 0.0
    for nom, tp, p, F, M in fuerzas_totales(modelo, R):
        if tp == "F":
            m = momento2d(p, pt, F)
        else:
            if modelo.tipo == "particula":
                continue
            m = M
        det_.append((nom, m))
        tot += m
    return tot, det_
def comprobar(modelo, R):
    sx = 0.0
    sy = 0.0
    for nom, tp, p, F, M in fuerzas_totales(modelo, R):
        if tp == "F":
            sx += F[0]
            sy += F[1]
    C = {"Fx": sx, "Fy": sy, "M": []}
    if modelo.tipo != "particula":
        pts = []
        if R.get("ref"):
            pts.append(R["ref"])
        pts.append(("O(0,0)", (0.0, 0.0)))
        for nd in modelo.nodos:
            if not R.get("ref") or nd.nom != R["ref"][0]:
                pts.append((nd.nom, nd.p()))
            if len(pts) >= 4:
                break
        for nm, p in pts:
            C["M"].append((nm, momento_en(modelo, R, p)[0]))
    esc = 1.0
    for nom, tp, p, F, M in fuerzas_totales(modelo, R):
        if tp == "F":
            esc = max(esc, abs(F[0]), abs(F[1]))
        else:
            esc = max(esc, abs(M))
    L = 1.0
    bx = caja(modelo.puntos())
    L = max(L, bx[2] - bx[0], bx[3] - bx[1])
    peor = max([abs(sx), abs(sy)] + [abs(m) / L for (nm, m) in C["M"]])
    C["ok"] = peor <= 1e-6 * esc
    C["peor"] = peor
    return C
def es_viga_horizontal(modelo):
    if len(modelo.nodos) < 2:
        return False
    y0 = modelo.nodos[0].y
    for n in modelo.nodos:
        if abs(n.y - y0) > 1e-9:
            return False
    return True
def internas(modelo, R, xs):
    sx = 0.0
    sy = 0.0
    sm = 0.0
    det_ = []
    y0 = modelo.nodos[0].y
    cut = (xs, y0)
    eps = 1e-9
    for k in R.get("kn", []):
        if isinstance(k.fuente, CargaD):
            continue
        if k.pt[0] < xs - eps:
            if k.tipo == "F":
                sx += k.F[0]
                sy += k.F[1]
                m = momento2d(k.pt, cut, k.F)
                sm += m
                det_.append((k.nom, k.F[0], k.F[1], m))
            else:
                sm += k.M
                det_.append((k.nom, 0.0, 0.0, k.M))
    if R.get("xv") is not None:
        for j in range(len(R["inc"])):
            u = R["inc"][j]
            v = R["xv"][j]
            if u.pt[0] < xs - eps:
                if u.tipo == "F":
                    F = v_esc(v, u.u)
                    sx += F[0]
                    sy += F[1]
                    m = momento2d(u.pt, cut, F)
                    sm += m
                    det_.append((u.nom, F[0], F[1], m))
                else:
                    sm += v
                    det_.append((u.nom, 0.0, 0.0, v))
    for c in modelo.cargas:
        pa = modelo.pos(c.a)
        pb = modelo.pos(c.b)
        if pa is None or pb is None:
            continue
        xa, xb, w1, w2 = pa[0], pb[0], c.w1, c.w2
        if xa > xb:
            xa, xb, w1, w2 = xb, xa, w2, w1
        if xs <= xa + eps or xb - xa < eps:
            continue
        xe = min(xs, xb)
        l = xe - xa
        wc = w1 + (w2 - w1) * l / (xb - xa)
        W, xc = carga_lineal(l, w1, wc)
        F = polar(W, c.ang)
        pt = (xa + xc, y0)
        m = momento2d(pt, cut, F)
        sx += F[0]
        sy += F[1]
        sm += m
        det_.append((c.nom + "[" + fmt(xa, 2) + "," + fmt(xe, 2) + "]",
                     F[0], F[1], m))
    N = -sx
    V = sy
    M = -sm
    return (limpia(N, 1e-9), limpia(V, 1e-9), limpia(M, 1e-9), det_)
def diagramas(modelo, R, npts=80):
    xs = sorted([n.x for n in modelo.nodos])
    x0 = xs[0]
    x1 = xs[-1]
    Lt = x1 - x0
    if Lt <= 0:
        return []
    d = Lt * 1e-6
    pts = []
    for i in range(npts + 1):
        pts.append(x0 + Lt * i / npts)
    for x in xs:
        pts.append(x - d)
        pts.append(x + d)
    pts = sorted([p for p in pts if x0 <= p <= x1])
    out = []
    for x in pts:
        N, V, M, _ = internas(modelo, R, x)
        out.append((x, V, M))
    return out

# ---- solucionador ----
import math
def _c(v):
    return fmt(v)
def termino(c, nom, primero):
    if abs(c - 1.0) < 1e-12:
        s = nom
        sg = "+"
    elif abs(c + 1.0) < 1e-12:
        s = nom
        sg = "-"
    else:
        sg = "-" if c < 0 else "+"
        s = fmt(abs(c)) + "·" + nom
    if primero:
        return (s if sg == "+" else "-" + s)
    return " " + sg + " " + s
def ec_texto(coef, cte, nombres, vals=None, forma="=0"):
    s = ""
    rest = 0.0
    for j in range(len(coef)):
        c = coef[j]
        if abs(c) < 1e-12:
            continue
        nm = nombres[j]
        if vals is not None and nm in vals:
            v = vals[nm]
            if abs(abs(c) - 1.0) < 1e-12:
                t = "(" + fmt(v) + ")"
            else:
                t = fmt(abs(c)) + "(" + fmt(v) + ")"
            if s == "":
                s = ("-" if c < 0 else "") + t
            else:
                s += (" - " if c < 0 else " + ") + t
            rest += c * v
            continue
        s += termino(c, nm, s == "")
    if forma == "=0":
        if abs(cte) > 0 or s == "":
            if s == "":
                s = fmt(cte)
            else:
                s += " " + ("-" if cte < 0 else "+") + " " + fmt(abs(cte))
        return s + " = 0"
    if s == "":
        s = "0"
    return s + " = " + fmt(-cte)
def _sentido(m):
    if abs(m) < 1e-12:
        return "(no produce momento)"
    return "(antihorario +)" if m > 0 else "(horario -)"
def _unidad(u):
    return uM() if u.tipo == "M" else uF()
def pasos(modelo, R):
    P = []
    part = modelo.tipo == "particula"
    L = []
    if part:
        L.append("Cuerpo: PARTICULA (fuerzas concurrentes). Solo hay 2" +
                 " ecuaciones: ΣFx=0, ΣFy=0.")
    else:
        L.append("Cuerpo: CUERPO RIGIDO 2D. Hay 3 ecuaciones de" +
                 " equilibrio: ΣFx=0, ΣFy=0, ΣM=0.")
    L.append("Convencion: x a la derecha, y hacia arriba, angulos desde" +
             " +x en sentido antihorario, momentos antihorarios (+).")
    L.append("Puntos (" + uL() + "):")
    for n in modelo.nodos:
        L.append("  " + n.nom + " = (" + fmt(n.x) + ", " + fmt(n.y) + ")")
    if modelo.miembros:
        L.append("Elementos:")
        for m in modelo.miembros:
            l = dist(modelo.pos(m.a), modelo.pos(m.b))
            L.append("  " + N_MIEMBRO[m.tipo] + " " + m.a + "-" + m.b +
                     "  L=" + fmt(l) + " " + uL())
    if modelo.apoyos:
        L.append("Apoyos:")
        for a in modelo.apoyos:
            s = "  " + a.nodo + ": " + N_APOYO[a.tipo]
            if a.tipo == "rod":
                s += ", N a " + fmt(a.ang, 1) + "°"
            if a.tipo in ("cab", "bie"):
                if a.ref:
                    s += " hacia " + a.ref
                else:
                    s += " a " + fmt(a.ang, 1) + "°"
            L.append(s)
            L.append("    -> " + C_APOYO[a.tipo])
    P.append(("1. Identificacion del cuerpo", L))
    if R["estado"] == "invalido":
        L = ["CONFIGURACION INVALIDA. No se puede plantear el equilibrio:"]
        for m in R["msgs"]:
            L.append(" * " + m)
        L.append("Corrija el modelo y vuelva a resolver.")
        P.append(("Error de geometria", L))
        return P
    inc = R["inc"]
    kn = R["kn"]
    nombres = [u.nom for u in inc]
    L = ["Se aisla el cuerpo y se reemplaza cada apoyo por las" +
         " reacciones que impide (fuerzas o pares).",
         "Fuerzas que actuan sobre el cuerpo:"]
    for k in kn:
        if k.tipo == "F":
            L.append("  " + k.nom + " en (" + fmt(k.pt[0], 2) + "," +
                     fmt(k.pt[1], 2) + ") [conocida]")
        else:
            L.append("  " + k.nom + " = " + fmt(k.M) + " " + uM() +
                     " par [conocido]")
    for u in inc:
        if u.tipo == "F":
            L.append("  " + u.nom + " en " + u.nodo + ", dir " +
                     fmt(ang_de(u.u), 1) + "° [incognita]")
        else:
            L.append("  " + u.nom + " par en " + u.nodo + " [incognita]")
    L.append("Sentidos de incognitas SUPUESTOS. Si el resultado sale" +
             " negativo, el sentido real es el contrario.")
    L.append("(Menu 'Ver DCL' muestra el diagrama grafico.)")
    P.append(("2. Diagrama de cuerpo libre", L))
    L = ["CONOCIDAS:"]
    if not kn:
        L.append("  (ninguna)")
    for k in kn:
        if k.tipo == "F":
            f = k.fuente
            if isinstance(f, Fuerza) and f.modo == "pol":
                L.append("  " + k.nom + " = " + fmt(f.mag) + " " + uF() +
                         " a " + fmt(f.ang, 2) + "°")
            elif isinstance(f, CargaD):
                L.append("  " + k.nom + ": " + k.desc)
            else:
                L.append("  " + k.nom + " = (" + fmt(k.F[0]) + ", " +
                         fmt(k.F[1]) + ") " + uF())
        else:
            L.append("  " + k.nom + " = " + fmt(k.M) + " " + uM() + " " +
                     _sentido(k.M))
    L.append("DESCONOCIDAS (" + str(len(inc)) + "):")
    for u in inc:
        if u.tipo == "F":
            org = "reaccion" if isinstance(u.origen, Apoyo) else "fuerza"
            L.append("  " + u.nom + " [" + uF() + "] (" + org + ")")
        else:
            L.append("  " + u.nom + " [" + uM() + "] (par de reaccion)")
    neq = len(R["ecs"])
    L.append("Ecuaciones disponibles: " + str(neq) + ".")
    if len(inc) == neq:
        L.append("n incognitas = n ecuaciones: posible solucion unica" +
                 " (si las ecuaciones son independientes).")
    elif len(inc) > neq:
        L.append("Mas incognitas que ecuaciones: sistema hiperestatico.")
    else:
        L.append("Menos incognitas que ecuaciones: solo hay equilibrio si" +
                 " las cargas lo permiten.")
    P.append(("3. Fuerzas conocidas y desconocidas", L))
    L = ["Cada fuerza se expresa en componentes: Fx = F·cosθ," +
         " Fy = F·sinθ (θ desde +x)."]
    for k in kn:
        if k.tipo != "F":
            continue
        f = k.fuente
        if isinstance(f, Fuerza) and f.modo == "pol":
            L.append(k.nom + ": F=" + fmt(f.mag) + ", θ=" +
                     fmt(f.ang, 2) + "°")
            L.append("  " + k.nom + "x = " + fmt(f.mag) + "·cos(" +
                     fmt(f.ang, 2) + "°) = " + fmt(k.F[0]))
            L.append("  " + k.nom + "y = " + fmt(f.mag) + "·sin(" +
                     fmt(f.ang, 2) + "°) = " + fmt(k.F[1]))
        elif isinstance(f, CargaD):
            pa = modelo.pos(f.a)
            pb = modelo.pos(f.b)
            Lm = dist(pa, pb)
            W, xc = carga_lineal(Lm, f.w1, f.w2)
            L.append(f.nom + ": carga distribuida " + f.a + "->" + f.b +
                     ", w=" + fmt(f.w1) + " a " + fmt(f.w2) + " " + uW() +
                     ", L=" + fmt(Lm) + " " + uL())
            L.append("  Resultante = area del diagrama:")
            L.append("  W = (w1+w2)/2·L = (" + fmt(f.w1) + "+" +
                     fmt(f.w2) + ")/2·" + fmt(Lm) + " = " + fmt(W) +
                     " " + uF())
            L.append("  Ubicacion (centroide) desde " + f.a + ":")
            L.append("  xc = L(w1+2w2)/(3(w1+w2)) = " + fmt(xc) + " " +
                     uL())
            L.append("  Punto de aplicacion: (" + fmt(k.pt[0]) + ", " +
                     fmt(k.pt[1]) + ")")
            L.append("  " + k.nom + "x = " + fmt(W) + "·cos(" +
                     fmt(f.ang, 1) + "°) = " + fmt(k.F[0]))
            L.append("  " + k.nom + "y = " + fmt(W) + "·sin(" +
                     fmt(f.ang, 1) + "°) = " + fmt(k.F[1]))
        else:
            L.append(k.nom + " dada en componentes: (" + fmt(k.F[0]) + ", " +
                     fmt(k.F[1]) + ")")
    for u in inc:
        if u.tipo != "F":
            continue
        a = u.origen
        if isinstance(a, Apoyo) and a.tipo in ("cab", "bie") and a.ref:
            p = modelo.pos(a.nodo)
            q = modelo.pos(a.ref)
            d = v_sub(q, p)
            l = v_norm(d)
            L.append(u.nom + " actua de " + a.nodo + " hacia " + a.ref + ":")
            L.append("  r = (" + fmt(d[0]) + ", " + fmt(d[1]) + "), |r| = " +
                     fmt(l))
            L.append("  u = r/|r| = (" + fmt(u.u[0], 4) + ", " +
                     fmt(u.u[1], 4) + ")")
            L.append("  " + u.nom + "x = " + fmt(u.u[0], 4) + "·" +
                     u.nom + ",  " + u.nom + "y = " + fmt(u.u[1], 4) +
                     "·" + u.nom)
        elif abs(u.u[0]) > 1e-12 and abs(u.u[1]) > 1e-12:
            g = ang_de(u.u)
            L.append(u.nom + " inclinada a " + fmt(g, 2) + "°:")
            L.append("  " + u.nom + "x = " + u.nom + "·cos(" +
                     fmt(g, 2) + "°) = " + fmt(u.u[0], 4) + "·" +
                     u.nom)
            L.append("  " + u.nom + "y = " + u.nom + "·sin(" +
                     fmt(g, 2) + "°) = " + fmt(u.u[1], 4) + "·" +
                     u.nom)
        else:
            eje = "x" if abs(u.u[0]) > 0.5 else "y"
            sg = "+" if (u.u[0] + u.u[1]) > 0 else "-"
            L.append(u.nom + ": dirigida segun " + sg + eje + ".")
    P.append(("4. Descomposicion de fuerzas", L))
    if not part:
        rn, rp = R["ref"]
        L = ["Momento de una fuerza respecto a " + rn + ":",
             "  M = rx·Fy - ry·Fx,  r = P - " + rn,
             "  brazo d = |M|/|F| (distancia perpendicular)."]
        ecm = R["ecs"][2]
        for t in ecm.terms:
            if t.get("par"):
                L.append(t["n"] + ": par, no depende del brazo.")
                continue
            rx, ry, Fx, Fy = t["rx"], t["ry"], t["Fx"], t["Fy"]
            if t["j"] < 0:
                Fm = math.sqrt(Fx * Fx + Fy * Fy)
                d = abs(t["v"]) / Fm if Fm > 0 else 0.0
                L.append(t["n"] + ": r=(" + fmt(rx) + "," + fmt(ry) + ")")
                L.append("  M = (" + fmt(rx) + ")(" + fmt(Fy) + ") - (" +
                         fmt(ry) + ")(" + fmt(Fx) + ")")
                L.append("    = " + fmt(t["v"]) + " " + uM() + " " +
                         _sentido(t["v"]))
                L.append("  d = " + fmt(d) + " " + uL())
            else:
                nm = t["n"]
                L.append(nm + ": r=(" + fmt(rx) + "," + fmt(ry) + ")")
                if abs(t["v"]) < 1e-12:
                    L.append("  su linea de accion pasa por " + rn +
                             ": M = 0")
                else:
                    L.append("  M = [(" + fmt(rx) + ")(" + fmt(Fy, 4) +
                             ") - (" + fmt(ry) + ")(" + fmt(Fx, 4) +
                             ")]·" + nm)
                    L.append("    = " + fmt(t["v"], 4) + "·" + nm)
                    L.append("  d = " + fmt(abs(t["v"])) + " " + uL())
        P.append(("5. Brazos de momento", L))
        elim = [t["n"] for t in ecm.terms if t["j"] >= 0 and
                abs(t["v"]) < 1e-12]
        L = ["Punto elegido: " + rn + " = (" + fmt(rp[0]) + ", " +
             fmt(rp[1]) + ")"]
        if elim:
            L.append("Por " + rn + " pasan las lineas de accion de: " +
                     ", ".join(elim) + ".")
            L.append("Estas incognitas NO aparecen en ΣM" + rn +
                     ", lo que simplifica la solucion.")
        else:
            L.append("Ninguna incognita pasa por este punto; ΣM" + rn +
                     " las incluye a todas.")
        L.append("(Puede elegir otro punto en el menu de resultados.)")
        P.append(("6. Punto de referencia de momentos", L))
    else:
        P.append(("5-6. Momentos", ["En una particula todas las fuerzas" +
                  " son concurrentes: no producen momento respecto al" +
                  " punto. No se usa ΣM."]))
    sig = ["La suma de componentes horizontales debe anularse" +
           " (no hay aceleracion en x).",
           "La suma de componentes verticales debe anularse" +
           " (no hay aceleracion en y).",
           "La suma de momentos respecto al punto debe anularse" +
           " (no hay rotacion)."]
    ecs = R["ecs"]
    for i in range(len(ecs)):
        e = ecs[i]
        L = [sig[i], "Planteamiento simbolico:"]
        simb = ""
        for t in e.terms:
            if t["j"] >= 0:
                nm = t["n"]
                if i == 0 and abs(abs(t["v"]) - 1) > 1e-12:
                    nm = t["n"] + "x"
                if i == 1 and abs(abs(t["v"]) - 1) > 1e-12:
                    nm = t["n"] + "y"
                if i == 2 and not t.get("par"):
                    nm = "M(" + t["n"] + ")"
                if i < 2 and abs(abs(t["v"]) - 1) < 1e-12 and t["v"] < 0:
                    simb += (" - " if simb else "-") + nm
                else:
                    simb += (" + " if simb else "") + nm
            else:
                if i == 2 and not t.get("par"):
                    nm = "M(" + t["n"] + ")"
                else:
                    nm = t["n"] + (["x", "y", ""][i])
                simb += (" + " if simb else "") + nm
        if simb == "":
            simb = "0"
        L.append("  " + e.nom + ": " + simb + " = 0")
        L.append("Con valores:")
        L.append("  " + ec_texto(e.coef, e.cte, nombres))
        P.append((str(7 + i) + ". Planteamiento de " + e.nom + " = 0", L))
    if part:
        P.append(("9. ΣM = 0", ["No aplica a una particula."]))
    L = ["Se agrupan los terminos conocidos al lado derecho:"]
    for e in ecs:
        L.append(e.nom + ":")
        L.append("  " + ec_texto(e.coef, e.cte, nombres, None, "rhs"))
    L.append("Forma matricial [A | b] (columnas: " + ", ".join(nombres) +
             "):")
    for s in mat_lineas(R["A"], R["b"]):
        L.append(s)
    P.append(("10. Sustitucion de valores", L))
    alg, gl = desarrollo(R)
    P.append(("11. Desarrollo algebraico", alg))
    P.append(("12. Resolucion del sistema", gl))
    P.append(("13. Resultados", resultados_txt(modelo, R)))
    P.append(("14. Comprobacion de equilibrio", comprobacion_txt(modelo, R)))
    if R["avisos"]:
        P.append(("Avisos", [" * " + a for a in R["avisos"]]))
    return P
def desarrollo(R):
    inc = R["inc"]
    nombres = [u.nom for u in inc]
    n = len(inc)
    ecs = R["ecs"]
    alg = []
    gl = []
    if n == 0:
        alg.append("No hay incognitas.")
        gl += R["msgs"]
        return alg, gl
    vals = {}
    usadas = []
    eps = 1e-10 * max(1.0, escala_mat(R["A"]))
    paso = 1
    while True:
        prog = False
        for i in range(len(ecs)):
            if i in usadas:
                continue
            e = ecs[i]
            pend = [j for j in range(n) if abs(e.coef[j]) > eps and
                    nombres[j] not in vals]
            if len(pend) != 1:
                continue
            j = pend[0]
            rhs = -e.cte
            for k in range(n):
                if k != j and abs(e.coef[k]) > eps:
                    rhs -= e.coef[k] * vals[nombres[k]]
            v = rhs / e.coef[j]
            alg.append("(" + str(paso) + ") De " + e.nom + " (1 incognita):")
            alg.append("  " + ec_texto(e.coef, e.cte, nombres, vals))
            if abs(e.coef[j] - 1.0) < 1e-12:
                alg.append("  " + nombres[j] + " = " + fmt(v) + " " +
                           _unidad(inc[j]))
            else:
                alg.append("  " + fmt(e.coef[j]) + "·" + nombres[j] +
                           " = " + fmt(rhs))
                alg.append("  " + nombres[j] + " = " + fmt(rhs) + " / (" +
                           fmt(e.coef[j]) + ") = " + fmt(v) + " " +
                           _unidad(inc[j]))
            vals[nombres[j]] = v
            usadas.append(i)
            paso += 1
            prog = True
            break
        if not prog:
            break
    rest = [j for j in range(n) if nombres[j] not in vals]
    if not rest and R["estado"] == "determinado":
        gl.append("Todas las incognitas se obtuvieron por sustitucion.")
    elif not rest:
        gl.append("Las incognitas se despejaron, pero el sistema no" +
                  " se cumple completo (ver paso 11).")
    if rest and R["estado"] == "determinado":
        filas = [i for i in range(len(ecs)) if i not in usadas]
        alg.append("Quedan " + str(len(rest)) + " incognitas acopladas (" +
                   ", ".join([nombres[j] for j in rest]) + "): se" +
                   " resuelven simultaneamente.")
        A2 = []
        b2 = []
        for i in filas:
            e = ecs[i]
            A2.append([e.coef[j] for j in rest])
            r = -e.cte
            for j in range(n):
                if nombres[j] in vals:
                    r -= e.coef[j] * vals[nombres[j]]
            b2.append(r)
            alg.append("  " + ec_texto([e.coef[j] for j in rest], -r,
                                       [nombres[j] for j in rest], None,
                                       "rhs"))
        log = []
        g2 = gauss(A2, b2, None, log, [nombres[j] for j in rest])
        gl.append("Eliminacion de Gauss-Jordan sobre:")
        for s in mat_lineas(A2, b2):
            gl.append(s)
        gl.append("Operaciones de fila:")
        for s in log:
            gl.append("  " + s)
        gl.append("Matriz reducida:")
        M = g2["M"]
        for s in mat_lineas([f[:-1] for f in M], [f[-1] for f in M]):
            gl.append(s)
        if g2["estado"] == "unica":
            usadas += filas
            for k in range(len(rest)):
                j = rest[k]
                vals[nombres[j]] = g2["x"][k]
                gl.append("  " + nombres[j] + " = " + fmt(g2["x"][k]) + " " +
                          _unidad(inc[j]))
    elif rest:
        gl.append("Analisis de rango (Gauss) del sistema completo:")
        log = []
        g = gauss(R["A"], R["b"], None, log, nombres)
        for s in log:
            gl.append("  " + s)
        M = g["M"]
        for s in mat_lineas([f[:-1] for f in M], [f[-1] for f in M]):
            gl.append(s)
        gl.append("rango(A) = " + str(g["rango"]) + ", rango([A|b]) = " +
                  str(g["rango_aum"]) + ", incognitas = " + str(n))
        if g["estado"] == "incompatible":
            gl.append("rango(A) < rango([A|b]) -> SIN SOLUCION.")
        else:
            gl.append("rango(A) < n -> INFINITAS SOLUCIONES.")
    esc = max(1.0, escala_mat(R["A"]), max([abs(v) for v in R["b"]] +
                                           [1.0]))
    for i in range(len(ecs)):
        if i in usadas:
            continue
        e = ecs[i]
        pend = [j for j in range(n) if abs(e.coef[j]) > eps and
                nombres[j] not in vals]
        if pend:
            continue
        r = e.cte
        for j in range(n):
            if abs(e.coef[j]) > eps:
                r += e.coef[j] * vals[nombres[j]]
        alg.append("Ecuacion " + e.nom + " con los valores hallados:")
        alg.append("  " + ec_texto(e.coef, e.cte, nombres, vals))
        if abs(r) > 1e-9 * esc:
            alg.append("  -> " + fmt(r) + " = 0  CONTRADICCION: esta" +
                       " ecuacion no puede cumplirse.")
        else:
            alg.append("  -> residuo " + fmte(r) + " (se cumple).")
    gl.append("Clasificacion:")
    for m in R["msgs"]:
        gl.append("  " + m)
    return alg, gl
def resultados_txt(modelo, R):
    L = []
    if R["estado"] != "determinado":
        L.append("No hay solucion unica.")
        for m in R["msgs"]:
            L.append(" * " + m)
        if R.get("parcial"):
            L.append("Valores determinados:")
            for nm, v in R["parcial"]:
                L.append("  " + nm + " = " + fmt(v))
        return L
    inc = R["inc"]
    for j in range(len(inc)):
        u = inc[j]
        v = R["xv"][j]
        L.append(u.nom + " = " + fmt(v) + " " + _unidad(u))
        if v < -1e-12:
            if u.tipo == "F":
                L.append("   negativo: actua en sentido contrario," +
                         " a " + fmt(ang_de(v_esc(-1.0, u.u)), 1) + "°")
            else:
                L.append("   negativo: el par es HORARIO")
        if u.signo == "T" and v >= 0:
            L.append("   cable en traccion (correcto)")
    vistos = []
    for j in range(len(inc)):
        u = inc[j]
        a = u.origen
        if isinstance(a, Apoyo) and a.tipo in ("pin", "emp") and \
                a.nodo not in vistos:
            vistos.append(a.nodo)
            comp = [R["xv"][k] for k in range(len(inc)) if inc[k].origen is a
                    and inc[k].tipo == "F"]
            if len(comp) == 2:
                Rm = math.sqrt(comp[0] ** 2 + comp[1] ** 2)
                L.append("Reaccion total en " + a.nodo + ":")
                L.append("  R = √(" + fmt(comp[0]) + "²+" +
                         fmt(comp[1]) + "²) = " + fmt(Rm) + " " + uF())
                if Rm > 1e-12:
                    L.append("  θ = " + fmt(ang_de((comp[0], comp[1])),
                                                  2) + "°")
    for a in R["avisos"]:
        L.append("AVISO: " + a)
    return L
def comprobacion_txt(modelo, R):
    L = []
    if R["estado"] != "determinado":
        L.append("No aplica: no hay solucion unica.")
        return L
    C = R["chk"]
    L.append("Se sustituyen TODAS las fuerzas (conocidas + calculadas):")
    L.append("  ΣFx = " + fmte(C["Fx"]))
    L.append("  ΣFy = " + fmte(C["Fy"]))
    for nm, m in C["M"]:
        L.append("  ΣM" + nm + " = " + fmte(m))
    if C["M"]:
        L.append("(El momento se anula respecto a CUALQUIER punto, no solo" +
                 " el usado para resolver.)")
    if C["ok"]:
        L.append("EQUILIBRIO VERIFICADO (residuos ~ 0).")
    else:
        L.append("ATENCION: residuo " + fmte(C["peor"]) + " no despreciable.")
    return L
def resumen_txt(modelo, R):
    L = ["Estado: " + R["estado"].upper()]
    if R["estado"] == "determinado":
        L += resultados_txt(modelo, R)
        C = R["chk"]
        L.append("Comprobacion: " + ("OK" if C["ok"] else "FALLA") +
                 " (residuo " + fmte(C["peor"]) + ")")
    else:
        for m in R["msgs"]:
            L.append(" * " + m)
        if R.get("parcial"):
            for nm, v in R["parcial"]:
                L.append("  " + nm + " = " + fmt(v))
        for a in R["avisos"]:
            L.append("AVISO: " + a)
    return L
def momento_txt(modelo, R, nom, pt):
    tot, det_ = momento_en(modelo, R, pt)
    L = ["Momentos respecto a " + nom + " (" + fmt(pt[0]) + ", " +
         fmt(pt[1]) + "):"]
    for nm, m in det_:
        L.append("  M(" + nm + ") = " + fmt(m) + " " + uM())
    L.append("  ΣM = " + fmt(tot) + " " + uM())
    if R.get("xv") is None:
        L.append("(Solo cargas conocidas: el sistema no esta resuelto.)")
    return L
def internas_txt(modelo, R, xs):
    N, V, M, det_ = internas(modelo, R, xs)
    L = ["Corte en x = " + fmt(xs) + " " + uL() + ". Se analiza el tramo" +
         " izquierdo.", "Fuerzas a la izquierda del corte:"]
    for nm, fx, fy, m in det_:
        L.append("  " + nm + ": Fx=" + fmt(fx) + " Fy=" + fmt(fy))
        L.append("     M(corte)=" + fmt(m))
    L.append("ΣFx: N + ΣFx_izq = 0 -> N = " + fmt(N) + " " + uF())
    L.append("ΣFy: ΣFy_izq - V = 0 -> V = " + fmt(V) + " " + uF())
    L.append("ΣM_corte: ΣM_izq + M = 0 -> M = " + fmt(M) + " " +
             uM())
    L.append("Convencion: N+ traccion, V+ abajo en cara derecha," +
             " M+ concavo arriba.")
    return L

# ---- graficos ----
import math
try:
    import ti_draw as _D
    HAY_GFX = True
except ImportError:
    _D = None
    HAY_GFX = False
try:
    from ti_system import get_key as _get_key
except ImportError:
    _get_key = None
SW = 318
SH = 212
TXT_H = 12
TXT_W = 7
BASE = 11
C_NEGRO = (0, 0, 0)
C_GRIS = (110, 110, 110)
C_VIGA = (60, 60, 60)
C_AZUL = (0, 60, 220)
C_ROJO = (220, 0, 0)
C_VERDE = (0, 150, 0)
C_NAR = (230, 120, 0)
C_FONDO = (255, 255, 255)
C_BARRA = (225, 230, 240)
C_REJ = (225, 225, 225)
C_MAG = (170, 0, 170)
_buf = [False]
def g_ok():
    return HAY_GFX
def g_color(c):
    _D.set_color(c[0], c[1], c[2])
def g_pen(grosor="thin", estilo="solid"):
    try:
        _D.set_pen(grosor, estilo)
    except Exception:
        pass
def g_ini():
    try:
        _D.use_buffer()
        _buf[0] = True
    except Exception:
        _buf[0] = False
    _D.clear()
    g_color(C_FONDO)
    _D.fill_rect(0, 0, SW, SH)
def g_mostrar():
    if _buf[0]:
        try:
            _D.paint_buffer()
        except Exception:
            pass
def g_linea(x1, y1, x2, y2):
    _D.draw_line(int(x1), int(y1), int(x2), int(y2))
def g_texto(x, y, s, c=None):
    if c is not None:
        g_color(c)
    _D.draw_text(int(x), int(y) + BASE, tx(s))
def g_rect(x, y, w, h, c, relleno=True):
    g_color(c)
    if relleno:
        _D.fill_rect(int(x), int(y), int(w), int(h))
    else:
        _D.draw_rect(int(x), int(y), int(w), int(h))
def g_circ(x, y, r, relleno=False):
    if relleno:
        _D.fill_circle(int(x), int(y), int(r))
    else:
        _D.draw_circle(int(x), int(y), int(r))
def g_poli(xs, ys, relleno=True):
    xs = [int(v) for v in xs]
    ys = [int(v) for v in ys]
    try:
        if relleno:
            _D.fill_poly(xs, ys)
        else:
            _D.draw_poly(xs, ys)
    except Exception:
        n = len(xs)
        for i in range(n):
            _D.draw_line(xs[i], ys[i], xs[(i + 1) % n], ys[(i + 1) % n])
def tecla():
    if _get_key is None:
        return "esc"
    while True:
        k = _get_key()
        if k:
            return k
def esperar_tecla():
    g_mostrar()
    return tecla()
def barra_sup(s, c=C_BARRA):
    g_rect(0, 0, SW, 14, c)
    g_texto(2, 0, s, C_NEGRO)
def barra_inf(s):
    g_rect(0, SH - 14, SW, 14, C_BARRA)
    g_texto(2, SH - 14, s, C_NEGRO)
class Vista:
    def __init__(self, pts, x0=0, y0=16, w=SW, h=SH - 46, marg=34):
        bx = caja(pts)
        xmin, ymin, xmax, ymax = bx
        dx = xmax - xmin
        dy = ymax - ymin
        if dx < 1e-9 and dy < 1e-9:
            dx = dy = 2.0
            xmin -= 1.0
            ymin -= 1.0
        aw = w - 2 * marg
        ah = h - 2 * marg
        if dx < 1e-9:
            s = ah / dy
        elif dy < 1e-9:
            s = aw / dx
        else:
            s = min(aw / dx, ah / dy)
        self.s = s
        cx = (xmin + xmax) / 2.0
        cy = (ymin + ymax) / 2.0
        self.ox = x0 + w / 2.0 - cx * s
        self.oy = y0 + h / 2.0 + cy * s
    def p(self, pt):
        return (self.ox + pt[0] * self.s, self.oy - pt[1] * self.s)
    def m(self, sx, sy):
        return ((sx - self.ox) / self.s, (self.oy - sy) / self.s)
def flecha(x1, y1, x2, y2, c, pen="medium", estilo="solid", cab=6):
    g_color(c)
    g_pen(pen, estilo)
    g_linea(x1, y1, x2, y2)
    g_pen("thin", "solid")
    dx = x2 - x1
    dy = y2 - y1
    L = math.sqrt(dx * dx + dy * dy)
    if L < 1:
        return
    ux = dx / L
    uy = dy / L
    px = -uy
    py = ux
    bx = x2 - ux * cab
    by = y2 - uy * cab
    g_poli([x2, bx + px * cab * 0.55, bx - px * cab * 0.55],
           [y2, by + py * cab * 0.55, by - py * cab * 0.55])
def flecha_fuerza(V, pt, F, c, etiqueta, tira=False, estilo="solid",
                  largo=30):
    u = v_unit(F)
    if u is None:
        return
    sx, sy = V.p(pt)
    dx = u[0] * largo
    dy = -u[1] * largo
    if tira:
        flecha(sx, sy, sx + dx, sy + dy, c, "medium", estilo)
        tx_, ty_ = sx + dx, sy + dy
    else:
        flecha(sx - dx, sy - dy, sx - 2 * u[0], sy + 2 * u[1], c, "medium",
               estilo)
        tx_, ty_ = sx - dx, sy - dy
    _etiqueta(tx_, ty_, u, etiqueta, c, tira)
def _etiqueta(x, y, u, s, c, tira):
    w = len(s) * TXT_W
    ox = 3 if u[0] >= -0.2 else -w - 3
    if tira:
        ox = 3 if u[0] >= 0 else -w - 3
    else:
        ox = -w - 3 if u[0] > 0.2 else 3
    oy = -TXT_H if u[1] > -0.2 else 0
    if not tira:
        oy = 0 if u[1] > 0.2 else -TXT_H
    xx = max(0, min(SW - w, x + ox))
    yy = max(15, min(SH - 36 - TXT_H, y + oy))
    g_texto(xx, yy, s, c)
def arco(cx, cy, r, ccw, c, etiqueta="", estilo="solid"):
    g_color(c)
    g_pen("medium", estilo)
    n = 14
    a0 = -45.0
    pts = []
    for i in range(n + 1):
        a = rad(a0 + 270.0 * i / n)
        pts.append((cx + r * math.cos(a), cy - r * math.sin(a)))
    if not ccw:
        pts.reverse()
    for i in range(n):
        g_linea(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1])
    g_pen("thin", "solid")
    x2, y2 = pts[-1]
    x1, y1 = pts[-2]
    flecha(x1, y1, x2, y2, c, "thin", "solid", 6)
    if etiqueta:
        g_texto(max(0, min(SW - len(etiqueta) * TXT_W, cx + r + 2)),
                max(15, cy - r - TXT_H), etiqueta, c)
def suelo(x1, y1, x2, y2, lado):
    g_color(C_GRIS)
    g_linea(x1, y1, x2, y2)
    L = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    if L < 1:
        return
    k = int(L / 5)
    for i in range(k + 1):
        t = i / max(1, k)
        x = x1 + (x2 - x1) * t
        y = y1 + (y2 - y1) * t
        g_linea(x, y, x + lado[0] * 4 - (x2 - x1) / L * 3,
                y + lado[1] * 4 - (y2 - y1) / L * 3)
def dib_apoyo(V, modelo, a):
    p = modelo.pos(a.nodo)
    if p is None:
        return
    sx, sy = V.p(p)
    g_color(C_GRIS)
    if a.tipo in ("pin", "rod"):
        if a.tipo == "rod":
            u = modelo.dir_apoyo(a)
        else:
            u = (0.0, 1.0)
        ux, uy = u[0], -u[1]
        px, py = -uy, ux
        h = 11
        bx = sx - ux * h
        by = sy - uy * h
        g_color(C_GRIS)
        g_poli([sx, bx + px * 7, bx - px * 7], [sy, by + py * 7, by - py * 7],
               False)
        if a.tipo == "rod":
            for t in (-4, 4):
                g_circ(bx - ux * 3 + px * t, by - uy * 3 + py * t, 2)
            bx -= ux * 6
            by -= uy * 6
        suelo(bx + px * 10, by + py * 10, bx - px * 10, by - py * 10,
              (-ux, -uy))
        g_color(C_FONDO)
        g_circ(sx, sy, 2, True)
        g_color(C_NEGRO)
        g_circ(sx, sy, 2, False)
    elif a.tipo == "emp":
        d = (1.0, 0.0)
        for m in modelo.miembros:
            if m.a == a.nodo or m.b == a.nodo:
                otro = m.b if m.a == a.nodo else m.a
                q = modelo.pos(otro)
                if q is not None:
                    uu = v_unit(v_sub(q, p))
                    if uu is not None:
                        d = uu
                break
        ux, uy = d[0], -d[1]
        px, py = -uy, ux
        g_color(C_GRIS)
        g_pen("thick", "solid")
        g_linea(sx + px * 12, sy + py * 12, sx - px * 12, sy - py * 12)
        g_pen("thin", "solid")
        suelo(sx + px * 12, sy + py * 12, sx - px * 12, sy - py * 12,
              (-ux, -uy))
    elif a.tipo in ("cab", "bie"):
        if a.ref is not None and modelo.pos(a.ref) is not None:
            q = V.p(modelo.pos(a.ref))
        else:
            u = modelo.dir_apoyo(a)
            q = (sx + u[0] * 40, sy - u[1] * 40)
        if a.tipo == "cab":
            g_color(C_NAR)
            g_pen("thin", "dashed")
            g_linea(sx, sy, q[0], q[1])
            g_pen("thin", "solid")
        else:
            g_color(C_GRIS)
            g_pen("medium", "solid")
            g_linea(sx, sy, q[0], q[1])
            g_pen("thin", "solid")
            g_circ(q[0], q[1], 2)
        g_color(C_GRIS)
        g_rect(q[0] - 2, q[1] - 2, 5, 5, C_GRIS)
def dib_carga(V, modelo, c):
    pa = modelo.pos(c.a)
    pb = modelo.pos(c.b)
    if pa is None or pb is None:
        return
    u = (cosd_l(c.ang), sind_l(c.ang))
    wmax = max(abs(c.w1), abs(c.w2), 1e-12)
    n = 7
    sa = V.p(pa)
    sb = V.p(pb)
    colas = []
    for i in range(n + 1):
        t = i / n
        w = c.w1 + (c.w2 - c.w1) * t
        L = 6 + 18 * abs(w) / wmax
        x = sa[0] + (sb[0] - sa[0]) * t
        y = sa[1] + (sb[1] - sa[1]) * t
        x0 = x - u[0] * L
        y0 = y + u[1] * L
        colas.append((x0, y0))
        if abs(w) > 1e-12:
            flecha(x0, y0, x - u[0] * 2, y + u[1] * 2, C_AZUL, "thin",
                   "solid", 4)
    g_color(C_AZUL)
    for i in range(n):
        g_linea(colas[i][0], colas[i][1], colas[i + 1][0], colas[i + 1][1])
    lab = c.nom + " " + fmt(c.w1, 1)
    if abs(c.w1 - c.w2) > 1e-12:
        lab += "-" + fmt(c.w2, 1)
    lab += uW()
    xm = (colas[0][0] + colas[-1][0]) / 2.0 - len(lab) * TXT_W / 2.0
    ym = min(colas[0][1], colas[-1][1]) - TXT_H - 1
    g_texto(max(0, min(SW - len(lab) * TXT_W, xm)), max(15, ym), lab,
            C_AZUL)
def cotas(V, modelo):
    if len(modelo.nodos) < 2:
        return
    g_color(C_MAG)
    xs = []
    for n in modelo.nodos:
        if not [x for x in xs if abs(x - n.x) < 1e-9]:
            xs.append(n.x)
    xs.sort()
    ys = []
    for n in modelo.nodos:
        if not [y for y in ys if abs(y - n.y) < 1e-9]:
            ys.append(n.y)
    ys.sort()
    yl = SH - 19
    if len(xs) > 1:
        x0 = V.p((xs[0], 0))[0]
        x1 = V.p((xs[-1], 0))[0]
        g_linea(x0, yl, x1, yl)
        for x in xs:
            sx = V.p((x, 0))[0]
            g_linea(sx, yl - 3, sx, yl + 3)
        for i in range(len(xs) - 1):
            s = fmt(xs[i + 1] - xs[i], 2)
            a = V.p((xs[i], 0))[0]
            b = V.p((xs[i + 1], 0))[0]
            if b - a > len(s) * TXT_W + 2:
                g_texto((a + b) / 2 - len(s) * TXT_W / 2, yl - TXT_H, s,
                        C_MAG)
    if len(ys) > 1:
        xl = 4
        y0 = V.p((0, ys[0]))[1]
        y1 = V.p((0, ys[-1]))[1]
        g_color(C_MAG)
        g_linea(xl, y0, xl, y1)
        for y in ys:
            sy = V.p((0, y))[1]
            g_linea(xl - 3, sy, xl + 3, sy)
        for i in range(len(ys) - 1):
            s = fmt(ys[i + 1] - ys[i], 2)
            a = V.p((0, ys[i]))[1]
            b = V.p((0, ys[i + 1]))[1]
            if a - b > TXT_H + 2:
                g_texto(xl + 3, (a + b) / 2 - TXT_H / 2, s, C_MAG)
def ejes(x, y):
    g_color(C_GRIS)
    flecha(x, y, x + 16, y, C_GRIS, "thin", "solid", 4)
    flecha(x, y, x, y - 16, C_GRIS, "thin", "solid", 4)
    g_texto(x + 16, y - 8, "x", C_GRIS)
    g_texto(x - 3, y - 30, "y", C_GRIS)
def puntos_vista(modelo, extra=None):
    pts = modelo.puntos()
    if extra:
        pts = pts + extra
    for a in modelo.apoyos:
        if a.tipo in ("cab", "bie") and a.ref is None:
            p = modelo.pos(a.nodo)
            if p is not None:
                pts.append(p)
    return pts
def dibujar(modelo, R=None, V=None, titulo=None, ayuda=None, cursor=None,
            rejilla=None, marca=None):
    if not HAY_GFX:
        return None
    if V is None:
        V = Vista(puntos_vista(modelo))
    g_ini()
    if rejilla:
        _rejilla(V, rejilla)
    for m in modelo.miembros:
        pa = modelo.pos(m.a)
        pb = modelo.pos(m.b)
        if pa is None or pb is None:
            continue
        a = V.p(pa)
        b = V.p(pb)
        if m.tipo == "viga":
            g_color(C_VIGA)
            g_pen("thick", "solid")
        elif m.tipo == "barra":
            g_color(C_VIGA)
            g_pen("medium", "solid")
        else:
            g_color((120, 90, 40))
            g_pen("thick", "solid")
        g_linea(a[0], a[1], b[0], b[1])
        g_pen("thin", "solid")
    for a in modelo.apoyos:
        dib_apoyo(V, modelo, a)
    for c in modelo.cargas:
        dib_carga(V, modelo, c)
    for n in modelo.nodos:
        sx, sy = V.p(n.p())
        g_color(C_NEGRO)
        g_circ(sx, sy, 2, True)
        g_texto(sx + 3, sy + 1, n.nom, C_NEGRO)
    for f in modelo.fuerzas:
        p = modelo.pos(f.nodo)
        if p is None:
            continue
        if f.modo == "pol":
            lab = f.nom + " " + fmt(f.mag, 1)
            g = f.ang % 360.0
            if abs(g % 90.0) > 1e-9:
                lab += " " + fmt(g, 0) + "°"
        else:
            lab = f.nom + " " + fmt(v_norm(f.F()), 1)
        flecha_fuerza(V, p, f.F(), C_AZUL, lab)
    for m in modelo.momentos:
        p = modelo.pos(m.nodo)
        if p is None:
            continue
        sx, sy = V.p(p)
        arco(sx, sy, 12, m.M >= 0, C_AZUL, m.nom + " " + fmt(abs(m.M), 1))
    _dib_incognitas(V, modelo, R)
    cotas(V, modelo)
    ejes(SW - 24, SH - 36)
    if marca is not None:
        sx, sy = V.p(marca)
        g_color(C_NAR)
        g_circ(sx, sy, 6)
    if cursor is not None:
        sx, sy = V.p(cursor)
        g_color(C_ROJO)
        g_linea(sx - 7, sy, sx + 7, sy)
        g_linea(sx, sy - 7, sx, sy + 7)
        g_circ(sx, sy, 3)
    if titulo is not None:
        barra_sup(titulo)
    if ayuda is not None:
        barra_inf(ayuda)
    g_mostrar()
    return V
def _dib_incognitas(V, modelo, R):
    if R is None:
        R = modelo.sol
    resuelto = R is not None and R.get("xv") is not None and \
        R.get("estado") == "determinado"
    inc = R["inc"] if (R is not None and "inc" in R) else \
        modelo.incognitas()
    for j in range(len(inc)):
        u = inc[j]
        if modelo.tipo == "particula" and u.tipo == "M":
            continue
        sx, sy = V.p(u.pt)
        if resuelto:
            v = R["xv"][j]
            if u.tipo == "F":
                F = v_esc(v, u.u)
                if abs(v) < 1e-9:
                    g_texto(sx + 4, sy + 4, u.nom + "=0", C_VERDE)
                    continue
                tira = isinstance(u.origen, Apoyo) and u.origen.tipo == "cab"
                if tira and v < 0:
                    tira = False
                flecha_fuerza(V, u.pt, F, C_VERDE,
                              u.nom + "=" + fmt(abs(v), 1), tira, "solid",
                              34)
            else:
                arco(sx, sy, 16, v >= 0, C_VERDE,
                     u.nom + "=" + fmt(abs(v), 1))
        else:
            if u.tipo == "F":
                tira = isinstance(u.origen, Apoyo) and u.origen.tipo == "cab"
                flecha_fuerza(V, u.pt, u.u, C_ROJO, u.nom + "?", tira,
                              "dashed", 26)
            else:
                arco(sx, sy, 16, True, C_ROJO, u.nom + "?", "dashed")
def _rejilla(V, paso):
    x0, y1 = V.m(0, 16)
    x1, y0 = V.m(SW, SH - 14)
    if paso * V.s < 6:
        return
    g_color(C_REJ)
    i0 = int(math.floor(x0 / paso))
    i1 = int(math.ceil(x1 / paso))
    for i in range(i0, i1 + 1):
        sx = V.p((i * paso, 0))[0]
        if 0 <= sx <= SW:
            g_linea(sx, 15, sx, SH - 15)
    j0 = int(math.floor(y0 / paso))
    j1 = int(math.ceil(y1 / paso))
    for j in range(j0, j1 + 1):
        sy = V.p((0, j * paso))[1]
        if 15 <= sy <= SH - 15:
            g_linea(0, sy, SW, sy)
    g_color((190, 190, 190))
    o = V.p((0.0, 0.0))
    if 0 <= o[0] <= SW:
        g_linea(o[0], 15, o[0], SH - 15)
    if 15 <= o[1] <= SH - 15:
        g_linea(0, o[1], SW, o[1])
def ver_dcl(modelo, R=None, titulo="DCL"):
    if not HAY_GFX:
        return False
    if R is None:
        R = modelo.sol
    res = R is not None and R.get("estado") == "determinado"
    t = titulo + (" (resuelto)" if res else "")
    dibujar(modelo, R, None, t,
            "azul=dato rojo=incog verde=reacc  [tecla]")
    esperar_tecla()
    return True
def ver_VM(modelo, R):
    if not HAY_GFX:
        return False
    D = diagramas(modelo, R)
    if not D:
        return False
    g_ini()
    barra_sup("Cortante V (" + uF() + ") y Momento M (" + uM() + ")")
    xs = [d[0] for d in D]
    x0 = min(xs)
    x1 = max(xs)
    for k, col, y0, h, nom in ((1, C_AZUL, 16, 88, "V"),
                               (2, C_ROJO, 108, 88, "M")):
        vals = [d[k] for d in D]
        vmax = max([abs(v) for v in vals] + [1e-12])
        ax0 = 30
        aw = SW - 40
        def X(x):
            return ax0 + (x - x0) / (x1 - x0) * aw
        ym = y0 + h / 2.0
        def Y(v):
            return ym - v / vmax * (h / 2.0 - 8)
        g_color(C_GRIS)
        g_linea(ax0, ym, ax0 + aw, ym)
        g_color(col)
        for i in range(len(D) - 1):
            g_linea(X(D[i][0]), Y(vals[i]), X(D[i + 1][0]), Y(vals[i + 1]))
        for i in range(0, len(D), 8):
            g_linea(X(D[i][0]), ym, X(D[i][0]), Y(vals[i]))
        imx = 0
        imn = 0
        for i in range(len(vals)):
            if vals[i] > vals[imx]:
                imx = i
            if vals[i] < vals[imn]:
                imn = i
        g_texto(2, y0 + 2, nom, col)
        for i in (imx, imn):
            s = fmt(vals[i], 1)
            xx = max(ax0, min(SW - len(s) * TXT_W, X(D[i][0]) - 10))
            yy = Y(vals[i]) - TXT_H if vals[i] >= 0 else Y(vals[i]) + 1
            yy = max(y0, min(y0 + h - TXT_H, yy))
            g_texto(xx, yy, s, col)
    barra_inf("x de " + fmt(x0, 2) + " a " + fmt(x1, 2) + " " + uL() +
              "   [tecla]")
    esperar_tecla()
    return True
def menu_gfx(titulo, opciones):
    n = len(opciones)
    h = 16 + 13 * n + 4
    y0 = max(16, (SH - h) // 2)
    g_rect(30, y0, SW - 60, h, (245, 245, 255))
    g_rect(30, y0, SW - 60, h, C_NEGRO, False)
    g_texto(34, y0 + 1, titulo, C_AZUL)
    for i in range(n):
        g_texto(36, y0 + 15 + 13 * i, str(i + 1) + " " + opciones[i],
                C_NEGRO)
    g_mostrar()
    while True:
        k = tecla()
        if k in ("esc", "del"):
            return -1
        if len(k) == 1 and k.isdigit():
            i = int(k) - 1
            if 0 <= i < n:
                return i
def entrada_gfx(prompt, defecto=None):
    s = ""
    if defecto is not None:
        s = fmt(defecto, 4)
        if "." in s:
            while s.endswith("0"):
                s = s[:-1]
            if s.endswith("."):
                s = s[:-1]
    err = ""
    while True:
        g_rect(10, SH - 50, SW - 20, 36, (255, 255, 230))
        g_rect(10, SH - 50, SW - 20, 36, C_NEGRO, False)
        g_texto(14, SH - 49, prompt + (" " + err if err else ""), C_AZUL)
        g_texto(14, SH - 35, "> " + s + "_", C_NEGRO)
        g_mostrar()
        k = tecla()
        if k == "esc":
            return None
        if k == "enter":
            try:
                return evaluar(s)
            except Exception:
                err = "(invalido)"
                continue
        if k in ("del", "clear"):
            s = s[:-1]
            continue
        if k in ("−", "(-)", "neg", "¯"):
            k = "-"
        if k == "×":
            k = "*"
        if k == "÷":
            k = "/"
        if len(k) == 1 and k in "0123456789.-+*/^()e":
            s += k
            err = ""
        elif k in ("sin", "cos", "tan", "sqrt", "pi", "π"):
            s += ("pi" if k == "π" else k + ("" if k == "pi" else "("))

# ---- entrada ----
try:
    from ti_system import disp_clr as _clr
except ImportError:
    _clr = None
class Cancelar(Exception):
    pass
def limpiar():
    if _clr is not None:
        try:
            _clr()
            return
        except Exception:
            pass
    print("")
def p(s=""):
    for l in wrap(tx(str(s))):
        print(l)
def leer(prompt):
    try:
        s = input(tx(prompt))
    except EOFError:
        raise Cancelar()
    return s.strip()
def leer_num(prompt, defecto=None, minv=None, maxv=None, cancel=True):
    pr = prompt
    if defecto is not None:
        pr = prompt + " [" + fmt(defecto, 4) + "]"
    while True:
        s = leer(pr + ": ")
        if s == "" and defecto is not None:
            return float(defecto)
        if cancel and s.lower() in ("q", "x", "esc"):
            raise Cancelar()
        try:
            v = evaluar(s)
        except ErrorExpr as e:
            p("  No valido: " + str(e) + ". Reintente (q=cancelar).")
            continue
        except Exception:
            p("  Valor invalido. Reintente (q=cancelar).")
            continue
        if minv is not None and v < minv:
            p("  Debe ser >= " + fmt(minv))
            continue
        if maxv is not None and v > maxv:
            p("  Debe ser <= " + fmt(maxv))
            continue
        return v
def leer_par(prompt):
    while True:
        s = leer(prompt + " (x,y): ")
        if s.lower() in ("q", "x", "esc"):
            raise Cancelar()
        if "," in s:
            a = s.split(",")
            if len(a) == 2:
                try:
                    return (evaluar(a[0]), evaluar(a[1]))
                except Exception:
                    pass
        p("  Formato: x,y  (ej. 2.5,0)")
def leer_vec(prompt, n):
    while True:
        s = leer(prompt + " (" + ",".join(["x", "y", "z"][:n]) + "): ")
        if s.lower() in ("q", "x", "esc"):
            raise Cancelar()
        a = s.split(",")
        if len(a) == n:
            try:
                return tuple([evaluar(c) for c in a])
            except Exception:
                pass
        p("  Escriba " + str(n) + " numeros separados por coma.")
def leer_ent(prompt, a, b, defecto=None):
    while True:
        v = leer_num(prompt, defecto)
        if int(v) == v and a <= v <= b:
            return int(v)
        p("  Entero entre " + str(a) + " y " + str(b) + ".")
def si_no(prompt, defecto=True):
    s = leer(prompt + (" [S/n]: " if defecto else " [s/N]: ")).lower()
    if s == "":
        return defecto
    return s[0] in ("s", "y", "1")
def menu(titulo, opciones, volver="Volver"):
    while True:
        print("")
        print(tx("== " + titulo + " =="))
        for i in range(len(opciones)):
            for l in wrap(tx(str(i + 1) + " " + opciones[i])):
                print(l)
        if volver:
            print(tx("0 " + volver))
        s = leer("> ")
        if s == "" and not volver:
            continue
        if s.lower() in ("q", "esc"):
            return 0
        try:
            k = int(s)
        except Exception:
            p("Opcion invalida.")
            continue
        if 0 <= k <= len(opciones) and (k != 0 or volver):
            return k
        p("Opcion invalida.")
def elegir(titulo, opciones, defecto=None):
    print(tx("-- " + titulo + " --"))
    for i in range(len(opciones)):
        print(tx(str(i + 1) + " " + opciones[i]))
    while True:
        d = None if defecto is None else defecto + 1
        k = leer_num("Opcion", d)
        if int(k) == k and 1 <= k <= len(opciones):
            return int(k) - 1
        if k == 0:
            raise Cancelar()
        p("Opcion invalida.")
def pausa(msg="-- ENTER para continuar --"):
    try:
        s = leer(msg)
    except Cancelar:
        return "q"
    return s.lower()
def mostrar(lineas, titulo=None):
    out = []
    if titulo:
        out.append("== " + titulo + " ==")
    for l in lineas:
        out += wrap(tx(str(l)))
    n = CFG["lineas"]
    k = 0
    for l in out:
        print(l)
        k += 1
        if k >= n:
            k = 0
            r = pausa("-- ENTER (q=salir) --")
            if r == "q":
                return False
    return True
def ver_pasos(P):
    i = 0
    while 0 <= i < len(P):
        tit, L = P[i]
        print("")
        if not mostrar(L, tit):
            return
        r = pausa("[ENTER sig, a ant, n# ir, q]")
        if r == "q":
            return
        if r == "a":
            i = max(0, i - 1)
            continue
        if r.startswith("n") and len(r) > 1:
            try:
                k = int(r[1:])
                i = max(0, min(len(P) - 1, k - 1))
                continue
            except Exception:
                pass
        i += 1
    p("-- Fin del desarrollo --")

# ---- guardar ----
try:
    from ti_system import store_list as _store, recall_list as _recall
except ImportError:
    _store = None
    _recall = None
_TA = ["pin", "rod", "emp", "cab", "bie"]
_TM = ["viga", "barra", "cuerpo"]
_MEM = {}
def cod_nom(nom):
    if nom is None:
        return -1
    L = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    k = L.find(nom[0])
    if len(nom) > 1:
        k += 26 * int(nom[1:])
    return k
def codificar(m):
    d = [1, 0 if m.tipo == "rigido" else 1, len(m.nodos)]
    for n in m.nodos:
        d += [cod_nom(n.nom), n.x, n.y]
    d.append(len(m.miembros))
    for e in m.miembros:
        d += [_TM.index(e.tipo), cod_nom(e.a), cod_nom(e.b)]
    d.append(len(m.apoyos))
    for a in m.apoyos:
        d += [_TA.index(a.tipo), cod_nom(a.nodo), a.ang, cod_nom(a.ref)]
    d.append(len(m.fuerzas))
    for f in m.fuerzas:
        d += [cod_nom(f.nodo), f.fx, f.fy, 1 if f.modo == "pol" else 0,
              f.mag, f.ang]
    d.append(len(m.momentos))
    for e in m.momentos:
        d += [cod_nom(e.nodo), e.M]
    d.append(len(m.cargas))
    for c in m.cargas:
        d += [cod_nom(c.a), cod_nom(c.b), c.w1, c.w2, c.ang]
    d.append(len(m.fdesc))
    for f in m.fdesc:
        d += [cod_nom(f.nodo), 1 if f.modo == "dir" else 0, f.ang]
    ref = m.ref if type(m.ref) is str else None
    d.append(cod_nom(ref))
    d.append(CFG["uni"])
    return [float(v) for v in d]
def decodificar(d):
    d = list(d)
    k = [0]
    def nx():
        v = d[k[0]]
        k[0] += 1
        return v
    def nn():
        v = int(nx())
        return None if v < 0 else nombre_letra(v)
    ver = int(nx())
    if ver != 1:
        raise ValueError("version")
    m = Modelo("rigido" if int(nx()) == 0 else "particula")
    for i in range(int(nx())):
        nom = nn()
        x = nx()
        y = nx()
        m.nodos.append(Nodo(nom, x, y))
    m._k = 0
    for n in m.nodos:
        c = cod_nom(n.nom) + 1
        if c > m._k:
            m._k = c
    for i in range(int(nx())):
        t = _TM[int(nx())]
        m.add_miembro(t, nn(), nn())
    for i in range(int(nx())):
        t = _TA[int(nx())]
        nd = nn()
        ang = nx()
        ref = nn()
        m.add_apoyo(t, nd, ang, ref)
    for i in range(int(nx())):
        nd = nn()
        fx = nx()
        fy = nx()
        pol = int(nx())
        mag = nx()
        ang = nx()
        f = m.add_fuerza_comp(nd, fx, fy)
        if pol:
            f.modo = "pol"
            f.mag = mag
            f.ang = ang
    for i in range(int(nx())):
        nd = nn()
        m.add_momento(nd, nx())
    for i in range(int(nx())):
        a = nn()
        b = nn()
        w1 = nx()
        w2 = nx()
        m.add_carga(a, b, w1, w2, nx())
    for i in range(int(nx())):
        nd = nn()
        md = "dir" if int(nx()) else "libre"
        m.add_fdesc(nd, md, nx())
    m.ref = nn()
    if k[0] < len(d):
        CFG["uni"] = int(nx())
    return m
def guardar(m, slot):
    nom = "esprob" + str(slot)
    d = codificar(m)
    if _store is not None:
        _store(nom, d)
    else:
        _MEM[nom] = d
    return nom
def cargar(slot):
    nom = "esprob" + str(slot)
    if _recall is not None:
        d = _recall(nom)
    else:
        if nom not in _MEM:
            raise ValueError("vacio")
        d = _MEM[nom]
    return decodificar(d)

# ---- ejemplos ----
def ej_viga_simple():
    m = Modelo("rigido", "Viga simple")
    m.nuevo_nodo(0, 0)
    m.nuevo_nodo(2, 0)
    m.nuevo_nodo(6, 0)
    m.add_miembro("viga", "A", "B")
    m.add_miembro("viga", "B", "C")
    m.add_apoyo("pin", "A")
    m.add_apoyo("rod", "C", 90)
    m.add_fuerza_pol("B", 1200, 270)
    return m, {"Ax": 0.0, "Ay": 800.0, "Cy": 400.0}
def ej_fuerza_inclinada():
    m = Modelo("rigido", "Fuerza inclinada")
    m.nuevo_nodo(0, 0)
    m.nuevo_nodo(3, 0)
    m.nuevo_nodo(5, 0)
    m.add_miembro("viga", "A", "B")
    m.add_miembro("viga", "B", "C")
    m.add_apoyo("pin", "A")
    m.add_apoyo("rod", "C", 90)
    m.add_fuerza_pol("B", 500, 240)
    return m, {"Ax": 250.0, "Ay": 173.20508, "Cy": 259.80762}
def ej_voladizo():
    m = Modelo("rigido", "Voladizo")
    m.nuevo_nodo(0, 0)
    m.nuevo_nodo(3, 0)
    m.add_miembro("viga", "A", "B")
    m.add_apoyo("emp", "A")
    m.add_carga("A", "B", 1, 1, 270)
    m.add_fuerza_pol("B", 2, 270)
    return m, {"Ax": 0.0, "Ay": 5.0, "MA": 10.5}
def ej_particula_cables():
    m = Modelo("particula", "Particula 2 cables")
    m.nuevo_nodo(0, 0, "P")
    m.nuevo_nodo(-3, 4, "A")
    m.nuevo_nodo(4, 3, "B")
    m.add_apoyo("cab", "P", 0, "A")
    m.add_apoyo("cab", "P", 0, "B")
    m.add_fuerza_pol("P", 100, 270)
    return m, {"TPA": 80.0, "TPB": 60.0}
def ej_momento():
    m = Modelo("rigido", "Par aplicado")
    m.nuevo_nodo(0, 0)
    m.nuevo_nodo(2, 0)
    m.nuevo_nodo(4, 0)
    m.add_miembro("viga", "A", "B")
    m.add_miembro("viga", "B", "C")
    m.add_apoyo("pin", "A")
    m.add_apoyo("rod", "C", 90)
    m.add_momento("B", 800)
    return m, {"Ax": 0.0, "Ay": 200.0, "Cy": -200.0}
def ej_pluma():
    m = Modelo("rigido", "Pluma con cable")
    m.nuevo_nodo(0, 0)
    m.nuevo_nodo(4, 0)
    m.nuevo_nodo(0, 3)
    m.add_miembro("viga", "A", "B")
    m.add_apoyo("pin", "A")
    m.add_apoyo("cab", "B", 0, "C")
    m.add_fuerza_pol("B", 2000, 270)
    return m, {"Ax": 2666.6667, "Ay": 0.0, "TBC": 3333.3333}
def ej_triangular():
    m = Modelo("rigido", "Carga triangular")
    m.nuevo_nodo(0, 0)
    m.nuevo_nodo(6, 0)
    m.add_miembro("viga", "A", "B")
    m.add_apoyo("pin", "A")
    m.add_apoyo("rod", "B", 90)
    m.add_carga("A", "B", 0, 600, 270)
    return m, {"Ax": 0.0, "Ay": 600.0, "By": 1200.0}
def ej_rodillo_inclinado():
    m = Modelo("rigido", "Rodillo inclinado")
    m.nuevo_nodo(0, 0)
    m.nuevo_nodo(2, 0)
    m.nuevo_nodo(4, 0)
    m.add_miembro("viga", "A", "B")
    m.add_miembro("viga", "B", "C")
    m.add_apoyo("pin", "A")
    m.add_apoyo("rod", "C", 120)
    m.add_fuerza_pol("B", 1000, 270)
    return m, {"Ax": 288.67513, "Ay": 500.0, "NC": 577.35027}
def ej_marco():
    m = Modelo("rigido", "Marco en L")
    m.nuevo_nodo(0, 0)
    m.nuevo_nodo(0, 3)
    m.nuevo_nodo(2, 3)
    m.nuevo_nodo(4, 3)
    m.add_miembro("viga", "A", "B")
    m.add_miembro("viga", "B", "C")
    m.add_miembro("viga", "C", "D")
    m.add_apoyo("pin", "A")
    m.add_apoyo("rod", "D", 90)
    m.add_fuerza_comp("B", 600, 0)
    m.add_fuerza_pol("C", 1000, 270)
    return m, {"Ax": -600.0, "Ay": 50.0, "Dy": 950.0}
def ej_indeterminado():
    m = Modelo("rigido", "Hiperestatica")
    m.nuevo_nodo(0, 0)
    m.nuevo_nodo(2, 0)
    m.nuevo_nodo(4, 0)
    m.add_miembro("viga", "A", "B")
    m.add_miembro("viga", "B", "C")
    m.add_apoyo("pin", "A")
    m.add_apoyo("pin", "C")
    m.add_fuerza_pol("B", 1000, 270)
    return m, "indeterminado"
def ej_incompatible():
    m = Modelo("rigido", "Mecanismo")
    m.nuevo_nodo(0, 0)
    m.nuevo_nodo(4, 0)
    m.add_miembro("viga", "A", "B")
    m.add_apoyo("rod", "A", 90)
    m.add_apoyo("rod", "B", 90)
    m.add_fuerza_comp("B", 100, -50)
    return m, "incompatible"
EJEMPLOS = [
    ("Viga simplemente apoyada", ej_viga_simple),
    ("Fuerza inclinada", ej_fuerza_inclinada),
    ("Voladizo w + P (kN)", ej_voladizo),
    ("Particula con 2 cables", ej_particula_cables),
    ("Viga con par aplicado", ej_momento),
    ("Pluma con cable", ej_pluma),
    ("Carga triangular", ej_triangular),
    ("Rodillo inclinado", ej_rodillo_inclinado),
    ("Marco en L", ej_marco),
    ("Hiperestatica (indet.)", ej_indeterminado),
    ("Mecanismo (incompatible)", ej_incompatible),
]

# ---- editor ----
PASOS = [0.1, 0.25, 0.5, 1.0, 2.0, 5.0, 10.0]
class Editor:
    def __init__(self, modelo):
        self.m = modelo
        self.g = CFG["grid"]
        self.cx = 0.0
        self.cy = 0.0
        if modelo.nodos:
            self.cx = modelo.nodos[0].x
            self.cy = modelo.nodos[0].y
        self.V = None
        self.msg = ""
        self.rehacer_vista()
    def rehacer_vista(self):
        pts = puntos_vista(self.m, [(self.cx, self.cy)])
        if len(self.m.nodos) < 2:
            g = self.g
            pts = pts + [(self.cx - 6 * g, self.cy - 3 * g),
                         (self.cx + 6 * g, self.cy + 3 * g)]
        self.V = Vista(pts)
    def en_pantalla(self):
        sx, sy = self.V.p((self.cx, self.cy))
        return 20 <= sx <= SW - 20 and 30 <= sy <= SH - 40
    def redibujar(self, ayuda=None):
        if not self.en_pantalla():
            self.rehacer_vista()
        n = self.nodo_cursor()
        t = "x=" + fmt(self.cx, 2) + " y=" + fmt(self.cy, 2)
        if n is not None:
            t += " [" + n.nom + "]"
        t += "  paso " + fmt(self.g, 2)
        if ayuda is None:
            ayuda = self.msg if self.msg else \
                "ENTER menu  h ayuda  r resolver  esc"
        dibujar(self.m, self.m.sol, self.V, t, ayuda, (self.cx, self.cy),
                self.g)
    def nodo_cursor(self):
        mejor = None
        dm = 1e30
        tol = max(0.45 * self.g, 6.0 / self.V.s)
        for n in self.m.nodos:
            d = dist(n.p(), (self.cx, self.cy))
            if d < dm:
                dm = d
                mejor = n
        if mejor is not None and dm <= tol:
            return mejor
        return None
    def nodo_o_nuevo(self):
        n = self.nodo_cursor()
        if n is None:
            n = self.m.nuevo_nodo(self._r(self.cx), self._r(self.cy))
        return n
    def _r(self, v):
        return round(v * 1e9) / 1e9
    def num(self, prompt, defecto=None):
        if CFG["gfxin"]:
            return entrada_gfx(prompt, defecto)
        try:
            return leer_num(prompt, defecto)
        except Cancelar:
            return None
    def opcion(self, titulo, ops):
        return menu_gfx(titulo, ops)
    def mover(self, k):
        g = self.g
        if k == "up":
            self.cy += g
        elif k == "down":
            self.cy -= g
        elif k == "left":
            self.cx -= g
        elif k == "right":
            self.cx += g
        else:
            return False
        self.cx = self._r(round(self.cx / g) * g)
        self.cy = self._r(round(self.cy / g) * g)
        return True
    def elegir_punto(self, msg):
        while True:
            self.redibujar(msg)
            k = tecla()
            if self.mover(k):
                continue
            if k in ("+", "-"):
                self.cambia_paso(k)
                continue
            if k == "esc":
                return None
            if k == "enter":
                return self.nodo_o_nuevo()
    def cambia_paso(self, k):
        i = 0
        for j in range(len(PASOS)):
            if abs(PASOS[j] - self.g) < 1e-12:
                i = j
        i = i + 1 if k == "+" else i - 1
        i = max(0, min(len(PASOS) - 1, i))
        self.g = PASOS[i]
        CFG["grid"] = self.g
    def a_nodo(self):
        n = self.nodo_o_nuevo()
        self.msg = "Nodo " + n.nom + " en (" + fmt(n.x, 2) + "," + \
            fmt(n.y, 2) + ")"
    def a_miembro(self):
        a = self.nodo_o_nuevo()
        b = self.elegir_punto("Miembro desde " + a.nom +
                              ": lleve el cursor al final, ENTER")
        if b is None:
            return
        if b.nom == a.nom:
            self.msg = "Miembro de longitud cero: cancelado"
            return
        i = self.opcion("Tipo de miembro", ["Viga", "Barra",
                                            "Cuerpo rigido"])
        if i < 0:
            return
        self.m.add_miembro(T_MIEMBRO[i], a.nom, b.nom)
        self.msg = N_MIEMBRO[T_MIEMBRO[i]] + " " + a.nom + "-" + b.nom
    def a_apoyo(self):
        n = self.nodo_o_nuevo()
        i = self.opcion("Apoyo en " + n.nom, ["Articulacion", "Rodillo",
                                               "Empotramiento", "Cable",
                                               "Biela"])
        if i < 0:
            return
        t = T_APOYO[i]
        if t == "rod":
            ang = self.num("Angulo de la reaccion N (90=arriba)", 90)
            if ang is None:
                return
            self.m.add_apoyo(t, n.nom, ang)
        elif t in ("cab", "bie"):
            j = self.opcion("Direccion", ["Hacia un punto (cursor)",
                                          "Por angulo"])
            if j < 0:
                return
            if j == 0:
                q = self.elegir_punto("Lleve el cursor al anclaje, ENTER")
                if q is None:
                    return
                if q.nom == n.nom:
                    self.msg = "Anclaje igual al nodo: cancelado"
                    return
                self.m.add_apoyo(t, n.nom, 0, q.nom)
            else:
                ang = self.num("Angulo (grados desde +x)", 90)
                if ang is None:
                    return
                self.m.add_apoyo(t, n.nom, ang)
        else:
            self.m.add_apoyo(t, n.nom)
        self.msg = N_APOYO[t] + " en " + n.nom
    def a_fuerza(self):
        n = self.nodo_o_nuevo()
        i = self.opcion("Fuerza en " + n.nom, ["Magnitud y angulo",
                                                "Componentes Fx, Fy"])
        if i < 0:
            return
        if i == 0:
            F = self.num("Magnitud (" + uF() + ")")
            if F is None:
                return
            a = self.num("Angulo (grados desde +x)", 270)
            if a is None:
                return
            f = self.m.add_fuerza_pol(n.nom, F, a)
        else:
            fx = self.num("Fx (" + uF() + ")", 0)
            if fx is None:
                return
            fy = self.num("Fy (" + uF() + ")", 0)
            if fy is None:
                return
            f = self.m.add_fuerza_comp(n.nom, fx, fy)
        self.msg = "Fuerza " + f.nom + " en " + n.nom
    def a_momento(self):
        n = self.nodo_o_nuevo()
        M = self.num("Momento (" + uM() + ", +antihorario)")
        if M is None:
            return
        mm = self.m.add_momento(n.nom, M)
        self.msg = "Momento " + mm.nom + " en " + n.nom
    def a_carga(self):
        a = self.nodo_o_nuevo()
        b = self.elegir_punto("Carga desde " + a.nom +
                              ": cursor al final, ENTER")
        if b is None or b.nom == a.nom:
            return
        w1 = self.num("w en " + a.nom + " (" + uW() + ")")
        if w1 is None:
            return
        w2 = self.num("w en " + b.nom + " (" + uW() + ")", w1)
        if w2 is None:
            return
        ang = self.num("Direccion (270=abajo)", 270)
        if ang is None:
            return
        c = self.m.add_carga(a.nom, b.nom, w1, w2, ang)
        self.msg = "Carga " + c.nom + " " + a.nom + "-" + b.nom
    def a_desconocida(self):
        n = self.nodo_o_nuevo()
        i = self.opcion("Fuerza desconocida", ["Direccion conocida",
                                                "Componentes libres"])
        if i < 0:
            return
        if i == 0:
            ang = self.num("Angulo de la fuerza", 0)
            if ang is None:
                return
            f = self.m.add_fdesc(n.nom, "dir", ang)
        else:
            f = self.m.add_fdesc(n.nom, "libre")
        self.msg = "Incognita " + f.nom + " en " + n.nom
    def a_borrar(self):
        n = self.nodo_cursor()
        if n is None:
            self.msg = "No hay nodo bajo el cursor"
            return
        els = self.m.elementos_en(n.nom)[:7]
        ops = [e[0][:30] for e in els] + ["Nodo " + n.nom + " y todo"]
        i = self.opcion("Borrar en " + n.nom, ops)
        if i < 0:
            return
        if i == len(els):
            self.m.borrar_nodo(n.nom)
            self.msg = "Nodo " + n.nom + " borrado"
        else:
            self.m.quitar(els[i][1], els[i][2])
            self.msg = "Borrado: " + els[i][0][:28]
    def a_editar(self):
        n = self.nodo_cursor()
        if n is None:
            self.msg = "No hay nodo bajo el cursor"
            return
        cargas = [f for f in self.m.fuerzas if f.nodo == n.nom] + \
            [mm for mm in self.m.momentos if mm.nodo == n.nom]
        ops = ["Coordenadas de " + n.nom] + ["Editar " + c.nom
                                             for c in cargas][:6]
        i = self.opcion("Editar", ops)
        if i < 0:
            return
        if i == 0:
            x = self.num("x de " + n.nom, n.x)
            if x is None:
                return
            y = self.num("y de " + n.nom, n.y)
            if y is None:
                return
            if self.m.nodo_en(x, y) not in (None, n):
                self.msg = "Ya existe un nodo en ese punto"
                return
            self.m.mover_nodo(n.nom, x, y)
            self.cx, self.cy = x, y
            self.rehacer_vista()
            self.msg = n.nom + " movido"
            return
        c = cargas[i - 1]
        if isinstance(c, Momento):
            M = self.num("Momento " + c.nom, c.M)
            if M is not None:
                c.M = M
        elif c.modo == "pol":
            F = self.num("Magnitud " + c.nom, c.mag)
            if F is None:
                return
            a = self.num("Angulo " + c.nom, c.ang)
            if a is None:
                return
            nf = fuerza_polar(c.nom, c.nodo, F, a)
            c.fx, c.fy, c.mag, c.ang = nf.fx, nf.fy, nf.mag, nf.ang
        else:
            fx = self.num("Fx " + c.nom, c.fx)
            if fx is None:
                return
            fy = self.num("Fy " + c.nom, c.fy)
            if fy is None:
                return
            c.fx, c.fy = fx, fy
        self.m.invalidar()
        self.msg = c.nom + " modificada"
    def a_ir(self):
        x = self.num("Ir a x", self.cx)
        if x is None:
            return
        y = self.num("Ir a y", self.cy)
        if y is None:
            return
        self.cx, self.cy = x, y
        self.rehacer_vista()
    def a_menu_punto(self):
        n = self.nodo_cursor()
        if n is None:
            self.a_nodo()
            return
        i = self.opcion("Nodo " + n.nom, ["Apoyo", "Fuerza", "Momento",
                                           "Miembro desde aqui",
                                           "Carga distribuida",
                                           "Fuerza desconocida", "Editar",
                                           "Borrar"])
        acc = [self.a_apoyo, self.a_fuerza, self.a_momento, self.a_miembro,
               self.a_carga, self.a_desconocida, self.a_editar,
               self.a_borrar]
        if i >= 0:
            acc[i]()
    def ayuda(self):
        L = ["Flechas: mover cursor", "+/-: paso de rejilla",
             "ENTER: crear nodo / menu del nodo", "n: nodo  b: viga/barra",
             "s: apoyo  f: fuerza  m: momento", "w: carga distribuida",
             "u: fuerza desconocida", "e: editar  d: borrar",
             "c: ir a coordenada  r: resolver", "esc: salir del editor"]
        g_ini()
        barra_sup("AYUDA DEL EDITOR")
        for i in range(len(L)):
            g_texto(8, 18 + 15 * i, L[i], C_NEGRO)
        barra_inf("Pulse una tecla")
        esperar_tecla()
    def bucle(self):
        tab = {"n": self.a_nodo, "b": self.a_miembro, "s": self.a_apoyo,
               "f": self.a_fuerza, "m": self.a_momento, "w": self.a_carga,
               "u": self.a_desconocida, "e": self.a_editar,
               "d": self.a_borrar, "del": self.a_borrar, "c": self.a_ir,
               "enter": self.a_menu_punto, "h": self.ayuda}
        while True:
            self.redibujar()
            k = tecla()
            if self.mover(k):
                continue
            if k in ("+", "-"):
                self.cambia_paso(k)
                continue
            if k == "esc":
                return "salir"
            if k == "r":
                return "resolver"
            if k in tab:
                self.msg = ""
                tab[k]()
def editar_grafico(modelo):
    if not g_ok():
        p("Pantalla grafica no disponible (ti_draw).")
        return "salir"
    return Editor(modelo).bucle()

# ---- herramientas ----
import math
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

# ---- pruebas ----
import math
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

# ---- interfaz ----
ACT = {"m": None}
def leer_nodo(m, prompt, crear=True):
    while True:
        s = leer(prompt + (" (nodo o x,y)" if crear else " (nodo)") + ": ")
        if s.lower() in ("q", "esc", ""):
            raise Cancelar()
        n = m.nodo(s)
        if n is not None:
            return n
        if crear and "," in s:
            a = s.split(",")
            try:
                x = evaluar(a[0])
                y = evaluar(a[1])
                n = m.nuevo_nodo(x, y)
                p("  Punto " + n.nom + " = (" + fmt(x) + ", " + fmt(y) + ")")
                return n
            except Exception:
                pass
        p("  No existe. Nodos: " + ", ".join([k.nom for k in m.nodos]))
def lista_nodos(m):
    L = []
    for n in m.nodos:
        L.append(n.nom + " (" + fmt(n.x) + ", " + fmt(n.y) + ")")
    return L
def desc_apoyo(m, a):
    s = a.nodo + ": " + N_APOYO[a.tipo]
    if a.tipo == "rod":
        s += " N a " + fmt(a.ang, 1) + "°"
    elif a.tipo in ("cab", "bie"):
        s += (" -> " + a.ref) if a.ref else (" a " + fmt(a.ang, 1) + "°")
    return s
def desc_fuerza(f):
    if f.modo == "pol":
        return f.nom + " en " + f.nodo + ": " + fmt(f.mag) + " " + uF() + \
            " a " + fmt(f.ang, 2) + "°"
    return f.nom + " en " + f.nodo + ": (" + fmt(f.fx) + ", " + fmt(f.fy) + \
        ") " + uF()
def resumen_modelo(m):
    L = ["Tipo: " + ("PARTICULA" if m.tipo == "particula" else
                     "CUERPO RIGIDO"),
         "Unidades: " + uF() + ", " + uL() + ", " + uM()]
    L.append("Nodos:")
    L += ["  " + s for s in lista_nodos(m)] or ["  -"]
    if m.miembros:
        L.append("Miembros:")
        for e in m.miembros:
            L.append("  " + N_MIEMBRO[e.tipo] + " " + e.a + "-" + e.b)
    if m.apoyos:
        L.append("Apoyos:")
        L += ["  " + desc_apoyo(m, a) for a in m.apoyos]
    if m.fuerzas:
        L.append("Fuerzas:")
        L += ["  " + desc_fuerza(f) for f in m.fuerzas]
    if m.momentos:
        L.append("Momentos (+ antihorario):")
        L += ["  " + e.nom + " en " + e.nodo + ": " + fmt(e.M) + " " + uM()
              for e in m.momentos]
    if m.cargas:
        L.append("Cargas distribuidas:")
        L += ["  " + c.nom + " " + c.a + "-" + c.b + ": " + fmt(c.w1) + "->" +
              fmt(c.w2) + " " + uW() + " a " + fmt(c.ang, 1) + "°"
              for c in m.cargas]
    if m.fdesc:
        L.append("Fuerzas desconocidas:")
        L += ["  " + f.nom + " en " + f.nodo + (" dir " + fmt(f.ang, 1) +
                                                 "°" if f.modo == "dir"
                                                 else " (Fx,Fy)")
              for f in m.fdesc]
    inc = m.incognitas()
    if m.tipo == "particula":
        inc = [u for u in inc if u.tipo != "M"]
    L.append("Incognitas (" + str(len(inc)) + "): " +
             ", ".join([u.nom for u in inc]))
    L.append("Ecuaciones: " + ("2" if m.tipo == "particula" else "3"))
    return L
def _borrar_de(m, lista, descs, titulo):
    if not lista:
        p("(no hay elementos)")
        return
    i = elegir(titulo, descs)
    m.quitar(lista, lista[i])
    p("Eliminado.")
def sm_nodos(m):
    while True:
        k = menu("PUNTOS / NODOS", ["Listar", "Agregar (x,y)", "Mover nodo",
                                    "Borrar nodo"])
        if k == 0:
            return
        try:
            if k == 1:
                mostrar(lista_nodos(m) or ["(sin nodos)"], "Nodos")
            elif k == 2:
                while True:
                    x, y = leer_par("Nuevo punto (q=fin)")
                    n0 = m.nodo_en(x, y)
                    n = m.nuevo_nodo(x, y)
                    p(("Ya existia " if n0 else "Creado ") + n.nom)
            elif k == 3:
                n = leer_nodo(m, "Nodo", False)
                x, y = leer_par("Nueva posicion de " + n.nom)
                o = m.nodo_en(x, y)
                if o is not None and o is not n:
                    p("Ya hay un nodo ahi (" + o.nom + ").")
                else:
                    m.mover_nodo(n.nom, x, y)
                    p("Movido. El dibujo se actualiza automaticamente.")
            elif k == 4:
                n = leer_nodo(m, "Nodo a borrar", False)
                m.borrar_nodo(n.nom)
                p("Borrado " + n.nom + " (y sus elementos).")
        except Cancelar:
            pass
def sm_miembros(m):
    while True:
        k = menu("VIGAS / BARRAS", ["Listar", "Agregar", "Borrar"])
        if k == 0:
            return
        try:
            if k == 1:
                mostrar([N_MIEMBRO[e.tipo] + " " + e.a + "-" + e.b + "  L=" +
                         fmt(dist(m.pos(e.a), m.pos(e.b))) + " " + uL()
                         for e in m.miembros] or ["(ninguno)"], "Miembros")
            elif k == 2:
                t = elegir("Tipo", ["Viga", "Barra", "Cuerpo rigido"])
                a = leer_nodo(m, "Extremo 1")
                b = leer_nodo(m, "Extremo 2")
                if a is b:
                    p("Los extremos deben ser distintos.")
                else:
                    m.add_miembro(T_MIEMBRO[t], a.nom, b.nom)
                    p("Agregado " + a.nom + "-" + b.nom + ", L=" +
                      fmt(dist(a.p(), b.p())))
            elif k == 3:
                _borrar_de(m, m.miembros, [e.a + "-" + e.b
                                           for e in m.miembros], "Borrar")
        except Cancelar:
            pass
def agregar_apoyo(m, n=None):
    t = elegir("Tipo de apoyo", [N_APOYO[x] + " - " + C_APOYO[x]
                                 for x in T_APOYO])
    tp = T_APOYO[t]
    if n is None:
        n = leer_nodo(m, "Nodo del apoyo")
    if tp == "rod":
        p("Direccion de la reaccion N (normal a la superficie, hacia el" +
          " cuerpo). 90=arriba, 0=derecha. Plano inclinado a α:" +
          " N a 90+α.")
        ang = leer_num("Angulo de N", 90)
        m.add_apoyo(tp, n.nom, ang)
    elif tp in ("cab", "bie"):
        i = elegir("Direccion", ["Hacia un punto de anclaje", "Por angulo"])
        if i == 0:
            q = leer_nodo(m, "Punto de anclaje")
            if q is n:
                p("El anclaje debe ser distinto del nodo.")
                return
            m.add_apoyo(tp, n.nom, 0, q.nom)
        else:
            ang = leer_num("Angulo desde +x (direccion de traccion)")
            m.add_apoyo(tp, n.nom, ang)
    else:
        m.add_apoyo(tp, n.nom)
    p("Apoyo agregado en " + n.nom)
def sm_apoyos(m):
    while True:
        k = menu("APOYOS", ["Listar", "Agregar", "Borrar"])
        if k == 0:
            return
        try:
            if k == 1:
                mostrar([desc_apoyo(m, a) for a in m.apoyos] or
                        ["(ninguno)"], "Apoyos")
            elif k == 2:
                agregar_apoyo(m)
            elif k == 3:
                _borrar_de(m, m.apoyos, [desc_apoyo(m, a) for a in m.apoyos],
                           "Borrar")
        except Cancelar:
            pass
def agregar_fuerza(m, n=None):
    if n is None:
        n = leer_nodo(m, "Punto de aplicacion")
    i = elegir("Definir por", ["Magnitud y angulo", "Componentes Fx, Fy",
                               "Horizontal", "Vertical",
                               "Direccion hacia un punto"])
    if i == 0:
        F = leer_num("Magnitud (" + uF() + ")")
        a = leer_num("Angulo desde +x (grados)")
        f = m.add_fuerza_pol(n.nom, F, a)
    elif i == 1:
        fx = leer_num("Fx (" + uF() + ")")
        fy = leer_num("Fy (" + uF() + ")")
        f = m.add_fuerza_comp(n.nom, fx, fy)
    elif i == 2:
        fx = leer_num("Fx (+ derecha, - izquierda)")
        f = m.add_fuerza_pol(n.nom, abs(fx), 0 if fx >= 0 else 180)
    elif i == 3:
        fy = leer_num("Fy (+ arriba, - abajo)")
        f = m.add_fuerza_pol(n.nom, abs(fy), 90 if fy >= 0 else 270)
    else:
        F = leer_num("Magnitud (" + uF() + ")")
        q = leer_par("Punto hacia el que apunta")
        u = v_unit(v_sub(q, n.p()))
        if u is None:
            p("Direccion nula.")
            return
        f = m.add_fuerza_pol(n.nom, F, ang_de(u))
    p("Agregada: " + desc_fuerza(f))
def editar_fuerza(m):
    if not m.fuerzas:
        p("(no hay fuerzas)")
        return
    i = elegir("Fuerza", [desc_fuerza(f) for f in m.fuerzas])
    f = m.fuerzas[i]
    if f.modo == "pol":
        F = leer_num("Magnitud", f.mag)
        a = leer_num("Angulo", f.ang)
        nf = fuerza_polar(f.nom, f.nodo, F, a)
        f.fx, f.fy, f.mag, f.ang = nf.fx, nf.fy, nf.mag, nf.ang
    else:
        f.fx = leer_num("Fx", f.fx)
        f.fy = leer_num("Fy", f.fy)
    m.invalidar()
    p("Modificada: " + desc_fuerza(f))
def sm_fuerzas(m):
    while True:
        k = menu("FUERZAS CONOCIDAS", ["Listar", "Agregar", "Editar",
                                       "Borrar"])
        if k == 0:
            return
        try:
            if k == 1:
                mostrar([desc_fuerza(f) for f in m.fuerzas] or ["(ninguna)"],
                        "Fuerzas")
            elif k == 2:
                agregar_fuerza(m)
            elif k == 3:
                editar_fuerza(m)
            elif k == 4:
                _borrar_de(m, m.fuerzas, [desc_fuerza(f) for f in m.fuerzas],
                           "Borrar")
        except Cancelar:
            pass
def sm_momentos(m):
    while True:
        k = menu("MOMENTOS / PARES", ["Listar", "Agregar", "Borrar"])
        if k == 0:
            return
        try:
            if k == 1:
                mostrar([e.nom + " en " + e.nodo + ": " + fmt(e.M) + " " +
                         uM() for e in m.momentos] or ["(ninguno)"],
                        "Momentos")
            elif k == 2:
                n = leer_nodo(m, "Punto")
                M = leer_num("M (" + uM() + "), + antihorario, - horario")
                e = m.add_momento(n.nom, M)
                p("Agregado " + e.nom)
            elif k == 3:
                _borrar_de(m, m.momentos, [e.nom for e in m.momentos],
                           "Borrar")
        except Cancelar:
            pass
def sm_cargas(m):
    while True:
        k = menu("CARGAS DISTRIBUIDAS", ["Listar", "Agregar (lineal)",
                                         "Borrar"])
        if k == 0:
            return
        try:
            if k == 1:
                mostrar([c.nom + " " + c.a + "-" + c.b + ": " + fmt(c.w1) +
                         "->" + fmt(c.w2) + " " + uW()
                         for c in m.cargas] or ["(ninguna)"], "Cargas")
            elif k == 2:
                p("Carga lineal entre dos puntos (uniforme si w1=w2," +
                  " triangular si una es 0).")
                a = leer_nodo(m, "Inicio")
                b = leer_nodo(m, "Fin")
                if a is b:
                    p("Inicio y fin deben ser distintos.")
                    continue
                w1 = leer_num("w en " + a.nom + " (" + uW() + ")")
                w2 = leer_num("w en " + b.nom, w1)
                ang = leer_num("Direccion (270 = hacia abajo)", 270)
                c = m.add_carga(a.nom, b.nom, w1, w2, ang)
                W, xc = carga_lineal(dist(a.p(), b.p()), w1, w2)
                p("Agregada " + c.nom + ": resultante " + fmt(W) + " " +
                  uF() + " a " + fmt(xc) + " " + uL() + " de " + a.nom)
            elif k == 3:
                _borrar_de(m, m.cargas, [c.nom for c in m.cargas], "Borrar")
        except Cancelar:
            pass
def sm_fdesc(m):
    while True:
        k = menu("FUERZAS DESCONOCIDAS", ["Listar", "Agregar", "Borrar"])
        if k == 0:
            return
        try:
            if k == 1:
                mostrar([f.nom + " en " + f.nodo + (" dir " + fmt(f.ang) if
                                                     f.modo == "dir" else
                                                     " libre")
                         for f in m.fdesc] or ["(ninguna)"], "Desconocidas")
            elif k == 2:
                n = leer_nodo(m, "Punto")
                i = elegir("Tipo", ["Direccion conocida (1 incognita)",
                                    "Magnitud y direccion desconocidas" +
                                    " (2 incognitas)"])
                if i == 0:
                    ang = leer_num("Angulo de la linea de accion")
                    f = m.add_fdesc(n.nom, "dir", ang)
                else:
                    f = m.add_fdesc(n.nom, "libre")
                p("Agregada " + f.nom)
            elif k == 3:
                _borrar_de(m, m.fdesc, [f.nom for f in m.fdesc], "Borrar")
        except Cancelar:
            pass
def sm_guardar(m):
    try:
        s = leer_ent("Ranura (1-9)", 1, 9)
        nom = guardar(m, s)
        p("Guardado en la variable '" + nom + "'. Guarde el documento" +
          " (ctrl+S) para conservarlo.")
    except Cancelar:
        pass
    except Exception as e:
        p("No se pudo guardar: " + str(e))
def cargar_problema():
    try:
        s = leer_ent("Ranura (1-9)", 1, 9)
        m = cargar(s)
        p("Problema cargado (" + str(len(m.nodos)) + " nodos).")
        return m
    except Cancelar:
        return None
    except Exception:
        p("No hay problema guardado en esa ranura.")
        return None
def configurador(m):
    while True:
        k = menu("PROBLEMA: " + m.titulo,
                 ["Puntos / nodos", "Vigas y barras", "Apoyos",
                  "Fuerzas conocidas", "Momentos", "Cargas distribuidas",
                  "Fuerzas desconocidas", "Editor grafico (dibujo)",
                  "Ver diagrama", "Resumen del modelo", "RESOLVER",
                  "Guardar problema", "Tipo: " +
                  ("particula" if m.tipo == "particula" else "cuerpo rigido")])
        if k == 0:
            return
        try:
            if k == 1:
                sm_nodos(m)
            elif k == 2:
                sm_miembros(m)
            elif k == 3:
                sm_apoyos(m)
            elif k == 4:
                sm_fuerzas(m)
            elif k == 5:
                sm_momentos(m)
            elif k == 6:
                sm_cargas(m)
            elif k == 7:
                sm_fdesc(m)
            elif k == 8:
                if editar_grafico(m) == "resolver":
                    resolver_y_mostrar(m)
            elif k == 9:
                if not ver_dcl(m):
                    p("Graficos no disponibles.")
            elif k == 10:
                mostrar(resumen_modelo(m), "Resumen")
            elif k == 11:
                resolver_y_mostrar(m)
            elif k == 12:
                sm_guardar(m)
            elif k == 13:
                m.tipo = "rigido" if m.tipo == "particula" else "particula"
                m.invalidar()
        except Cancelar:
            pass
def resolver_y_mostrar(m):
    R = resolver(m)
    p("")
    mostrar(resumen_txt(m, R), "RESULTADO")
    menu_resultados(m, R)
def menu_resultados(m, R):
    while True:
        ops = ["Resumen de resultados", "Solucion PASO A PASO",
               "DCL con reacciones (grafico)",
               "Momento respecto a un punto",
               "Cambiar punto de momentos y resolver"]
        viga = es_viga_horizontal(m) and R["estado"] == "determinado" and \
            m.tipo != "particula"
        if viga:
            ops += ["Fuerzas internas en una seccion",
                    "Diagramas V y M (grafico)"]
        k = menu("RESULTADOS", ops)
        if k == 0:
            return
        try:
            if k == 1:
                mostrar(resumen_txt(m, R), "RESULTADO")
            elif k == 2:
                ver_pasos(pasos(m, R))
            elif k == 3:
                if not ver_dcl(m, R):
                    p("Graficos no disponibles.")
            elif k == 4:
                if m.tipo == "particula":
                    p("En una particula todas las fuerzas concurren.")
                    continue
                n = leer(("Punto (nodo o x,y): "))
                pt = None
                nm = n.upper()
                if m.nodo(n) is not None:
                    pt = m.pos(n)
                elif "," in n:
                    a = n.split(",")
                    pt = (evaluar(a[0]), evaluar(a[1]))
                    nm = "(" + n + ")"
                if pt is None:
                    p("Punto invalido.")
                else:
                    mostrar(momento_txt(m, R, nm, pt), "Momento")
            elif k == 5:
                if m.tipo == "particula":
                    p("No aplica a particulas.")
                    continue
                s = leer("Nodo o x,y (ENTER = automatico): ")
                if s == "":
                    m.ref = None
                elif m.nodo(s) is not None:
                    m.ref = s.upper()
                elif "," in s:
                    a = s.split(",")
                    m.ref = (evaluar(a[0]), evaluar(a[1]))
                else:
                    p("Punto invalido.")
                    continue
                R = resolver(m)
                mostrar(resumen_txt(m, R), "RESULTADO")
            elif k == 6 and viga:
                xs = leer_num("x de la seccion (" + uL() + ")")
                mostrar(internas_txt(m, R, xs), "Fuerzas internas")
            elif k == 7 and viga:
                if not ver_VM(m, R):
                    p("Graficos no disponibles.")
        except Cancelar:
            pass
        except Exception as e:
            p("Error: " + str(e))
def _nodo_x(m, x):
    return m.nuevo_nodo(x, 0.0)
def _rehacer_viga(m):
    ns = sorted([n for n in m.nodos if abs(n.y) < 1e-12],
                key=lambda n: n.x)
    m.miembros = [e for e in m.miembros if not (m.pos(e.a)[1] == 0 and
                                                 m.pos(e.b)[1] == 0)]
    for i in range(len(ns) - 1):
        m.add_miembro("viga", ns[i].nom, ns[i + 1].nom)
def asistente_viga():
    p("ASISTENTE DE VIGA HORIZONTAL (eje x, y=0). Distancias desde el" +
      " extremo izquierdo.")
    m = Modelo("rigido", "Viga")
    L = leer_num("Longitud total L (" + uL() + ")", None, 1e-9)
    _nodo_x(m, 0.0)
    _nodo_x(m, L)
    while True:
        k = menu("Apoyos de la viga", ["Articulacion", "Rodillo",
                                       "Empotramiento", "Cable"],
                 "Terminar apoyos")
        if k == 0:
            break
        x = leer_num("Posicion x", 0.0 if not m.apoyos else L, 0, L)
        n = _nodo_x(m, x)
        t = T_APOYO[[0, 1, 2, 3][k - 1]]
        if t == "rod":
            m.add_apoyo(t, n.nom, leer_num("Angulo de N", 90))
        elif t == "cab":
            q = leer_par("Punto de anclaje del cable")
            a = m.nuevo_nodo(q[0], q[1])
            m.add_apoyo(t, n.nom, 0, a.nom)
        else:
            m.add_apoyo(t, n.nom)
    while True:
        k = menu("Cargas de la viga", ["Fuerza puntual", "Carga" +
                                       " distribuida", "Momento (par)"],
                 "Terminar cargas")
        if k == 0:
            break
        if k == 1:
            x = leer_num("Posicion x", None, 0, L)
            n = _nodo_x(m, x)
            F = leer_num("Magnitud (" + uF() + ")")
            a = leer_num("Angulo (270 = abajo)", 270)
            m.add_fuerza_pol(n.nom, F, a)
        elif k == 2:
            x1 = leer_num("Desde x", 0, 0, L)
            x2 = leer_num("Hasta x", L, 0, L)
            if abs(x2 - x1) < 1e-12:
                p("Longitud cero.")
                continue
            w1 = leer_num("w inicial (" + uW() + ")")
            w2 = leer_num("w final", w1)
            a = _nodo_x(m, x1)
            b = _nodo_x(m, x2)
            m.add_carga(a.nom, b.nom, w1, w2, 270)
        else:
            x = leer_num("Posicion x", None, 0, L)
            n = _nodo_x(m, x)
            m.add_momento(n.nom, leer_num("M (+ antihorario)"))
    _rehacer_viga(m)
    return m
def asistente_particula():
    p("ASISTENTE DE PARTICULA: la particula esta en P(0,0). Las" +
      " fuerzas concurren en P.")
    m = Modelo("particula", "Particula")
    P = m.nuevo_nodo(0.0, 0.0, "P")
    while True:
        k = menu("Fuerzas sobre P", ["Cable hacia un punto (T?)",
                                     "Cable por angulo (T?)",
                                     "Fuerza conocida",
                                     "Fuerza desconocida (dir. conocida)",
                                     "Fuerza desconocida (libre)",
                                     "Peso (vertical abajo)"],
                 "Terminar")
        if k == 0:
            break
        try:
            if k == 1:
                q = leer_par("Punto de anclaje")
                a = m.nuevo_nodo(q[0], q[1])
                if a is P:
                    p("El anclaje no puede ser P.")
                    continue
                m.add_apoyo("cab", "P", 0, a.nom)
            elif k == 2:
                m.add_apoyo("cab", "P", leer_num("Angulo del cable"))
            elif k == 3:
                agregar_fuerza(m, P)
            elif k == 4:
                m.add_fdesc("P", "dir", leer_num("Angulo de la fuerza"))
            elif k == 5:
                m.add_fdesc("P", "libre")
            elif k == 6:
                m.add_fuerza_pol("P", leer_num("Peso (" + uF() + ")"), 270)
        except Cancelar:
            pass
    return m
def nuevo_general(tipo, titulo):
    m = Modelo(tipo, titulo)
    i = elegir("Metodo de configuracion", ["Por coordenadas (menus)",
                                           "Por dibujo (editor grafico)"])
    ACT["m"] = m
    if i == 1:
        if editar_grafico(m) == "resolver":
            resolver_y_mostrar(m)
    configurador(m)
def menu_ejemplos():
    k = menu("EJEMPLOS RESUELTOS", [e[0] for e in EJEMPLOS])
    if k == 0:
        return None
    m, e = EJEMPLOS[k - 1][1]()
    if "kN" in EJEMPLOS[k - 1][0]:
        CFG["uni"] = 1
    elif m.tipo == "particula":
        CFG["uni"] = 2
    else:
        CFG["uni"] = 0
    p("Cargado: " + m.titulo + " (unidades " + uF() + ", " + uL() + ")")
    return m
def menu_estatica():
    while True:
        k = menu("ESTATICA", ["Equilibrio 2D (problema nuevo)",
                              "Equilibrio 3D  [futuro]",
                              "Particulas",
                              "Cuerpos rigidos",
                              "Vigas y estructuras",
                              "Ejemplos resueltos",
                              "Continuar problema actual",
                              "Cargar problema guardado"])
        if k == 0:
            return
        try:
            if k == 1:
                nuevo_general("rigido", "Equilibrio 2D")
            elif k == 2:
                mostrar(["Modulo en desarrollo para una version futura.",
                         "La arquitectura (vectores 3D, producto cruz," +
                         " Gauss n x n) ya esta preparada.",
                         "Mientras tanto use HERRAMIENTAS > Momento 3D y" +
                         " Vectores 3D."], "Equilibrio 3D")
            elif k == 3:
                i = elegir("Particula", ["Asistente rapido",
                                         "Configuracion libre"])
                if i == 0:
                    m = asistente_particula()
                    ACT["m"] = m
                    resolver_y_mostrar(m)
                    configurador(m)
                else:
                    nuevo_general("particula", "Particula")
            elif k == 4:
                nuevo_general("rigido", "Cuerpo rigido")
            elif k == 5:
                i = elegir("Vigas", ["Asistente de viga horizontal",
                                     "Estructura libre (coordenadas/dibujo)"])
                if i == 0:
                    m = asistente_viga()
                    ACT["m"] = m
                    resolver_y_mostrar(m)
                    configurador(m)
                else:
                    nuevo_general("rigido", "Estructura")
            elif k == 6:
                m = menu_ejemplos()
                if m is not None:
                    ACT["m"] = m
                    if si_no("Ver diagrama antes de resolver?"):
                        ver_dcl(m)
                    resolver_y_mostrar(m)
                    configurador(m)
            elif k == 7:
                if ACT["m"] is None:
                    p("No hay problema activo.")
                else:
                    configurador(ACT["m"])
            elif k == 8:
                m = cargar_problema()
                if m is not None:
                    ACT["m"] = m
                    configurador(m)
        except Cancelar:
            pass
def menu_config():
    while True:
        k = menu("CONFIGURACION",
                 ["Decimales: " + str(CFG["dec"]),
                  "Unidades: " + uF() + ", " + uL(),
                  "Simbolos ASCII: " + ("si" if CFG["ascii"] else "no"),
                  "Lineas por pagina: " + str(CFG["lineas"]),
                  "Ancho de linea: " + str(CFG["ancho"]),
                  "Entrada en editor: " + ("grafica" if CFG["gfxin"]
                                           else "shell"),
                  "Paso de rejilla: " + fmt(CFG["grid"], 2),
                  "Ejecutar autopruebas",
                  "Acerca de"])
        if k == 0:
            return
        try:
            if k == 1:
                CFG["dec"] = leer_ent("Decimales (0-8)", 0, 8, CFG["dec"])
            elif k == 2:
                i = elegir("Sistema", [u[0] + ", " + u[1] + ", " + u[2]
                                       for u in SIS_UNI], CFG["uni"])
                CFG["uni"] = i
            elif k == 3:
                CFG["ascii"] = 1 - CFG["ascii"]
            elif k == 4:
                CFG["lineas"] = leer_ent("Lineas (4-40)", 4, 40,
                                         CFG["lineas"])
            elif k == 5:
                CFG["ancho"] = leer_ent("Ancho (20-60)", 20, 60, CFG["ancho"])
            elif k == 6:
                CFG["gfxin"] = 1 - CFG["gfxin"]
            elif k == 7:
                CFG["grid"] = leer_num("Paso", CFG["grid"], 1e-6)
            elif k == 8:
                p("Ejecutando pruebas...")
                try:
                    ok, f, log = correr()
                except NameError:
                    p("Autopruebas no incluidas en esta version (lite).")
                    p("Use EngTest.py.")
                    continue
                mostrar(["Correctas: " + str(ok), "Fallidas: " + str(f)] +
                        log, "Autopruebas")
            elif k == 9:
                mostrar(["ENGINEERING SOLVER v" + VERSION,
                         "Estatica 2D paso a paso para TI-Nspire CX II.",
                         "Motor propio: vectores, Gauss con pivoteo," +
                         " deteccion de singularidad.",
                         "Convencion: angulos desde +x antihorario," +
                         " momentos + antihorarios."], "Acerca de")
        except Cancelar:
            pass

# ---- main ----
def principal():
    limpiar()
    p("ENGINEERING SOLVER v" + VERSION)
    p("Estatica paso a paso - TI-Nspire CX II")
    while True:
        k = menu("MENU PRINCIPAL", ["ESTATICA",
                                    "DINAMICA  [bloqueado: futuro]",
                                    "HERRAMIENTAS MATEMATICAS",
                                    "CONFIGURACION"], "Salir")
        try:
            if k == 0:
                p("Hasta luego.")
                return
            elif k == 1:
                menu_estatica()
            elif k == 2:
                mostrar(["El modulo de Dinamica estara disponible en" +
                         " una version futura."], "DINAMICA")
            elif k == 3:
                menu_herramientas()
            elif k == 4:
                menu_config()
        except Cancelar:
            pass
        except MemoryError:
            p("Memoria insuficiente. Simplifique el problema.")
        except KeyboardInterrupt:
            p("Interrumpido.")
            return
principal()
