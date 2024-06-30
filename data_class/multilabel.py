from dataclasses import dataclass
from .postition import Position
@dataclass
class MultilabelObject:
    position: Position
    type: str
    value: float
    brands: object