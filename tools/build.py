"""Empaquetador: une los modulos de src/ en UN solo archivo para la
TI-Nspire CX II (dist/EngSolver.py).

- Elimina las importaciones entre modulos locales.
- Elimina comentarios y docstrings para ahorrar memoria.
- Comprueba colisiones de nombres globales entre modulos.
- Ejecuta el verificador de compatibilidad.

Uso: python tools/build.py
"""
import ast
import io
import os
import re
import sys
import tokenize

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(RAIZ, "src")
DIST = os.path.join(RAIZ, "dist")

ORDEN = ["config", "vectores", "matrices", "expresion", "geometria",
         "elementos", "estatica2d", "solucionador", "graficos", "entrada",
         "guardar", "ejemplos", "editor", "herramientas", "pruebas",
         "interfaz", "main"]

sys.path.insert(0, os.path.join(RAIZ, "tools"))
import compat  # noqa: E402


def quitar_comentarios_docstrings(src):
    arbol = ast.parse(src)
    lineas_doc = set()
    for n in ast.walk(arbol):
        if isinstance(n, (ast.Module, ast.FunctionDef, ast.ClassDef)):
            if n.body and isinstance(n.body[0], ast.Expr) and \
                    isinstance(n.body[0].value, ast.Constant) and \
                    isinstance(n.body[0].value.value, str):
                d = n.body[0]
                if len(n.body) == 1:
                    continue  # no dejar el cuerpo vacio
                for l in range(d.lineno, d.end_lineno + 1):
                    lineas_doc.add(l)
    out = []
    toks = tokenize.generate_tokens(io.StringIO(src).readline)
    comentarios = {}
    for t in toks:
        if t.type == tokenize.COMMENT:
            comentarios[t.start[0]] = t.start[1]
    for i, l in enumerate(src.split("\n"), 1):
        if i in lineas_doc:
            continue
        if i in comentarios:
            l = l[:comentarios[i]].rstrip()
        if l.strip() == "":
            continue
        out.append(l.rstrip())
    return "\n".join(out) + "\n"


def nombres_globales(src):
    arbol = ast.parse(src)
    s = set()
    for n in arbol.body:
        if isinstance(n, (ast.FunctionDef, ast.ClassDef)):
            s.add(n.name)
        elif isinstance(n, ast.Assign):
            for t in n.targets:
                if isinstance(t, ast.Name):
                    s.add(t.id)
    return s


def construir(min_=True, orden=None, nombre="EngSolver.py", pie=""):
    if orden is None:
        orden = ORDEN
    patron = re.compile(r"^(from\s+(%s)\s+import\s+.*|import\s+(%s))\s*$" % (
        "|".join(ORDEN), "|".join(ORDEN)))
    partes = []
    vistos = {}
    problemas = []
    for mod in orden:
        src = open(os.path.join(SRC, mod + ".py"), encoding="utf-8").read()
        for nm in nombres_globales(src):
            if nm in vistos and nm not in ("PI",):
                problemas.append("Nombre global repetido '%s' en %s y %s" %
                                 (nm, vistos[nm], mod))
            vistos[nm] = mod
        lineas = []
        for l in src.split("\n"):
            if patron.match(l):
                continue
            if re.match(r"^\s+(from|import)\s+(%s)\b" % "|".join(ORDEN), l):
                problemas.append("Import local anidado en " + mod + ": " + l)
            lineas.append(l)
        cuerpo = "\n".join(lineas)
        if min_:
            cuerpo = quitar_comentarios_docstrings(cuerpo)
        partes.append("# ---- " + mod + " ----\n" + cuerpo)
    cab = ("# ENGINEERING SOLVER v1.0 - TI-Nspire CX II CAS (Python)\n"
           "# Archivo generado por tools/build.py a partir de src/.\n"
           "# Estatica 2D paso a paso. Ejecutar con ctrl+R.\n")
    final = cab + "\n".join(partes) + pie
    os.makedirs(DIST, exist_ok=True)
    ruta = os.path.join(DIST, nombre)
    with open(ruta, "w", encoding="utf-8", newline="\n") as f:
        f.write(final)
    ast.parse(final)
    errs = compat.revisar(ruta)
    return ruta, final, problemas, errs


PIE_TEST = """
def _correr_pruebas():
    print("ENGINEERING SOLVER - autopruebas")
    ok, f, log = correr()
    for l in log:
        print(l)
    print("Correctas: " + str(ok))
    print("Fallidas: " + str(f))


_correr_pruebas()
"""


def copiar_modular():
    d = os.path.join(DIST, "modular")
    os.makedirs(d, exist_ok=True)
    for mod in ORDEN:
        src = open(os.path.join(SRC, mod + ".py"), encoding="utf-8").read()
        with open(os.path.join(d, mod + ".py"), "w", encoding="utf-8",
                  newline="\n") as f:
            f.write(quitar_comentarios_docstrings(src))
    return d


if __name__ == "__main__":
    salida = []
    malos = 0
    sin_pruebas = [m for m in ORDEN if m != "pruebas"]
    motor = ["config", "vectores", "matrices", "expresion", "geometria",
             "elementos", "estatica2d", "solucionador", "guardar",
             "ejemplos", "pruebas"]
    for args in ((None, "EngSolver.py", ""),
                 (sin_pruebas, "EngSolver_lite.py", ""),
                 (motor, "EngTest.py", PIE_TEST)):
        ruta, txt, problemas, errs = construir(True, args[0], args[1],
                                               args[2])
        for p in problemas:
            print("AVISO:", p)
        for e in errs:
            print("COMPAT:", e)
        malos += len(problemas) + len(errs)
        print("Generado %s: %d lineas, %d bytes" % (
            os.path.relpath(ruta, RAIZ), txt.count("\n"),
            len(txt.encode("utf-8"))))
    d = copiar_modular()
    print("Version modular en", os.path.relpath(d, RAIZ))
    sys.exit(1 if malos else 0)
