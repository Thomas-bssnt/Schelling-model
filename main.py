from dataclasses import dataclass
from random import choice, shuffle

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


@dataclass(frozen=True)
class Location:
    x: int
    y: int

    def __add__(self, other):
        return Location(self.x + other.x, self.y + other.y)


class House:
    def __init__(self, location: Location) -> None:
        self.location = location
        self.inhabitant_id = None

    def __repr__(self) -> str:
        return f"House({self.location}, {self.inhabitant_id})"

    @property
    def is_inhabited(self) -> bool:
        return self.inhabitant_id is not None


class City:
    def __init__(self, size: tuple[int, int]) -> None:
        self.size_x = size[0]
        self.size_y = size[1]
        self.grid = [
            [House(Location(i, j)) for i in range(self.size_x)]
            for j in range(self.size_y)
        ]
        self.empty_locations = {
            Location(i, j) for i in range(self.size_x) for j in range(self.size_y)
        }

    def __getitem__(self, location: Location) -> House:
        return self.grid[location.y][location.x]

    def populate(self, population) -> None:
        for inhabitant in population.values():
            inhabitant.move(self, self.get_empty_location())

    def get_empty_location(self) -> Location:
        return choice(tuple(self.empty_locations))

    def is_location_valid(self, location: Location) -> bool:
        return 0 <= location.x < self.size_x and 0 <= location.y < self.size_y


class Inhabitant:
    def __init__(self, id_: int, type_: int, happiness_threshold: float) -> None:
        self.id = id_
        self.type = type_
        self.happiness_threshold = happiness_threshold
        self.location = None

    def __repr__(self) -> str:
        return f"Inhabitant({self.id}, {self.type})"

    def is_happy(self, neighbors_type: list[int]) -> bool:
        if len(neighbors_type) == 0:
            return False
        return (
            neighbors_type.count(self.type) / len(neighbors_type)
            >= self.happiness_threshold
        )

    def move(self, city: City, new_location: Location) -> None:
        if self.location is not None:
            city.empty_locations.add(self.location)
            city[self.location].inhabitant_id = None
        city.empty_locations.remove(new_location)
        city[new_location].inhabitant_id = self.id
        self.location = new_location


class Schelling:
    def __init__(
        self,
        city_size: tuple[int, int],
        population_density: float,
        happiness_threshold: float,
    ) -> None:
        self.city_size = city_size

        # Initialization of the city
        self.city = City(city_size)

        # Initialization of the population
        n_inhabitant = int(population_density * city_size[0] * city_size[1])
        self.population = {
            id_: Inhabitant(id_, 0, happiness_threshold)
            for id_ in range(n_inhabitant // 2)
        } | {
            id_: Inhabitant(id_, 1, happiness_threshold)
            for id_ in range(n_inhabitant // 2, n_inhabitant)
        }

        # Populate the city
        self.city.populate(self.population)

    def __repr__(self) -> str:
        repr_ = "\n".join(
            "".join(
                ("O" if type_ == 0 else "X" if type_ == 1 else "•") for type_ in row
            )
            for row in self.generate_type_map()
        )
        return repr_

    def update(self) -> None:
        inhabitant = choice(list(self.population.values()))
        neighbors = self._get_neighbors_color(inhabitant.location)
        if not inhabitant.is_happy(neighbors):
            new_location = self._get_new_location(inhabitant)
            inhabitant.move(self.city, new_location)

    def _get_new_location(self, inhabitant: Inhabitant) -> Location:
        empty_locations = list(self.city.empty_locations)
        shuffle(empty_locations)

        last_checked_location = None
        for new_location in empty_locations:
            last_checked_location = new_location
            new_neighbors = self._get_neighbors_color(new_location)
            if inhabitant.is_happy(new_neighbors):
                return new_location

        # Return the last checked location if no suitable location is found
        return last_checked_location

    def _get_neighbors_color(self, location: Location) -> list[int]:
        neighbor_offsets = [
            (-1, -1),
            (-1, 0),
            (-1, 1),
            (0, -1),
            (0, 1),
            (1, -1),
            (1, 0),
            (1, 1),
        ]
        neighbors_color = []
        for di, dj in neighbor_offsets:
            new_location = location + Location(di, dj)
            if (
                self.city.is_location_valid(new_location)
                and self.city[new_location].is_inhabited
            ):
                neighbors_color.append(
                    self.population[self.city[new_location].inhabitant_id].type
                )
        return neighbors_color

    def generate_type_map(self) -> list[list[int]]:

        def _get_type(location):
            house = self.city[location]
            if house.is_inhabited:
                return self.population[house.inhabitant_id].type
            return None

        return [
            [_get_type(Location(i, j)) for i in range(self.city_size[0])]
            for j in range(self.city_size[1])
        ]


class Visualizer:
    COLOR_TYPE_0 = (93, 147, 183)
    COLOR_TYPE_1 = (14, 61, 144)
    COLOR_EMPTY = (255, 255, 255)

    def __init__(self, schelling: Schelling) -> None:
        self.schelling = schelling
        self.fig, self.ax = plt.subplots(figsize=(6, 6))
        self.ax.axes.xaxis.set_ticks([])
        self.ax.axes.yaxis.set_ticks([])
        self.fig.tight_layout()
        self.im = self.ax.imshow(self.generate_color_map())

    def generate_color_map(self) -> np.ndarray:
        type_map = self.schelling.generate_type_map()

        def get_color(type_):
            if type_ == 0:
                return self.COLOR_TYPE_0
            elif type_ == 1:
                return self.COLOR_TYPE_1
            else:
                return self.COLOR_EMPTY

        return np.array([[get_color(type_) for type_ in row] for row in type_map])

    def update(self, _, updates_per_frame) -> list:
        for _ in range(updates_per_frame):
            self.schelling.update()
        self.im.set_data(self.generate_color_map())
        return [self.im]

    def animate(self, updates_per_frame=100, interval=200) -> None:
        anim = FuncAnimation(
            self.fig,
            self.update,
            interval=interval,
            fargs=(updates_per_frame,),
        )
        plt.show()


def main() -> None:
    city_size = (50, 50)
    population_density = 0.9
    happiness_threshold = 0.5

    schelling = Schelling(city_size, population_density, happiness_threshold)
    visualizer = Visualizer(schelling)
    visualizer.animate(updates_per_frame=100, interval=200)


if __name__ == "__main__":

    main()
