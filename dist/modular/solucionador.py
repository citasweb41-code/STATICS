import math
from config import *
from vectores import *
from geometria import *
from matrices import *
from elementos import *
from estatica2d import *
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
