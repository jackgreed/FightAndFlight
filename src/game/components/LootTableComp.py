from typing import Any
import copy
from ecs import Component
class LootTableComp(Component):
    def __init__(self,
                 common_loot:dict[str,float]|None=None,
                 specialized_loot: (dict[str, dict[str, float]] | None) = None,):
        if common_loot is not None and not isinstance(common_loot,dict):
            raise ValueError("common_loot must be a dict")
        if specialized_loot is not None and not isinstance(specialized_loot,dict):
            raise ValueError("specialized_loot must be a dict")
        self.common_loot=copy.deepcopy(common_loot or {})
        self.specialized_loot=copy.deepcopy(specialized_loot or {})
        self._validate_loot_table(self.common_loot)
        for context,loot in self.specialized_loot.items():
            if not isinstance(context,str) or not context:
                raise ValueError("Invalid specialized loot context")
            if not isinstance(loot,dict):
                raise ValueError(
                    f"Specialized loot table must be a dict: {context}"
                )
            self._validate_loot_table(loot)
    def to_dict(self) -> dict[str, Any]:
        """return deepcopy version of dicts"""
        return {
            "common_loot": copy.deepcopy(
                self.common_loot
            ),
            "specialized_loot": copy.deepcopy(
                self.specialized_loot
            ),
        }
    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> "LootTableComp":
        """create dict from data"""
        return cls(
            common_loot=copy.deepcopy(
                data.get("common_loot", {})
            ),
            specialized_loot=copy.deepcopy(
                data.get("specialized_loot", {})
            ),
        )

    @staticmethod
    def _validate_loot_table(loot_table:dict[str,float])->None:
        """Validate item IDs and non-negative drop rates."""
        for loot_id,loot_rate in loot_table.items():
            if not isinstance(loot_id,str) or not loot_id:
                raise ValueError("Invalid loot item ID")
            if (
                isinstance(loot_rate,bool)
                or not isinstance(loot_rate,(int,float))
                or loot_rate<0
            ):
                raise ValueError(
                    f"Invalid drop rate: {loot_id}"
                )
