class Inhabitant:
    def __init__(self, type_: int, happiness_threshold: float) -> None:
        self.type = type_
        self.happiness_threshold = happiness_threshold

    def __repr__(self) -> str:
        return f"Inhabitant({self.type})"

    def is_happy(self, neighbors_type: list[int]) -> bool:
        if len(neighbors_type) == 0:
            return False
        return (
            neighbors_type.count(self.type) / len(neighbors_type)
            >= self.happiness_threshold
        )
