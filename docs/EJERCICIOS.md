# Ejercicios de prueba resueltos

Estos son los 11 problemas de `src/ejemplos.py`, resueltos **a mano** para
validar el programa. Todos se pueden cargar en
`ESTATICA > 6 Ejemplos resueltos`, y la batería de pruebas los verifica
automáticamente. La salida completa del programa está en
[EJERCICIOS_PASO_A_PASO.md](EJERCICIOS_PASO_A_PASO.md).

Convención: ángulos desde +x en sentido antihorario y momentos positivos
antihorarios.

---

### 1. Viga simplemente apoyada
L = 6 m, articulación en A(0,0), rodillo en C(6,0), P = 1200 N hacia abajo
en B(2,0).

- ΣM_A: 6·Cy − 2·1200 = 0 → **Cy = 400 N**
- ΣFy: Ay + 400 − 1200 = 0 → **Ay = 800 N**
- ΣFx: **Ax = 0**

### 2. Fuerza inclinada
L = 5 m, articulación A(0,0), rodillo C(5,0), F = 500 N a 240° en B(3,0).
Componentes: Fx = 500·cos240° = −250 N y Fy = 500·sin240° = −433.013 N.

- ΣFx: Ax − 250 = 0 → **Ax = 250 N**
- ΣM_A: 5·Cy + 3·(−433.013) = 0 → **Cy = 259.808 N**
- ΣFy: Ay + 259.808 − 433.013 = 0 → **Ay = 173.205 N**

### 3. Voladizo (kN, m)
Empotramiento en A(0,0), L = 3 m, w = 1 kN/m uniforme y P = 2 kN en el
extremo B. La resultante de la carga es W = 3 kN, aplicada en x = 1.5 m.

- ΣFy: Ay − 3 − 2 = 0 → **Ay = 5 kN**
- ΣM_A: M_A − 3·1.5 − 2·3 = 0 → **M_A = 10.5 kN·m** (antihorario)
- **Ax = 0**

### 4. Partícula con dos cables (lb)
Peso de 100 lb en P(0,0), cables hacia A(−3,4) y B(4,3).
Vectores unitarios: u_PA = (−0.6, 0.8) y u_PB = (0.8, 0.6).

- ΣFx: −0.6·T_PA + 0.8·T_PB = 0
- ΣFy: 0.8·T_PA + 0.6·T_PB − 100 = 0
- Solución: **T_PA = 80 lb**, **T_PB = 60 lb**

### 5. Viga con par aplicado
Articulación A(0,0), rodillo C(4,0), par de 800 N·m antihorario en B(2,0).

- ΣM_A: 4·Cy + 800 = 0 → **Cy = −200 N** (actúa hacia abajo)
- ΣFy: **Ay = 200 N**; **Ax = 0**

Un par puro necesita como reacción otro par: las dos reacciones forman un
par horario de 200·4 = 800 N·m.

### 6. Pluma con cable
Pluma horizontal AB de 4 m, articulada en A(0,0), cable de B a C(0,3) y
carga de 2000 N en B. Vector unitario u_BC = (−4, 3)/5 = (−0.8, 0.6).

- ΣM_A: 4·(0.6·T) − 4·2000 = 0 → **T = 3333.333 N**
- ΣFx: Ax − 0.8·T = 0 → **Ax = 2666.667 N**
- ΣFy: Ay + 0.6·T − 2000 = 0 → **Ay = 0**

### 7. Carga triangular
Viga de 6 m con articulación en A y rodillo en B, carga de 0 a 600 N/m.
Resultante W = ½·600·6 = 1800 N, aplicada en x = 2L/3 = 4 m.

- ΣM_A: 6·By − 1800·4 = 0 → **By = 1200 N**, **Ay = 600 N**
- Momento interno: M(x) = 600x − 600x³/36, de modo que M(3) = 1350 N·m.
  También se verifica.

### 8. Rodillo sobre plano inclinado
Articulación A(0,0) y rodillo en C(4,0) sobre un plano a 30°, con la normal
N a 120°. Hay 1000 N hacia abajo en B(2,0). Dirección de N:
u = (−0.5, 0.866).

- ΣM_A: 4·(0.866·N) − 2·1000 = 0 → **N = 577.350 N**
- ΣFx: Ax − 0.5·N = 0 → **Ax = 288.675 N**
- ΣFy: Ay + 0.866·N − 1000 = 0 → **Ay = 500 N**

### 9. Marco en L
Articulación A(0,0), columna hasta B(0,3), viga hasta D(4,3) con un rodillo
vertical en D. Cargas: 600 N horizontal (+x) en B y 1000 N hacia abajo en
C(2,3).

- ΣM_A: 4·Dy − 3·600 − 2·1000 = 0 → **Dy = 950 N**
- ΣFx: **Ax = −600 N** (hacia la izquierda); ΣFy: **Ay = 50 N**

Este ejercicio comprueba el signo del momento de una fuerza horizontal
aplicada por encima del punto de referencia: −ry·Fx = −3·600.

### 10. Viga hiperestática (indeterminada)
Dos articulaciones, A(0,0) y C(4,0), con 1000 N en el centro. Hay 4
incógnitas y 3 ecuaciones, pero el rango es 3: el sistema es **indeterminado
de grado 1**. El programa informa de que **Ay = Cy = 500 N** quedan
determinadas, mientras que Ax y Cx solo cumplen Ax + Cx = 0. No inventa sus
valores: hace falta la deformación (Resistencia de Materiales).

### 11. Mecanismo (incompatible)
Dos rodillos verticales y una fuerza (100, −50). Ninguna reacción tiene
componente x, así que ΣFx: 100 = 0 es imposible. El sistema es
**incompatible**: rango(A) = 2 < rango([A|b]) = 3.

---

## Pruebas adicionales de la batería (`src/pruebas.py`)

- **Traslación**: todos los ejercicios desplazados (+7.3, −2.1) dan las
  mismas reacciones.
- **Punto de momentos**: se resuelve tomando momentos en cada nodo y en un
  punto arbitrario (3.7, −8.2), y la solución es idéntica.
- **Rotación**: la pluma girada 30°, 117° y 245° mantiene T y |R_A|.
- **Momentos**: una fuerza +y en x = +1 da un momento antihorario (+); una
  fuerza +x en y = +1 da un momento horario (−).
- **Restricciones impropias**: tres reacciones concurrentes → incompatible;
  tres rodillos paralelos → indeterminado.
- **Cable en compresión** → aviso de solución no física.
- **Partícula** con fuerza desconocida libre y con dirección conocida;
  partícula con 3 cables → indeterminada.
- **Fuerzas internas**: V y M en vigas con carga puntual, triangular y en
  voladizo, comparados con las fórmulas cerradas.
- **Guardar/cargar**: la codificación conserva los 11 ejercicios.
