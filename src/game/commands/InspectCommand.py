from typing import Any

from ecs import World
from engine.command_queue import Command
from game.components import InfoPanelComp


class InspectCommand(Command):
    # just show entity info
    def __init__(self, world_id: str, entity_id: str):
        super().__init__(world_id=world_id)
        self.entity_id = entity_id
        
    def execute(self, world: World):
        """Create or update the unique info panel for the inspected entity."""
        entity = world.get_entity(self.entity_id)
        if entity is None:
            return

        title = entity.get_name()
        info = self._build_info(entity)
        panels = world.get_entities_with(InfoPanelComp)
        if not panels:
            panel = world.create_entity(name="panel")
            panel.add_component(
                InfoPanelComp(
                    panel_id="panel",
                    title=title,
                    info=info,
                )
            )
        else:
            comp = panels[0].get_component(InfoPanelComp)
            if comp is None:
                return
            comp.panel_id = "panel"
            comp.title = title
            comp.info = info

    def to_dict(self):
        """Serialize command."""
        return {
            "type": "InspectCommand",
            "world_id": self.world_id,
            "entity_id": self.entity_id,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "InspectCommand":
        """Deserialize command."""
        return cls(
            world_id=data["world_id"],
            entity_id=data["entity_id"],
        )

    @staticmethod
    def _build_info(entity) -> str:
        """Build display text from the entity and its components."""
        lines = [
            f"id: {entity.id}",
            f"name: {entity.get_name()}",
        ]

        for component_name, component in entity.components.items():
            lines.append(f"{component_name}: {component.to_dict()}")

        return "\n".join(lines)
