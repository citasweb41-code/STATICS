"""Pruebas en PC del archivo empaquetado dist/EngSolver.py.

1) Ejecuta la bateria matematica (pruebas.correr).
2) Simula sesiones completas de un estudiante (entradas de teclado y
   teclas del editor grafico) usando los simuladores tools/mock/ti_*.py.
   Falla si aparece cualquier excepcion o mensaje 'Error:'.
3) Guarda capturas PNG de las pantallas graficas en docs/capturas/.

Uso: python tools/build.py && python tools/test_pc.py
"""
import builtins
import io
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "tools", "mock"))
os.environ.setdefault("TIDRAW_OUT", os.path.join(RAIZ, "docs", "capturas"))
import ti_draw  # noqa: E402  (simulador)
import ti_system  # noqa: E402

APP = os.path.join(RAIZ, "dist", "EngSolver.py")


class FinGuion(BaseException):
    pass


def sesion(nombre, entradas, teclas=(), capturas=False):
    entradas = list(entradas)
    ti_system.KEYS[:] = list(teclas)
    ti_draw.SNAP[0] = capturas
    ti_draw._st["n"] = 0
    ti_draw.PREF[0] = nombre.lower().replace(" ", "_")
    out = io.StringIO()
    viejo_in = builtins.input
    viejo_out = sys.stdout
    usadas = [0]

    def fake_input(prompt=""):
        out.write(prompt)
        if "ENTER" in prompt:   # paginador: avanzar automaticamente
            out.write("\n")
            return ""
        if not entradas:
            raise FinGuion()
        v = entradas.pop(0)
        usadas[0] += 1
        out.write(v + "\n")
        return v

    builtins.input = fake_input
    sys.stdout = out
    err = None
    try:
        code = compile(open(APP, encoding="utf-8").read(), APP, "exec")
        exec(code, {"__name__": "__main__"})
    except FinGuion:
        err = "el guion termino antes de salir (" + str(usadas[0]) + \
            " entradas usadas)"
    except BaseException as e:  # noqa
        import traceback
        err = traceback.format_exc()
    finally:
        builtins.input = viejo_in
        sys.stdout = viejo_out
    txt = out.getvalue()
    if err is None and "Error:" in txt:
        i = txt.index("Error:")
        err = "mensaje de error: " + txt[max(0, i - 300):i + 200]
    if err is None and ti_system.KEYS:
        err = "teclas sin consumir: " + str(ti_system.KEYS)
    estado = "OK " if err is None else "FALLO"
    print(estado, nombre)
    if err:
        print(err)
    return txt, err is None


