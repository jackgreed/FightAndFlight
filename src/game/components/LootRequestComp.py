from typing import Any

from ecs import Component
class LootRequestComp(Component):
    def __init__(
        self,
        source_entity_id: str,
        receiver_entity_id: str,
        context: str = "default",
    ):
        self.source_entity_id=source_entity_id
        self.receiver_entity_id=receiver_entity_id
        self.context=context
    def to_dict(self) -> dict[str, Any]:
        return {
            "source_entity_id":self.source_entity_id,
            "receiver_entity_id":self.receiver_entity_id,
            "context":self.context
        }
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "LootRequestComp":
        return cls(
            data.get("source_entity_id",data.get("source")),
            data.get("receiver_entity_id",data.get("target")),
            data.get("context","default")
        )
