# Ejercicios resueltos: salida del programa paso a paso

Este archivo se genera con `python tools/gen_docs.py` y contiene
exactamente el texto que muestra la calculadora (opcion
*Solucion PASO A PASO*). La solucion teorica de cada ejercicio
esta en [EJERCICIOS.md](EJERCICIOS.md).

## 1. Viga simplemente apoyada

```
== 1. Identificacion del cuerpo ==
Cuerpo: CUERPO RIGIDO 2D. Hay 3 ecuaciones de equilibrio: ΣFx=0, ΣFy=0, ΣM=0.
Convencion: x a la derecha, y hacia arriba, angulos desde +x en sentido antihorario, momentos antihorarios (+).
Puntos (m):
  A = (0.000, 0.000)
  B = (2.000, 0.000)
  C = (6.000, 0.000)
Elementos:
  Viga A-B  L=2.000 m
  Viga B-C  L=4.000 m
Apoyos:
  A: Articulacion (pasador)
    -> 2 incognitas: Rx, Ry
  C: Rodillo / apoyo simple, N a 90.0°
    -> 1 incognita: N normal a la superficie

== 2. Diagrama de cuerpo libre ==
Se aisla el cuerpo y se reemplaza cada apoyo por las reacciones que impide (fuerzas o pares).
Fuerzas que actuan sobre el cuerpo:
  F1 en (2.00,0.00) [conocida]
  Ax en A, dir 0.0° [incognita]
  Ay en A, dir 90.0° [incognita]
  Cy en C, dir 90.0° [incognita]
Sentidos de incognitas SUPUESTOS. Si el resultado sale negativo, el sentido real es el contrario.
(Menu 'Ver DCL' muestra el diagrama grafico.)

== 3. Fuerzas conocidas y desconocidas ==
CONOCIDAS:
  F1 = 1200.000 N a 270.00°
DESCONOCIDAS (3):
  Ax [N] (reaccion)
  Ay [N] (reaccion)
  Cy [N] (reaccion)
Ecuaciones disponibles: 3.
n incognitas = n ecuaciones: posible solucion unica (si las ecuaciones son independientes).

== 4. Descomposicion de fuerzas ==
Cada fuerza se expresa en componentes: Fx = F·cosθ, Fy = F·sinθ (θ desde +x).
F1: F=1200.000, θ=270.00°
  F1x = 1200.000·cos(270.00°) = 0.000
  F1y = 1200.000·sin(270.00°) = -1200.000
Ax: dirigida segun +x.
Ay: dirigida segun +y.
Cy: dirigida segun +y.

== 5. Brazos de momento ==
Momento de una fuerza respecto a A:
  M = rx·Fy - ry·Fx,  r = P - A
  brazo d = |M|/|F| (distancia perpendicular).
F1: r=(2.000,0.000)
  M = (2.000)(-1200.000) - (0.000)(0.000)
    = -2400.000 N·m (horario -)
  d = 2.000 m
Ax: r=(0.000,0.000)
  su linea de accion pasa por A: M = 0
Ay: r=(0.000,0.000)
  su linea de accion pasa por A: M = 0
Cy: r=(6.000,0.000)
  M = [(6.000)(1.0000) - (0.000)(0.0000)]·Cy
    = 6.0000·Cy
  d = 6.000 m

== 6. Punto de referencia de momentos ==
Punto elegido: A = (0.000, 0.000)
Por A pasan las lineas de accion de: Ax, Ay.
Estas incognitas NO aparecen en ΣMA, lo que simplifica la solucion.
(Puede elegir otro punto en el menu de resultados.)

== 7. Planteamiento de ΣFx = 0 ==
La suma de componentes horizontales debe anularse (no hay aceleracion en x).
Planteamiento simbolico:
  ΣFx: F1x + Ax = 0
Con valores:
  Ax = 0

== 8. Planteamiento de ΣFy = 0 ==
La suma de componentes verticales debe anularse (no hay aceleracion en y).
Planteamiento simbolico:
  ΣFy: F1y + Ay + Cy = 0
Con valores:
  Ay + Cy - 1200.000 = 0

== 9. Planteamiento de ΣMA = 0 ==
La suma de momentos respecto al punto debe anularse (no hay rotacion).
Planteamiento simbolico:
  ΣMA: M(F1) + M(Ax) + M(Ay) + M(Cy) = 0
Con valores:
  6.000·Cy - 2400.000 = 0

== 10. Sustitucion de valores ==
Se agrupan los terminos conocidos al lado derecho:
ΣFx:
  Ax = 0.000
ΣFy:
  Ay + Cy = 1200.000
ΣMA:
  6.000·Cy = 2400.000
Forma matricial [A | b] (columnas: Ax, Ay, Cy):
[    1.00     0.00     0.00 |    0.00]
[    0.00     1.00     1.00 | 1200.00]
[    0.00     0.00     6.00 | 2400.00]

== 11. Desarrollo algebraico ==
(1) De ΣFx (1 incognita):
  Ax = 0
  Ax = 0.000 N
(2) De ΣMA (1 incognita):
  6.000·Cy - 2400.000 = 0
  6.000·Cy = 2400.000
  Cy = 2400.000 / (6.000) = 400.000 N
(3) De ΣFy (1 incognita):
  Ay + (400.000) - 1200.000 = 0
  Ay = 800.000 N

== 12. Resolucion del sistema ==
Todas las incognitas se obtuvieron por sustitucion.
Clasificacion:
  Sistema estaticamente determinado (isostatico): 3 incognitas, 3 ecuaciones independientes.

== 13. Resultados ==
Ax = 0.000 N
Ay = 800.000 N
Cy = 400.000 N
Reaccion total en A:
  R = √(0.000²+800.000²) = 800.000 N
  θ = 90.00°

== 14. Comprobacion de equilibrio ==
Se sustituyen TODAS las fuerzas (conocidas + calculadas):
  ΣFx = 0.00e+00
  ΣFy = 0.00e+00
  ΣMA = 0.00e+00
  ΣMO(0,0) = 0.00e+00
  ΣMB = 0.00e+00
  ΣMC = 0.00e+00
(El momento se anula respecto a CUALQUIER punto, no solo el usado para resolver.)
EQUILIBRIO VERIFICADO (residuos ~ 0).

```

## 2. Fuerza inclinada

