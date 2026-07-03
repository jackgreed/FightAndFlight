from ecs.system import System
from game.components import PathComp,PositionComp,MovementComp,AttributeComp,TileComp
from ecs.world import World
class MovementSystem(System):
    def tick(self,world:World,*args,**kwargs):
        """
        we will do two jobs
        1. with PathComp, move them accroding to the PathComp and skip them in job2
        2. without PathComp but with MovementComp, move them directly
        """
        #get tile infomation
        tile_costs: dict[tuple[int, int], float] = {}
        for entity in world.get_entities_with(PositionComp, TileComp):
            position = entity.get_component(PositionComp)
            tile = entity.get_component(TileComp)
            if position is None or tile is None:
                continue
            coordinate = (
                int(round(position.x)),
                int(round(position.y)),
            )
            tile_costs[coordinate] = float(tile.move_cost)
        for entity in world.get_entities_with(PositionComp,AttributeComp,PathComp):
                position = entity.get_component(PositionComp)
                attribute = entity.get_component(AttributeComp)
                path_comp = entity.get_component(PathComp)

                if position is None or attribute is None or path_comp is None:
                    continue

                if not path_comp.move_list:
                    continue

                target = path_comp.move_list[0]
                move_cost = tile_costs.get(target)

                if move_cost is None or move_cost >= 999:
                    path_comp.move_list.clear()
                    continue

                if move_cost <= 0:
                    move_cost = 1.0
                speed = attribute.speed / move_cost
                delta_x = target[0] - position.x
                delta_y = target[1] - position.y
                distance = (delta_x ** 2 + delta_y ** 2) ** 0.5

                if distance <= speed:
                    position.x = target[0]
                    position.y = target[1]
                    path_comp.move_list.pop(0)
                    continue

                position.x += speed * delta_x / distance
                position.y += speed * delta_y / distance
        for entity in world.get_entities_with(PositionComp,MovementComp,AttributeComp):
            if entity.has_component(PathComp):
                continue
            speed = entity.get_component(AttributeComp).speed
            position = entity.get_component(PositionComp).x, entity.get_component(PositionComp).y
            movement = entity.get_component(MovementComp).target_x, entity.get_component(MovementComp).target_y
            if position == movement:
                entity.remove_component(MovementComp)
                continue
            distance = ((movement[0] - position[0]) ** 2 + (movement[1] - position[1]) ** 2) ** 0.5
            if distance <= speed:
                entity.get_component(PositionComp).x = movement[0]
                entity.get_component(PositionComp).y = movement[1]
                entity.remove_component(MovementComp)
                continue
            else:
                entity.get_component(PositionComp).x += speed * (movement[0] - position[0]) / distance
                entity.get_component(PositionComp).y += speed * (movement[1] - position[1]) / distance

            