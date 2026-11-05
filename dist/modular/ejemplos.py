from elementos import *
def ej_viga_simple():
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
    m = Modelo("rigido", "Voladizo")
    m.nuevo_nodo(0, 0)
    m.nuevo_nodo(3, 0)
    m.add_miembro("viga", "A", "B")
    m.add_apoyo("emp", "A")
    m.add_carga("A", "B", 1, 1, 270)
    m.add_fuerza_pol("B", 2, 270)
    return m, {"Ax": 0.0, "Ay": 5.0, "MA": 10.5}
def ej_particula_cables():
    m = Modelo("particula", "Particula 2 cables")
    m.nuevo_nodo(0, 0, "P")
    m.nuevo_nodo(-3, 4, "A")
    m.nuevo_nodo(4, 3, "B")
    m.add_apoyo("cab", "P", 0, "A")
    m.add_apoyo("cab", "P", 0, "B")
    m.add_fuerza_pol("P", 100, 270)
    return m, {"TPA": 80.0, "TPB": 60.0}
def ej_momento():
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
    m = Modelo("rigido", "Carga triangular")
    m.nuevo_nodo(0, 0)
    m.nuevo_nodo(6, 0)
    m.add_miembro("viga", "A", "B")
    m.add_apoyo("pin", "A")
    m.add_apoyo("rod", "B", 90)
    m.add_carga("A", "B", 0, 600, 270)
    return m, {"Ax": 0.0, "Ay": 600.0, "By": 1200.0}
def ej_rodillo_inclinado():
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
