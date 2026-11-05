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

def _correr_pruebas():
    print("ENGINEERING SOLVER - autopruebas")
    ok, f, log = correr()
    for l in log:
        print(l)
    print("Correctas: " + str(ok))
    print("Fallidas: " + str(f))


_correr_pruebas()
