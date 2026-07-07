from typing import Any

from ecs import Component
class InteractableComp(Component):
    def __init__(self,actions:dict[str,bool]|None=None):
        self.actions=actions or {}
    def to_dict(self) -> dict[str, Any]:
        return {
            "actions":self.actions
        }
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "InteractableComp":
        """Create InteractableComp from serialized data."""
        actions = data.get("actions", {})
        if actions is None:
            actions = {}
        if not isinstance(actions, dict):
            raise ValueError("InteractableComp.actions must be a dict")
        return cls({str(action_id): bool(enabled) for action_id, enabled in actions.items()})