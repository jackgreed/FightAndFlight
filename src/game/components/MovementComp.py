from ecs.component import Component
from typing import Any
class MovementComp(Component):
    def __init__(self,target_x:int,target_y:int):
        self.target_x=target_x
        self.target_y=target_y
    def to_dict(self) -> dict[str, Any]:
        return {"target_x": self.target_x, "target_y": self.target_y}
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "MovementComp":
        return cls(target_x=data["target_x"], target_y=data["target_y"])
