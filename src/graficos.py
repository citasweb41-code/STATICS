# Engineering Solver - graficos.py
# Diagramas de cuerpo libre y graficos con el modulo nativo ti_draw
# (pantalla 318 x 212, origen arriba-izquierda).
# Colores: azul = carga conocida, rojo = incognita (sentido supuesto),
# verde = reaccion calculada (sentido real), gris = geometria.

import math
from config import *
from vectores import *
from geometria import *
from elementos import *
from estatica2d import *
from expresion import *

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
TXT_H = 12       # alto aproximado de la fuente
TXT_W = 7        # ancho aproximado por caracter
BASE = 11        # draw_text usa la linea base: y_superior + BASE

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
    """Texto con esquina superior izquierda en (x, y)."""
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
    """Espera y devuelve una tecla (cadena)."""
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


# ---------------- transformacion mundo -> pantalla ----------------

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


# ---------------- primitivas de ingenieria ----------------

def flecha(x1, y1, x2, y2, c, pen="medium", estilo="solid", cab=6):
    """Flecha de (x1,y1) a (x2,y2) con punta en (x2,y2)."""
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
    """Dibuja una fuerza aplicada en pt (mundo). Por defecto la punta
    toca el punto (empuja); si tira=True la cola esta en el punto."""
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
    """Momento: arco de 270 grados con punta de flecha."""
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
    """Linea de suelo con rayado hacia 'lado' (vector unitario pantalla)."""
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
        # u en pantalla (y invertida)
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
        # muro perpendicular al primer miembro conectado
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
        # anclaje
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
    """Cotas horizontales (y verticales si hay varios niveles)."""
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
    """Dibuja el modelo completo. R: resultado (para reacciones)."""
    if not HAY_GFX:
        return None
    if V is None:
        V = Vista(puntos_vista(modelo))
    g_ini()
    if rejilla:
        _rejilla(V, rejilla)
    # miembros
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
    # nodos
    for n in modelo.nodos:
        sx, sy = V.p(n.p())
        g_color(C_NEGRO)
        g_circ(sx, sy, 2, True)
        g_texto(sx + 3, sy + 1, n.nom, C_NEGRO)
    # cargas conocidas
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
    # incognitas / reacciones
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
    """Muestra el diagrama y espera una tecla."""
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
    """Diagramas de fuerza cortante y momento flector."""
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


# ---------------- entrada en pantalla grafica ----------------

def menu_gfx(titulo, opciones):
    """Menu en pantalla grafica. Devuelve indice (0..) o -1 (esc)."""
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
    """Lee un numero en pantalla grafica usando el teclado.
    Acepta digitos, '.', '-', 'e'. ENTER acepta, ESC cancela."""
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
