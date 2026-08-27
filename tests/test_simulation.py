import numpy as np

from src.table_tennis_sim.parameters import DEFAULT_PARAMETERS
from src.table_tennis_sim.simulation import run_simulation


def test_simulation_shape_events_finiteness_and_initial_state() -> None:
    parameters = DEFAULT_PARAMETERS
    result = run_simulation()

    assert result.time.size == 301
    for history in (
        result.position,
        result.velocity,
        result.acceleration,
        result.theta,
        result.angular_velocity,
        result.angular_acceleration,
    ):
        assert history.shape == (3, 301)
        assert np.isfinite(history).all()
    assert result.table_collision_indices == (18, 110)
    assert result.net_collision_indices == ()
    np.testing.assert_array_equal(result.position[:, 0], parameters.initial_position)
    np.testing.assert_array_equal(result.velocity[:, 0], parameters.initial_velocity)
    np.testing.assert_array_equal(result.angular_velocity[:, 0], parameters.initial_angular_velocity)
