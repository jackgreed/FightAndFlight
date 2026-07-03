from heapq import heappop, heappush

from ecs import World
from game.components import PositionComp, TileComp


class PathFinder:
    """Calculate paths across a world's tile grid."""

    BLOCKED_MOVE_COST = 999
    DIRECTIONS = ((0, -1), (1, 0), (0, 1), (-1, 0))

    def __init__(self, world: World):
        self.world = world

    def find_path(
        self,
        start: tuple[int, int],
        goal: tuple[int, int],
    ) -> list[tuple[int, int]]:
        """Return a path excluding start and including goal."""
        tile_map = self._build_tile_map()
        if start == goal:
            return []
        if start not in tile_map or not self._is_passable(tile_map, goal):
            return []

        open_set: list[tuple[float, tuple[int, int]]] = []
        heappush(open_set, (0.0, start))
        came_from: dict[tuple[int, int], tuple[int, int]] = {}
        g_score: dict[tuple[int, int], float] = {start: 0.0}

        while open_set:
            _, current = heappop(open_set)
            if current == goal:
                return self._reconstruct_path(came_from, start, goal)

            for neighbor in self._get_neighbors(current, tile_map):
                move_cost = tile_map[neighbor]
                tentative_score = g_score[current] + move_cost
                if tentative_score >= g_score.get(neighbor, float("inf")):
                    continue

                came_from[neighbor] = current
                g_score[neighbor] = tentative_score
                priority = tentative_score + self._heuristic(neighbor, goal)
                heappush(open_set, (priority, neighbor))

        return []

    def _build_tile_map(self) -> dict[tuple[int, int], float]:
        """Build a coordinate-to-move-cost lookup from tile entities."""
        tile_map: dict[tuple[int, int], float] = {}
        for entity in self.world.get_entities_with(PositionComp, TileComp):
            position = entity.get_component(PositionComp)
            tile = entity.get_component(TileComp)
            if position is None or tile is None:
                continue
            tile_map[(int(position.x), int(position.y))] = float(tile.move_cost)
        return tile_map

    def _get_neighbors(
        self,
        position: tuple[int, int],
        tile_map: dict[tuple[int, int], float],
    ) -> list[tuple[int, int]]:
        """Return passable orthogonal neighbors."""
        x, y = position
        neighbors = []
        for offset_x, offset_y in self.DIRECTIONS:
            neighbor = (x + offset_x, y + offset_y)
            if self._is_passable(tile_map, neighbor):
                neighbors.append(neighbor)
        return neighbors

    def _is_passable(
        self,
        tile_map: dict[tuple[int, int], float],
        position: tuple[int, int],
    ) -> bool:
        """Return whether a tile exists and permits movement."""
        return tile_map.get(position, self.BLOCKED_MOVE_COST) < self.BLOCKED_MOVE_COST

    @staticmethod
    def _heuristic(
        position: tuple[int, int],
        goal: tuple[int, int],
    ) -> int:
        """Return Manhattan distance between two grid positions."""
        return abs(position[0] - goal[0]) + abs(position[1] - goal[1])

    @staticmethod
    def _reconstruct_path(
        came_from: dict[tuple[int, int], tuple[int, int]],
        start: tuple[int, int],
        goal: tuple[int, int],
    ) -> list[tuple[int, int]]:
        """Reconstruct a path excluding start and including goal."""
        path = [goal]
        current = goal
        while current != start:
            current = came_from[current]
            path.append(current)
        path.reverse()
        return path[1:]
