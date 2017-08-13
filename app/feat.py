__all__ = [
    "Feat",
    "Flaw",
]

from typing import List, Optional, Union

from app.base import DndBase


class Feat(DndBase):
    def __init__(self, name: str, description: str,
                 prerequisites: Optional[List[Union[str, "Feat"]]] = None):
        super().__init__()
        self.name = name
        self.description = description
        self.prerequisites = prerequisites

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)


class Flaw(Feat):
    def __init__(self, name: str, description: str,
                 feat: Feat):
        super().__init__(name, description)
        self.feat = feat

    def __str__(self):
        return f"{self.name}({self.feat})"
