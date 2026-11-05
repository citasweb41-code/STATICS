from config import *
from vectores import *
from geometria import *
from elementos import *
from estatica2d import *
from solucionador import *
from graficos import *
from entrada import *
from guardar import *
from ejemplos import *
from editor import *
from herramientas import *
from pruebas import *
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
