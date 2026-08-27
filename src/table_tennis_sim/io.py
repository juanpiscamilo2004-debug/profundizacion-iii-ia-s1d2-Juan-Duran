"""Exportación reproducible de resultados numéricos."""

from __future__ import annotations

from pathlib import Path

import numpy as np

from .simulation import SimulationResult


def save_results_csv(
    result: SimulationResult, output_directory: str | Path = "results"
) -> Path:
    """Guarda los historiales numéricos en un CSV de columnas estables.

    Se escribe ``simulation_results.csv`` y se preserva el orden temporal de
    :class:`SimulationResult`. No se exportan eventos ni objetos de Python.
    """
    directory = Path(output_directory)
    directory.mkdir(parents=True, exist_ok=True)
    output_path = directory / "simulation_results.csv"
    values = np.column_stack(
        (
            result.time,
            result.position.T,
            result.velocity.T,
            result.acceleration.T,
            result.theta.T,
            result.angular_velocity.T,
            result.angular_acceleration.T,
        )
    )
    header = (
        "time,position_x,position_y,position_z,velocity_x,velocity_y,velocity_z,"
        "acceleration_x,acceleration_y,acceleration_z,theta_x,theta_y,theta_z,"
        "angular_velocity_x,angular_velocity_y,angular_velocity_z,"
        "angular_acceleration_x,angular_acceleration_y,angular_acceleration_z"
    )
    np.savetxt(output_path, values, delimiter=",", header=header, comments="", fmt="%.17g")
    return output_path
