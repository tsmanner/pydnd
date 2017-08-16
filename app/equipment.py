__all__ = [
    "Equipment",
]

from app.base import DndBase


class Equipment(DndBase):
    def __init__(self, name: str, price: int):
        super().__init__()
        self.name = name
        self.price = price

    def __str__(self):
        return f"{self.name}"
