from typing import Any

from ecs import World
from engine.command_queue import Command
from game.components import InfoPanelComp


class CloseInfoPanelCommand(Command):
    def __init__(self, world_id: str, panel_id: str):
        super().__init__(world_id=world_id)
        self.panel_id = panel_id

    def execute(self, world: World):
        """Remove the info panel matching panel_id."""
        panels = world.get_entities_with(InfoPanelComp)

        for panel in panels:
            comp = panel.get_component(InfoPanelComp)
            if comp is None:
                continue
            if comp.panel_id == self.panel_id:
                world.destroy_entity(panel.id)
                return

    def to_dict(self):
        """Serialize command."""
        return {
            "type": "CloseInfoPanelCommand",
            "world_id": self.world_id,
            "panel_id": self.panel_id,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "CloseInfoPanelCommand":
        """Deserialize command."""
        return cls(
            world_id=data["world_id"],
            panel_id=data["panel_id"],
        )
