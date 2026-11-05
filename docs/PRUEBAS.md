# Pruebas y validación

## Cómo ejecutarlas

| Dónde | Cómo |
|---|---|
| Calculadora | `CONFIGURACION > 8 Ejecutar autopruebas`, o el documento `EngTest` |
| PC | `python tools/build.py && python tools/test_pc.py` |

## Resultado actual

```
Bateria matematica: 218 correctas, 0 fallidas
OK  Asistente de viga
OK  Editor grafico
OK  Coordenadas y guardado
OK  Ejemplo 1 … Ejemplo 11
OK  Asistente particula
OK  Herramientas
OK  Configuracion
OK  Entradas invalidas
RESULTADO GLOBAL: OK
```

`tools/compat.py` revisa los 17 módulos y los 3 archivos de `dist/` y
encuentra **0 problemas de compatibilidad**.

## Qué se prueba

1. **Matemáticas** (`src/pruebas.py`, 218 comprobaciones): vectores,
   producto cruz, signos de momentos 2D y 3D, ángulos, proyecciones; Gauss
   con solución única, infinitas soluciones, incompatible, pivoteo, pivote
   casi nulo y sistemas sobredeterminados; rango, determinante e inversa;
   evaluador de expresiones (precedencia, potencias, trigonometría en
   grados, errores); resultantes de cargas distribuidas.
2. **Ejercicios de referencia**: 11 problemas resueltos a mano (ver
   [EJERCICIOS.md](EJERCICIOS.md)), cada uno con su comprobación de
   equilibrio y la generación del paso a paso.
3. **Invariancia**: traslación del modelo, cambio del punto de momentos (cada
   nodo y un punto arbitrario) y rotación completa del sistema.
4. **Detección**: geometría inválida, partícula no concurrente, signos
   mixtos en cargas, restricciones concurrentes o paralelas, cable en
   compresión e hiperestaticidad.
5. **Fuerzas internas** frente a las fórmulas cerradas (Pab/L, carga
   triangular, voladizo).
6. **Sesiones simuladas de la interfaz**: se ejecuta el archivo empaquetado
   `dist/EngSolver.py` con entradas de teclado guionizadas y los simuladores
   de `ti_draw`/`ti_system`. Se recorren el asistente de viga, el editor
   gráfico (con teclas), el configurador por coordenadas con guardado y
   carga, los 11 ejemplos, el asistente de partícula, todas las
   herramientas, la configuración con autopruebas y entradas inválidas o
   canceladas. La prueba falla ante cualquier excepción.

## Errores encontrados y corregidos durante el desarrollo

| # | Error | Corrección |
|---|---|---|
| 1 | En la sustitución se mostraba `Ax + -0.800(3333.333)` | Signos tratados por término: `Ax - 0.800(3333.333)` |
| 2 | En un sistema incompatible, el paso 11 no mostraba la ecuación imposible y el 12 decía que todo se había resuelto | Las ecuaciones sobrantes se evalúan con los valores hallados y se marca la **CONTRADICCIÓN** (ej. `ΣFx: 100 = 0`) |
| 3 | En un sistema acoplado (partícula), las ecuaciones ya resueltas por Gauss se repetían como "comprobación" | Se marcan como usadas tras Gauss |
| 4 | Una ecuación sin incógnitas se mostraba como `= -100` | Se muestra `0 = -100` |
| 5 | Etiquetas de reacciones encima de las cotas inferiores del DCL | Cotas más abajo y zona de etiquetas limitada |
| 6 | `x̄` (carácter combinado) no se muestra en la fuente de la calculadora | Sustituido por `xc` |
| 7 | El paso de dividir entre 1 era redundante (`Ax = 2666.667 / 1.000`) | Se omite cuando el coeficiente es 1 |

## Lo que no se pudo probar

Las pruebas se ejecutaron en CPython con simuladores de `ti_draw` y
`ti_system`. **No se han ejecutado en una calculadora física.** Lo que solo
puede confirmarse en el aparato está en [LIMITACIONES.md](LIMITACIONES.md).
La forma más rápida de comprobarlo es el Paso 4 de
[INSTALACION.md](INSTALACION.md).
