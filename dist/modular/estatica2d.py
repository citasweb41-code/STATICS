from config import *
from vectores import *
from geometria import *
from matrices import *
from elementos import *
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
