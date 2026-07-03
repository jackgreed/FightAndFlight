from ecs.system import System,World
from game.pathfinding import PathFinder
from game.components import PositionComp,PathComp,PathRequestComp
class PathfindingSystem(System):
    def tick(self,world:World,*args,**kwargs)->None:
        """
        transform pathrequest into real path list
        """
        pathfinder=PathFinder(world)
        entities=world.get_entities_with(
            PositionComp,
            PathComp,
            PathRequestComp
        )
        for entity in entities:
            position=entity.get_component(PositionComp)
            path_comp=entity.get_component(PathComp)
            request=entity.get_component(PathRequestComp)
            if position is None or path_comp is None or request is None:
                continue
            start = (
                int(round(position.x)),
                int(round(position.y)),
            )
            goal = (
                request.target_x,
                request.target_y,
            )

            new_path = pathfinder.find_path(start, goal)
            if (position.x, position.y) != start:
                new_path.insert(0, start)
            path_comp.move_list = new_path
            entity.remove_component(PathRequestComp)            