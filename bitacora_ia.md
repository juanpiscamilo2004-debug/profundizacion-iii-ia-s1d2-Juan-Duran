# Bitácora de IA generativa

## Introducción

Durante la migración del proyecto de simulación de una pelota de tenis de mesa se utilizó inteligencia artificial generativa como asistente de ingeniería de software. La IA se utilizó para analizar el código MATLAB original, proponer una estructura modular en Python, apoyar la implementación, crear pruebas, revisar la equivalencia numérica y ayudar con la documentación.

Todo cambio generado fue revisado y ejecutado localmente antes de considerarlo válido.

## Interacción 1

- **Fecha:** Agosto de 2026
- **Herramienta usada:** IA generativa / asistente de programación
- **Objetivo:** Analizar el script MATLAB original y establecer una estrategia de migración.
- **Prompt resumido:** Analizar el código MATLAB de simulación de tenis de mesa, identificar sus responsabilidades, riesgos de migración y proponer una estructura Python modular.
- **Resultado obtenido:** Se identificaron las responsabilidades de parámetros, física, simulación, visualización y pruebas.
- **Cambios aceptados:** Separación conceptual del proyecto en módulos.
- **Cambios rechazados:** No se aceptaron modificaciones automáticas sin revisión.
- **Verificación realizada:** Revisión manual del código MATLAB original legacy/TableTennisTests.mlx.
- **Commit asociado:** Commits iniciales de la migración.

## Interacción 2

- **Fecha:** Agosto de 2026
- **Herramienta usada:** IA generativa / asistente de programación
- **Objetivo:** Crear la estructura modular de la simulación Python.
- **Prompt resumido:** Separar parámetros, física, simulación y visualización en módulos reutilizables.
- **Resultado obtenido:** Se desarrollaron módulos dentro de src/table_tennis_sim/, incluyendo parameters.py, physics.py, simulation.py y isualization.py.
- **Cambios aceptados:** Código modular y funciones reutilizables.
- **Cambios rechazados:** Implementaciones innecesariamente complejas o cambios que no conservaran el comportamiento original.
- **Verificación realizada:** Ejecución de la simulación y revisión de resultados.
- **Commit asociado:** Commits de estructura, simulación y visualización.

## Interacción 3

- **Fecha:** Agosto de 2026
- **Herramienta usada:** IA generativa / asistente de programación
- **Objetivo:** Crear pruebas automatizadas para comprobar el comportamiento de la migración.
- **Prompt resumido:** Crear pruebas para parámetros, física, simulación, visualización y equivalencia con MATLAB.
- **Resultado obtenido:** Se creó la carpeta 	ests/ con pruebas automatizadas.
- **Cambios aceptados:** Pruebas de parámetros principales, fuerzas y aceleraciones, simulación, visualización y equivalencia numérica.
- **Cambios rechazados:** Pruebas que dependieran únicamente de resultados visuales o que no pudieran reproducirse.
- **Verificación realizada:** python -m pytest -q
- **Resultado:** 9 pruebas superadas.
- **Commit asociado:** Commit de implementación y pruebas.

## Interacción 4

- **Fecha:** Agosto de 2026
- **Herramienta usada:** IA generativa / asistente de programación
- **Objetivo:** Comparar la simulación Python con la ejecución original de MATLAB.
- **Prompt resumido:** Exportar resultados de MATLAB a CSV y comparar posiciones, velocidades, aceleraciones y variables angulares con Python.
- **Resultado obtenido:** MATLAB produjo 301 muestras para una duración de 1.5 segundos con paso de 0.005 segundos. Los resultados fueron exportados a matlab_results.csv.
- **Cambios aceptados:** Prueba de equivalencia numérica basada en el estado final de MATLAB.
- **Cambios rechazados:** Correcciones físicas del modelo original durante esta primera migración.
- **Verificación realizada:** Comparación del estado final de MATLAB y Python.
- **Resultado:** Las variables principales coincidieron dentro de la precisión numérica utilizada.
- **Commit asociado:** Completar migracion de MATLAB a Python

## Interacción 5

- **Fecha:** Agosto de 2026
- **Herramienta usada:** IA generativa / asistente de programación
- **Objetivo:** Crear un notebook interactivo para explorar la simulación mediante sliders.
- **Prompt resumido:** Crear 
otebooks/01_simulacion_interactiva.ipynb utilizando ipywidgets, importando la simulación desde src/ y permitiendo modificar parámetros relevantes.
- **Resultado obtenido:** Notebook interactivo con sliders para velocidades iniciales, velocidad angular, arrastre, Magnus, restitución de mesa, restitución de red, fricción y duración.
- **Cambios aceptados:** Uso de funciones del paquete Python en lugar de duplicar la física dentro del notebook.
- **Cambios rechazados:** Duplicación del código de simulación dentro del notebook.
- **Verificación realizada:** Ejecución del notebook en Jupyter y comprobación visual de los sliders y gráficas.
- **Resultado:** Los sliders funcionan y regeneran la trayectoria y las gráficas.
- **Commit asociado:** Pendiente de commit final.

## Interacción 6

- **Fecha:** Agosto de 2026
- **Herramienta usada:** IA generativa / asistente de programación
- **Objetivo:** Revisar documentación, dependencias y estado final del proyecto.
- **Prompt resumido:** Revisar README, plan de migración, requisitos, pruebas, notebook y estado de Git para preparar la entrega.
- **Resultado obtenido:** Se actualizaron la documentación, equirements.txt, .gitignore y el notebook interactivo.
- **Cambios aceptados:** Inclusión de 
umpy, matplotlib, pytest, ipywidgets y Jupyter; exclusión de archivos temporales de Jupyter.
- **Cambios rechazados:** No se modificó el modelo físico con el objetivo de mantener la equivalencia con MATLAB.
- **Verificación realizada:** python -m pytest -q y ejecución de python -m src.table_tennis_sim.main.
- **Resultado:** 9 pruebas superadas. La simulación genera 301 muestras, dura 1.5 segundos, registra 2 colisiones con la mesa y 0 con la red.
- **Commit asociado:** Pendiente de commit final.

## Reflexión final

### ¿Qué parte del resultado entiendo completamente?

Se comprende la separación del proyecto en módulos, el funcionamiento general de la simulación temporal, los parámetros principales, las pruebas automatizadas y el uso del notebook para modificar parámetros y observar sus efectos.

### ¿Qué parte debo estudiar mejor?

Se debe profundizar en el modelo físico utilizado por el código MATLAB, especialmente en las ecuaciones de arrastre, efecto Magnus, torque rotacional y tratamiento de las colisiones.

### ¿Qué riesgo tendría entregar esto sin revisión humana?

La principal consecuencia sería aceptar errores de traducción, unidades o comportamiento físico sin detectarlos. Por esta razón se ejecutaron pruebas automatizadas y se compararon resultados con la referencia de MATLAB.

## Conclusión

La IA se utilizó como herramienta de apoyo y no como sustituto de la revisión. Los cambios relevantes fueron ejecutados, probados y comparados con el comportamiento del programa MATLAB original antes de considerarlos parte de la migración.
