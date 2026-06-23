from engine.command_queue import Command
from game.components import MovementComp
class MovementCommand(Command):
    def __init__(self, world_id: str, entity_id: str, target_x: int, target_y: int):
        super().__init__(world_id)
        self.world_id = world_id
        self.entity_id = entity_id
        self.target_x = target_x
        self.target_y = target_y

    def execute(self, world):
        entity = world.get_entity(self.entity_id)
        if entity is not None:
            if entity.has_component(MovementComp):
                movement_comp = entity.get_component(MovementComp)
                movement_comp.target_x = self.target_x
                movement_comp.target_y = self.target_y
            else:
                entity.add_component(MovementComp(target_x=self.target_x, target_y=self.target_y))

    def to_dict(self):
        return {
            "type": "MovementCommand",
            "world_id": self.world_id,
            "entity_id": self.entity_id,
            "target_x": self.target_x,
            "target_y": self.target_y,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            world_id=data["world_id"],
            entity_id=data["entity_id"],
            target_x=data["target_x"],
            target_y=data["target_y"],
        )