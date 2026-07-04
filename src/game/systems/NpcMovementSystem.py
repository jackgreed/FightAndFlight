import random

from ecs import System, World
from game.components import (
    NpcMovementComp,
    PathComp,
    PathRequestComp,
    PositionComp,
    TileComp,
)


class NpcMovementSystem(System):
    """根据 NPC 移动模式生成寻路请求。"""

    WANDER_COOLDOWN = 60

    def tick(self, world: World, *args, **kwargs) -> None:
        """为空闲 NPC 生成有效的移动目标。"""
        passable_tiles = self._get_passable_tiles(world)

        entities = world.get_entities_with(
            PositionComp,
            PathComp,
            NpcMovementComp,
        )

        for entity in entities:
            position:PositionComp = entity.get_component(PositionComp)#type:ignore
            path_comp:PathComp = entity.get_component(PathComp)#type:ignore
            movement:NpcMovementComp= entity.get_component(NpcMovementComp)#type:ignore

            if position is None or path_comp is None or movement is None:
                continue
            
            if movement.mode == "idle":
                path_comp.move_list.clear()
                if entity.has_component(PathRequestComp):
                    entity.remove_component(PathRequestComp)
                continue
            if movement.decision_cooldown > 0:#cooldown don't touch it
                movement.decision_cooldown -= 1
                #in cooldown,skip
                continue
            elif movement.mode=="wander":
                if path_comp.move_list:#the pawn is moving
                    continue
                if entity.has_component(PathRequestComp):#the pawn will move next tick
                    continue
                if movement.home_position is None:#use current pos as home
                    movement.home_position = (
                        int(round(position.x)),
                        int(round(position.y)),
                    )
                target = self._choose_wander_target(
                    passable_tiles,
                    movement.home_position,
                    movement.wander_radius,
                    (int(round(position.x)), int(round(position.y))),
                )

                if target is None:#no where to go
                    movement.decision_cooldown = self.WANDER_COOLDOWN
                    continue

                movement.target_entity_id = None
                movement.target_position = target
                movement.decision_cooldown = self.WANDER_COOLDOWN
                entity.add_component(PathRequestComp(target[0], target[1]))
            else:
                continue#TODO: more mode         

    def _get_passable_tiles(
        self,
        world: World,
    ) -> list[tuple[int, int]]:
        """返回所有可通行地块坐标。"""
        result = []

        for entity in world.get_entities_with(
            PositionComp,
            TileComp,
        ):
            position = entity.get_component(PositionComp)
            tile = entity.get_component(TileComp)

            if position is None or tile is None:
                continue

            if tile.move_cost >= 999:
                continue

            result.append((
                int(round(position.x)),
                int(round(position.y)),
            ))

        return result

    @staticmethod
    def _choose_wander_target(
        passable_tiles: list[tuple[int, int]],
        home: tuple[int, int],
        radius: int,
        current: tuple[int, int],
    ) -> tuple[int, int] | None:
        """从活动范围内选择一个非当前地块。"""
        candidates = [
            position
            for position in passable_tiles
            if position != current
            and abs(position[0] - home[0]) <= radius
            and abs(position[1] - home[1]) <= radius
        ]

        if not candidates:
            return None

        return random.choice(candidates)