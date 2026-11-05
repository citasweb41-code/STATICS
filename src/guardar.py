# Engineering Solver - guardar.py
# Guarda/recupera problemas en variables de lista del documento .tns
# (ti_system.store_list / recall_list). El modelo se codifica como una
# lista de numeros.

from config import *
from elementos import *

try:
    from ti_system import store_list as _store, recall_list as _recall
except ImportError:
    _store = None
    _recall = None

_TA = ["pin", "rod", "emp", "cab", "bie"]
_TM = ["viga", "barra", "cuerpo"]
_MEM = {}   # respaldo en memoria si no hay ti_system


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
