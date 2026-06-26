from game.world_manager import WorldManager
from ecs.world import World
from game.world_map import WorldMapGenerator
from game.colony_map import ColonyMapGenerator
from game.components import WorldTileComp,PositionComp
class MapInitializer:
    def __init__(self,world_manager:WorldManager):
        self.world_manager=world_manager
        self.world_map=None
    def set_world_map(self,world:World):
        self.world_map=world
    def initialize_specific_world_map(self,size:tuple[int,int],noise_level:dict[str,float],seed:int,name:str="world_map"):
        self.world_map=self.world_manager.create_world(name)
        gen=WorldMapGenerator(
            world=self.world_map,
            size=size,
            noise_level=noise_level,
            seed=seed
        )
        gen.generate_world_tile()
        return self.world_map
    def initalize_specific_colony(self,pos:tuple[int,int],size:tuple[int,int],seed:int,name:str="colony"):
        if self.world_map is None:
            print("[ERROR]NO EXISTING WORLD MAP")
            return None
        x=pos[0]
        y=pos[1]
        size_x=size[0]
        size_y=size[1]
        location=None
        for entity in self.world_map.get_entities_with(WorldTileComp):
            map_pos=entity.get_component(PositionComp)
            if x==map_pos.x and y==map_pos.y:#type:ignore
                location=entity
                break
        if location is None:
            print("[ERROR]POSTION NOT ON MAP")
            return None
        world=self.world_manager.create_world(name)
        gen=ColonyMapGenerator(
            world=world,
            size=size,
            seed=seed,
            localWorldTileComp=location.get_component(WorldTileComp)#type:ignore
        )
        gen.generate_colony_map()
        return world