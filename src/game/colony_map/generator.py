from perlin_noise import PerlinNoise
from ecs.world import World
from game.components import PositionComp, TileComp,WorldTileComp
from enum import Enum
class _RoughTerrainType(Enum):
    ground=0
    rock=1
    mineral=2
    water=3
    forest=4

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
        self.noise_config = {
            "rock": 3,
            "mineral":5,
            "water": 2,
            "forest":4,       
        }
        self.noise_threshold = {
            "rock": 0.38 - self.localWorldTileComp.elevation * 0.18,
            "mineral": 0.42 - self.localWorldTileComp.mineral * 0.25,
            "water": 0.34 - self.localWorldTileComp.water * 0.30,
            "forest": 0.36 - self.localWorldTileComp.forest * 0.28,
        }
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
        self._generate_mountain()
        self._generate_mineral()
        self._generate_water()
        self._generate_vegetation()
        ground_type=self._base_type()
        for x in range(self.x):
            for y in range(self.y):
                tileEntity=self.world.create_entity(name="ColonyTile")
                tileEntity.add_component(PositionComp(x=x,y=y))
                roughtype=self.roughmap[x][y]
                if roughtype==_RoughTerrainType.ground:
                    tileEntity.add_component(TileComp(terrain_type=ground_type,move_cost=1,buildable=True))
                elif roughtype==_RoughTerrainType.rock:
                    tileEntity.add_component(TileComp(terrain_type="rock",move_cost=999,buildable=False))
                elif roughtype==_RoughTerrainType.mineral:
                    tileEntity.add_component(TileComp(terrain_type="ore",move_cost=999,buildable=False))
                elif roughtype==_RoughTerrainType.water:
                    tileEntity.add_component(TileComp(terrain_type="water",move_cost=999,buildable=False))
                elif roughtype==_RoughTerrainType.forest:
                    tileEntity.add_component(TileComp(terrain_type="forest",move_cost=2,buildable=False))
                else:
                    continue
            
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
    def _generate_mountain(self)->bool:
        """
        basically,spawn rocks on the map
        """
        octaves=self.noise_config["rock"]
        seed=self.seed+100
        noise_data=self._noise_generator((self.x,self.y),octaves,seed)
        if noise_data is None:
            print("[ERROR]map size too low")
            return False
        for x in range(self.x):
            for y in range(self.y):
                if noise_data[x][y]>self.noise_threshold["rock"]:
                    self.roughmap[x][y]=_RoughTerrainType.rock
        return True
    def _generate_mineral(self)->bool:
        """
        basically,spawn mineral on the map
        """
        octaves=self.noise_config["mineral"]
        seed=self.seed+200
        noise_data=self._noise_generator((self.x,self.y),octaves,seed)
        if noise_data is None:
            print("[ERROR]map size too low")
            return False
        for x in range(self.x):
            for y in range(self.y):
                if (
                    noise_data[x][y]>self.noise_threshold["mineral"]
                    
                ):
                    self.roughmap[x][y]=_RoughTerrainType.mineral
        return True
    def _generate_water(self)->bool:
        """
        basically,spawn water on the map
        """
        octaves=self.noise_config["water"]
        seed=self.seed+300
        noise_data=self._noise_generator((self.x,self.y),octaves,seed)
        if noise_data is None:
            print("[ERROR]map size too low")
            return False
        for x in range(self.x):
            for y in range(self.y):
                if noise_data[x][y]>self.noise_threshold["water"] and self.roughmap[x][y]==_RoughTerrainType.ground:
                    self.roughmap[x][y]=_RoughTerrainType.water
        return True
    def _generate_vegetation(self)->bool:
        """
        basically,spawn vegetation on the map
        """
        octaves=self.noise_config["forest"]
        seed=self.seed+400
        noise_data=self._noise_generator((self.x,self.y),octaves,seed)
        if noise_data is None:
            print("[ERROR]map size too low")
            return False
        for x in range(self.x):
            for y in range(self.y):
                if noise_data[x][y]>self.noise_threshold["forest"] and self.roughmap[x][y]==_RoughTerrainType.ground:
                    self.roughmap[x][y]=_RoughTerrainType.forest
        return True
    def _noise_generator(self,size:tuple[int,int],noise_level:int,seed:int)->list[list[float]]|None:
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
    def _base_type(self)->str:
        temp = self.localWorldTileComp.temperature
        moisture = self.localWorldTileComp.moisture
        elevation = self.localWorldTileComp.elevation

        if temp < 0.15:
            return "ice"
        if temp < 0.3:
            return "snow"
        if moisture < 0.2 and temp > 0.55:
            return "desert"
        if moisture > 0.55 and temp > 0.35:
            return "grass"
        if elevation > 0.6:
            return "dry_plain"
        return "plain"