```
== 1. Identificacion del cuerpo ==
Cuerpo: CUERPO RIGIDO 2D. Hay 3 ecuaciones de equilibrio: ΣFx=0, ΣFy=0, ΣM=0.
Convencion: x a la derecha, y hacia arriba, angulos desde +x en sentido antihorario, momentos antihorarios (+).
Puntos (m):
  A = (0.000, 0.000)
  B = (3.000, 0.000)
  C = (5.000, 0.000)
Elementos:
  Viga A-B  L=3.000 m
  Viga B-C  L=2.000 m
Apoyos:
  A: Articulacion (pasador)
    -> 2 incognitas: Rx, Ry
  C: Rodillo / apoyo simple, N a 90.0°
    -> 1 incognita: N normal a la superficie

== 2. Diagrama de cuerpo libre ==
Se aisla el cuerpo y se reemplaza cada apoyo por las reacciones que impide (fuerzas o pares).
Fuerzas que actuan sobre el cuerpo:
  F1 en (3.00,0.00) [conocida]
  Ax en A, dir 0.0° [incognita]
  Ay en A, dir 90.0° [incognita]
  Cy en C, dir 90.0° [incognita]
Sentidos de incognitas SUPUESTOS. Si el resultado sale negativo, el sentido real es el contrario.
(Menu 'Ver DCL' muestra el diagrama grafico.)

== 3. Fuerzas conocidas y desconocidas ==
CONOCIDAS:
  F1 = 500.000 N a 240.00°
DESCONOCIDAS (3):
  Ax [N] (reaccion)
  Ay [N] (reaccion)
  Cy [N] (reaccion)
Ecuaciones disponibles: 3.
n incognitas = n ecuaciones: posible solucion unica (si las ecuaciones son independientes).

== 4. Descomposicion de fuerzas ==
Cada fuerza se expresa en componentes: Fx = F·cosθ, Fy = F·sinθ (θ desde +x).
F1: F=500.000, θ=240.00°
  F1x = 500.000·cos(240.00°) = -250.000
  F1y = 500.000·sin(240.00°) = -433.013
Ax: dirigida segun +x.
Ay: dirigida segun +y.
Cy: dirigida segun +y.

== 5. Brazos de momento ==
Momento de una fuerza respecto a A:
  M = rx·Fy - ry·Fx,  r = P - A
  brazo d = |M|/|F| (distancia perpendicular).
F1: r=(3.000,0.000)
  M = (3.000)(-433.013) - (0.000)(-250.000)
    = -1299.038 N·m (horario -)
  d = 2.598 m
Ax: r=(0.000,0.000)
  su linea de accion pasa por A: M = 0
Ay: r=(0.000,0.000)
  su linea de accion pasa por A: M = 0
Cy: r=(5.000,0.000)
  M = [(5.000)(1.0000) - (0.000)(0.0000)]·Cy
    = 5.0000·Cy
  d = 5.000 m

== 6. Punto de referencia de momentos ==
Punto elegido: A = (0.000, 0.000)
Por A pasan las lineas de accion de: Ax, Ay.
Estas incognitas NO aparecen en ΣMA, lo que simplifica la solucion.
(Puede elegir otro punto en el menu de resultados.)

== 7. Planteamiento de ΣFx = 0 ==
La suma de componentes horizontales debe anularse (no hay aceleracion en x).
Planteamiento simbolico:
  ΣFx: F1x + Ax = 0
Con valores:
  Ax - 250.000 = 0

== 8. Planteamiento de ΣFy = 0 ==
La suma de componentes verticales debe anularse (no hay aceleracion en y).
Planteamiento simbolico:
  ΣFy: F1y + Ay + Cy = 0
Con valores:
  Ay + Cy - 433.013 = 0

== 9. Planteamiento de ΣMA = 0 ==
La suma de momentos respecto al punto debe anularse (no hay rotacion).
Planteamiento simbolico:
  ΣMA: M(F1) + M(Ax) + M(Ay) + M(Cy) = 0
Con valores:
  5.000·Cy - 1299.038 = 0

== 10. Sustitucion de valores ==
Se agrupan los terminos conocidos al lado derecho:
ΣFx:
  Ax = 250.000
ΣFy:
  Ay + Cy = 433.013
ΣMA:
  5.000·Cy = 1299.038
Forma matricial [A | b] (columnas: Ax, Ay, Cy):
[    1.00     0.00     0.00 |  250.00]
[    0.00     1.00     1.00 |  433.01]
[    0.00     0.00     5.00 | 1299.04]

== 11. Desarrollo algebraico ==
(1) De ΣFx (1 incognita):
  Ax - 250.000 = 0
  Ax = 250.000 N
(2) De ΣMA (1 incognita):
  5.000·Cy - 1299.038 = 0
  5.000·Cy = 1299.038
  Cy = 1299.038 / (5.000) = 259.808 N
(3) De ΣFy (1 incognita):
  Ay + (259.808) - 433.013 = 0
  Ay = 173.205 N

== 12. Resolucion del sistema ==
Todas las incognitas se obtuvieron por sustitucion.
Clasificacion:
  Sistema estaticamente determinado (isostatico): 3 incognitas, 3 ecuaciones independientes.

== 13. Resultados ==
Ax = 250.000 N
Ay = 173.205 N
Cy = 259.808 N
Reaccion total en A:
  R = √(250.000²+173.205²) = 304.138 N
  θ = 34.72°

== 14. Comprobacion de equilibrio ==
Se sustituyen TODAS las fuerzas (conocidas + calculadas):
  ΣFx = 0.00e+00
  ΣFy = 0.00e+00
  ΣMA = -2.27e-13
  ΣMO(0,0) = -2.27e-13
  ΣMB = -1.14e-13
  ΣMC = -1.14e-13
(El momento se anula respecto a CUALQUIER punto, no solo el usado para resolver.)
EQUILIBRIO VERIFICADO (residuos ~ 0).

```

## 3. Voladizo w + P (kN)

```
== 1. Identificacion del cuerpo ==
Cuerpo: CUERPO RIGIDO 2D. Hay 3 ecuaciones de equilibrio: ΣFx=0, ΣFy=0, ΣM=0.
Convencion: x a la derecha, y hacia arriba, angulos desde +x en sentido antihorario, momentos antihorarios (+).
Puntos (m):
  A = (0.000, 0.000)
  B = (3.000, 0.000)
Elementos:
  Viga A-B  L=3.000 m
Apoyos:
  A: Empotramiento
    -> 3 incognitas: Rx, Ry, M

== 2. Diagrama de cuerpo libre ==
Se aisla el cuerpo y se reemplaza cada apoyo por las reacciones que impide (fuerzas o pares).
Fuerzas que actuan sobre el cuerpo:
  F1 en (3.00,0.00) [conocida]
  W1 en (1.50,0.00) [conocida]
  Ax en A, dir 0.0° [incognita]
  Ay en A, dir 90.0° [incognita]
  MA par en A [incognita]
Sentidos de incognitas SUPUESTOS. Si el resultado sale negativo, el sentido real es el contrario.
(Menu 'Ver DCL' muestra el diagrama grafico.)

== 3. Fuerzas conocidas y desconocidas ==
CONOCIDAS:
  F1 = 2.000 kN a 270.00°
  W1: resultante de w1
DESCONOCIDAS (3):
  Ax [kN] (reaccion)
  Ay [kN] (reaccion)
  MA [kN·m] (par de reaccion)
Ecuaciones disponibles: 3.
n incognitas = n ecuaciones: posible solucion unica (si las ecuaciones son independientes).

== 4. Descomposicion de fuerzas ==
Cada fuerza se expresa en componentes: Fx = F·cosθ, Fy = F·sinθ (θ desde +x).
F1: F=2.000, θ=270.00°
  F1x = 2.000·cos(270.00°) = 0.000
  F1y = 2.000·sin(270.00°) = -2.000
w1: carga distribuida A->B, w=1.000 a 1.000 kN/m, L=3.000 m
  Resultante = area del diagrama:
  W = (w1+w2)/2·L = (1.000+1.000)/2·3.000 = 3.000 kN
  Ubicacion (centroide) desde A:
  xc = L(w1+2w2)/(3(w1+w2)) = 1.500 m
  Punto de aplicacion: (1.500, 0.000)
  W1x = 3.000·cos(270.0°) = 0.000
  W1y = 3.000·sin(270.0°) = -3.000
Ax: dirigida segun +x.
Ay: dirigida segun +y.

== 5. Brazos de momento ==
Momento de una fuerza respecto a A:
  M = rx·Fy - ry·Fx,  r = P - A
  brazo d = |M|/|F| (distancia perpendicular).
F1: r=(3.000,0.000)
  M = (3.000)(-2.000) - (0.000)(0.000)
    = -6.000 kN·m (horario -)
  d = 3.000 m
W1: r=(1.500,0.000)
  M = (1.500)(-3.000) - (0.000)(0.000)
    = -4.500 kN·m (horario -)
  d = 1.500 m
Ax: r=(0.000,0.000)
  su linea de accion pasa por A: M = 0
Ay: r=(0.000,0.000)
  su linea de accion pasa por A: M = 0
MA: par, no depende del brazo.

== 6. Punto de referencia de momentos ==
Punto elegido: A = (0.000, 0.000)
Por A pasan las lineas de accion de: Ax, Ay.
Estas incognitas NO aparecen en ΣMA, lo que simplifica la solucion.
(Puede elegir otro punto en el menu de resultados.)

== 7. Planteamiento de ΣFx = 0 ==
La suma de componentes horizontales debe anularse (no hay aceleracion en x).
Planteamiento simbolico:
  ΣFx: F1x + W1x + Ax = 0
Con valores:
  Ax = 0

== 8. Planteamiento de ΣFy = 0 ==
La suma de componentes verticales debe anularse (no hay aceleracion en y).
Planteamiento simbolico:
  ΣFy: F1y + W1y + Ay = 0
Con valores:
  Ay - 5.000 = 0

== 9. Planteamiento de ΣMA = 0 ==
La suma de momentos respecto al punto debe anularse (no hay rotacion).
Planteamiento simbolico:
  ΣMA: M(F1) + M(W1) + M(Ax) + M(Ay) + MA = 0
Con valores:
  MA - 10.500 = 0

== 10. Sustitucion de valores ==
Se agrupan los terminos conocidos al lado derecho:
ΣFx:
  Ax = 0.000
ΣFy:
  Ay = 5.000
ΣMA:
  MA = 10.500
Forma matricial [A | b] (columnas: Ax, Ay, MA):
[    1.00     0.00     0.00 |    0.00]
[    0.00     1.00     0.00 |    5.00]
[    0.00     0.00     1.00 |   10.50]

== 11. Desarrollo algebraico ==
(1) De ΣFx (1 incognita):
  Ax = 0
  Ax = 0.000 kN
(2) De ΣFy (1 incognita):
  Ay - 5.000 = 0
  Ay = 5.000 kN
(3) De ΣMA (1 incognita):
  MA - 10.500 = 0
  MA = 10.500 kN·m

== 12. Resolucion del sistema ==
Todas las incognitas se obtuvieron por sustitucion.
Clasificacion:
  Sistema estaticamente determinado (isostatico): 3 incognitas, 3 ecuaciones independientes.

== 13. Resultados ==
Ax = 0.000 kN
Ay = 5.000 kN
MA = 10.500 kN·m
Reaccion total en A:
  R = √(0.000²+5.000²) = 5.000 kN
  θ = 90.00°

== 14. Comprobacion de equilibrio ==
Se sustituyen TODAS las fuerzas (conocidas + calculadas):
  ΣFx = 0.00e+00
  ΣFy = 0.00e+00
  ΣMA = 0.00e+00
  ΣMO(0,0) = 0.00e+00
  ΣMB = 0.00e+00
(El momento se anula respecto a CUALQUIER punto, no solo el usado para resolver.)
EQUILIBRIO VERIFICADO (residuos ~ 0).

```

