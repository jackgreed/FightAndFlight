from perlin_noise import PerlinNoise
from ecs.world import World
from game.components import PositionComp, TileComp,WorldTileComp
from enum import Enum
class _RoughTerrainType(Enum):
    ground=0
    rock=1
    mineral=2
    water=3
    tree=4

class ColonyMapGenerator:
    def __init__(self,world:World,size:tuple[int,int],seed:int,localWorldTileComp:WorldTileComp):
        """
        we dont neet noise_level this time
        we will use the data in WorldTileComp to determine the noise_level
        """
        self.world=world
        self.localWorldTileComp=localWorldTileComp
        self.x=size[0]
        self.y=size[1]
        self.seed=seed
        self.roughmap:list[list[_RoughTerrainType]]=[]
        for x in range(self.x):
            col=[]
            for y in range(self.y):
                col.append(_RoughTerrainType.ground)
            self.roughmap.append(col)
    def generate_colony_map(self):
        """
        actually gennerate the colony map
        """
        #first the ground
        self._generate_base_ground()
        for x in range(self.x):
            for y in range(self.y):
                ...
    def _generate_base_ground(self)->bool:
        """
        basically, empty the list
        """
        self.roughmap.clear()
        for x in range(self.x):
            col=[]
            for y in range(self.y):
                col.append(_RoughTerrainType.ground)
            self.roughmap.append(col)
        return True
    def _generate_mountain(self,seed:int,noise_level:int)->bool:
        ...
    def _generate_mineral(self,seed:int,noise_level:int)->bool:
        ...
    def _generate_water(self,seed:int,noise_level:int)->bool:
        ...
    def _generate_vegetation(self,seed:int,noise_level:int)->bool:
        ...
    def _noise_generator(self,size:tuple[int,int],noise_level:int,seed:int):
        noise_x=size[0]
        noise_y=size[1]
        if noise_x<=0 or noise_y <=0:
            print("[ERROR]noise size must be at least 1x1")
            return None
        noise_level=max(1,noise_level)
        noise=PerlinNoise(octaves=noise_level,seed=seed)
        noise_data=[]
        for x in range(noise_x):
            col=[]
            for y in range(noise_y):
                noise_val=noise([x/noise_x,y/noise_y])
                col.append(noise_val)
            noise_data.append(col)
        return noise_data# basiclly it's in [-0.5,0.5]
