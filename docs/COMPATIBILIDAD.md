# Fase 1: compatibilidad y restricciones de la TI-Nspire CX II

## Entorno Python de la calculadora

| Aspecto | Realidad en la CX II (OS 5.2 o posterior) | Decisión en el proyecto |
|---|---|---|
| Intérprete | Basado en **MicroPython** (sintaxis ~Python 3.4). Sin f-strings ni anotaciones; biblioteca estándar mínima | Solo `%`, `str()` y concatenación; el verificador `tools/compat.py` lo comprueba |
| Módulos disponibles | `math`, `cmath`, `random`, `time` y los propios de TI: `ti_system`, `ti_draw`, `ti_plotlib`, `ti_image`, `ti_hub`, `ti_rover` | Solo se usan `math`, `ti_draw` y `ti_system`. **No** se usan NumPy, SciPy ni SymPy |
| Métodos de `str` | MicroPython no tiene `ljust`, `rjust`, `center`, `zfill`, `title`… | Funciones propias `pad`, `padl` y `wrap` |
| `math` | Faltan `hypot`, `isclose`, `degrees`/`radians` en algunas versiones | `rad`, `grad` y la norma implementadas a mano |
| Orden de los `dict` | No garantizado en MicroPython antiguo | Toda la lógica que depende del orden usa listas |
| Pantalla gráfica | 318 × 212 px, origen arriba a la izquierda, con `ti_draw` (líneas, rectángulos, círculos, polígonos, texto, color, grosor y estilo de trazo, `use_buffer`/`paint_buffer`) | DCL y diagramas a medida de esa resolución; doble búfer si está disponible; coordenadas siempre enteras |
| Teclado | `ti_system.get_key()` devuelve el nombre de la tecla (`"up"`, `"enter"`, `"esc"`, dígitos, letras…) | El editor gráfico funciona solo con flechas, letras y dígitos |
| Shell de texto | ~32 caracteres por línea y ~11 líneas visibles | Ajuste de línea propio y paginador configurables |
| Memoria | Montón de Python de pocos MB; un archivo grande puede dar `MemoryError` al compilarse | Comentarios y docstrings eliminados en `dist/`; versiones *lite* y *modular* |
| Persistencia | `ti_system.store_list`/`recall_list` guardan listas numéricas en variables del documento | Los problemas se codifican como listas de números (`esprob1`…`esprob9`) |
| Archivos | Un documento `.tns` puede contener varios programas Python que se importan entre sí si están en el mismo problema | Versión de un solo archivo (principal) y versión modular |
| Conversión a `.tns` | El software oficial de TI o **Luna** (`luna archivo.py salida.tns`; OS ≥ 5.2) | Workflow manual de GitHub Actions con Luna |

Referencias: guía oficial de TI-Nspire Python (menú TI Draw:
<https://education.ti.com/html/eguides/nspire/eg_nspire/en/content/eg_python/m_menumap/mm_tidraw.HTML>)
y Luna (<https://github.com/ndless-nspire/Luna>).

## Decisiones de diseño derivadas

1. **Motor matemático propio**: vectores 2D/3D, Gauss-Jordan con pivoteo
   parcial, rango, determinante, inversa, tolerancias relativas y detección
   de singularidad.
2. **Evaluador de expresiones propio** en lugar de `eval`, para aceptar datos
   como `500*cos(30)` de forma segura y en grados.
3. **Un solo archivo** (`dist/EngSolver.py`) generado a partir de módulos
   (`src/`). El empaquetador elimina los imports locales y comprueba que no
   haya colisiones de nombres.
4. **Editor gráfico con cursor** en lugar de dibujo táctil, porque el
   *touchpad* no está accesible desde Python. Si una tecla no llega, el
   editor tiene alternativa en el shell, y todo se puede hacer también por
   coordenadas.
5. **Unicode opcional**: Σ, °, ·, θ y √ se pueden sustituir por ASCII.
