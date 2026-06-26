from perlin_noise import PerlinNoise
from ecs.world import World
from game.components import PositionComp, WorldTileComp
class WorldMapGenerator:
    "generate a World map"
    def __init__(self,world:World,size:tuple[int,int],noise_level:dict[str,float],seed=42):
        """
        we will need 4 paraments for noise level,
        they are :elevation,moisture,temperature,mineral
        """
        self.world=world
        self.x=size[0]
        self.y=size[1]
        self.noise_level=noise_level
        self.seed=seed
        
    def generate_world_tile(self)->None:
        """
        actually generate the world map
        """
        size=(self.x,self.y)
        elevation=self._noise_generator(size,self.noise_level.get("elevation",1),self.seed+100)
        moisture=self._noise_generator(size,self.noise_level.get("moisture",1),self.seed+200)
        temperature=self._noise_generator(size,self.noise_level.get("temperature",1),self.seed+300)
        mineral=self._noise_generator(size,self.noise_level.get("mineral",1),self.seed+400)
        if elevation is None or moisture is None or temperature is None or mineral is None:
            print("[ERROR]ERROR OCCURED IN GENERATION")
            return
        for y in range(self.y):
            for x in range(self.x):
                entity=self.world.create_entity(name=f"WorldTile{x},{y}")
                entity.add_component(PositionComp(x=x,y=y))
                entity_elevation=self._clamp(elevation[x][y]+0.5)
                entity_moisture=self._clamp(moisture[x][y]+0.5)
                entity_raw_temperature=self._clamp(temperature[x][y]+0.5)
                latitude=abs((y/self.y)*2-1)
                entity_temperature=self._clamp(
                    entity_raw_temperature*0.3
                    +(1.0-latitude)*0.5
                    +(1.0-entity_elevation)*0.2
                )
                entity_mineral=self._clamp(mineral[x][y]+0.5)
                entity_water=self._clamp(entity_moisture*0.65+(1.0-entity_elevation)*0.25)
                entity_temperature_fit = 1.0 - abs(entity_temperature - 0.55) * 2
                entity_fertility = self._clamp(
                                    entity_moisture * 0.45
                                    + entity_water * 0.2
                                    + entity_temperature_fit * 0.25
                                    + (1.0 - entity_elevation) * 0.1
                                )
                entity_forest = self._clamp(
                                    entity_moisture * 0.5
                                    + entity_fertility * 0.35
                                    + entity_temperature_fit * 0.15
                                )
                entity.add_component(WorldTileComp(
                    elevation=entity_elevation,
                    moisture=entity_moisture,
                    temperature=entity_temperature,
                    mineral=entity_mineral,
                    water=entity_water,
                    fertility=entity_fertility,
                    forest=entity_forest,
                        ))
                
                
    def _clamp(self,num:float):
        return min(max(num,0),1)

    def _noise_generator(self,size:tuple[int,int],noise_level:float,seed:int):
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
