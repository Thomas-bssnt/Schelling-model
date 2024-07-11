from itertools import product
from random import choice, shuffle
from .city import City
from .inhabitant import Inhabitant


class Schelling:
    def __init__(
        self,
        city_size: tuple[int, int],
        population_density: float,
        happiness_threshold: float,
    ) -> None:
        self.city_size = city_size

        self.city = City(city_size)

        n_inhabitant = int(population_density * city_size[0] * city_size[1])
        self.population = {
            id_: Inhabitant(id_, 0, happiness_threshold)
            for id_ in range(n_inhabitant // 2)
        } | {
            id_: Inhabitant(id_, 1, happiness_threshold)
            for id_ in range(n_inhabitant // 2, n_inhabitant)
        }

        self.populate()

    def __repr__(self) -> str:
        repr_ = "\n".join(
            "".join(
                ("O" if type_ == 0 else "X" if type_ == 1 else "•") for type_ in row
            )
            for row in self.generate_type_map()
        )
        return repr_

    def populate(self) -> None:
        for inhabitant in self.population.values():
            self.city.add_inhabitant(inhabitant, self._get_empty_location())

    def update(self) -> None:
        location = choice(list(self.city.inhabited_locations))
        inhabitant = self.city[location]
        neighbors = self._get_neighbors_color(location)
        if not inhabitant.is_happy(neighbors):
            new_location = self._get_new_location(inhabitant)
            self.city.move_inhabitant(location, new_location)

    def _get_empty_location(self) -> tuple[int, int]:
        return choice(tuple(self.city.empty_locations))

    def _get_new_location(self, inhabitant: Inhabitant) -> tuple[int, int]:
        empty_locations = list(self.city.empty_locations)
        shuffle(empty_locations)

        last_checked_location = None
        for new_location in empty_locations:
            last_checked_location = new_location
            new_neighbors = self._get_neighbors_color(new_location)
            if inhabitant.is_happy(new_neighbors):
                return new_location

        return last_checked_location

    def _get_neighbors_color(self, location: tuple[int, int]) -> list[int]:
        neighbor_offsets = product([-1, 0, 1], repeat=2)
        print(list(neighbor_offsets))
        neighbors_color = []
        for di, dj in neighbor_offsets:
            if (di, dj) != (0, 0):
                new_location = (location[0] + di, location[1] + dj)
                if self.city.is_location_valid(new_location) and self.city.is_inhabited(
                    new_location
                ):
                    neighbors_color.append(self.city[new_location].type)
        return neighbors_color

    def generate_type_map(self) -> list[list[int]]:
        def _get_type(location):
            if self.city.is_inhabited(location):
                return self.population[self.city[location].id].type
            return None

        return [
            [_get_type((i, j)) for i in range(self.city_size[0])]
            for j in range(self.city_size[1])
        ]
