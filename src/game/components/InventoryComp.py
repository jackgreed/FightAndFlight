from typing import Any

from ecs import Component
class InventoryComp(Component):
    def __init__(self,capacity:int=8,max_weight:float=20.0,slots:list[str|None]|None=None):
        self.capacity=capacity if capacity>=0 else 8
        self.max_weight=max_weight if max_weight>=0 else 20.0
        self.slots=(slots if slots is not None and len(slots)==self.capacity else [None]*capacity)
    def to_dict(self) -> dict[str, Any]:
        return {
            "capacity":self.capacity,
            "max_weight":self.max_weight,
            "slots":self.slots
        }
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "InventoryComp":
        return cls(
            capacity=data.get("capacity",8),
            max_weight=data.get("max_weight",20.0),
            slots=data.get("slots")
        )