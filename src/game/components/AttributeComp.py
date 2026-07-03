from ecs.component import Component
from typing import Any
class AttributeComp(Component):
    def __init__(self,speed:float=1.0,specialMutiplier=None):
        self.speed=speed
        self.specialMutiplier:dict[str,float]=specialMutiplier if specialMutiplier is not None else {}
    def to_dict(self) -> dict[str, Any]:
        return {"speed": self.speed,
                "specialMutiplier": self.specialMutiplier
                }
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "AttributeComp":
        return cls(speed=data["speed"],specialMutiplier=data["speicialMutiplier"])
