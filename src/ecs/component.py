from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any
COMPONENT_REGISTRY: dict[str, type[Component]] = {}


class Component(ABC):
    def __init_subclass__(cls,**kwargs):
        super().__init_subclass__(**kwargs)
        COMPONENT_REGISTRY[cls.__name__] = cls
    @abstractmethod
    def to_dict(self) -> dict[str, Any]:
        pass
    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict[str, Any]) -> "Component":
        pass
class exampleComponent(Component):
    def __init__(self, value: int):
        self.exampleValue = value
    def to_dict(self) -> dict[str, Any]:
        return {"exampleValue": self.exampleValue}
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "exampleComponent":
        return cls(value=data["exampleValue"])