## 4. Particula con 2 cables

```
== 1. Identificacion del cuerpo ==
Cuerpo: PARTICULA (fuerzas concurrentes). Solo hay 2 ecuaciones: ΣFx=0, ΣFy=0.
Convencion: x a la derecha, y hacia arriba, angulos desde +x en sentido antihorario, momentos antihorarios (+).
Puntos (ft):
  P = (0.000, 0.000)
  A = (-3.000, 4.000)
  B = (4.000, 3.000)
Apoyos:
  P: Cable / tensor hacia A
    -> 1 incognita: T (solo traccion)
  P: Cable / tensor hacia B
    -> 1 incognita: T (solo traccion)

== 2. Diagrama de cuerpo libre ==
Se aisla el cuerpo y se reemplaza cada apoyo por las reacciones que impide (fuerzas o pares).
Fuerzas que actuan sobre el cuerpo:
  F1 en (0.00,0.00) [conocida]
  TPA en P, dir 126.9° [incognita]
  TPB en P, dir 36.9° [incognita]
Sentidos de incognitas SUPUESTOS. Si el resultado sale negativo, el sentido real es el contrario.
(Menu 'Ver DCL' muestra el diagrama grafico.)

== 3. Fuerzas conocidas y desconocidas ==
CONOCIDAS:
  F1 = 100.000 lb a 270.00°
DESCONOCIDAS (2):
  TPA [lb] (reaccion)
  TPB [lb] (reaccion)
Ecuaciones disponibles: 2.
n incognitas = n ecuaciones: posible solucion unica (si las ecuaciones son independientes).

== 4. Descomposicion de fuerzas ==
Cada fuerza se expresa en componentes: Fx = F·cosθ, Fy = F·sinθ (θ desde +x).
F1: F=100.000, θ=270.00°
  F1x = 100.000·cos(270.00°) = 0.000
  F1y = 100.000·sin(270.00°) = -100.000
TPA actua de P hacia A:
  r = (-3.000, 4.000), |r| = 5.000
  u = r/|r| = (-0.6000, 0.8000)
  TPAx = -0.6000·TPA,  TPAy = 0.8000·TPA
TPB actua de P hacia B:
  r = (4.000, 3.000), |r| = 5.000
  u = r/|r| = (0.8000, 0.6000)
  TPBx = 0.8000·TPB,  TPBy = 0.6000·TPB

== 5-6. Momentos ==
En una particula todas las fuerzas son concurrentes: no producen momento respecto al punto. No se usa ΣM.

== 7. Planteamiento de ΣFx = 0 ==
La suma de componentes horizontales debe anularse (no hay aceleracion en x).
Planteamiento simbolico:
  ΣFx: F1x + TPAx + TPBx = 0
Con valores:
  -0.600·TPA + 0.800·TPB = 0

== 8. Planteamiento de ΣFy = 0 ==
La suma de componentes verticales debe anularse (no hay aceleracion en y).
Planteamiento simbolico:
  ΣFy: F1y + TPAy + TPBy = 0
Con valores:
  0.800·TPA + 0.600·TPB - 100.000 = 0

== 9. ΣM = 0 ==
No aplica a una particula.

== 10. Sustitucion de valores ==
Se agrupan los terminos conocidos al lado derecho:
ΣFx:
  -0.600·TPA + 0.800·TPB = 0.000
ΣFy:
  0.800·TPA + 0.600·TPB = 100.000
Forma matricial [A | b] (columnas: TPA, TPB):
[   -0.60     0.80 |    0.00]
[    0.80     0.60 |  100.00]

== 11. Desarrollo algebraico ==
Quedan 2 incognitas acopladas (TPA, TPB): se resuelven simultaneamente.
  -0.600·TPA + 0.800·TPB = 0.000
  0.800·TPA + 0.600·TPB = 100.000

== 12. Resolucion del sistema ==
Eliminacion de Gauss-Jordan sobre:
[   -0.60     0.80 |    0.00]
[    0.80     0.60 |  100.00]
Operaciones de fila:
  F1 <-> F2
  F1 <- F1 / (0.800)
  F2 <- F2 - (-0.600)F1
  F2 <- F2 / (1.250)
  F1 <- F1 - (0.750)F2
Matriz reducida:
[    1.00     0.00 |   80.00]
[    0.00     1.00 |   60.00]
  TPA = 80.000 lb
  TPB = 60.000 lb
Clasificacion:
  Sistema estaticamente determinado (isostatico): 2 incognitas, 2 ecuaciones independientes.

== 13. Resultados ==
TPA = 80.000 lb
   cable en traccion (correcto)
TPB = 60.000 lb
   cable en traccion (correcto)

== 14. Comprobacion de equilibrio ==
Se sustituyen TODAS las fuerzas (conocidas + calculadas):
  ΣFx = -7.11e-15
  ΣFy = 7.11e-15
EQUILIBRIO VERIFICADO (residuos ~ 0).

```

## 5. Viga con par aplicado

