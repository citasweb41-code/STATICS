import math
PI = math.pi
def rad(g):
    return g * PI / 180.0
def grad(r):
    return r * 180.0 / PI
def sind(g):
    return math.sin(rad(g))
def cosd(g):
    return math.cos(rad(g))
def limpia(v, eps=1e-12):
    if abs(v) < eps:
        return 0.0
    return v
def cosd_l(g):
    return limpia(cosd(g))
def sind_l(g):
    return limpia(sind(g))
def v_add(a, b):
    return tuple([a[i] + b[i] for i in range(len(a))])
def v_sub(a, b):
    return tuple([a[i] - b[i] for i in range(len(a))])
def v_esc(k, a):
    return tuple([k * a[i] for i in range(len(a))])
def v_dot(a, b):
    s = 0.0
    for i in range(len(a)):
        s += a[i] * b[i]
    return s
def v_norm(a):
    return math.sqrt(v_dot(a, a))
def v_unit(a, tol=1e-12):
    n = v_norm(a)
    if n < tol:
        return None
    return v_esc(1.0 / n, a)
def v_cross(a, b):
    a3 = to3(a)
    b3 = to3(b)
    return (a3[1] * b3[2] - a3[2] * b3[1],
            a3[2] * b3[0] - a3[0] * b3[2],
            a3[0] * b3[1] - a3[1] * b3[0])
def cruz2(a, b):
    return a[0] * b[1] - a[1] * b[0]
def to3(a):
    if len(a) >= 3:
        return (a[0], a[1], a[2])
    return (a[0], a[1], 0.0)
def v_sum(lista):
    if not lista:
        return (0.0, 0.0)
    s = [0.0] * len(lista[0])
    for v in lista:
        for i in range(len(v)):
            s[i] += v[i]
    return tuple(s)
def polar(mag, ang_g):
    return (limpia(mag * cosd(ang_g)), limpia(mag * sind(ang_g)))
def ang_de(v):
    a = grad(math.atan2(v[1], v[0]))
    if a < 0:
        a += 360.0
    if a >= 360.0 - 1e-10:
        a = 0.0
    return a
def ang_entre(a, b):
    na = v_norm(a)
    nb = v_norm(b)
    if na < 1e-12 or nb < 1e-12:
        return None
    c = v_dot(a, b) / (na * nb)
    if c > 1.0:
        c = 1.0
    if c < -1.0:
        c = -1.0
    return grad(math.acos(c))
def proy(a, b):
    u = v_unit(b)
    if u is None:
        return None
    s = v_dot(a, u)
    return (s, v_esc(s, u))
def momento2d(punto, ref, F):
    rx = punto[0] - ref[0]
    ry = punto[1] - ref[1]
    return rx * F[1] - ry * F[0]
def momento3d(punto, ref, F):
    r = v_sub(to3(punto), to3(ref))
    return v_cross(r, to3(F))
def dir_cosenos(v):
    n = v_norm(v)
    if n < 1e-12:
        return None
    r = []
    for c in to3(v):
        x = c / n
        if x > 1.0:
            x = 1.0
        if x < -1.0:
            x = -1.0
        r.append(grad(math.acos(x)))
    return tuple(r)
def v_str(v, f=None):
    if f is None:
        f = str
    return "(" + ", ".join([f(c) for c in v]) + ")"
