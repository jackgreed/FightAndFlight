import ecs
class WorldManager:
    def __init__(self):
        self.worlds:dict[str,ecs.World]={}
        self.active_world_id:str|None=None
    def create_world(self,world_id:str)->ecs.World:
        world=ecs.World()
        self.worlds[world_id]=world
        #I dont want the default action,maybe the world need init before use
        return world
    def get_world(self,world_id:str)->ecs.World|None:
        return self.worlds.get(world_id)
    def set_active_world(self,world_id:str):
        if world_id in self.worlds:
            self.active_world_id=world_id
        else:
            print(f"World {world_id} does not exist.")
    def get_active_world(self)->ecs.World|None:
        if self.active_world_id:
            return self.worlds.get(self.active_world_id)
        return None