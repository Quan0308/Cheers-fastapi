from dataclasses import dataclass
from .postition import Position
@dataclass
class Drinker:
    position: Position
    value: float