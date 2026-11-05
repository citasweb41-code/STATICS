"""Simulador de escritorio de ti_draw (TI-Nspire CX II) basado en PIL.
Solo para pruebas en PC: guarda capturas PNG de la pantalla 318x212.
draw_text usa la linea base (como en la calculadora, aproximado)."""
import os
from PIL import Image, ImageDraw, ImageFont

W, H, K = 318, 212, 2
_st = {"img": None, "d": None, "col": (0, 0, 0), "w": 1, "dash": None,
       "n": 0}
OUT = os.environ.get("TIDRAW_OUT", "capturas")
SNAP = [True]
PREF = ["pantalla"]

try:
    _font = ImageFont.truetype("DejaVuSans.ttf", 11 * K)
except Exception:
    try:
        _font = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 11 * K)
    except Exception:
        _font = ImageFont.load_default()


def _ini():
    if _st["img"] is None:
        _st["img"] = Image.new("RGB", (W * K, H * K), (255, 255, 255))
        _st["d"] = ImageDraw.Draw(_st["img"])


def clear():
    _st["img"] = None
    _ini()


def set_color(r, g, b):
    _st["col"] = (int(r), int(g), int(b))


def set_pen(grosor="thin", estilo="solid"):
    _st["w"] = {"thin": 1, "medium": 2, "thick": 3}.get(grosor, 1)
    _st["dash"] = estilo if estilo in ("dashed", "dotted") else None


def _chk(*a):
    for v in a:
        if not isinstance(v, int):
            raise TypeError("ti_draw requiere enteros: %r" % (a,))


def draw_line(x1, y1, x2, y2):
    _chk(x1, y1, x2, y2)
    _ini()
    if _st["dash"]:
        import math
        L = math.hypot(x2 - x1, y2 - y1)
        seg = 5 if _st["dash"] == "dashed" else 2
        n = max(1, int(L / seg))
        for i in range(0, n, 2):
            a = i / n
            b = min(1, (i + 1) / n)
            _st["d"].line([((x1 + (x2 - x1) * a) * K, (y1 + (y2 - y1) * a) * K),
                           ((x1 + (x2 - x1) * b) * K, (y1 + (y2 - y1) * b) * K)],
                          fill=_st["col"], width=_st["w"] * K)
        return
    _st["d"].line([(x1 * K, y1 * K), (x2 * K, y2 * K)], fill=_st["col"],
                  width=_st["w"] * K)


def fill_rect(x, y, w, h):
    _chk(x, y, w, h)
    _ini()
    _st["d"].rectangle([x * K, y * K, (x + w) * K - 1, (y + h) * K - 1],
                       fill=_st["col"])


def draw_rect(x, y, w, h):
    _chk(x, y, w, h)
    _ini()
    _st["d"].rectangle([x * K, y * K, (x + w) * K - 1, (y + h) * K - 1],
                       outline=_st["col"], width=K)


def draw_circle(x, y, r):
    _chk(x, y, r)
    _ini()
    _st["d"].ellipse([(x - r) * K, (y - r) * K, (x + r) * K, (y + r) * K],
                     outline=_st["col"], width=K)


def fill_circle(x, y, r):
    _chk(x, y, r)
    _ini()
    _st["d"].ellipse([(x - r) * K, (y - r) * K, (x + r) * K, (y + r) * K],
                     fill=_st["col"])


def draw_text(x, y, s):
    _chk(x, y)
    _ini()
    _st["d"].text((x * K, y * K), str(s), fill=_st["col"], font=_font,
                  anchor="ls")


def draw_poly(xs, ys):
    _chk(*xs)
    _chk(*ys)
    _ini()
    p = [(xs[i] * K, ys[i] * K) for i in range(len(xs))]
    _st["d"].polygon(p, outline=_st["col"])


def fill_poly(xs, ys):
    _chk(*xs)
    _chk(*ys)
    _ini()
    p = [(xs[i] * K, ys[i] * K) for i in range(len(xs))]
    _st["d"].polygon(p, fill=_st["col"])


def draw_arc(x, y, w, h, a0, da):
    _ini()


def use_buffer():
    pass


def paint_buffer():
    pass


def get_screen_dim():
    return (W, H)


def snapshot(nombre=None):
    _ini()
    os.makedirs(OUT, exist_ok=True)
    _st["n"] += 1
    if nombre is None:
        nombre = "%s_%03d" % (PREF[0], _st["n"])
    p = os.path.join(OUT, nombre + ".png")
    _st["img"].save(p)
    return p
