from config import *
from vectores import *
from geometria import *
from elementos import *
from graficos import *
from entrada import *
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
