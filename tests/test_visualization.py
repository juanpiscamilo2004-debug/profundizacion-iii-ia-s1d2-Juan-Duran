import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from src.table_tennis_sim.parameters import DEFAULT_PARAMETERS
from src.table_tennis_sim.simulation import run_simulation
from src.table_tennis_sim.visualization import plot_time_series, plot_trajectory


def test_plot_time_series_returns_figure_and_six_axes() -> None:
    figure, axes = plot_time_series(run_simulation())
    try:
        assert isinstance(figure, Figure)
        assert axes.size == 6
    finally:
        plt.close(figure)


def test_plot_trajectory_returns_figure_and_axes() -> None:
    figure, axis = plot_trajectory(run_simulation(), DEFAULT_PARAMETERS)
    try:
        assert isinstance(figure, Figure)
        assert isinstance(axis, Axes)
    finally:
        plt.close(figure)
