# Migración de simulación de tenis de mesa: MATLAB → Python

## Descripción

Este proyecto corresponde a la migración de una simulación de tenis de mesa originalmente desarrollada en MATLAB hacia Python.

La simulación modela el movimiento traslacional y rotacional de una pelota de tenis de mesa, considerando:

- gravedad;
- resistencia aerodinámica;
- efecto Magnus;
- resistencia rotacional;
- rebotes sobre la mesa;
- colisiones con la red;
- posición, velocidad y aceleración;
- orientación, velocidad angular y aceleración angular;
- visualización 3D de la trayectoria.

La implementación Python conserva el orden y el comportamiento numérico del algoritmo original.

## Estructura del proyecto

```text
.
├── legacy/
│   └── TableTennisTests.mlx
├── src/
│   └── table_tennis_sim/
│       ├── __init__.py
│       ├── parameters.py
│       ├── physics.py
│       ├── simulation.py
│       ├── visualization.py
│       ├── io.py
│       └── main.py
├── tests/
│   ├── test_parameters.py
│   ├── test_physics.py
│   ├── test_simulation.py
│   ├── test_visualization.py
│   └── test_matlab_equivalence.py
├── results/
│   └── .gitkeep
├── docs/
│   └── plan_migracion.md
├── .gitignore
├── requirements.txt
├── bitacora_ia.md
└── README.md
