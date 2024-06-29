from dataclasses import dataclass
from PIL import Image
from .postition import Position

@dataclass
class DetectedObject:
    position: Position
    type: str
    image: Image.Image
