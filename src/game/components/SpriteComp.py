from ecs.component import Component
class SpriteComp(Component):
    def __init__(self, image_path: str = "", decoration_set: list[tuple[str, int,int, int,int, int]]|None = None):
        self.image_path: str = image_path
        self.decoration_set: list[tuple[str, int,int, int,int, int]] = decoration_set if decoration_set is not None else []
        # hex code ; startx;endx;starty;endy; layer

    def to_dict(self) -> dict:
        return {"image_path": self.image_path, "decoration_set": self.decoration_set}

    @classmethod
    def from_dict(cls, data: dict) -> "SpriteComp":
        return cls(image_path=data["image_path"], decoration_set=data["decoration_set"])