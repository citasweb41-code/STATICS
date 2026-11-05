"""Verificador estatico de compatibilidad con el Python de la
TI-Nspire CX II (basado en MicroPython, sintaxis ~3.4).

Detecta construcciones que NO existen o son arriesgadas en la
calculadora: f-strings, operador morsa, async, argumentos solo-clave,
anotaciones de tipo, metodos de str ausentes en MicroPython, modulos
no disponibles y funciones de math inexistentes.

Uso: python tools/compat.py archivo.py [...]
"""
import ast
import sys

MODULOS_OK = {"math", "cmath", "random", "time", "ti_draw", "ti_system",
              "ti_plotlib", "ti_image", "ti_hub", "ti_rover"}
STR_PROHIBIDOS = {"ljust", "rjust", "center", "zfill", "title", "swapcase",
                  "casefold", "expandtabs", "format_map", "isidentifier",
                  "isprintable", "isdecimal", "isnumeric", "removeprefix",
                  "removesuffix", "maketrans", "translate"}
MATH_OK = {"sqrt", "sin", "cos", "tan", "asin", "acos", "atan", "atan2",
           "pi", "e", "log", "exp", "floor", "ceil", "fabs", "pow", "trunc",
           "fmod", "modf", "frexp", "ldexp", "isnan", "isinf", "copysign"}


def revisar(ruta, locales=()):
    src = open(ruta, encoding="utf-8").read()
    arbol = ast.parse(src, ruta)
    errores = []

    def err(n, msg):
        errores.append("%s:%d: %s" % (ruta, getattr(n, "lineno", 0), msg))

    for n in ast.walk(arbol):
        if isinstance(n, ast.JoinedStr):
            err(n, "f-string no soportada")
        elif isinstance(n, ast.NamedExpr):
            err(n, "operador := no soportado")
        elif isinstance(n, (ast.AsyncFunctionDef, ast.Await, ast.AsyncFor,
                            ast.AsyncWith)):
            err(n, "async no soportado")
        elif isinstance(n, (ast.FunctionDef, ast.Lambda)):
            a = n.args
            if a.kwonlyargs:
                err(n, "argumentos solo-clave")
            if getattr(a, "posonlyargs", []):
                err(n, "argumentos solo-posicionales")
            if isinstance(n, ast.FunctionDef):
                if n.returns is not None:
                    err(n, "anotacion de retorno")
                for x in a.args:
                    if x.annotation is not None:
                        err(n, "anotacion de tipo")
                if n.decorator_list:
                    for d in n.decorator_list:
                        if not (isinstance(d, ast.Name) and
                                d.id in ("staticmethod", "property",
                                         "classmethod")):
                            err(n, "decorador no estandar")
        elif isinstance(n, ast.AnnAssign):
            err(n, "asignacion anotada")
        elif isinstance(n, ast.Match if hasattr(ast, "Match") else ()):
            err(n, "match/case no soportado")
        elif isinstance(n, ast.Attribute):
            if n.attr in STR_PROHIBIDOS:
                err(n, "metodo ." + n.attr + "() no existe en MicroPython")
            if isinstance(n.value, ast.Name) and n.value.id == "math" and \
                    n.attr not in MATH_OK:
                err(n, "math." + n.attr + " no disponible")
        elif isinstance(n, ast.Import):
            for a in n.names:
                if a.name not in MODULOS_OK and a.name not in locales:
                    err(n, "modulo no disponible: " + a.name)
        elif isinstance(n, ast.ImportFrom):
            if n.module not in MODULOS_OK and n.module not in locales:
                err(n, "modulo no disponible: " + str(n.module))
        elif isinstance(n, ast.Call) and isinstance(n.func, ast.Name):
            if n.func.id in ("open", "exec", "compile", "__import__",
                             "breakpoint", "memoryview", "frozenset"):
                err(n, "funcion no recomendada: " + n.func.id)
    return errores


if __name__ == "__main__":
    total = []
    loc = set()
    for r in sys.argv[1:]:
        import os
        loc.add(os.path.splitext(os.path.basename(r))[0])
    for r in sys.argv[1:]:
        total += revisar(r, loc)
    for e in total:
        print(e)
    print("Compatibilidad: %d problema(s)" % len(total))
    sys.exit(1 if total else 0)
