# Engineering Solver - entrada.py
# Entrada/salida en el shell de Python: lectura validada de numeros
# (con expresiones), menus numerados y paginador de texto.

from config import *
from expresion import *

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
    """print con adaptacion ASCII y ajuste de ancho."""
    for l in wrap(tx(str(s))):
        print(l)


def leer(prompt):
    try:
        s = input(tx(prompt))
    except EOFError:
        raise Cancelar()
    return s.strip()


def leer_num(prompt, defecto=None, minv=None, maxv=None, cancel=True):
    """Lee un numero (admite expresiones: 500*cos(30), 3/5, sqrt(2)).
    ENTER vacio -> defecto. 'q' -> Cancelar (si cancel)."""
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
    """Lee 'x,y' (o dos preguntas si no se usa coma)."""
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
    """Lee un vector de n componentes separadas por coma."""
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
    """Muestra un menu numerado. Devuelve 1..n o 0 (volver)."""
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
    """Elige una opcion de la lista; devuelve indice 0.. (Cancelar si 0)."""
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
    """Paginador: muestra lineas en bloques de CFG['lineas'].
    Devuelve False si el usuario escribe q."""
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
    """Muestra el desarrollo paso a paso, un paso por pantalla."""
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
