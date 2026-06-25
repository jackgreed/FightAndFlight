from typing import Any

import ecs
class WorldTileComp(ecs.Component):
    """
    basic data for world tile
    """
    def __init__(
        self,
        elevation: float,
        moisture: float,
        temperature: float,
        fertility: float,
        forest: float,
        mineral: float,
        water: float,
    ):
        self.elevation=elevation
        self.moisture=moisture
        self.temperature=temperature
        self.fertility=fertility
        self.forest=forest
        self.mineral=mineral
        self.water=water
    def to_dict(self) -> dict[str, Any]:
        return {
            "elevation": self.elevation,
            "moisture": self.moisture,
            "temperature": self.temperature,
            "fertility": self.fertility,
            "forest": self.forest,
            "mineral": self.mineral,
            "water": self.water,
        }
    @classmethod
    def from_dict(cls, data: dict[str, Any])->"WorldTileComp":
        return cls(
            elevation=data["elevation"],
            moisture=data["moisture"],
            temperature=data["temperature"],
            fertility=data["fertility"],
            forest=data["forest"],
            mineral=data["mineral"],
            water=data["water"]
        )