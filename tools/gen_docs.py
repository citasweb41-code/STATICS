"""Genera docs/EJERCICIOS_PASO_A_PASO.md con la salida REAL del
programa para cada ejercicio de referencia (src/ejemplos.py)."""
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "src"))
from config import CFG  # noqa: E402
from estatica2d import resolver  # noqa: E402
from solucionador import pasos  # noqa: E402
from ejemplos import EJEMPLOS  # noqa: E402

L = ["# Ejercicios resueltos: salida del programa paso a paso", "",
     "Este archivo se genera con `python tools/gen_docs.py` y contiene",
     "exactamente el texto que muestra la calculadora (opcion",
     "*Solucion PASO A PASO*). La solucion teorica de cada ejercicio",
     "esta en [EJERCICIOS.md](EJERCICIOS.md).", ""]
for i, (nom, f) in enumerate(EJEMPLOS, 1):
    m, e = f()
    CFG["uni"] = 1 if "kN" in nom else (2 if m.tipo == "particula" else 0)
    R = resolver(m)
    L.append("## %d. %s" % (i, nom))
    L.append("")
    L.append("```")
    for t, ls in pasos(m, R):
        L.append("== " + t + " ==")
        L += ls
        L.append("")
    L.append("```")
    L.append("")
CFG["uni"] = 0
open(os.path.join(RAIZ, "docs", "EJERCICIOS_PASO_A_PASO.md"), "w",
     encoding="utf-8").write("\n".join(L))
print("ok")
