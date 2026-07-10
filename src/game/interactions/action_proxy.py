from game.components import InteractableComp
from game.interactions.action_registry import ACTION_REGISTRY


class ActionProxy:
    """唯一 Action 代理，负责查表并构造 Command。"""

    @classmethod
    def is_interactable(cls, entity) -> bool:
        """Return whether entity can expose an interaction menu."""
        return entity.get_component(InteractableComp) is not None

    @classmethod
    def get_enabled_action_ids(cls, entity) -> list[str]:
        """Return enabled action ids that are registered."""
        interactable = entity.get_component(InteractableComp)
        if interactable is None:
            return []

        result = []
        for action_id, enabled in interactable.actions.items():
            if not enabled or action_id not in ACTION_REGISTRY:
                continue
            result.append(action_id)
        return result

    @classmethod
    def get_label(cls, action_id: str) -> str:
        """Return display label for an action id."""
        action = ACTION_REGISTRY.get(action_id)
        if action is None:
            return action_id
        return action.label

    @classmethod
    def _get_command_type(cls, command_type: str):
        """Resolve command class lazily to avoid package import cycles."""
        if command_type == "InspectCommand":
            from game.commands.InspectCommand import InspectCommand
            return InspectCommand
        return None

    @classmethod
    def create_command(
        cls,
        action_id: str,
        world_id: str,
        actor_entity_id: str | None,
        target_entity_id: str,
        args: dict | None = None,
    ):
        """Create command for action id."""
        action = ACTION_REGISTRY.get(action_id)
        if action is None:
            return None

        command_cls = cls._get_command_type(action.command_type)
        if command_cls is None:
            return None

        if action.command_type == "InspectCommand":
            return command_cls(world_id, target_entity_id)

        return None
