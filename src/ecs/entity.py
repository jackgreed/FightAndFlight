from __future__ import annotations
from typing import Any
import uuid
from .component import Component, COMPONENT_REGISTRY
class Entity:
    def __init__(self,id=None,name="If you see this, there is a bug",components=None):
        self.id=str(uuid.uuid4()) if id == None else str(id)  
        self.name=name
        if self.name == "If you see this, there is a bug":
            print(f"Warning: Entity {self.id} has default name. Please set a name using set_name() method.")
        self.components: dict[str, Component] = components if components is not None else {}
    def get_name(self) -> str:
        return self.name
    def set_name(self, name: str):
        self.name = name
        return self
    def add_component(self, component: Component):
        self.components[component.__class__.__name__] = component
        return self
    def get_component(self, component_type: type[Component]) -> Component | None:
        return self.components.get(component_type.__name__)
    def has_component(self, component_type: type[Component]) -> bool:
        return component_type.__name__ in self.components
    def remove_component(self, component_type: type[Component]):
        if component_type.__name__ in self.components:
            del self.components[component_type.__name__]
        return self
    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,  
            "components": {name: comp.to_dict() for name, comp in self.components.items()}
        }
    @classmethod
    def from_dict(cls, data: dict[str, Any]):
        entity = cls(id=data["id"], name=data["name"])
        for comp_name, comp_data in data["components"].items():
            comp_cls = COMPONENT_REGISTRY.get(comp_name)
            if comp_cls:
                component = comp_cls.from_dict(comp_data)
                entity.add_component(component)
        return entity

