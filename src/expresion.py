# Engineering Solver - expresion.py
# Evaluador seguro de expresiones numericas (descenso recursivo).
# Permite escribir datos como 500*cos(30), 3/5, 2^2+1, sqrt(2)/2.
# Trigonometria en GRADOS.

import math
from vectores import *

_FUN = {
    "sin": lambda g: math.sin(rad(g)),
    "cos": lambda g: math.cos(rad(g)),
    "tan": lambda g: math.tan(rad(g)),
    "asin": lambda v: grad(math.asin(v)),
    "acos": lambda v: grad(math.acos(v)),
    "atan": lambda v: grad(math.atan(v)),
    "sqrt": math.sqrt,
    "abs": abs,
    "ln": math.log,
    "log": lambda v: math.log(v) / math.log(10.0),
    "exp": math.exp,
}
_CONST = {"pi": math.pi, "e": math.e}


class ErrorExpr(Exception):
    pass


class _Parser:
    def __init__(self, s):
        s = s.replace(" ", "").replace("−", "-").replace("**", "^")
        s = s.replace("·", "*").replace("×", "*")
        s = s.replace("π", "pi").replace("√", "sqrt")
        self.s = s.lower()
        self.i = 0

    def ver(self):
        if self.i < len(self.s):
            return self.s[self.i]
        return ""

    def tomar(self, c):
        if self.ver() == c:
            self.i += 1
            return True
        return False

    def expr(self):
        v = self.term()
        while True:
            if self.tomar("+"):
                v = v + self.term()
            elif self.tomar("-"):
                v = v - self.term()
            else:
                return v

    def term(self):
        v = self.unario()
        while True:
            if self.tomar("*"):
                v = v * self.unario()
            elif self.tomar("/"):
                d = self.unario()
                if d == 0:
                    raise ErrorExpr("division por cero")
                v = v / d
            else:
                c = self.ver()
                # multiplicacion implicita: 2pi, 3(4), 2sqrt(2)
                if c != "" and (c == "(" or c.isalpha()):
                    v = v * self.unario()
                else:
                    return v

    def unario(self):
        if self.tomar("-"):
            return -self.unario()
        if self.tomar("+"):
            return self.unario()
        return self.potencia()

    def potencia(self):
        b = self.atomo()
        if self.tomar("^"):
            e = self.unario()
            return b ** e
        return b

    def atomo(self):
        c = self.ver()
        if c == "(":
            self.i += 1
            v = self.expr()
            if not self.tomar(")"):
                raise ErrorExpr("falta ')'")
            return v
        if c.isdigit() or c == ".":
            j = self.i
            while self.i < len(self.s) and (self.s[self.i].isdigit() or
                                            self.s[self.i] == "."):
                self.i += 1
            if self.i < len(self.s) and self.s[self.i] == "e":
                k = self.i + 1
                if k < len(self.s) and self.s[k] in "+-":
                    k += 1
                if k < len(self.s) and self.s[k].isdigit():
                    self.i = k
                    while self.i < len(self.s) and self.s[self.i].isdigit():
                        self.i += 1
            try:
                return float(self.s[j:self.i])
            except Exception:
                raise ErrorExpr("numero invalido")
        if c.isalpha():
            j = self.i
            while self.i < len(self.s) and self.s[self.i].isalpha():
                self.i += 1
            nom = self.s[j:self.i]
            if nom in _FUN:
                if not self.tomar("("):
                    raise ErrorExpr("falta '(' tras " + nom)
                a = self.expr()
                if not self.tomar(")"):
                    raise ErrorExpr("falta ')'")
                try:
                    return float(_FUN[nom](a))
                except ErrorExpr:
                    raise
                except Exception:
                    raise ErrorExpr("dominio invalido en " + nom)
            if nom in _CONST:
                return _CONST[nom]
            raise ErrorExpr("desconocido: " + nom)
        raise ErrorExpr("expresion incompleta")


def evaluar(s):
    """Evalua una expresion; lanza ErrorExpr si no es valida."""
    p = _Parser(s)
    if p.s == "":
        raise ErrorExpr("vacio")
    v = p.expr()
    if p.i != len(p.s):
        raise ErrorExpr("caracter inesperado '" + p.s[p.i] + "'")
    return v