```
== 1. Identificacion del cuerpo ==
Cuerpo: CUERPO RIGIDO 2D. Hay 3 ecuaciones de equilibrio: ΣFx=0, ΣFy=0, ΣM=0.
Convencion: x a la derecha, y hacia arriba, angulos desde +x en sentido antihorario, momentos antihorarios (+).
Puntos (m):
  A = (0.000, 0.000)
  B = (2.000, 0.000)
  C = (4.000, 0.000)
Elementos:
  Viga A-B  L=2.000 m
  Viga B-C  L=2.000 m
Apoyos:
  A: Articulacion (pasador)
    -> 2 incognitas: Rx, Ry
  C: Rodillo / apoyo simple, N a 90.0°
    -> 1 incognita: N normal a la superficie

== 2. Diagrama de cuerpo libre ==
Se aisla el cuerpo y se reemplaza cada apoyo por las reacciones que impide (fuerzas o pares).
Fuerzas que actuan sobre el cuerpo:
  M1 = 800.000 N·m par [conocido]
  Ax en A, dir 0.0° [incognita]
  Ay en A, dir 90.0° [incognita]
  Cy en C, dir 90.0° [incognita]
Sentidos de incognitas SUPUESTOS. Si el resultado sale negativo, el sentido real es el contrario.
(Menu 'Ver DCL' muestra el diagrama grafico.)

== 3. Fuerzas conocidas y desconocidas ==
CONOCIDAS:
  M1 = 800.000 N·m (antihorario +)
DESCONOCIDAS (3):
  Ax [N] (reaccion)
  Ay [N] (reaccion)
  Cy [N] (reaccion)
Ecuaciones disponibles: 3.
n incognitas = n ecuaciones: posible solucion unica (si las ecuaciones son independientes).

== 4. Descomposicion de fuerzas ==
Cada fuerza se expresa en componentes: Fx = F·cosθ, Fy = F·sinθ (θ desde +x).
Ax: dirigida segun +x.
Ay: dirigida segun +y.
Cy: dirigida segun +y.

== 5. Brazos de momento ==
Momento de una fuerza respecto a A:
  M = rx·Fy - ry·Fx,  r = P - A
  brazo d = |M|/|F| (distancia perpendicular).
M1: par, no depende del brazo.
Ax: r=(0.000,0.000)
  su linea de accion pasa por A: M = 0
Ay: r=(0.000,0.000)
  su linea de accion pasa por A: M = 0
Cy: r=(4.000,0.000)
  M = [(4.000)(1.0000) - (0.000)(0.0000)]·Cy
    = 4.0000·Cy
  d = 4.000 m

== 6. Punto de referencia de momentos ==
Punto elegido: A = (0.000, 0.000)
Por A pasan las lineas de accion de: Ax, Ay.
Estas incognitas NO aparecen en ΣMA, lo que simplifica la solucion.
(Puede elegir otro punto en el menu de resultados.)

== 7. Planteamiento de ΣFx = 0 ==
La suma de componentes horizontales debe anularse (no hay aceleracion en x).
Planteamiento simbolico:
  ΣFx: Ax = 0
Con valores:
  Ax = 0

== 8. Planteamiento de ΣFy = 0 ==
La suma de componentes verticales debe anularse (no hay aceleracion en y).
Planteamiento simbolico:
  ΣFy: Ay + Cy = 0
Con valores:
  Ay + Cy = 0

== 9. Planteamiento de ΣMA = 0 ==
La suma de momentos respecto al punto debe anularse (no hay rotacion).
Planteamiento simbolico:
  ΣMA: M1 + M(Ax) + M(Ay) + M(Cy) = 0
Con valores:
  4.000·Cy + 800.000 = 0

== 10. Sustitucion de valores ==
Se agrupan los terminos conocidos al lado derecho:
ΣFx:
  Ax = 0.000
ΣFy:
  Ay + Cy = 0.000
ΣMA:
  4.000·Cy = -800.000
Forma matricial [A | b] (columnas: Ax, Ay, Cy):
[    1.00     0.00     0.00 |    0.00]
[    0.00     1.00     1.00 |    0.00]
[    0.00     0.00     4.00 | -800.00]

== 11. Desarrollo algebraico ==
(1) De ΣFx (1 incognita):
  Ax = 0
  Ax = 0.000 N
(2) De ΣMA (1 incognita):
  4.000·Cy + 800.000 = 0
  4.000·Cy = -800.000
  Cy = -800.000 / (4.000) = -200.000 N
(3) De ΣFy (1 incognita):
  Ay + (-200.000) = 0
  Ay = 200.000 N

== 12. Resolucion del sistema ==
Todas las incognitas se obtuvieron por sustitucion.
Clasificacion:
  Sistema estaticamente determinado (isostatico): 3 incognitas, 3 ecuaciones independientes.

== 13. Resultados ==
Ax = 0.000 N
Ay = 200.000 N
Cy = -200.000 N
   negativo: actua en sentido contrario, a 270.0°
Reaccion total en A:
  R = √(0.000²+200.000²) = 200.000 N
  θ = 90.00°
AVISO: El rodillo Cy tendria que tirar del cuerpo: si es apoyo simple se despegaria (valido solo si esta guiado).

== 14. Comprobacion de equilibrio ==
Se sustituyen TODAS las fuerzas (conocidas + calculadas):
  ΣFx = 0.00e+00
  ΣFy = 0.00e+00
  ΣMA = 0.00e+00
  ΣMO(0,0) = 0.00e+00
  ΣMB = 0.00e+00
  ΣMC = 0.00e+00
(El momento se anula respecto a CUALQUIER punto, no solo el usado para resolver.)
EQUILIBRIO VERIFICADO (residuos ~ 0).

== Avisos ==
 * El rodillo Cy tendria que tirar del cuerpo: si es apoyo simple se despegaria (valido solo si esta guiado).

```

## 6. Pluma con cable

```
== 1. Identificacion del cuerpo ==
Cuerpo: CUERPO RIGIDO 2D. Hay 3 ecuaciones de equilibrio: ΣFx=0, ΣFy=0, ΣM=0.
Convencion: x a la derecha, y hacia arriba, angulos desde +x en sentido antihorario, momentos antihorarios (+).
Puntos (m):
  A = (0.000, 0.000)
  B = (4.000, 0.000)
  C = (0.000, 3.000)
Elementos:
  Viga A-B  L=4.000 m
Apoyos:
  A: Articulacion (pasador)
    -> 2 incognitas: Rx, Ry
  B: Cable / tensor hacia C
    -> 1 incognita: T (solo traccion)

== 2. Diagrama de cuerpo libre ==
Se aisla el cuerpo y se reemplaza cada apoyo por las reacciones que impide (fuerzas o pares).
Fuerzas que actuan sobre el cuerpo:
  F1 en (4.00,0.00) [conocida]
  Ax en A, dir 0.0° [incognita]
  Ay en A, dir 90.0° [incognita]
  TBC en B, dir 143.1° [incognita]
Sentidos de incognitas SUPUESTOS. Si el resultado sale negativo, el sentido real es el contrario.
(Menu 'Ver DCL' muestra el diagrama grafico.)

== 3. Fuerzas conocidas y desconocidas ==
CONOCIDAS:
  F1 = 2000.000 N a 270.00°
DESCONOCIDAS (3):
  Ax [N] (reaccion)
  Ay [N] (reaccion)
  TBC [N] (reaccion)
Ecuaciones disponibles: 3.
n incognitas = n ecuaciones: posible solucion unica (si las ecuaciones son independientes).

== 4. Descomposicion de fuerzas ==
Cada fuerza se expresa en componentes: Fx = F·cosθ, Fy = F·sinθ (θ desde +x).
F1: F=2000.000, θ=270.00°
  F1x = 2000.000·cos(270.00°) = 0.000
  F1y = 2000.000·sin(270.00°) = -2000.000
Ax: dirigida segun +x.
Ay: dirigida segun +y.
TBC actua de B hacia C:
  r = (-4.000, 3.000), |r| = 5.000
  u = r/|r| = (-0.8000, 0.6000)
  TBCx = -0.8000·TBC,  TBCy = 0.6000·TBC

== 5. Brazos de momento ==
Momento de una fuerza respecto a A:
  M = rx·Fy - ry·Fx,  r = P - A
  brazo d = |M|/|F| (distancia perpendicular).
F1: r=(4.000,0.000)
  M = (4.000)(-2000.000) - (0.000)(0.000)
    = -8000.000 N·m (horario -)
  d = 4.000 m
Ax: r=(0.000,0.000)
  su linea de accion pasa por A: M = 0
Ay: r=(0.000,0.000)
  su linea de accion pasa por A: M = 0
TBC: r=(4.000,0.000)
  M = [(4.000)(0.6000) - (0.000)(-0.8000)]·TBC
    = 2.4000·TBC
  d = 2.400 m

== 6. Punto de referencia de momentos ==
Punto elegido: A = (0.000, 0.000)
Por A pasan las lineas de accion de: Ax, Ay.
Estas incognitas NO aparecen en ΣMA, lo que simplifica la solucion.
(Puede elegir otro punto en el menu de resultados.)

== 7. Planteamiento de ΣFx = 0 ==
La suma de componentes horizontales debe anularse (no hay aceleracion en x).
Planteamiento simbolico:
  ΣFx: F1x + Ax + TBCx = 0
Con valores:
  Ax - 0.800·TBC = 0

== 8. Planteamiento de ΣFy = 0 ==
La suma de componentes verticales debe anularse (no hay aceleracion en y).
Planteamiento simbolico:
  ΣFy: F1y + Ay + TBCy = 0
Con valores:
  Ay + 0.600·TBC - 2000.000 = 0

== 9. Planteamiento de ΣMA = 0 ==
La suma de momentos respecto al punto debe anularse (no hay rotacion).
Planteamiento simbolico:
  ΣMA: M(F1) + M(Ax) + M(Ay) + M(TBC) = 0
Con valores:
  2.400·TBC - 8000.000 = 0

== 10. Sustitucion de valores ==
Se agrupan los terminos conocidos al lado derecho:
ΣFx:
  Ax - 0.800·TBC = 0.000
ΣFy:
  Ay + 0.600·TBC = 2000.000
ΣMA:
  2.400·TBC = 8000.000
Forma matricial [A | b] (columnas: Ax, Ay, TBC):
[    1.00     0.00    -0.80 |    0.00]
[    0.00     1.00     0.60 | 2000.00]
[    0.00     0.00     2.40 | 8000.00]

== 11. Desarrollo algebraico ==
(1) De ΣMA (1 incognita):
  2.400·TBC - 8000.000 = 0
  2.400·TBC = 8000.000
  TBC = 8000.000 / (2.400) = 3333.333 N
(2) De ΣFx (1 incognita):
  Ax - 0.800(3333.333) = 0
  Ax = 2666.667 N
(3) De ΣFy (1 incognita):
  Ay + 0.600(3333.333) - 2000.000 = 0
  Ay = 0.000 N

== 12. Resolucion del sistema ==
Todas las incognitas se obtuvieron por sustitucion.
Clasificacion:
  Sistema estaticamente determinado (isostatico): 3 incognitas, 3 ecuaciones independientes.

== 13. Resultados ==
Ax = 2666.667 N
Ay = 0.000 N
TBC = 3333.333 N
   cable en traccion (correcto)
Reaccion total en A:
  R = √(2666.667²+0.000²) = 2666.667 N
  θ = 0.00°

== 14. Comprobacion de equilibrio ==
Se sustituyen TODAS las fuerzas (conocidas + calculadas):
  ΣFx = 0.00e+00
  ΣFy = 2.27e-13
  ΣMA = 9.09e-13
  ΣMO(0,0) = 9.09e-13
  ΣMB = 0.00e+00
  ΣMC = 9.09e-13
(El momento se anula respecto a CUALQUIER punto, no solo el usado para resolver.)
EQUILIBRIO VERIFICADO (residuos ~ 0).

```

