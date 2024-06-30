from dataclasses import dataclass
from .postition import Position

@dataclass
class Product:
    position: Position
    brand: object
    type: str