from __future__ import annotations
from typing import Any
from .entity import Entity
from .component import Component, COMPONENT_REGISTRY
class World:
    def __init__(self):
        self.entities: dict[str, Entity] = {}
    def create_entity(self,name="If you see this, there is a bug",components=None) -> Entity:
        entity = Entity(name=name,components=components)
        self.entities[entity.id] = entity
        return entity
    def destroy_entity(self, entity_id: str):
        if entity_id in self.entities:
            del self.entities[entity_id]
    def get_entities_with(self, *args: type[Component]) -> list[Entity]:
        result = []
        for entity in self.entities.values():
            if all(entity.has_component(comp) for comp in args):
                result.append(entity)
        return result
    def get_entity(self, entity_id: str) -> Entity | None:
        return self.entities.get(entity_id)
    def to_dict(self) -> dict[str, Any]:
        return {
            "entities": {entity_id: entity.to_dict() for entity_id, entity in self.entities.items()}
        }
    @classmethod
    def from_dict(cls, data: dict[str, Any]):
        world = cls()
        world.entities = {entity_id: Entity.from_dict(entity_data) for entity_id, entity_data in data["entities"].items()}
        return world