"""
contain a list of important move tile target
"""
from typing import Any

from ecs import Component
class PathComp(Component):
    def __init__(self,move_list:list[tuple[int,int]]|None=None):
        self.move_list = move_list if move_list is not None else []
    def to_dict(self) -> dict[str, Any]:
        return {"move_list":self.move_list}
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "PathComp":
        move_list = [
            (int(position[0]), int(position[1]))
            for position in data.get("move_list", [])
        ]
        return cls(move_list=move_list)