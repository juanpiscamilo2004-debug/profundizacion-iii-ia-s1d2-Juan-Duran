"""Parámetros heredados del modelo MATLAB de tenis de mesa.

Este módulo solo declara valores y condiciones iniciales; no implementa
física ni ejecuta simulaciones. Las unidades se conservan tal como las usa
``TableTennisTests.mlx``: milímetros, gramos y segundos, con coeficientes de
fuerza/torque etiquetados en mN según los comentarios originales.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import pi


Vector3 = tuple[float, float, float]


@dataclass(frozen=True)
class TableTennisParameters:
    """Valores del modelo original y sus condiciones iniciales.

    Las magnitudes espaciales usan mm, las velocidades lineales mm/s y las
    angulares rad/s. La combinación de g, mm, s y mN no es dimensionalmente
    homogénea en el script legado; aquí se preserva deliberadamente su escala
    numérica para reproducir MATLAB antes de cualquier corrección de física.
    """

    # Pelota: g, mm y g·mm² respectivamente.
    ball_mass: float = 2.7
    ball_radius: float = 20.25
    ball_rot_inertia: float = 2.0 / 3.0 * 2.7 * 20.25**2

    # Mesa y red (mm).
    table_length: float = 2740.0
    table_width: float = 1525.0
    table_height: float = 760.0
    net_height: float = 152.5
    net_extra: float = 180.0

    # Coeficientes originales: restituciones y fricción adimensionales.
    table_restitution: float = 0.77
    net_restitution: float = 0.5
    drag: float = 2.7  # mN/(mm/s), según el comentario de MATLAB.
    rot_drag: float = 350.0  # mN·mm/(rad/s), según el comentario de MATLAB.
    magnus: float = 0.01  # mN/(mm/s²), según el comentario de MATLAB.
    table_friction: float = 0.25

    # Gravedad e integración temporal: mm/s², s y s.
    gravity: float = 9800.0
    dt: float = 0.005
    duration: float = 1.5

    # Estado inicial: posición (mm), velocidad (mm/s), giro (rad/s).
    initial_position: Vector3 = (0.0, 762.5, 1065.0)
    initial_velocity: Vector3 = (7000.0, -3000.0, -3000.0)
    initial_angular_velocity: Vector3 = (0.0, 0.0, 75.0 * 2.0 * pi)

    # Parámetros de visualización heredados, sin efecto en la física.
    plot_period: int = 5  # Pasos de simulación.
    animate: bool = True
    yaw: float = -45.0  # Grados.
    pitch: float = 23.0  # ``23,5`` en MATLAB requiere verificación.


# Punto único de configuración para las fases posteriores de la migración.
DEFAULT_PARAMETERS = TableTennisParameters()
