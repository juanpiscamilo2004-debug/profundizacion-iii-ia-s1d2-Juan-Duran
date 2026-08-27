from pathlib import Path

import numpy as np

from src.table_tennis_sim.io import save_results_csv
from src.table_tennis_sim.simulation import run_simulation


def test_python_matches_matlab_reference() -> None:
    """Compara todas las muestras de Python contra la referencia exportada de MATLAB."""
    matlab_path = Path("matlab_results.csv")

    assert matlab_path.exists(), (
        f"No se encontró la referencia de MATLAB: {matlab_path}"
    )

    matlab_data = np.loadtxt(matlab_path, delimiter=",")
    result = run_simulation()

    python_data = np.column_stack(
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

    assert matlab_data.shape == python_data.shape
    assert matlab_data.shape == (301, 19)

    np.testing.assert_allclose(
        python_data,
        matlab_data,
        rtol=1e-10,
        atol=1e-10,
    )


def test_exported_python_csv_has_expected_shape(tmp_path: Path) -> None:
    """Comprueba que la exportación Python conserva las 301 muestras y 19 columnas."""
    result = run_simulation()
    output_path = save_results_csv(result, tmp_path)

    exported = np.loadtxt(output_path, delimiter=",", skiprows=1)

    assert exported.shape == (301, 19)