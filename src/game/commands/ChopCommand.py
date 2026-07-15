from typing import Any

from ecs.world import World
from engine.command_queue import Command
from game.components import InteractableComp,LootRequestComp
class ChopCommand(Command):
    def __init__(self, world_id: str,actor_entity_id:str,target_entity_id:str,method:str|None=None):
        super().__init__(world_id)
        self.actor_entity_id=actor_entity_id
        self.target_entity_id=target_entity_id
        self.method=method or None
    def execute(self, world: World):
        #check is entity exist
        actor=world.get_entity(self.actor_entity_id)
        target=world.get_entity(self.target_entity_id)
        if actor is None or target is None:
            return
            #means before the chop,either the actor or the target died or erorr occurs 
        interaction:InteractableComp|None=target.get_component(InteractableComp)#type:ignore
        #loot_table:LootTableComp|None=target.get_component(LootTableComp)#type:ignore
        if interaction is None :#or loot_table is None:
            return
        if "chop" not in interaction.actions or not interaction.actions["chop"]:
            return
        request=world.create_entity(name="loot_request")
        request.add_component(
            LootRequestComp(
                source_entity_id=self.target_entity_id,
                receiver_entity_id=self.actor_entity_id,
                context=self.method or "chop",
            )
        )
    def to_dict(self):
        return {
            "world_id":self.world_id,    
            "actor_entity_id":self.actor_entity_id,
            "target_entity_id":self.target_entity_id,
            "method":self.method
        }
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ChopCommand":
        return cls(data["world_id"],data["actor_entity_id"],data["target_entity_id"],data.get("method"))
        
