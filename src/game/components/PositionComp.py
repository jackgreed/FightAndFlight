from ecs.component import Component
class PositionComp(Component):
    def __init__(self,x:int=0,y:int=0):
        self.x=x
        self.y=y
    def to_dict(self) -> dict[str, int]:
        return {"x": self.x, "y": self.y}
    @classmethod
    def from_dict(cls, data: dict[str, int]) -> "PositionComp":
        return cls(x=data["x"], y=data["y"])
