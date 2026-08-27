"""Punto de entrada para ejecutar la simulación sin efectos al importar."""

from __future__ import annotations

import argparse

from .io import save_results_csv
from .parameters import DEFAULT_PARAMETERS
from .simulation import run_simulation
from .visualization import animate_trajectory, plot_simulation


def main() -> None:
    """Ejecuta la simulación y muestra opcionalmente sus visualizaciones."""
    parser = argparse.ArgumentParser(
        description="Simulación de tenis de mesa heredada de MATLAB"
    )
    parser.add_argument(
        "--plot",
        action="store_true",
        help="mostrar las gráficas estáticas",
    )
    parser.add_argument(
        "--animate",
        action="store_true",
        help="mostrar la animación 3D",
    )
    parser.add_argument(
        "--output-dir",
        default="results",
        help="directorio donde guardar los resultados CSV",
    )
    arguments = parser.parse_args()

    result = run_simulation()
    output_path = save_results_csv(result, arguments.output_dir)

    duration = result.time[-1] - result.time[0]
    print(f"Muestras: {result.time.size}")
    print(f"Duración: {duration:g} s")
    print(f"Colisiones con mesa: {len(result.table_collision_indices)}")
    print(f"Colisiones con red: {len(result.net_collision_indices)}")
    print(f"Resultados guardados en: {output_path}")

    if arguments.plot:
        plot_simulation(result, DEFAULT_PARAMETERS)
    elif arguments.animate:
        animation, figure, _ = animate_trajectory(
            result, DEFAULT_PARAMETERS
        )
        # Mantiene viva la animación hasta que se cierre la ventana.
        figure._table_tennis_animation = animation

        import matplotlib.pyplot as plt

        plt.show()


if __name__ == "__main__":
    main()
