from typing import Any

from ecs import Component
class NpcMovementComp(Component):
    """
    idle:just stop
    wander:walk around randomly
    
    """
    def __init__(
        self,
        mode: str = "idle",
        target_entity_id: str | None = None,
        target_position: tuple[int, int] | None = None,
        home_position: tuple[int, int] | None = None,
        wander_radius: int = 5,
        decision_cooldown: int = 0,
    ):
        self.mode = mode
        self.target_entity_id = target_entity_id
        self.target_position = target_position
        self.home_position = home_position
        self.wander_radius = wander_radius
        self.decision_cooldown = decision_cooldown
    def to_dict(self) -> dict[str, Any]:
        """to dict for serialization"""
        return {
            "mode":self.mode,
            "target_entity_id":self.target_entity_id,
            "target_position":self.target_position,
            "home_position":self.home_position,
            "wander_radius":self.wander_radius,
            "decision_cooldown":self.decision_cooldown
        }
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "NpcMovementComp":
        """
        from dict to NpcMovementComp instance
        """
        target_position = data.get("target_position")
        if target_position is not None:
            target_position = (target_position[0], target_position[1])
        home_position = data.get("home_position")
        if home_position is not None:
            home_position = (home_position[0], home_position[1])
        return cls(mode=data.get("mode", "idle"),
                   target_entity_id=data.get("target_entity_id"),
                   target_position=target_position,
                   home_position=home_position,
                   wander_radius=data.get("wander_radius", 5),
                   decision_cooldown=data.get("decision_cooldown", 0)
                   )