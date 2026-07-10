from typing import Any

from ecs import World
from engine.command_queue import Command
from game.components import InfoPanelComp
from game.interactions import ActionProxy


class OpenInteractableMenuCommand(Command):
    def __init__(self, world_id: str, target_entity_id: str):
        super().__init__(world_id=world_id)
        self.target_entity_id = target_entity_id

    def execute(self, world: World):
        """Create or update the interaction menu info panel."""
        target = world.get_entity(self.target_entity_id)
        if target is None:
            return

        if not ActionProxy.is_interactable(target):
            return

        actions = ActionProxy.get_enabled_action_ids(target)
        actions.append("move_to")
        if not actions:
            return
        
        title = target.get_name()
        info = "\n".join(actions)
        panels = world.get_entities_with(InfoPanelComp)

        if not panels:
            panel = world.create_entity(name="interaction_menu")
            panel.add_component(
                InfoPanelComp(
                    panel_id="interaction_menu",
                    title=title,
                    info=info,
                )
            )
            return

        comp = panels[0].get_component(InfoPanelComp)
        if comp is None:
            return
        comp.panel_id = "interaction_menu"
        comp.title = title
        comp.info = info

    def to_dict(self):
        """Serialize command."""
        return {
            "type": "OpenInteractableMenuCommand",
            "world_id": self.world_id,
            "target_entity_id": self.target_entity_id,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "OpenInteractableMenuCommand":
        """Deserialize command."""
        return cls(
            world_id=data["world_id"],
            target_entity_id=data["target_entity_id"],
        )
