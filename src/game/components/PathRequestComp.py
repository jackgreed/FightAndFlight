from ecs import Component
class PathRequestComp(Component):
    def __init__(self, target_x: int, target_y: int):
        self.target_x = target_x
        self.target_y = target_y

    def to_dict(self) -> dict:
        return {
            "target_x": self.target_x,
            "target_y": self.target_y,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "PathRequestComp":
        return cls(
            target_x=int(data["target_x"]),
            target_y=int(data["target_y"]),
        )