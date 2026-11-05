"""Simulador de escritorio de ti_system: teclas desde una cola.
Cada vez que el programa espera una tecla se guarda una captura."""
KEYS = []
STORE = {}
_wait = [0]


def get_key(*a):
    import ti_draw
    if ti_draw.SNAP[0] and ti_draw._st["img"] is not None:
        _wait[0] += 1
        ti_draw.snapshot()
    if KEYS:
        return KEYS.pop(0)
    return "esc"


def store_list(nombre, lista):
    STORE[nombre] = [float(v) for v in lista]


def recall_list(nombre):
    if nombre not in STORE:
        raise Exception("no existe")
    return list(STORE[nombre])
