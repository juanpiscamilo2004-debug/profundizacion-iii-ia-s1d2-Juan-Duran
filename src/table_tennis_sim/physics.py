"""Cálculos físicos puros heredados de ``TableTennisTests.mlx``.

Las funciones preservan deliberadamente los valores numéricos y las unidades
del modelo MATLAB: milímetros (mm), gramos (g), segundos (s) y coeficientes
de fuerza/torque etiquetados como mN. No se corrigen aquí sus inconsistencias
dimensionales heredadas.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

from .parameters import TableTennisParameters


Vector3 = NDArray[np.float64]


def calculate_gravitational_force(parameters: TableTennisParameters) -> Vector3:
    """Devuelve la fuerza gravitatoria en mN del modelo legado."""
    return parameters.gravity * parameters.ball_mass * np.array([0.0, 0.0, -1.0])


def calculate_linear_drag(velocity: Vector3, parameters: TableTennisParameters) -> Vector3:
    """Devuelve el arrastre lineal en mN para ``velocity`` en mm/s."""
    return -parameters.drag * velocity


def calculate_magnus_force(
    angular_velocity: Vector3,
    velocity: Vector3,
    parameters: TableTennisParameters,
) -> Vector3:
    """Devuelve la fuerza de Magnus en mN: ``magnus * (omega × v)``.

    ``angular_velocity`` usa rad/s y ``velocity`` usa mm/s.
    """
    return parameters.magnus * np.cross(angular_velocity, velocity)


def calculate_total_force(
    velocity: Vector3,
    angular_velocity: Vector3,
    parameters: TableTennisParameters,
) -> Vector3:
    """Suma gravedad, arrastre y Magnus en mN según MATLAB."""
    return (
        calculate_gravitational_force(parameters)
        + calculate_linear_drag(velocity, parameters)
        + calculate_magnus_force(angular_velocity, velocity, parameters)
    )


def calculate_linear_acceleration(total_force: Vector3, parameters: TableTennisParameters) -> Vector3:
    """Devuelve ``F / masa`` con la escala numérica heredada (mm/s²)."""
    return total_force / parameters.ball_mass


def calculate_rotational_drag_torque(
    angular_velocity: Vector3, parameters: TableTennisParameters
) -> Vector3:
    """Devuelve el torque de arrastre rotacional en mN·mm.

    ``angular_velocity`` se expresa en rad/s.
    """
    return -parameters.rot_drag * angular_velocity


def calculate_angular_acceleration(torque: Vector3, parameters: TableTennisParameters) -> Vector3:
    """Devuelve ``torque / inercia`` con la escala heredada (rad/s²)."""
    return torque / parameters.ball_rot_inertia


def resolve_table_bounce(
    position: Vector3,
    velocity: Vector3,
    angular_velocity: Vector3,
    parameters: TableTennisParameters,
) -> tuple[Vector3, Vector3, Vector3]:
    """Resuelve un rebote con la mesa usando la lógica MATLAB original.

    Posición en mm, velocidad en mm/s y velocidad angular en rad/s. Los
    arreglos devueltos son copias, para que esta función no modifique entradas.
    """
    bounced_position = position.astype(float, copy=True)
    bounced_velocity = velocity.astype(float, copy=True)
    bounced_angular_velocity = angular_velocity.astype(float, copy=True)

    is_over_table = (
        0.0 < bounced_position[0] < parameters.table_length
        and 0.0 < bounced_position[1] < parameters.table_width
    )
    has_reached_table = bounced_position[2] < parameters.table_height + parameters.ball_radius
    if not (is_over_table and has_reached_table):
        return bounced_position, bounced_velocity, bounced_angular_velocity

    bounced_position[2] = parameters.table_height + parameters.ball_radius
    radius_vector = np.array([0.0, 0.0, parameters.ball_radius])
    delta_linear_rotational = (
        np.cross(bounced_angular_velocity, radius_vector)
        - np.array([bounced_velocity[0], bounced_velocity[1], 0.0])
    )
    bounced_velocity += parameters.table_friction * delta_linear_rotational
    bounced_angular_velocity += (
        parameters.table_friction
        * np.cross(delta_linear_rotational, np.array([0.0, 0.0, 1.0]))
        / parameters.ball_radius
    )
    bounced_velocity[2] = -parameters.table_restitution * bounced_velocity[2]
    return bounced_position, bounced_velocity, bounced_angular_velocity


def resolve_net_collision(
    position: Vector3,
    velocity: Vector3,
    angular_velocity: Vector3,
    parameters: TableTennisParameters,
) -> tuple[Vector3, Vector3]:
    """Resuelve una colisión con la red según la condición MATLAB original.

    Posición en mm, velocidad en mm/s y velocidad angular en rad/s. Los
    arreglos devueltos son copias y solo se modifican cuando hay colisión.
    """
    collided_velocity = velocity.astype(float, copy=True)
    collided_angular_velocity = angular_velocity.astype(float, copy=True)

    is_at_net_plane = (
        parameters.table_length / 2.0 - parameters.ball_radius
        <= position[0]
        <= parameters.table_length / 2.0 + parameters.ball_radius
    )
    is_within_net_width = (
        -parameters.net_extra < position[1] < parameters.table_width + parameters.net_extra
    )
    is_within_net_height = (
        parameters.table_height + parameters.ball_radius
        < position[2]
        < parameters.table_height + parameters.net_height + parameters.ball_radius
    )
    if is_at_net_plane and is_within_net_width and is_within_net_height:
        collided_angular_velocity *= parameters.net_restitution
        collided_velocity[0] = -parameters.net_restitution * collided_velocity[0]

    return collided_velocity, collided_angular_velocity