## 7. Carga triangular

```
== 1. Identificacion del cuerpo ==
Cuerpo: CUERPO RIGIDO 2D. Hay 3 ecuaciones de equilibrio: ΣFx=0, ΣFy=0, ΣM=0.
Convencion: x a la derecha, y hacia arriba, angulos desde +x en sentido antihorario, momentos antihorarios (+).
Puntos (m):
  A = (0.000, 0.000)
  B = (6.000, 0.000)
Elementos:
  Viga A-B  L=6.000 m
Apoyos:
  A: Articulacion (pasador)
    -> 2 incognitas: Rx, Ry
  B: Rodillo / apoyo simple, N a 90.0°
    -> 1 incognita: N normal a la superficie

== 2. Diagrama de cuerpo libre ==
Se aisla el cuerpo y se reemplaza cada apoyo por las reacciones que impide (fuerzas o pares).
Fuerzas que actuan sobre el cuerpo:
  W1 en (4.00,0.00) [conocida]
  Ax en A, dir 0.0° [incognita]
  Ay en A, dir 90.0° [incognita]
  By en B, dir 90.0° [incognita]
Sentidos de incognitas SUPUESTOS. Si el resultado sale negativo, el sentido real es el contrario.
(Menu 'Ver DCL' muestra el diagrama grafico.)

== 3. Fuerzas conocidas y desconocidas ==
CONOCIDAS:
  W1: resultante de w1
DESCONOCIDAS (3):
  Ax [N] (reaccion)
  Ay [N] (reaccion)
  By [N] (reaccion)
Ecuaciones disponibles: 3.
n incognitas = n ecuaciones: posible solucion unica (si las ecuaciones son independientes).

== 4. Descomposicion de fuerzas ==
Cada fuerza se expresa en componentes: Fx = F·cosθ, Fy = F·sinθ (θ desde +x).
w1: carga distribuida A->B, w=0.000 a 600.000 N/m, L=6.000 m
  Resultante = area del diagrama:
  W = (w1+w2)/2·L = (0.000+600.000)/2·6.000 = 1800.000 N
  Ubicacion (centroide) desde A:
  xc = L(w1+2w2)/(3(w1+w2)) = 4.000 m
  Punto de aplicacion: (4.000, 0.000)
  W1x = 1800.000·cos(270.0°) = 0.000
  W1y = 1800.000·sin(270.0°) = -1800.000
Ax: dirigida segun +x.
Ay: dirigida segun +y.
By: dirigida segun +y.

== 5. Brazos de momento ==
Momento de una fuerza respecto a A:
  M = rx·Fy - ry·Fx,  r = P - A
  brazo d = |M|/|F| (distancia perpendicular).
W1: r=(4.000,0.000)
  M = (4.000)(-1800.000) - (0.000)(0.000)
    = -7200.000 N·m (horario -)
  d = 4.000 m
Ax: r=(0.000,0.000)
  su linea de accion pasa por A: M = 0
Ay: r=(0.000,0.000)
  su linea de accion pasa por A: M = 0
By: r=(6.000,0.000)
  M = [(6.000)(1.0000) - (0.000)(0.0000)]·By
    = 6.0000·By
  d = 6.000 m

== 6. Punto de referencia de momentos ==
Punto elegido: A = (0.000, 0.000)
Por A pasan las lineas de accion de: Ax, Ay.
Estas incognitas NO aparecen en ΣMA, lo que simplifica la solucion.
(Puede elegir otro punto en el menu de resultados.)

== 7. Planteamiento de ΣFx = 0 ==
La suma de componentes horizontales debe anularse (no hay aceleracion en x).
Planteamiento simbolico:
  ΣFx: W1x + Ax = 0
Con valores:
  Ax = 0

== 8. Planteamiento de ΣFy = 0 ==
La suma de componentes verticales debe anularse (no hay aceleracion en y).
Planteamiento simbolico:
  ΣFy: W1y + Ay + By = 0
Con valores:
  Ay + By - 1800.000 = 0

== 9. Planteamiento de ΣMA = 0 ==
La suma de momentos respecto al punto debe anularse (no hay rotacion).
Planteamiento simbolico:
  ΣMA: M(W1) + M(Ax) + M(Ay) + M(By) = 0
Con valores:
  6.000·By - 7200.000 = 0

== 10. Sustitucion de valores ==
Se agrupan los terminos conocidos al lado derecho:
ΣFx:
  Ax = 0.000
ΣFy:
  Ay + By = 1800.000
ΣMA:
  6.000·By = 7200.000
Forma matricial [A | b] (columnas: Ax, Ay, By):
[    1.00     0.00     0.00 |    0.00]
[    0.00     1.00     1.00 | 1800.00]
[    0.00     0.00     6.00 | 7200.00]

== 11. Desarrollo algebraico ==
(1) De ΣFx (1 incognita):
  Ax = 0
  Ax = 0.000 N
(2) De ΣMA (1 incognita):
  6.000·By - 7200.000 = 0
  6.000·By = 7200.000
  By = 7200.000 / (6.000) = 1200.000 N
(3) De ΣFy (1 incognita):
  Ay + (1200.000) - 1800.000 = 0
  Ay = 600.000 N

== 12. Resolucion del sistema ==
Todas las incognitas se obtuvieron por sustitucion.
Clasificacion:
  Sistema estaticamente determinado (isostatico): 3 incognitas, 3 ecuaciones independientes.

== 13. Resultados ==
Ax = 0.000 N
Ay = 600.000 N
By = 1200.000 N
Reaccion total en A:
  R = √(0.000²+600.000²) = 600.000 N
  θ = 90.00°

== 14. Comprobacion de equilibrio ==
Se sustituyen TODAS las fuerzas (conocidas + calculadas):
  ΣFx = 0.00e+00
  ΣFy = 0.00e+00
  ΣMA = 0.00e+00
  ΣMO(0,0) = 0.00e+00
  ΣMB = 0.00e+00
(El momento se anula respecto a CUALQUIER punto, no solo el usado para resolver.)
EQUILIBRIO VERIFICADO (residuos ~ 0).

```

