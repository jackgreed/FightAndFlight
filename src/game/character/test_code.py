from ecs import World
from game.components import PathComp,CharacterComp,PositionComp,SpriteComp,AttributeComp,TileComp

def test_init(world:World):
    """
    test init
    """
    tile_list=find_possible_tile(world=world)
    list_size=len(tile_list)
    if list_size <2:
        print("map too small")
        return
    user=world.create_entity("user")
    npc=world.create_entity("npc")
    user.add_component(CharacterComp(True,"42")).add_component(PositionComp(tile_list[0][0],tile_list[0][1])).add_component(SpriteComp()).add_component(AttributeComp(1)).add_component(PathComp())
    npc.add_component(CharacterComp(False,None)).add_component(PositionComp(tile_list[1][0],tile_list[1][1])).add_component(SpriteComp()).add_component(AttributeComp(1)).add_component(PathComp())
def find_possible_tile(world:World):
    """
    find moveable tile
    """
    result:list[tuple[int,int]]=[]
    for entity in world.get_entities_with(TileComp):
        if entity.get_component(TileComp).move_cost !=999: #type:ignore
            x=entity.get_component(PositionComp).x#type: ignore
            y=entity.get_component(PositionComp).y#type: ignore
            result.append((x,y))
    return result

