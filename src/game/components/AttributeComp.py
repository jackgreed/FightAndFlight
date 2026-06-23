from ecs.component import Component
class AttributeComp(Component):
    def __init__(self,speed:float=1.0):
        self.speed=speed
    def to_dict(self) -> dict[str, float]:
        return {"speed": self.speed}
    @classmethod
    def from_dict(cls, data: dict[str, float]) -> "AttributeComp":
        return cls(speed=data["speed"])
