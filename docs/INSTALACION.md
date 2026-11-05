# Instalación en la TI-Nspire CX II / CX II CAS

## Requisitos

- **TI-Nspire CX II**, **CX II CAS** o **CX II-T** con **OS 5.2 o
  posterior**. Python no existe en la CX original (sin "II"). Para ver tu
  versión: `home` > `5 Configuración` > `4 Estado`. Si es anterior a 5.2,
  actualízala con el software gratuito de TI.
- Un ordenador con **TI-Nspire Computer Link** (gratuito) o con **TI-Nspire
  CX Student / Teacher Software**, y el cable USB de la calculadora.

## Paso 1: conseguir el archivo

Tienes dos caminos.

### Opción A: documento `.tns` generado automáticamente (recomendada)

El repositorio incluye un workflow que convierte los `.py` en documentos
`.tns` con **Luna**, el convertidor libre de la comunidad Ndless.

1. En GitHub, abre el repositorio y entra en la pestaña **Actions**.
2. Elige **"Generar .tns"** en la lista de la izquierda y pulsa **Run
   workflow** (rama: la que contenga el proyecto).
3. Cuando termine (marca verde, unos 2 minutos), entra en la ejecución y
   descarga el artefacto **EngineeringSolver-tns** (un `.zip`).
4. Descomprímelo. Dentro están `EngSolver.tns` (completo),
   `EngSolver_lite.tns`, `EngTest.tns` y `EngSolver_modular.tns`.

### Opción B: crear el `.tns` a mano desde el `.py`

1. Abre **TI-Nspire CX Student/Teacher Software** (5.2 o superior) en el
   ordenador y crea un documento nuevo (`Archivo > Nuevo documento`).
2. Pon la vista de **unidad portátil** (handheld) y elige
   `Insertar > Python > Nuevo…`. Nómbralo `EngSolver`.
3. Abre `dist/EngSolver.py` con un editor de texto en el PC, **selecciona
   todo**, cópialo y **pégalo** en el editor de Python del software.
4. Pulsa `ctrl+B` (comprobar sintaxis y guardar).
5. Guarda el documento como `EngSolver.tns`.

> Algunas versiones del software también abren un `.py` directamente con
> `Archivo > Abrir` y lo convierten en documento. Si la tuya lo permite, es
> lo más rápido.

## Paso 2: pasarlo a la calculadora

1. Conecta la calculadora encendida al PC con el cable USB.
2. Abre **TI-Nspire Computer Link** (o el software, en el panel *Explorador
   de contenido*).
3. Arrastra `EngSolver.tns` a la carpeta de la calculadora donde lo quieras
   (por ejemplo `Mis documentos`).
4. Espera a que termine la transferencia y desconecta.

## Paso 3: ejecutarlo

1. En la calculadora: `home` > `2 Mis documentos` > abre **EngSolver**.
2. Se abre el editor de Python con el programa. Pulsa **`ctrl` + `R`**
   (o `menu` > `Ejecutar` > `Ejecutar`).
3. Aparece el shell con el **MENÚ PRINCIPAL**. Escribe el número de la
   opción y pulsa `enter`.

Para volver a usarlo más tarde basta con abrir el documento y pulsar
`ctrl+R`. **Interrumpir** un programa en marcha: mantén pulsada la tecla
`on`.

## Paso 4 (recomendado): comprobar que todo funciona

1. En el menú principal elige `4 CONFIGURACION` > `8 Ejecutar autopruebas`.
   Debe salir **"Correctas: 218, Fallidas: 0"**.
2. Elige `1 ESTATICA` > `6 Ejemplos resueltos` > `1`, contesta `s` a *Ver
   diagrama*. Aparece el DCL gráfico; pulsa cualquier tecla. Debe dar
   `Ay = 800`, `Cy = 400`.
3. Entra en el **editor gráfico** (`1 ESTATICA` > `1` > `2 Por dibujo`) y
   mueve el cursor con las flechas. Si al escribir números en la pantalla
   gráfica no aparecen el punto decimal o el signo menos, ve a
   `CONFIGURACION` > `6 Entrada en editor` y cámbiala a **shell** (ver
   [LIMITACIONES](LIMITACIONES.md)).
4. Si los símbolos Σ, ° o · se ven como cuadros, activa
   `CONFIGURACION` > `3 Simbolos ASCII`.

## Si aparece `MemoryError` al cargar

El archivo completo ocupa unos 160 KB de código. Prueba en este orden:

1. Cierra los demás documentos abiertos y vuelve a ejecutar.
2. Usa **`EngSolver_lite`**, que no lleva la batería de autopruebas.
3. Usa **`EngSolver_modular.tns`**, donde cada módulo se compila por
   separado y el pico de memoria es menor. En la Opción B, crea un programa
   Python por cada archivo de `dist/modular/` **en el mismo documento y
   problema**, con el mismo nombre, y ejecuta `main.py`.

## Guardar problemas

Dentro de un problema, `12 Guardar problema` lo guarda en la variable
`esprob1`…`esprob9` del documento. Después **guarda el documento** con
`ctrl+S`, o las variables se pierden al cerrarlo. Para recuperarlo:
`ESTATICA` > `8 Cargar problema guardado`.
