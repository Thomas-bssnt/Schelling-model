from schelling.model import Schelling
from schelling.visualizer import Visualizer


def main() -> None:
    city_size = (50, 50)
    population_density = 0.9
    happiness_threshold = 0.5
    number_types = 2

    schelling = Schelling(
        city_size,
        population_density,
        happiness_threshold,
        number_types,
    )

    visualizer = Visualizer(schelling)
    visualizer.animate(updates_per_frame=100, interval=200)


if __name__ == "__main__":
    main()