def main():
    ok = True
    # 1) bateria matematica sobre el motor empaquetado
    sys.path.insert(0, os.path.join(RAIZ, "src"))
    import pruebas
    c, f, log = pruebas.correr()
    print("Bateria matematica: %d correctas, %d fallidas" % (c, f))
    for l in log:
        print("  ", l)
    ok = ok and f == 0

    # 2) sesion: asistente de viga + paso a paso + DCL + internas + V/M
    txt, r = sesion("Asistente de viga", [
        "1", "5", "1",            # ESTATICA > Vigas > asistente
        "6",                      # L
        "1", "0",                 # articulacion en x=0
        "2", "6", "",             # rodillo en x=6, N a 90
        "0",                      # terminar apoyos
        "1", "2", "1200", "",     # fuerza 1200 en x=2, 270 grados
        "2", "2", "6", "300", "",  # carga distribuida 300 N/m de 2 a 6
        "3", "4", "-500",         # par horario 500 en x=4
        "0",                      # terminar cargas
        "2",                      # paso a paso
        "3",                      # DCL
        "4", "A",                 # momento respecto a A
        "5", "C",                 # cambiar punto de momentos
        "6", "3",                 # internas en x=3
        "7",                      # diagramas V y M
        "0", "0", "0", "0"], ["esc", "esc"], True)
    ok = ok and r
    assert "Ay = " in txt and "14. Comprobacion" in txt
    # Ay: SMA = 6By - 1200*2 - 1200*4 - 500 = 0 -> By=1283.333
    ok = ok and ("By = 1283.333" in txt or "Cy = 1283.333" in txt or
                 "1283.333" in txt)

    # 3) sesion: editor grafico (dibujo) completo
    teclas = ["enter",                       # nodo A en (0,0)
              "s", "1",                       # articulacion
              "right"] + ["right"] * 7 + [   # x = 4
              "s", "2", "enter",              # rodillo N 90 por defecto
              "left", "left", "left", "left",  # x = 2
              "f", "1", "1", "0", "0", "0", "enter", "enter",  # F 1000 a 270
              "left", "left", "left", "left",  # x = 0
              "b"] + ["right"] * 8 + ["enter", "1",  # viga A-B
              "up", "up", "m", "5", "0", "enter",   # momento en (4,1)? nodo
              "d", "1",                       # borrar ese momento
              "h", "x",                       # ayuda
              "r"]                            # resolver
    txt, r = sesion("Editor grafico", [
        "1", "1", "2",            # ESTATICA > Equilibrio 2D > dibujo
        "1", "2", "0",            # resultados: resumen, pasos, volver
        "10", "0", "0", "0"], teclas, True)
    ok = ok and r
    ok = ok and "500.000" in txt   # Ay = By = 500
    # 4) sesion: configurador por coordenadas + guardar/cargar
    txt, r = sesion("Coordenadas y guardado", [
        "1", "4", "1",            # ESTATICA > Cuerpos rigidos > coordenadas
        "1", "2", "0,0", "4,0", "0,3", "q", "1", "3", "C", "0,4", "0",
        "2", "2", "1", "A", "B", "0",
        "3", "2", "1", "A", "2", "4", "B", "1", "C", "0",
        "4", "2", "B", "1", "2000", "270", "3", "1", "1500", "270", "0",
        "5", "2", "A", "100", "0",
        "6", "2", "A", "B", "200", "", "", "0",
        "7", "0", "9",
        "10", "11", "2", "0",
        "12", "3",
        "0",
        "8", "3",                 # cargar ranura 3
        "11", "0", "0", "0", "0"], ["esc"], False)
    ok = ok and r and "TBC" in txt
    # 5) ejemplos: todos con paso a paso
    for i in range(1, 12):
        txt, r = sesion("Ejemplo " + str(i), [
            "1", "6", str(i), "n", "2", "3", "0", "0", "0", "0"],
            ["esc"])
        ok = ok and r
    # 6) particula por asistente
    txt, r = sesion("Asistente particula", [
        "1", "3", "1", "1", "-3,4", "1", "4,3", "6", "100", "0",
        "2", "0", "0", "0", "0"])
    ok = ok and r and "80.000" in txt and "60.000" in txt
    # 7) herramientas
    txt, r = sesion("Herramientas", [
        "3",
        "1", "1", "100", "30",
        "1", "3", "10", "2,3,6",
        "2", "2", "1", "100", "0", "2", "0,100",
        "3", "1", "2,0", "0,0", "1", "50", "90",
        "3", "2", "1,2,3", "4,5,6",
        "4", "2", "1,0,0", "0,1,0",
        "5", "2", "2", "2", "1", "8", "1", "-1", "1",
        "5", "2", "2", "1", "2", "3", "2", "4", "7",
        "6", "1", "3", "1", "100", "7", "1", "180", "0",
        "7", "1", "1", "1,2", "3,4", "2", "2", "1,0,0", "0,1,0",
        "4", "1", "3,4", "5", "1", "3,4", "1,0", "0",
        "0", "0"])
    ok = ok and r and "86.603" in txt and "x1 = 3.000" in txt
    # 8) configuracion + autopruebas
    txt, r = sesion("Configuracion", [
        "4", "1", "2", "2", "2", "3", "4", "12", "6", "8", "9", "3", "0",
        "0"])
    ok = ok and r and "Fallidas: 0" in txt
    # 9) entradas invalidas y cancelaciones
    txt, r = sesion("Entradas invalidas", [
        "9", "abc", "1", "5", "1", "seis", "2*3", "1", "q", "0", "0",
        "1", "1", "1", "1", "2", "2+", "q", "q", "0", "11", "0", "0", "0",
        "0", "0"])
    ok = ok and r
    print("RESULTADO GLOBAL:", "OK" if ok else "FALLO")
    return ok


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
