# Engineering Solver - ejemplos.py
# Problemas de referencia con solucion conocida (resuelta a mano).
# Se usan como ejemplos cargables y como casos de prueba.

from elementos import *


def ej_viga_simple():
    """Viga simplemente apoyada L=6 m, carga 1200 N hacia abajo a 2 m.
    Solucion: Ax=0, Ay=800 N, By=400 N."""
    m = Modelo("rigido", "Viga simple")
    m.nuevo_nodo(0, 0)
    m.nuevo_nodo(2, 0)
    m.nuevo_nodo(6, 0)
    m.add_miembro("viga", "A", "B")
    m.add_miembro("viga", "B", "C")
    m.add_apoyo("pin", "A")
    m.add_apoyo("rod", "C", 90)
    m.add_fuerza_pol("B", 1200, 270)
    return m, {"Ax": 0.0, "Ay": 800.0, "Cy": 400.0}


def ej_fuerza_inclinada():
    """Viga L=5 m, pasador A, rodillo B; F=500 N a 240 grados en x=3.
    Fx=-250, Fy=-433.013. Ax=250, By=3(433.013)/5=259.808,
    Ay=433.013-259.808=173.205."""
    m = Modelo("rigido", "Fuerza inclinada")
    m.nuevo_nodo(0, 0)
    m.nuevo_nodo(3, 0)
    m.nuevo_nodo(5, 0)
    m.add_miembro("viga", "A", "B")
    m.add_miembro("viga", "B", "C")
    m.add_apoyo("pin", "A")
    m.add_apoyo("rod", "C", 90)
    m.add_fuerza_pol("B", 500, 240)
    return m, {"Ax": 250.0, "Ay": 173.20508, "Cy": 259.80762}


def ej_voladizo():
    """Voladizo L=3 m empotrado en A, w=1 kN/m uniforme y P=2 kN en el
    extremo. Ay=5 kN, MA=2*3+3*1.5=10.5 kN*m (antihorario), Ax=0."""
    m = Modelo("rigido", "Voladizo")
    m.nuevo_nodo(0, 0)
    m.nuevo_nodo(3, 0)
    m.add_miembro("viga", "A", "B")
    m.add_apoyo("emp", "A")
    m.add_carga("A", "B", 1, 1, 270)
    m.add_fuerza_pol("B", 2, 270)
    return m, {"Ax": 0.0, "Ay": 5.0, "MA": 10.5}


def ej_particula_cables():
    """Peso de 100 lb colgado en P(0,0) de dos cables hacia A(-3,4) y
    B(4,3). uA=(-0.6,0.8), uB=(0.8,0.6) -> TPA=80 lb, TPB=60 lb."""
    m = Modelo("particula", "Particula 2 cables")
    m.nuevo_nodo(0, 0, "P")
    m.nuevo_nodo(-3, 4, "A")
    m.nuevo_nodo(4, 3, "B")
    m.add_apoyo("cab", "P", 0, "A")
    m.add_apoyo("cab", "P", 0, "B")
    m.add_fuerza_pol("P", 100, 270)
    return m, {"TPA": 80.0, "TPB": 60.0}


def ej_momento():
    """Viga L=4 m, pasador A, rodillo C, par 800 N*m antihorario en B
    (x=2). SMA: 4Cy+800=0 -> Cy=-200 N, Ay=200 N."""
    m = Modelo("rigido", "Par aplicado")
    m.nuevo_nodo(0, 0)
    m.nuevo_nodo(2, 0)
    m.nuevo_nodo(4, 0)
    m.add_miembro("viga", "A", "B")
    m.add_miembro("viga", "B", "C")
    m.add_apoyo("pin", "A")
    m.add_apoyo("rod", "C", 90)
    m.add_momento("B", 800)
    return m, {"Ax": 0.0, "Ay": 200.0, "Cy": -200.0}


def ej_pluma():
    """Pluma horizontal AB (4 m) articulada en A, cable de B a C(0,3),
    carga 2000 N en B. uBC=(-0.8,0.6): 2.4T=8000 -> T=3333.33 N,
    Ax=2666.67 N, Ay=0."""
    m = Modelo("rigido", "Pluma con cable")
    m.nuevo_nodo(0, 0)
    m.nuevo_nodo(4, 0)
    m.nuevo_nodo(0, 3)
    m.add_miembro("viga", "A", "B")
    m.add_apoyo("pin", "A")
    m.add_apoyo("cab", "B", 0, "C")
    m.add_fuerza_pol("B", 2000, 270)
    return m, {"Ax": 2666.6667, "Ay": 0.0, "TBC": 3333.3333}


