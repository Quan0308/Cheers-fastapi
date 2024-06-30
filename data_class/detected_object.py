from dataclasses import dataclass
from PIL import Image
from .postition import Position

@dataclass
class DetectedObject:
    position: Position
    type: str
    value: float
    image: Image.Image
