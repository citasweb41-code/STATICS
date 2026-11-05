from config import *
from entrada import *
from interfaz import *
from herramientas import *
def principal():
    limpiar()
    p("ENGINEERING SOLVER v" + VERSION)
    p("Estatica paso a paso - TI-Nspire CX II")
    while True:
        k = menu("MENU PRINCIPAL", ["ESTATICA",
                                    "DINAMICA  [bloqueado: futuro]",
                                    "HERRAMIENTAS MATEMATICAS",
                                    "CONFIGURACION"], "Salir")
        try:
            if k == 0:
                p("Hasta luego.")
                return
            elif k == 1:
                menu_estatica()
            elif k == 2:
                mostrar(["El modulo de Dinamica estara disponible en" +
                         " una version futura."], "DINAMICA")
            elif k == 3:
                menu_herramientas()
            elif k == 4:
                menu_config()
        except Cancelar:
            pass
        except MemoryError:
            p("Memoria insuficiente. Simplifique el problema.")
        except KeyboardInterrupt:
            p("Interrumpido.")
            return
principal()
