from enum import Enum, auto


class Turn(Enum):
    """Class to represent a turn in chess."""

    WHITE = auto()
    BLACK = auto()

    def is_white(self):
        return self.name == "WHITE"
