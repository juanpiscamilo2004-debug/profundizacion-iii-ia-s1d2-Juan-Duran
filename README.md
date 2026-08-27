# Migración de simulación de tenis de mesa: MATLAB ? Python

## Propósito

Este proyecto corresponde a la migración de una simulación de tenis de mesa originalmente desarrollada en MATLAB hacia Python.

El archivo original legacy/TableTennisTests.mlx se conserva como referencia. La implementación Python separa el modelo físico, la simulación, la visualización, la exportación de resultados y las pruebas automatizadas.

La simulación considera:

- gravedad;
- resistencia aerodinámica;
- efecto Magnus;
- resistencia rotacional;
- rebotes sobre la mesa;
- colisiones con la red;
- posición, velocidad y aceleración;
- orientación, velocidad angular y aceleración angular;
- visualización 3D.

## Estructura del proyecto

`	ext
.
+-- legacy/
¦   +-- TableTennisTests.mlx
+-- src/
¦   +-- table_tennis_sim/
¦       +-- __init__.py
¦       +-- parameters.py
¦       +-- physics.py
¦       +-- simulation.py
¦       +-- visualization.py
¦       +-- io.py
¦       +-- main.py
+-- tests/
¦   +-- test_parameters.py
¦   +-- test_physics.py
¦   +-- test_simulation.py
¦   +-- test_visualization.py
¦   +-- test_matlab_equivalence.py
+-- notebooks/
¦   +-- 01_simulacion_interactiva.ipynb
+-- results/
¦   +-- .gitkeep
+-- docs/
¦   +-- plan_migracion.md
+-- .gitignore
+-- requirements.txt
+-- bitacora_ia.md
+-- README.md
