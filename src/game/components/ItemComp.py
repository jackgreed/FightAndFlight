from typing import Any

from ecs import Component
class ItemComp(Component):
    def __init__(self,item_id:str,weight:float,category:str="uncategorized"):
        self.item_id=item_id
        self.weight=weight if weight >=0 else 1
        self.category=category
    def to_dict(self) -> dict[str, Any]:
        return {
            "item_id":self.item_id,
            "weight":self.weight,
            "category":self.category
        }
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ItemComp":
        return cls(
            item_id=data["item_id"],
            weight=data["weight"],
            category=data.get("category", "uncategorized")
        )