from math import pi

from src.table_tennis_sim.parameters import DEFAULT_PARAMETERS


def test_default_parameters_principal_values() -> None:
    parameters = DEFAULT_PARAMETERS
    assert parameters.ball_mass == 2.7
    assert parameters.ball_radius == 20.25
    assert parameters.gravity == 9800.0
    assert parameters.dt == 0.005
    assert parameters.duration == 1.5
    assert parameters.initial_position == (0.0, 762.5, 1065.0)
    assert parameters.initial_velocity == (7000.0, -3000.0, -3000.0)
    assert parameters.initial_angular_velocity == (0.0, 0.0, 150.0 * pi)
