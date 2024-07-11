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
        number_types: int,
    ) -> None:
        if not (0 < population_density < 1):
            raise ValueError(
                f"Invalid population_density {population_density}."
                "It must be between 0 and 1 (exclusive)."
            )

        if not (0 <= happiness_threshold <= 1):
            raise ValueError(
                f"Invalid happiness_threshold {happiness_threshold}."
                "It must be between 0 and 1 (inclusive)."
            )

        self.population_density = population_density
        self.happiness_threshold = happiness_threshold
        self.number_types = number_types

        self.city = City(city_size)

        self.populate()

    def __repr__(self) -> str:
        repr_ = "\n".join(
            "".join(str(type_) if type_ is not None else "•" for type_ in row)
            for row in self.generate_type_map()
        )
        return repr_

    def populate(self) -> None:
        number_inhabitant_per_type = int(
            (self.population_density * self.city.size_x * self.city.size_y)
            // self.number_types
        )
        for type_ in range(self.number_types):
            for _ in range(number_inhabitant_per_type):
                inhabitant = Inhabitant(type_, self.happiness_threshold)
                self.city.add_inhabitant(inhabitant, self._get_empty_location())

    def update(self) -> None:
        location = choice(list(self.city.inhabited_locations))
        inhabitant = self.city[location]
        neighbors = self._get_neighbors_type(location)
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
            new_neighbors = self._get_neighbors_type(new_location)
            if inhabitant.is_happy(new_neighbors):
                return new_location

        return last_checked_location

    def _get_neighbors_type(self, location: tuple[int, int]) -> list[int]:
        neighbor_offsets = product([-1, 0, 1], repeat=2)
        neighbors_type = []
        for di, dj in neighbor_offsets:
            if (di, dj) != (0, 0):
                new_location = (location[0] + di, location[1] + dj)
                if self.city.is_location_valid(new_location) and self.city.is_inhabited(
                    new_location
                ):
                    neighbors_type.append(self.city[new_location].type)
        return neighbors_type

    def generate_type_map(self) -> list[list[int]]:
        def _get_type(location):
            if self.city.is_inhabited(location):
                return self.city[location].type
            return None

        return [
            [_get_type((i, j)) for i in range(self.city.size_x)]
            for j in range(self.city.size_y)
        ]