## 8. Rodillo inclinado

```
== 1. Identificacion del cuerpo ==
Cuerpo: CUERPO RIGIDO 2D. Hay 3 ecuaciones de equilibrio: ΣFx=0, ΣFy=0, ΣM=0.
Convencion: x a la derecha, y hacia arriba, angulos desde +x en sentido antihorario, momentos antihorarios (+).
Puntos (m):
  A = (0.000, 0.000)
  B = (2.000, 0.000)
  C = (4.000, 0.000)
Elementos:
  Viga A-B  L=2.000 m
  Viga B-C  L=2.000 m
Apoyos:
  A: Articulacion (pasador)
    -> 2 incognitas: Rx, Ry
  C: Rodillo / apoyo simple, N a 120.0°
    -> 1 incognita: N normal a la superficie

== 2. Diagrama de cuerpo libre ==
Se aisla el cuerpo y se reemplaza cada apoyo por las reacciones que impide (fuerzas o pares).
Fuerzas que actuan sobre el cuerpo:
  F1 en (2.00,0.00) [conocida]
  Ax en A, dir 0.0° [incognita]
  Ay en A, dir 90.0° [incognita]
  NC en C, dir 120.0° [incognita]
Sentidos de incognitas SUPUESTOS. Si el resultado sale negativo, el sentido real es el contrario.
(Menu 'Ver DCL' muestra el diagrama grafico.)

== 3. Fuerzas conocidas y desconocidas ==
CONOCIDAS:
  F1 = 1000.000 N a 270.00°
DESCONOCIDAS (3):
  Ax [N] (reaccion)
  Ay [N] (reaccion)
  NC [N] (reaccion)
Ecuaciones disponibles: 3.
n incognitas = n ecuaciones: posible solucion unica (si las ecuaciones son independientes).

== 4. Descomposicion de fuerzas ==
Cada fuerza se expresa en componentes: Fx = F·cosθ, Fy = F·sinθ (θ desde +x).
F1: F=1000.000, θ=270.00°
  F1x = 1000.000·cos(270.00°) = 0.000
  F1y = 1000.000·sin(270.00°) = -1000.000
Ax: dirigida segun +x.
Ay: dirigida segun +y.
NC inclinada a 120.00°:
  NCx = NC·cos(120.00°) = -0.5000·NC
  NCy = NC·sin(120.00°) = 0.8660·NC

== 5. Brazos de momento ==
Momento de una fuerza respecto a A:
  M = rx·Fy - ry·Fx,  r = P - A
  brazo d = |M|/|F| (distancia perpendicular).
F1: r=(2.000,0.000)
  M = (2.000)(-1000.000) - (0.000)(0.000)
    = -2000.000 N·m (horario -)
  d = 2.000 m
Ax: r=(0.000,0.000)
  su linea de accion pasa por A: M = 0
Ay: r=(0.000,0.000)
  su linea de accion pasa por A: M = 0
NC: r=(4.000,0.000)
  M = [(4.000)(0.8660) - (0.000)(-0.5000)]·NC
    = 3.4641·NC
  d = 3.464 m

== 6. Punto de referencia de momentos ==
Punto elegido: A = (0.000, 0.000)
Por A pasan las lineas de accion de: Ax, Ay.
Estas incognitas NO aparecen en ΣMA, lo que simplifica la solucion.
(Puede elegir otro punto en el menu de resultados.)

== 7. Planteamiento de ΣFx = 0 ==
La suma de componentes horizontales debe anularse (no hay aceleracion en x).
Planteamiento simbolico:
  ΣFx: F1x + Ax + NCx = 0
Con valores:
  Ax - 0.500·NC = 0

== 8. Planteamiento de ΣFy = 0 ==
La suma de componentes verticales debe anularse (no hay aceleracion en y).
Planteamiento simbolico:
  ΣFy: F1y + Ay + NCy = 0
Con valores:
  Ay + 0.866·NC - 1000.000 = 0

== 9. Planteamiento de ΣMA = 0 ==
La suma de momentos respecto al punto debe anularse (no hay rotacion).
Planteamiento simbolico:
  ΣMA: M(F1) + M(Ax) + M(Ay) + M(NC) = 0
Con valores:
  3.464·NC - 2000.000 = 0

== 10. Sustitucion de valores ==
Se agrupan los terminos conocidos al lado derecho:
ΣFx:
  Ax - 0.500·NC = 0.000
ΣFy:
  Ay + 0.866·NC = 1000.000
ΣMA:
  3.464·NC = 2000.000
Forma matricial [A | b] (columnas: Ax, Ay, NC):
[    1.00     0.00    -0.50 |    0.00]
[    0.00     1.00     0.87 | 1000.00]
[    0.00     0.00     3.46 | 2000.00]

== 11. Desarrollo algebraico ==
(1) De ΣMA (1 incognita):
  3.464·NC - 2000.000 = 0
  3.464·NC = 2000.000
  NC = 2000.000 / (3.464) = 577.350 N
(2) De ΣFx (1 incognita):
  Ax - 0.500(577.350) = 0
  Ax = 288.675 N
(3) De ΣFy (1 incognita):
  Ay + 0.866(577.350) - 1000.000 = 0
  Ay = 500.000 N

== 12. Resolucion del sistema ==
Todas las incognitas se obtuvieron por sustitucion.
Clasificacion:
  Sistema estaticamente determinado (isostatico): 3 incognitas, 3 ecuaciones independientes.

== 13. Resultados ==
Ax = 288.675 N
Ay = 500.000 N
NC = 577.350 N
Reaccion total en A:
  R = √(288.675²+500.000²) = 577.350 N
  θ = 60.00°

== 14. Comprobacion de equilibrio ==
Se sustituyen TODAS las fuerzas (conocidas + calculadas):
  ΣFx = 0.00e+00
  ΣFy = 0.00e+00
  ΣMA = 0.00e+00
  ΣMO(0,0) = 0.00e+00
  ΣMB = 0.00e+00
  ΣMC = 0.00e+00
(El momento se anula respecto a CUALQUIER punto, no solo el usado para resolver.)
EQUILIBRIO VERIFICADO (residuos ~ 0).

```

## 9. Marco en L