def ej_triangular():
    """Viga L=6 m, carga triangular 0 -> 600 N/m. W=1800 N en x=4.
    By=1200 N, Ay=600 N."""
    m = Modelo("rigido", "Carga triangular")
    m.nuevo_nodo(0, 0)
    m.nuevo_nodo(6, 0)
    m.add_miembro("viga", "A", "B")
    m.add_apoyo("pin", "A")
    m.add_apoyo("rod", "B", 90)
    m.add_carga("A", "B", 0, 600, 270)
    return m, {"Ax": 0.0, "Ay": 600.0, "By": 1200.0}


def ej_rodillo_inclinado():
    """Pasador A(0,0); rodillo en B(4,0) sobre plano a 30 grados (normal
    a 120 grados); 1000 N abajo en x=2. N=577.350, Ax=288.675, Ay=500."""
    m = Modelo("rigido", "Rodillo inclinado")
    m.nuevo_nodo(0, 0)
    m.nuevo_nodo(2, 0)
    m.nuevo_nodo(4, 0)
    m.add_miembro("viga", "A", "B")
    m.add_miembro("viga", "B", "C")
    m.add_apoyo("pin", "A")
    m.add_apoyo("rod", "C", 120)
    m.add_fuerza_pol("B", 1000, 270)
    return m, {"Ax": 288.67513, "Ay": 500.0, "NC": 577.35027}


def ej_marco():
    """Marco en L: A(0,0) pasador, columna hasta B(0,3), viga hasta
    D(4,3) con rodillo vertical en D. Carga horizontal 600 N en B y
    1000 N hacia abajo en C(2,3).
    SMA: 4Dy - 3(600) - 2(1000) = 0 -> Dy=950, Ax=-600, Ay=50."""
    m = Modelo("rigido", "Marco en L")
    m.nuevo_nodo(0, 0)
    m.nuevo_nodo(0, 3)
    m.nuevo_nodo(2, 3)
    m.nuevo_nodo(4, 3)
    m.add_miembro("viga", "A", "B")
    m.add_miembro("viga", "B", "C")
    m.add_miembro("viga", "C", "D")
    m.add_apoyo("pin", "A")
    m.add_apoyo("rod", "D", 90)
    m.add_fuerza_comp("B", 600, 0)
    m.add_fuerza_pol("C", 1000, 270)
    return m, {"Ax": -600.0, "Ay": 50.0, "Dy": 950.0}


def ej_indeterminado():
    """Viga con dos pasadores (hiperestatica grado 1). Carga 1000 N en
    el centro. Ay=By=500 quedan determinadas; Ax, Bx no."""
    m = Modelo("rigido", "Hiperestatica")
    m.nuevo_nodo(0, 0)
    m.nuevo_nodo(2, 0)
    m.nuevo_nodo(4, 0)
    m.add_miembro("viga", "A", "B")
    m.add_miembro("viga", "B", "C")
    m.add_apoyo("pin", "A")
    m.add_apoyo("pin", "C")
    m.add_fuerza_pol("B", 1000, 270)
    return m, "indeterminado"


def ej_incompatible():
    """Dos rodillos verticales y una fuerza horizontal: no hay reaccion
    horizontal posible -> incompatible (mecanismo)."""
    m = Modelo("rigido", "Mecanismo")
    m.nuevo_nodo(0, 0)
    m.nuevo_nodo(4, 0)
    m.add_miembro("viga", "A", "B")
    m.add_apoyo("rod", "A", 90)
    m.add_apoyo("rod", "B", 90)
    m.add_fuerza_comp("B", 100, -50)
    return m, "incompatible"


EJEMPLOS = [
    ("Viga simplemente apoyada", ej_viga_simple),
    ("Fuerza inclinada", ej_fuerza_inclinada),
    ("Voladizo w + P (kN)", ej_voladizo),
    ("Particula con 2 cables", ej_particula_cables),
    ("Viga con par aplicado", ej_momento),
    ("Pluma con cable", ej_pluma),
    ("Carga triangular", ej_triangular),
    ("Rodillo inclinado", ej_rodillo_inclinado),
    ("Marco en L", ej_marco),
    ("Hiperestatica (indet.)", ej_indeterminado),
    ("Mecanismo (incompatible)", ej_incompatible),
]
