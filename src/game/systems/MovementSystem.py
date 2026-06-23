from ecs.system import System
from ecs.component import Component
from game.components.PositionComp import PositionComp
from game.components.MovementComp import MovementComp
from game.components.AttributeComp import AttributeComp
from ecs.world import World
class MovementSystem(System):
    def tick(self,world,*args,**kwargs):
        for entity in world.get_entities_with(PositionComp,MovementComp,AttributeComp):
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

            