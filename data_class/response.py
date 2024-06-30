from dataclasses import dataclass
from .product import Product
from .staff import Staff
from .drinker import Drinker

@dataclass
class Response:
    products: list[Product]
    staffs: list[Staff]
    drinker: list[Drinker]