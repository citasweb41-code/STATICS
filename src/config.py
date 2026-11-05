# Engineering Solver - config.py
# Configuracion global, formato numerico, unidades y texto.
# Compatible con MicroPython (TI-Nspire CX II): sin f-strings,
# sin str.ljust/rjust/center, sin dependencias externas.

VERSION = "1.0"

CFG = {
    "dec": 3,          # decimales mostrados
    "uni": 0,          # indice en SIS_UNI
    "ascii": 0,        # 1 = reemplazar simbolos unicode
    "lineas": 10,      # lineas por pagina en el paginador
    "ancho": 32,       # ancho de linea del shell
    "grid": 0.5,       # paso de rejilla del editor grafico
    "gfxin": 1,        # 1 = entrada numerica en pantalla grafica
    "tol": 1e-9,       # tolerancia numerica relativa
}

# (fuerza, longitud, momento, carga distribuida)
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
    """Adapta un texto al modo ASCII si esta activado."""
    if CFG["ascii"]:
        for a, b in _ASCII_MAP:
            if a in s:
                s = s.replace(a, b)
    return s


def fmt(v, d=None):
    """Formatea un numero con decimales fijos; evita '-0.000'."""
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
    """Como fmt pero con signo explicito (+/-)."""
    s = fmt(v, d)
    if s[0] != "-":
        s = "+" + s
    return s


def fmte(v):
    """Formato cientifico corto (para residuos)."""
    return "%.2e" % v


def pad(s, n):
    """Rellena con espacios a la derecha (sustituto de ljust)."""
    s = str(s)
    if len(s) < n:
        s = s + " " * (n - len(s))
    return s


def padl(s, n):
    """Rellena con espacios a la izquierda (sustituto de rjust)."""
    s = str(s)
    if len(s) < n:
        s = " " * (n - len(s)) + s
    return s


def wrap(s, w=None):
    """Divide un texto en lineas de ancho maximo w (por palabras)."""
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