```
== 1. Identificacion del cuerpo ==
Cuerpo: CUERPO RIGIDO 2D. Hay 3 ecuaciones de equilibrio: ΣFx=0, ΣFy=0, ΣM=0.
Convencion: x a la derecha, y hacia arriba, angulos desde +x en sentido antihorario, momentos antihorarios (+).
Puntos (m):
  A = (0.000, 0.000)
  B = (0.000, 3.000)
  C = (2.000, 3.000)
  D = (4.000, 3.000)
Elementos:
  Viga A-B  L=3.000 m
  Viga B-C  L=2.000 m
  Viga C-D  L=2.000 m
Apoyos:
  A: Articulacion (pasador)
    -> 2 incognitas: Rx, Ry
  D: Rodillo / apoyo simple, N a 90.0°
    -> 1 incognita: N normal a la superficie

== 2. Diagrama de cuerpo libre ==
Se aisla el cuerpo y se reemplaza cada apoyo por las reacciones que impide (fuerzas o pares).
Fuerzas que actuan sobre el cuerpo:
  F1 en (0.00,3.00) [conocida]
  F2 en (2.00,3.00) [conocida]
  Ax en A, dir 0.0° [incognita]
  Ay en A, dir 90.0° [incognita]
  Dy en D, dir 90.0° [incognita]
Sentidos de incognitas SUPUESTOS. Si el resultado sale negativo, el sentido real es el contrario.
(Menu 'Ver DCL' muestra el diagrama grafico.)

== 3. Fuerzas conocidas y desconocidas ==
CONOCIDAS:
  F1 = (600.000, 0.000) N
  F2 = 1000.000 N a 270.00°
DESCONOCIDAS (3):
  Ax [N] (reaccion)
  Ay [N] (reaccion)
  Dy [N] (reaccion)
Ecuaciones disponibles: 3.
n incognitas = n ecuaciones: posible solucion unica (si las ecuaciones son independientes).

== 4. Descomposicion de fuerzas ==
Cada fuerza se expresa en componentes: Fx = F·cosθ, Fy = F·sinθ (θ desde +x).
F1 dada en componentes: (600.000, 0.000)
F2: F=1000.000, θ=270.00°
  F2x = 1000.000·cos(270.00°) = 0.000
  F2y = 1000.000·sin(270.00°) = -1000.000
Ax: dirigida segun +x.
Ay: dirigida segun +y.
Dy: dirigida segun +y.

== 5. Brazos de momento ==
Momento de una fuerza respecto a A:
  M = rx·Fy - ry·Fx,  r = P - A
  brazo d = |M|/|F| (distancia perpendicular).
F1: r=(0.000,3.000)
  M = (0.000)(0.000) - (3.000)(600.000)
    = -1800.000 N·m (horario -)
  d = 3.000 m
F2: r=(2.000,3.000)
  M = (2.000)(-1000.000) - (3.000)(0.000)
    = -2000.000 N·m (horario -)
  d = 2.000 m
Ax: r=(0.000,0.000)
  su linea de accion pasa por A: M = 0
Ay: r=(0.000,0.000)
  su linea de accion pasa por A: M = 0
Dy: r=(4.000,3.000)
  M = [(4.000)(1.0000) - (3.000)(0.0000)]·Dy
    = 4.0000·Dy
  d = 4.000 m

== 6. Punto de referencia de momentos ==
Punto elegido: A = (0.000, 0.000)
Por A pasan las lineas de accion de: Ax, Ay.
Estas incognitas NO aparecen en ΣMA, lo que simplifica la solucion.
(Puede elegir otro punto en el menu de resultados.)

== 7. Planteamiento de ΣFx = 0 ==
La suma de componentes horizontales debe anularse (no hay aceleracion en x).
Planteamiento simbolico:
  ΣFx: F1x + F2x + Ax = 0
Con valores:
  Ax + 600.000 = 0

== 8. Planteamiento de ΣFy = 0 ==
La suma de componentes verticales debe anularse (no hay aceleracion en y).
Planteamiento simbolico:
  ΣFy: F1y + F2y + Ay + Dy = 0
Con valores:
  Ay + Dy - 1000.000 = 0

== 9. Planteamiento de ΣMA = 0 ==
La suma de momentos respecto al punto debe anularse (no hay rotacion).
Planteamiento simbolico:
  ΣMA: M(F1) + M(F2) + M(Ax) + M(Ay) + M(Dy) = 0
Con valores:
  4.000·Dy - 3800.000 = 0

== 10. Sustitucion de valores ==
Se agrupan los terminos conocidos al lado derecho:
ΣFx:
  Ax = -600.000
ΣFy:
  Ay + Dy = 1000.000
ΣMA:
  4.000·Dy = 3800.000
Forma matricial [A | b] (columnas: Ax, Ay, Dy):
[    1.00     0.00     0.00 | -600.00]
[    0.00     1.00     1.00 | 1000.00]
[    0.00     0.00     4.00 | 3800.00]

== 11. Desarrollo algebraico ==
(1) De ΣFx (1 incognita):
  Ax + 600.000 = 0
  Ax = -600.000 N
(2) De ΣMA (1 incognita):
  4.000·Dy - 3800.000 = 0
  4.000·Dy = 3800.000
  Dy = 3800.000 / (4.000) = 950.000 N
(3) De ΣFy (1 incognita):
  Ay + (950.000) - 1000.000 = 0
  Ay = 50.000 N

== 12. Resolucion del sistema ==
Todas las incognitas se obtuvieron por sustitucion.
Clasificacion:
  Sistema estaticamente determinado (isostatico): 3 incognitas, 3 ecuaciones independientes.

== 13. Resultados ==
Ax = -600.000 N
   negativo: actua en sentido contrario, a 180.0°
Ay = 50.000 N
Dy = 950.000 N
Reaccion total en A:
  R = √(-600.000²+50.000²) = 602.080 N
  θ = 175.24°

== 14. Comprobacion de equilibrio ==
Se sustituyen TODAS las fuerzas (conocidas + calculadas):
  ΣFx = 0.00e+00
  ΣFy = 0.00e+00
  ΣMA = 0.00e+00
  ΣMO(0,0) = 0.00e+00
  ΣMB = 0.00e+00
  ΣMC = 0.00e+00
(El momento se anula respecto a CUALQUIER punto, no solo el usado para resolver.)
EQUILIBRIO VERIFICADO (residuos ~ 0).

```

## 10. Hiperestatica (indet.)

```
== 1. Identificacion del cuerpo ==
Cuerpo: CUERPO RIGIDO 2D. Hay 3 ecuaciones de equilibrio: ΣFx=0, ΣFy=0, ΣM=0.
Convencion: x a la derecha, y hacia arriba, angulos desde +x en sentido antihorario, momentos antihorarios (+).
Puntos (m):
  A = (0.000, 0.000)
  B = (2.000, 0.000)
  C = (4.000, 0.000)
Elementos:
  Viga A-B  L=2.000 m
  Viga B-C  L=2.000 m
Apoyos:
  A: Articulacion (pasador)
    -> 2 incognitas: Rx, Ry
  C: Articulacion (pasador)
    -> 2 incognitas: Rx, Ry

== 2. Diagrama de cuerpo libre ==
Se aisla el cuerpo y se reemplaza cada apoyo por las reacciones que impide (fuerzas o pares).
Fuerzas que actuan sobre el cuerpo:
  F1 en (2.00,0.00) [conocida]
  Ax en A, dir 0.0° [incognita]
  Ay en A, dir 90.0° [incognita]
  Cx en C, dir 0.0° [incognita]
  Cy en C, dir 90.0° [incognita]
Sentidos de incognitas SUPUESTOS. Si el resultado sale negativo, el sentido real es el contrario.
(Menu 'Ver DCL' muestra el diagrama grafico.)

== 3. Fuerzas conocidas y desconocidas ==
CONOCIDAS:
  F1 = 1000.000 N a 270.00°
DESCONOCIDAS (4):
  Ax [N] (reaccion)
  Ay [N] (reaccion)
  Cx [N] (reaccion)
  Cy [N] (reaccion)
Ecuaciones disponibles: 3.
Mas incognitas que ecuaciones: sistema hiperestatico.

== 4. Descomposicion de fuerzas ==
Cada fuerza se expresa en componentes: Fx = F·cosθ, Fy = F·sinθ (θ desde +x).
F1: F=1000.000, θ=270.00°
  F1x = 1000.000·cos(270.00°) = 0.000
  F1y = 1000.000·sin(270.00°) = -1000.000
Ax: dirigida segun +x.
Ay: dirigida segun +y.
Cx: dirigida segun +x.
Cy: dirigida segun +y.

== 5. Brazos de momento ==
Momento de una fuerza respecto a A:
  M = rx·Fy - ry·Fx,  r = P - A
  brazo d = |M|/|F| (distancia perpendicular).
F1: r=(2.000,0.000)
  M = (2.000)(-1000.000) - (0.000)(0.000)
    = -2000.000 N·m (horario -)
  d = 2.000 m
Ax: r=(0.000,0.000)
  su linea de accion pasa por A: M = 0
Ay: r=(0.000,0.000)
  su linea de accion pasa por A: M = 0
Cx: r=(4.000,0.000)
  su linea de accion pasa por A: M = 0
Cy: r=(4.000,0.000)
  M = [(4.000)(1.0000) - (0.000)(0.0000)]·Cy
    = 4.0000·Cy
  d = 4.000 m

== 6. Punto de referencia de momentos ==
Punto elegido: A = (0.000, 0.000)
Por A pasan las lineas de accion de: Ax, Ay, Cx.
Estas incognitas NO aparecen en ΣMA, lo que simplifica la solucion.
(Puede elegir otro punto en el menu de resultados.)

== 7. Planteamiento de ΣFx = 0 ==
La suma de componentes horizontales debe anularse (no hay aceleracion en x).
Planteamiento simbolico:
  ΣFx: F1x + Ax + Cx = 0
Con valores:
  Ax + Cx = 0

== 8. Planteamiento de ΣFy = 0 ==
La suma de componentes verticales debe anularse (no hay aceleracion en y).
Planteamiento simbolico:
  ΣFy: F1y + Ay + Cy = 0
Con valores:
  Ay + Cy - 1000.000 = 0

== 9. Planteamiento de ΣMA = 0 ==
La suma de momentos respecto al punto debe anularse (no hay rotacion).
Planteamiento simbolico:
  ΣMA: M(F1) + M(Ax) + M(Ay) + M(Cx) + M(Cy) = 0
Con valores:
  4.000·Cy - 2000.000 = 0

== 10. Sustitucion de valores ==
Se agrupan los terminos conocidos al lado derecho:
ΣFx:
  Ax + Cx = 0.000
ΣFy:
  Ay + Cy = 1000.000
ΣMA:
  4.000·Cy = 2000.000
Forma matricial [A | b] (columnas: Ax, Ay, Cx, Cy):
[    1.00     0.00     1.00     0.00 |    0.00]
[    0.00     1.00     0.00     1.00 | 1000.00]
[    0.00     0.00     0.00     4.00 | 2000.00]

== 11. Desarrollo algebraico ==
(1) De ΣMA (1 incognita):
  4.000·Cy - 2000.000 = 0
  4.000·Cy = 2000.000
  Cy = 2000.000 / (4.000) = 500.000 N
(2) De ΣFy (1 incognita):
  Ay + (500.000) - 1000.000 = 0
  Ay = 500.000 N

== 12. Resolucion del sistema ==
Analisis de rango (Gauss) del sistema completo:
  Col Cx: sin pivote (0)
  F3 <- F3 / (4.000)
  F2 <- F2 - (1.000)F3
[    1.00     0.00     1.00     0.00 |    0.00]
[    0.00     1.00     0.00     0.00 |  500.00]
[    0.00     0.00     0.00     1.00 |  500.00]
rango(A) = 3, rango([A|b]) = 3, incognitas = 4
rango(A) < n -> INFINITAS SOLUCIONES.
Clasificacion:
  Sistema estaticamente INDETERMINADO: 4 incognitas y solo 3 ecuaciones independientes. Grado de indeterminacion = 1.
  La estatica no da solucion unica: se requieren ecuaciones de deformacion (Resistencia de Materiales). No se inventa una solucion.
  Aun asi quedan determinadas: Ay, Cy.

== 13. Resultados ==
No hay solucion unica.
 * Sistema estaticamente INDETERMINADO: 4 incognitas y solo 3 ecuaciones independientes. Grado de indeterminacion = 1.
 * La estatica no da solucion unica: se requieren ecuaciones de deformacion (Resistencia de Materiales). No se inventa una solucion.
 * Aun asi quedan determinadas: Ay, Cy.
Valores determinados:
  Ay = 500.000
  Cy = 500.000

== 14. Comprobacion de equilibrio ==
No aplica: no hay solucion unica.

```

