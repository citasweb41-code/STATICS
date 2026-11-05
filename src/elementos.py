# Engineering Solver - elementos.py
# Modelo del problema: nodos, miembros (vigas, barras, cuerpos),
# apoyos (articulacion, rodillo, empotramiento, cable, biela),
# cargas (fuerzas, momentos, distribuidas) y fuerzas desconocidas.

from vectores import *
from geometria import *

# Tipos de miembro
T_MIEMBRO = ["viga", "barra", "cuerpo"]
N_MIEMBRO = {"viga": "Viga", "barra": "Barra", "cuerpo": "Cuerpo rigido"}

# Tipos de apoyo
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
    """0->A, 1->B, ... 25->Z, 26->A1 ..."""
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
        self.ang = float(ang)   # rod: direccion de N; cab/bie sin ref
        self.ref = ref          # nodo hacia el que tira el cable/biela


class Fuerza:
    """Fuerza conocida. Se guarda en componentes; se recuerda el modo
    de entrada para explicar la descomposicion."""
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
        self.M = float(M)   # positivo = antihorario


class CargaD:
    """Carga distribuida lineal sobre el segmento a-b.
    w1 en a, w2 en b (por unidad de longitud), direccion 'ang'."""
    def __init__(self, nom, a, b, w1, w2, ang=270.0):
        self.nom = nom
        self.a = a
        self.b = b
        self.w1 = float(w1)
        self.w2 = float(w2)
        self.ang = float(ang)


class FDesc:
    """Fuerza desconocida aplicada en un nodo.
    modo 'dir': direccion conocida (ang), magnitud incognita.
    modo 'libre': componentes x e y incognitas."""
    def __init__(self, nom, nodo, modo="libre", ang=0.0):
        self.nom = nom
        self.nodo = nodo
        self.modo = modo
        self.ang = float(ang)


class Incog:
    """Incognita del sistema de equilibrio."""
    def __init__(self, nom, tipo, pt, u, nodo, origen, signo=None):
        self.nom = nom
        self.tipo = tipo      # 'F' fuerza escalar a lo largo de u, 'M' par
        self.pt = pt
        self.u = u
        self.nodo = nodo
        self.origen = origen
        self.signo = signo    # 'T' (traccion >= 0), 'C' (compresion >= 0)


class Conocida:
    """Carga conocida ya reducida a fuerza puntual o par."""
    def __init__(self, nom, tipo, pt, F, M, nodo, desc, fuente):
        self.nom = nom
        self.tipo = tipo      # 'F' o 'M'
        self.pt = pt
        self.F = F
        self.M = M
        self.nodo = nodo
        self.desc = desc
        self.fuente = fuente


class Modelo:
    def __init__(self, tipo="rigido", titulo="Problema"):
        self.tipo = tipo          # 'rigido' o 'particula'
        self.titulo = titulo
        self.nodos = []
        self.miembros = []
        self.apoyos = []
        self.fuerzas = []
        self.momentos = []
        self.cargas = []
        self.fdesc = []
        self.sol = None           # resultado del ultimo calculo
        self.ref = None           # punto de momentos elegido (nombre o None)
        self._k = 0

    # ---------- nodos ----------
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

    # ---------- altas ----------
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
        """Lista de (descripcion, lista, objeto) asociados a un nodo."""
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

    # ---------- direcciones ----------
    def dir_apoyo(self, a):
        """Vector unitario de la incognita de rodillo/cable/biela."""
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

    # ---------- incognitas ----------
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

    # ---------- cargas conocidas ----------
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

    # ---------- validacion ----------
    def validar(self):
        """Devuelve lista de (nivel, mensaje). nivel 'E' error, 'A' aviso."""
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
