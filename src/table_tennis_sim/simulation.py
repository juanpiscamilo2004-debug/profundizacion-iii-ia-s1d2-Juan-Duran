"""Temporal coordination preserving ``legacy/TableTennisTests.mlx`` order."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from .parameters import DEFAULT_PARAMETERS, TableTennisParameters
from .physics import (
    calculate_angular_acceleration,
    calculate_linear_acceleration,
    calculate_rotational_drag_torque,
    calculate_total_force,
    resolve_net_collision,
    resolve_table_bounce,
)

History = NDArray[np.float64]


@dataclass(frozen=True)
class SimulationResult:
    """State histories, each vector history shaped ``(3, len(time))``."""

    time: NDArray[np.float64]
    position: History
    velocity: History
    acceleration: History
    theta: History
    angular_velocity: History
    angular_acceleration: History
    table_collision_indices: tuple[int, ...]
    net_collision_indices: tuple[int, ...]

    # MATLAB-compatible names, useful when comparing histories with the script.
    @property
    def t(self) -> NDArray[np.float64]:
        return self.time

    @property
    def x(self) -> History:
        return self.position

    @property
    def v(self) -> History:
        return self.velocity

    @property
    def a(self) -> History:
        return self.acceleration

    @property
    def rotation(self) -> History:
        """Alias descriptivo de :attr:`theta`."""
        return self.theta

    @property
    def omega(self) -> History:
        return self.angular_velocity

    @property
    def alpha(self) -> History:
        return self.angular_acceleration


def _time_vector(parameters: TableTennisParameters) -> NDArray[np.float64]:
    """Build ``0:dt:duration`` without losing its final sample to rounding."""
    step_count = round(parameters.duration / parameters.dt)
    if not np.isclose(step_count * parameters.dt, parameters.duration):
        raise ValueError("duration must be an integer multiple of dt")
    return np.arange(step_count + 1, dtype=float) * parameters.dt


def _initial_vector(values: object, name: str) -> NDArray[np.float64]:
    """Return one three-component initial state with a clear error otherwise."""
    vector = np.asarray(values, dtype=float)
    if vector.shape != (3,):
        raise ValueError(f"{name} must contain exactly three components; got shape {vector.shape}")
    return vector


def _has_table_collision(position: NDArray[np.float64], parameters: TableTennisParameters) -> bool:
    return (
        0.0 < position[0] < parameters.table_length
        and 0.0 < position[1] < parameters.table_width
        and position[2] < parameters.table_height + parameters.ball_radius
    )


def _has_net_collision(position: NDArray[np.float64], parameters: TableTennisParameters) -> bool:
    net_x = parameters.table_length / 2.0
    return (
        net_x - parameters.ball_radius <= position[0] <= net_x + parameters.ball_radius
        and -parameters.net_extra < position[1] < parameters.table_width + parameters.net_extra
        and parameters.table_height + parameters.ball_radius
        < position[2]
        < parameters.table_height + parameters.net_height + parameters.ball_radius
    )


def run_simulation(parameters: TableTennisParameters = DEFAULT_PARAMETERS) -> SimulationResult:
    """Run the original semi-explicit Euler sequence and final collisions.

    Linear and angular accelerations are evaluated from step ``k - 1``.
    Position and rotation use their newly updated velocities. Table and net
    rules are applied last, in that order.
    """
    time = _time_vector(parameters)
    sample_count = time.size
    position = np.zeros((3, sample_count), dtype=float)
    velocity = np.zeros((3, sample_count), dtype=float)
    acceleration = np.zeros((3, sample_count), dtype=float)
    theta = np.zeros((3, sample_count), dtype=float)
    angular_velocity = np.zeros((3, sample_count), dtype=float)
    angular_acceleration = np.zeros((3, sample_count), dtype=float)

    position[:, 0] = _initial_vector(parameters.initial_position, "initial_position")
    velocity[:, 0] = _initial_vector(parameters.initial_velocity, "initial_velocity")
    angular_velocity[:, 0] = _initial_vector(
        parameters.initial_angular_velocity, "initial_angular_velocity"
    )
    table_events: list[int] = []
    net_events: list[int] = []

    for step in range(1, sample_count):
        force = calculate_total_force(velocity[:, step - 1], angular_velocity[:, step - 1], parameters)
        acceleration[:, step] = calculate_linear_acceleration(force, parameters)
        velocity[:, step] = velocity[:, step - 1] + acceleration[:, step] * parameters.dt
        position[:, step] = position[:, step - 1] + velocity[:, step] * parameters.dt

        torque = calculate_rotational_drag_torque(angular_velocity[:, step - 1], parameters)
        angular_acceleration[:, step] = calculate_angular_acceleration(torque, parameters)
        angular_velocity[:, step] = angular_velocity[:, step - 1] + angular_acceleration[:, step] * parameters.dt
        theta[:, step] = theta[:, step - 1] + angular_velocity[:, step] * parameters.dt

        # Collisions occur only after both integration stages, as in MATLAB.
        if _has_table_collision(position[:, step], parameters):
            table_events.append(step)
        position[:, step], velocity[:, step], angular_velocity[:, step] = resolve_table_bounce(
            position[:, step], velocity[:, step], angular_velocity[:, step], parameters
        )

        if _has_net_collision(position[:, step], parameters):
            net_events.append(step)
        velocity[:, step], angular_velocity[:, step] = resolve_net_collision(
            position[:, step], velocity[:, step], angular_velocity[:, step], parameters
        )

    return SimulationResult(
        time=time,
        position=position,
        velocity=velocity,
        acceleration=acceleration,
        theta=theta,
        angular_velocity=angular_velocity,
        angular_acceleration=angular_acceleration,
        table_collision_indices=tuple(table_events),
        net_collision_indices=tuple(net_events),
    )


simulate = run_simulation
"""Brief alias for :func:`run_simulation`."""