## 11. Mecanismo (incompatible)

```
== 1. Identificacion del cuerpo ==
Cuerpo: CUERPO RIGIDO 2D. Hay 3 ecuaciones de equilibrio: ΣFx=0, ΣFy=0, ΣM=0.
Convencion: x a la derecha, y hacia arriba, angulos desde +x en sentido antihorario, momentos antihorarios (+).
Puntos (m):
  A = (0.000, 0.000)
  B = (4.000, 0.000)
Elementos:
  Viga A-B  L=4.000 m
Apoyos:
  A: Rodillo / apoyo simple, N a 90.0°
    -> 1 incognita: N normal a la superficie
  B: Rodillo / apoyo simple, N a 90.0°
    -> 1 incognita: N normal a la superficie

== 2. Diagrama de cuerpo libre ==
Se aisla el cuerpo y se reemplaza cada apoyo por las reacciones que impide (fuerzas o pares).
Fuerzas que actuan sobre el cuerpo:
  F1 en (4.00,0.00) [conocida]
  Ay en A, dir 90.0° [incognita]
  By en B, dir 90.0° [incognita]
Sentidos de incognitas SUPUESTOS. Si el resultado sale negativo, el sentido real es el contrario.
(Menu 'Ver DCL' muestra el diagrama grafico.)

== 3. Fuerzas conocidas y desconocidas ==
CONOCIDAS:
  F1 = (100.000, -50.000) N
DESCONOCIDAS (2):
  Ay [N] (reaccion)
  By [N] (reaccion)
Ecuaciones disponibles: 3.
Menos incognitas que ecuaciones: solo hay equilibrio si las cargas lo permiten.

== 4. Descomposicion de fuerzas ==
Cada fuerza se expresa en componentes: Fx = F·cosθ, Fy = F·sinθ (θ desde +x).
F1 dada en componentes: (100.000, -50.000)
Ay: dirigida segun +y.
By: dirigida segun +y.

== 5. Brazos de momento ==
Momento de una fuerza respecto a A:
  M = rx·Fy - ry·Fx,  r = P - A
  brazo d = |M|/|F| (distancia perpendicular).
F1: r=(4.000,0.000)
  M = (4.000)(-50.000) - (0.000)(100.000)
    = -200.000 N·m (horario -)
  d = 1.789 m
Ay: r=(0.000,0.000)
  su linea de accion pasa por A: M = 0
By: r=(4.000,0.000)
  M = [(4.000)(1.0000) - (0.000)(0.0000)]·By
    = 4.0000·By
  d = 4.000 m

== 6. Punto de referencia de momentos ==
Punto elegido: A = (0.000, 0.000)
Por A pasan las lineas de accion de: Ay.
Estas incognitas NO aparecen en ΣMA, lo que simplifica la solucion.
(Puede elegir otro punto en el menu de resultados.)

== 7. Planteamiento de ΣFx = 0 ==
La suma de componentes horizontales debe anularse (no hay aceleracion en x).
Planteamiento simbolico:
  ΣFx: F1x = 0
Con valores:
  100.000 = 0

== 8. Planteamiento de ΣFy = 0 ==
La suma de componentes verticales debe anularse (no hay aceleracion en y).
Planteamiento simbolico:
  ΣFy: F1y + Ay + By = 0
Con valores:
  Ay + By - 50.000 = 0

== 9. Planteamiento de ΣMA = 0 ==
La suma de momentos respecto al punto debe anularse (no hay rotacion).
Planteamiento simbolico:
  ΣMA: M(F1) + M(Ay) + M(By) = 0
Con valores:
  4.000·By - 200.000 = 0

== 10. Sustitucion de valores ==
Se agrupan los terminos conocidos al lado derecho:
ΣFx:
  0 = -100.000
ΣFy:
  Ay + By = 50.000
ΣMA:
  4.000·By = 200.000
Forma matricial [A | b] (columnas: Ay, By):
[    0.00     0.00 | -100.00]
[    1.00     1.00 |   50.00]
[    0.00     4.00 |  200.00]

== 11. Desarrollo algebraico ==
(1) De ΣMA (1 incognita):
  4.000·By - 200.000 = 0
  4.000·By = 200.000
  By = 200.000 / (4.000) = 50.000 N
(2) De ΣFy (1 incognita):
  Ay + (50.000) - 50.000 = 0
  Ay = 0.000 N
Ecuacion ΣFx con los valores hallados:
  100.000 = 0
  -> 100.000 = 0  CONTRADICCION: esta ecuacion no puede cumplirse.

== 12. Resolucion del sistema ==
Las incognitas se despejaron, pero el sistema no se cumple completo (ver paso 11).
Clasificacion:
  Sistema INCOMPATIBLE: ninguna combinacion de reacciones equilibra las cargas.
  Causa probable: restricciones impropias (todas las reacciones son paralelas o concurren en un punto) o apoyos insuficientes: el cuerpo es un mecanismo.

== 13. Resultados ==
No hay solucion unica.
 * Sistema INCOMPATIBLE: ninguna combinacion de reacciones equilibra las cargas.
 * Causa probable: restricciones impropias (todas las reacciones son paralelas o concurren en un punto) o apoyos insuficientes: el cuerpo es un mecanismo.

== 14. Comprobacion de equilibrio ==
No aplica: no hay solucion unica.

```
