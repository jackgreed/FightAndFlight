from ecs.world import World
from engine.command_queue import Command
from game.components import PathComp,PathRequestComp
class PathfindCommand(Command):
    def __init__(self,world_id:str,entity_id:str,target_x:int,target_y:int):
        super().__init__(world_id)
        self.entity_id=entity_id
        self.target_x=target_x
        self.target_y=target_y
    def execute(self, world: World):
        entity=world.get_entity(self.entity_id)
        if entity is None or not entity.has_component(PathComp):
            return
        entity.add_component(PathRequestComp(self.target_x,self.target_y))
    def to_dict(self) -> dict:
        return {
            "type": "PathfindCommand",
            "world_id": self.world_id,
            "entity_id": self.entity_id,
            "target_x": self.target_x,
            "target_y": self.target_y,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "PathfindCommand":
        return cls(
            world_id=data["world_id"],
            entity_id=data["entity_id"],
            target_x=int(data["target_x"]),
            target_y=int(data["target_y"]),
        )