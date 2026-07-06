import random
from typing import Any
from ecs import Entity, World
from game.components import (

    PositionComp,

    TileComp,

)
from game.entity_templates import EntityTemplateLoader,EntityFactory

class CharacterInitializer:
    """Create player and NPC entities on passable colony tiles."""
    def __init__(self,loader:EntityTemplateLoader|None=None,factory:EntityFactory|None=None):
        self.loader=loader if loader is not None else EntityTemplateLoader()
        self.loader.load()
        self.factory=factory if factory is not None else EntityFactory(self.loader)
    def _generate_character(
        self,
        world: World,
        name: str,
        pos: tuple[int, int],
        is_player: bool,
        player_uuid: str | None,
    ) -> Entity:
        template_id = "player" if is_player else "npc"

        overrides:dict[str,dict[str,Any]] = {
            "PositionComp": {
                "x": pos[0],
                "y": pos[1],
            }
        }

        if is_player:
            overrides["CharacterComp"] = {
                "player_uuid": player_uuid,
            }

        return self.factory.create_entity(
            world=world,
            template_id=template_id,
            overrides=overrides,
            name=name,
        )

    def _find_possible_tiles(self, world: World) -> list[tuple[int, int]]:
        result: list[tuple[int, int]] = []
        for entity in world.get_entities_with(TileComp, PositionComp):
            tile:TileComp = entity.get_component(TileComp)#type:ignore
            position:PositionComp = entity.get_component(PositionComp)#type:ignore
            if tile is None or position is None or tile.move_cost >= 999:
                continue
            result.append((int(position.x), int(position.y)))
        return result

    def generate_pawn(
        self,
        world: World,
        name: str = "examplename",
        pos: tuple[int, int] | None = None,
        is_player: bool = False,
        player_uuid: str | None = None,
    ) -> Entity | None:
        """Create a pawn at a supplied or randomly selected passable tile."""
        if pos is None:
            possible_tiles = self._find_possible_tiles(world)
            if not possible_tiles:
                return None
            pos = random.choice(possible_tiles)
        return self._generate_character(
            world,
            name,
            pos,
            is_player,
            player_uuid,
        )
