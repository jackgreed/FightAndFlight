from typing import Any

from ecs import Component
class CharacterComp(Component):
    def __init__(self,character_type:bool,player_uuid:str|None=None):
        """
        charater_type: False for npc, True for player
        player_uuid: leave fr further functions like muti-player
        """
        self.character_type=character_type
        self.player_uuid=player_uuid
    def to_dict(self) -> dict[str, Any]:
        return {
            "character_type":self.character_type,
            "player_uuid":self.player_uuid
        }
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "CharacterComp":
        return cls(character_type=data["character_type"],player_uuid=data["player_uuid"])