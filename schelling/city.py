from .inhabitant import Inhabitant


class City:
    def __init__(self, size: tuple[int, int]) -> None:
        self.size_x = size[0]
        self.size_y = size[1]
        self.grid = [[None for _ in range(self.size_x)] for _ in range(self.size_y)]
        self.empty_locations = {
            (i, j) for i in range(self.size_x) for j in range(self.size_y)
        }
        self.inhabited_locations = set()

    def __getitem__(self, location: tuple[int, int]) -> Inhabitant | None:
        x, y = location
        return self.grid[y][x]

    def __setitem__(self, location: tuple[int, int], value: Inhabitant | None) -> None:
        x, y = location
        self.grid[y][x] = value

    def is_location_valid(self, location: tuple[int, int]) -> bool:
        x, y = location
        return 0 <= x < self.size_x and 0 <= y < self.size_y

    def is_inhabited(self, location: tuple[int, int]) -> bool:
        return self[location] is not None

    def add_inhabitant(self, inhabitant: Inhabitant, location: tuple[int, int]) -> None:
        if self.is_inhabited(location):
            raise ValueError(f"Location {location} is inhabited")

        self[location] = inhabitant
        self.empty_locations.remove(location)
        self.inhabited_locations.add(location)

    def move_inhabitant(
        self,
        old_location: tuple[int, int],
        new_location: tuple[int, int],
    ) -> None:
        if not self.is_inhabited(old_location):
            raise ValueError(f"Location {old_location} is empty")

        if self.is_inhabited(new_location):
            raise ValueError(f"Location {new_location} is inhabited")

        self[old_location], self[new_location] = self[new_location], self[old_location]
        self.empty_locations.add(old_location)
        self.empty_locations.remove(new_location)
        self.inhabited_locations.remove(old_location)
        self.inhabited_locations.add(new_location)
