from typing import Any

import ecs
class TileComp(ecs.Component):
    def __init__(self,
        terrain_type:str,
        move_cost:int,
        buildable:bool
        ):
        self.terrain_type=terrain_type
        self.move_cost=move_cost
        self.buildable=buildable
    def to_dict(self) -> dict[str, Any]:
        return {
            "terrain_type":self.terrain_type,
            "move_cost":self.move_cost,
            "buildable":self.buildable
        }
    @classmethod
    def from_dict(cls, data: dict[str, Any]):
        return cls(terrain_type=data["terrain_type"],move_cost=data["move_cost"],buildable=data["buildable"])
