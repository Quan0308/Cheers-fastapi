from dataclasses import dataclass
from .postition import Position

@dataclass
class Staff:
    position: Position
    value: float