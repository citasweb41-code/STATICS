# Limitaciones conocidas (v1.0)

## Por verificar en la calculadora física

La aplicación se probó en PC con simuladores de `ti_draw` y `ti_system`, no
en el aparato. Estos detalles dependen del OS y **no se han confirmado**:

1. **Nombres de teclas** de `get_key()`. El editor espera `"up"`, `"down"`,
   `"left"`, `"right"`, `"enter"`, `"esc"`, `"del"`, dígitos, letras, `"."`,
   `"-"` y `"+"`. Si el signo negativo o el punto decimal no llegan a la
   entrada gráfica, cambia `CONFIGURACION > Entrada en editor` a **shell**:
   los números se pedirán en el shell y luego se vuelve al dibujo.
2. **Métrica del texto gráfico**. Se asume que `draw_text(x, y)` coloca la
   línea base en `y`, con unos 7 px por carácter. Si el texto sale un poco
   desplazado, solo cambian las constantes `TXT_W`/`BASE` de `graficos.py`.
3. **Unicode** (Σ ° · θ √ ²). Si aparecen cuadros, activa *Símbolos ASCII*.
4. **Memoria**: el archivo completo tiene unos 160 KB de código. Si da
   `MemoryError`, usa la versión *lite* o la *modular* (ver INSTALACION).
5. **`.tns`**: no se pudo generar dentro de este entorno. Se genera con el
   workflow *Generar .tns* (Luna) o con el software de TI.

## Alcance de la versión 1.0

- **Un solo cuerpo rígido** (o una partícula) por problema. No resuelve
  armaduras por nudos ni secciones, ni bastidores o máquinas de varios
  cuerpos. Cada cuerpo se puede analizar por separado introduciendo las
  fuerzas entre piezas como fuerzas desconocidas.
- **Sin fricción**. Los rodillos son apoyos **lisos** y se tratan como
  bilaterales: si N sale negativa, el programa avisa de que el rodillo se
  despegaría.
- **Cables** idealizados: rectos, sin peso y solo a tracción. Una tensión
  negativa se señala como solución no física; no se recalcula con el cable
  flojo.
- **Cargas distribuidas** solo lineales (uniforme, triangular o trapecial),
  con la intensidad por unidad de longitud **del segmento** y dirección
  constante. w1 y w2 deben tener el mismo signo: una carga que cambia de
  signo se introduce como dos cargas.
- **Fuerzas internas y diagramas V/M** solo para **vigas horizontales**
  (todos los nodos con la misma y), usando el tramo izquierdo.
- Las **unidades** son etiquetas: no se convierten los datos al cambiar de
  sistema (para eso está la herramienta de conversión).
- **Equilibrio 3D y Dinámica** aparecen como bloqueados. Las herramientas sí
  trabajan con vectores 3D (producto cruz, momento r × F, ángulos
  directores).
- El **editor gráfico** trabaja por cursor y rejilla: el touchpad no está
  accesible desde Python. Las coordenadas que no caen en la rejilla se
  introducen con `e` (editar) o `c` (ir a coordenada).
- En diagramas muy cargados, algunas **etiquetas** pueden solaparse. Los
  valores exactos siempre están en el texto.
- **Persistencia**: el problema se guarda en variables del documento. Hay
  que guardar el documento (`ctrl+S`) para conservarlo. La configuración
  (decimales, unidades…) no se guarda.
- Los nombres de los nodos son automáticos (A, B, C…). Las fuerzas se
  numeran F1, F2…, los momentos M1…, las cargas w1… y las incógnitas
  adicionales P1….

## Previsto para versiones futuras

Estática 3D (la arquitectura de vectores 3D y Gauss n × m ya existe),
armaduras (método de nudos), bastidores de varios cuerpos, fricción,
centroides y momentos de inercia, y dinámica.
