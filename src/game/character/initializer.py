import random

from ecs import Entity, World
from game.components import (
    AttributeComp,
    CharacterComp,
    PathComp,
    PositionComp,
    SpriteComp,
    TileComp,
)


class CharacterInitializer:
    """Create player and NPC entities on passable colony tiles."""

    def _generate_character(
        self,
        world: World,
        name: str,
        pos: tuple[int, int],
        is_player: bool,
        player_uuid: str | None,
    ) -> Entity:
        character = world.create_entity(name)
        character.add_component(AttributeComp(1))
        character.add_component(CharacterComp(is_player, player_uuid))
        character.add_component(PathComp())
        character.add_component(PositionComp(pos[0], pos[1]))
        character.add_component(SpriteComp())
        return character

    def _find_possible_tiles(self, world: World) -> list[tuple[int, int]]:
        result: list[tuple[int, int]] = []
        for entity in world.get_entities_with(TileComp, PositionComp):
            tile = entity.get_component(TileComp)
            position = entity.get_component(PositionComp)
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
