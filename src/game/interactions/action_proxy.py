import inspect

from engine.command_queue import COMMAND_REGISTRY
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
    def create_command(
        cls,
        action_id: str,
        data: dict,
    ):
        """Create command for action id from provided data."""
        action = ACTION_REGISTRY.get(action_id)
        if action is None:
            return None

        command_cls = COMMAND_REGISTRY.get(action.command_type)
        if command_cls is None:
            return None

        command_args = {}
        parameters = inspect.signature(command_cls).parameters
        for name, parameter in parameters.items():
            if name in data:
                command_args[name] = data[name]
                continue
            if parameter.default is inspect.Parameter.empty:
                return None

        return command_cls(**command_args)
