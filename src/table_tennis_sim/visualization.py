"""Visualizaciones de los resultados de la simulacion de tenis de mesa.

Las funciones de este modulo solo consumen :class:`SimulationResult`; no
alteran los historiales ni ejecutan la simulacion por su cuenta.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import Animation, FuncAnimation
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401: registra la proyeccion 3D.

from .parameters import TableTennisParameters
from .simulation import SimulationResult

if TYPE_CHECKING:
    from numpy.typing import NDArray


def plot_time_series(result: SimulationResult) -> tuple[Figure, NDArray[Axes]]:
    """Grafica los historiales lineales y angulares frente al tiempo.

    Cada fila contiene las componentes ``x``, ``y`` y ``z`` de una magnitud
    vectorial, cuyos historiales conservan la forma ``(3, N)`` definida por
    :class:`~src.table_tennis_sim.simulation.SimulationResult`.
    """
    figure, axes = plt.subplots(3, 2, figsize=(13, 11), sharex=True, layout="constrained")
    components = ("x", "y", "z")
    series = (
        ("Posicion", result.position, "mm"),
        ("Velocidad", result.velocity, "mm/s"),
        ("Aceleracion", result.acceleration, "mm/s²"),
        ("Theta", result.theta, "rad"),
        ("Velocidad angular", result.angular_velocity, "rad/s"),
        ("Aceleracion angular", result.angular_acceleration, "rad/s²"),
    )

    for axis, (title, values, unit) in zip(axes.flat, series):
        for component, values_component in zip(components, values):
            axis.plot(result.time, values_component, label=component)
        axis.set_title(title)
        axis.set_ylabel(unit)
        axis.grid(True, alpha=0.35)
        axis.legend()

    for axis in axes[-1, :]:
        axis.set_xlabel("Tiempo (s)")
    return figure, axes


def _draw_table(axis: Axes, parameters: TableTennisParameters) -> None:
    """Dibuja la superficie rectangular de la mesa en sus coordenadas fisicas."""
    x, y = np.meshgrid(
        np.array([0.0, parameters.table_length]),
        np.array([0.0, parameters.table_width]),
    )
    z = np.full_like(x, parameters.table_height)
    axis.plot_surface(x, y, z, color="tab:green", alpha=0.45, shade=False)


def _draw_net(axis: Axes, parameters: TableTennisParameters) -> None:
    """Dibuja la red vertical, perpendicular al eje x y centrada en la mesa."""
    y, z = np.meshgrid(
        np.array([-parameters.net_extra, parameters.table_width + parameters.net_extra]),
        np.array([parameters.table_height, parameters.table_height + parameters.net_height]),
    )
    x = np.full_like(y, parameters.table_length / 2.0)
    axis.plot_surface(x, y, z, color="black", alpha=0.45, shade=False)


def _set_scene_limits(axis: Axes, result: SimulationResult, parameters: TableTennisParameters) -> None:
    """Ajusta limites que incluyen mesa, red, radio de pelota y trayectoria."""
    radius = parameters.ball_radius
    x_data, y_data, z_data = result.position
    x_limits = (
        min(-radius, float(np.min(x_data)) - radius),
        max(parameters.table_length + radius, float(np.max(x_data)) + radius),
    )
    y_limits = (
        min(-parameters.net_extra - radius, float(np.min(y_data)) - radius),
        max(parameters.table_width + parameters.net_extra + radius, float(np.max(y_data)) + radius),
    )
    z_limits = (
        min(0.0, float(np.min(z_data)) - radius),
        max(parameters.table_height + parameters.net_height + radius, float(np.max(z_data)) + radius),
    )

    axis.set_xlim(*x_limits)
    axis.set_ylim(*y_limits)
    axis.set_zlim(*z_limits)
    axis.set_box_aspect(
        (x_limits[1] - x_limits[0], y_limits[1] - y_limits[0], z_limits[1] - z_limits[0])
    )


def plot_trajectory(
    result: SimulationResult, parameters: TableTennisParameters
) -> tuple[Figure, Axes]:
    """Crea una escena 3D con mesa, red, trayectoria, pelota y colisiones.

    La esfera representa la pelota en la ultima muestra. Las colisiones ya
    registradas por la simulacion se destacan sin recalcularlas.
    """
    figure = plt.figure(figsize=(11, 8), layout="constrained")
    axis = figure.add_subplot(111, projection="3d")
    _draw_table(axis, parameters)
    _draw_net(axis, parameters)

    x, y, z = result.position
    axis.plot(x, y, z, color="tab:blue", linewidth=2, label="Trayectoria")

    # Resolucion comparable a sphere(25) de MATLAB.
    azimuth, polar = np.meshgrid(
        np.linspace(0.0, 2.0 * np.pi, 26), np.linspace(0.0, np.pi, 26)
    )
    center = result.position[:, -1]
    radius = parameters.ball_radius
    sphere_x = center[0] + radius * np.cos(azimuth) * np.sin(polar)
    sphere_y = center[1] + radius * np.sin(azimuth) * np.sin(polar)
    sphere_z = center[2] + radius * np.cos(polar)
    axis.plot_surface(sphere_x, sphere_y, sphere_z, color="tab:orange", alpha=0.9, shade=True)

    final_velocity = result.velocity[:, -1]
    velocity_norm = float(np.linalg.norm(final_velocity))
    if velocity_norm > 0.0:
        direction = final_velocity / velocity_norm * (4.0 * radius)
        axis.quiver(
            *center, *direction, color="tab:red", arrow_length_ratio=0.2, label="Direccion"
        )

    if result.table_collision_indices:
        indices = np.asarray(result.table_collision_indices, dtype=int)
        axis.scatter(
            x[indices], y[indices], z[indices], color="tab:purple", s=35, label="Colision mesa"
        )
    if result.net_collision_indices:
        indices = np.asarray(result.net_collision_indices, dtype=int)
        axis.scatter(
            x[indices], y[indices], z[indices], color="tab:red", marker="x", s=55, label="Colision red"
        )

    _set_scene_limits(axis, result, parameters)
    axis.set_xlabel("x (mm)")
    axis.set_ylabel("y (mm)")
    axis.set_zlabel("z (mm)")
    axis.set_title("Trayectoria 3D de la pelota")
    axis.view_init(elev=parameters.pitch, azim=parameters.yaw)
    axis.legend()
    return figure, axis


def animate_trajectory(
    result: SimulationResult,
    parameters: TableTennisParameters,
    interval: int = 50,
    show_vectors: bool = True,
) -> tuple[Animation, Figure, Axes]:
    """Anima una trayectoria ya calculada sin ejecutar ni alterar la simulación.

    Los fotogramas se separan conforme a ``parameters.plot_period``. Los
    vectores se normalizan solo para presentación, debido a la escala numérica
    heredada del modelo.
    """
    if interval <= 0:
        raise ValueError("interval must be positive")
    frame_indices = np.arange(0, result.time.size, parameters.plot_period, dtype=int)
    if frame_indices[-1] != result.time.size - 1:
        frame_indices = np.append(frame_indices, result.time.size - 1)

    figure = plt.figure(figsize=(11, 8), layout="constrained")
    axis = figure.add_subplot(111, projection="3d")
    _draw_table(axis, parameters)
    _draw_net(axis, parameters)
    _set_scene_limits(axis, result, parameters)
    axis.set_xlabel("x (mm)")
    axis.set_ylabel("y (mm)")
    axis.set_zlabel("z (mm)")
    axis.set_title("Animación 3D de la trayectoria")
    axis.view_init(elev=parameters.pitch, azim=parameters.yaw)

    travelled_path, = axis.plot([], [], [], color="tab:blue", linewidth=2, label="Trayectoria")
    ball, = axis.plot([], [], [], marker="o", color="tab:orange", markersize=8, label="Pelota")
    time_label = axis.text2D(0.02, 0.95, "", transform=axis.transAxes)
    vector_artists: list[object] = []
    axis.legend()

    def scaled_direction(values: np.ndarray) -> np.ndarray:
        norm = float(np.linalg.norm(values))
        return np.zeros(3) if norm == 0.0 else values / norm * (4.0 * parameters.ball_radius)

    def update(frame_number: int) -> tuple[object, ...]:
        index = frame_indices[frame_number]
        center = result.position[:, index]
        travelled_path.set_data(result.position[0, : index + 1], result.position[1, : index + 1])
        travelled_path.set_3d_properties(result.position[2, : index + 1])
        ball.set_data([center[0]], [center[1]])
        ball.set_3d_properties([center[2]])
        time_label.set_text(f"t = {result.time[index]:.3f} s")
        for artist in vector_artists:
            artist.remove()
        vector_artists.clear()
        if show_vectors:
            for values, color in (
                (result.velocity[:, index], "tab:red"),
                (result.acceleration[:, index], "tab:purple"),
                (result.angular_velocity[:, index], "tab:brown"),
            ):
                direction = scaled_direction(values)
                if np.any(direction):
                    vector_artists.append(
                        axis.quiver(*center, *direction, color=color, arrow_length_ratio=0.2)
                    )
        return travelled_path, ball, time_label, *vector_artists

    animation = FuncAnimation(
        figure, update, frames=len(frame_indices), interval=interval, blit=False, repeat=False
    )
    return animation, figure, axis


def plot_simulation(
    result: SimulationResult, parameters: TableTennisParameters
) -> tuple[tuple[Figure, NDArray[Axes]], tuple[Figure, Axes]]:
    """Genera y muestra las series temporales y la escena 3D principales."""
    time_series = plot_time_series(result)
    trajectory = plot_trajectory(result, parameters)
    plt.show()
    return time_series, trajectory
