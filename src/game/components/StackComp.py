from typing import Any

from ecs import Component
class StackComp(Component):
    def __init__(
        self,
        quantity: int,
        max_quantity: int,
    ):
        
        self.max_quantity = max_quantity if max_quantity>0 else 1
        self.quantity = quantity if quantity<=self.max_quantity and quantity>=0 else 1
    def to_dict(self) -> dict[str, Any]:
        return {
            "quantity":self.quantity,
            "max_quantity":self.max_quantity
        }
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "StackComp":
        return cls(
            quantity=data["quantity"],
            max_quantity=data["max_quantity"]
        )