import copy
import json
import random
from pathlib import Path
from typing import Any

from ecs import Entity,World
from game.components import PositionComp,TileComp
from game.entity_templates.factory import EntityFactory

DEFAULT_SPAWN_CONFIG = (
    Path(__file__).resolve().parents[2]
    / "assets"
    / "data"
    / "colony_start.json"
)
class SpawnInitializer:
    """
    spawn entity accroding to json file
    """
    def __init__(self,factory:EntityFactory,config_path:Path=DEFAULT_SPAWN_CONFIG,rng:random.Random|None=None):
        self.factory=factory
        if self.factory is None:
            raise RuntimeError("factory is None")
        self.config_path=config_path
        self.rng=rng or random.Random()
    def spawn_all(
        self,
        world: World,
        runtime_overrides: (
            dict[str, dict[str, dict[str, Any]]] | None
        ) = None,
    ) -> dict[str, list[Entity]]:
        """spawn all entities"""
        #load config
        config = self._load_config()
        groups = config["spawn_groups"]
        runtime_overrides = runtime_overrides or {}

        spawn_plans = []
        total_count = 0
        #randomly choose the number to spawn
        for group in groups:
            minimum, maximum = group["count_range"]
            count = self.rng.randint(minimum, maximum)
            total_count += count
            spawn_plans.append((group, count))
        #find postions
        positions = self._get_passable_positions(world)
        if len(positions) < total_count:
            raise ValueError(
                "Not enough passable tiles for initial entities"
            )

        self.rng.shuffle(positions)
        created: list[Entity] = []
        result: dict[str, list[Entity]] = {}

        try:
            for group, count in spawn_plans:
                template_id = group["template_id"]
                name_prefix = group["name_prefix"]
                result[template_id] = []

                for index in range(count):
                    position = positions.pop()
                    overrides = copy.deepcopy(
                        runtime_overrides.get(
                            template_id,
                            {},
                        )
                    )
                    overrides["PositionComp"] = {
                        "x": position[0],
                        "y": position[1],
                    }

                    name = (
                        name_prefix
                        if count == 1
                        else f"{name_prefix}_{index + 1}"
                    )

                    entity = self.factory.create_entity(
                        world=world,
                        template_id=template_id,
                        overrides=overrides,
                        name=name,
                    )

                    created.append(entity)
                    result[template_id].append(entity)

        except Exception:
            for entity in created:
                world.destroy_entity(entity.id)
            raise

        return result

    def _load_config(self) -> dict[str, Any]:
        """load and validate"""
        with self.config_path.open(
            "r",
            encoding="utf-8",
        ) as file:
            config = json.load(file)

        groups = config.get("spawn_groups")
        if not isinstance(groups, list):
            raise ValueError("spawn_groups must be a list")

        for index, group in enumerate(groups):
            self._validate_group(index, group)

        return config

    def _validate_group(
        self,
        index: int,
        group: object,
    ) -> None:
        """validate。"""
        if not isinstance(group, dict):
            raise ValueError(
                f"Spawn group {index} must be an object"
            )

        template_id = group.get("template_id")
        if not isinstance(template_id, str):
            raise ValueError(
                f"Invalid template_id in group {index}"
            )

        if template_id not in self.factory.loader.get_template_ids():
            raise ValueError(
                f"Unknown template: {template_id}"
            )

        name_prefix = group.get("name_prefix")
        if not isinstance(name_prefix, str) or not name_prefix:
            raise ValueError(
                f"Invalid name_prefix in group {index}"
            )

        count = group.get("count_range")
        if (
            not isinstance(count, list)
            or len(count) != 2
            or not all(
                isinstance(value, int)
                and not isinstance(value, bool)
                for value in count
            )
            or count[0] < 0
            or count[1] < count[0]
        ):
            raise ValueError(
                f"Invalid count range in group {index}"
            )

        spawn = group.get("spawn")
        if (
            not isinstance(spawn, dict)
            or spawn.get("mode") != "random_passable"
        ):
            raise ValueError(
                f"Unsupported spawn mode in group {index}"
            )

    @staticmethod
    def _get_passable_positions(
        world: World,
    ) -> list[tuple[int, int]]:
        """return all movable tile position。"""
        positions = []

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

            positions.append((
                int(position.x),
                int(position.y),
            ))

        return positions