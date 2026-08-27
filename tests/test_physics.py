import numpy as np

from src.table_tennis_sim.parameters import DEFAULT_PARAMETERS
from src.table_tennis_sim.physics import (
    calculate_gravitational_force,
    calculate_linear_acceleration,
    calculate_linear_drag,
    calculate_magnus_force,
    calculate_rotational_drag_torque,
    calculate_total_force,
    resolve_net_collision,
    resolve_table_bounce,
)


def _initial_state() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    parameters = DEFAULT_PARAMETERS
    return (
        np.asarray(parameters.initial_position, dtype=float),
        np.asarray(parameters.initial_velocity, dtype=float),
        np.asarray(parameters.initial_angular_velocity, dtype=float),
    )


def test_initial_forces_and_acceleration() -> None:
    parameters = DEFAULT_PARAMETERS
    _, velocity, angular_velocity = _initial_state()
    gravity = calculate_gravitational_force(parameters)
    drag = calculate_linear_drag(velocity, parameters)
    magnus = calculate_magnus_force(angular_velocity, velocity, parameters)
    total = calculate_total_force(velocity, angular_velocity, parameters)

    np.testing.assert_allclose(gravity, [0.0, 0.0, -26460.0])
    np.testing.assert_allclose(drag, [-18900.0, 8100.0, 8100.0])
    np.testing.assert_allclose(magnus, [14137.16694115, 32986.72286269, 0.0])
    np.testing.assert_allclose(total, [-4762.83305885, 41086.72286269, -18360.0])
    np.testing.assert_allclose(calculate_linear_acceleration(total, parameters), total / parameters.ball_mass)


def test_rotational_drag_torque() -> None:
    parameters = DEFAULT_PARAMETERS
    _, _, angular_velocity = _initial_state()
    np.testing.assert_allclose(
        calculate_rotational_drag_torque(angular_velocity, parameters),
        -parameters.rot_drag * angular_velocity,
    )


def test_collision_functions_do_not_modify_inputs() -> None:
    parameters = DEFAULT_PARAMETERS
    position = np.array([100.0, 100.0, parameters.table_height])
    velocity = np.array([1.0, 2.0, -3.0])
    angular_velocity = np.array([4.0, 5.0, 6.0])
    originals = tuple(value.copy() for value in (position, velocity, angular_velocity))

    resolve_table_bounce(position, velocity, angular_velocity, parameters)
    resolve_net_collision(position, velocity, angular_velocity, parameters)

    for value, original in zip((position, velocity, angular_velocity), originals):
        np.testing.assert_array_equal(value, original)
