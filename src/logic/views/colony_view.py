"""
ColonyView - 战棋殖民视图

处理殖民逻辑：建筑建造、资源管理、单位生产等。
"""
from logic.views.base import GameView
TILE_SIZE=32

class ColonyView(GameView):
    """战棋殖民视图。"""

    view_id = "colony"
    def __init__(self,main_window_logic,world_id:str="colony_main"):
        super().__init__()
        self.world_id=world_id
        self.current_pos = (0, 0)
        self.zoom_level = 1.0
        self.mouse_pressed = False
        self.last_mouse_pos = None
    def handle_input(self, cmd: dict) -> None:
        """处理殖民视图下的用户输入。

        TODO: 实现殖民操作逻辑（建造建筑、管理资源、生产单位等）
        """
        print(f"ColonyView received input: {cmd}")
        cmd_type = cmd.get("type")
        
        if cmd_type == "mouse_press":
            # 处理鼠标点击事件            
            if "pos" in cmd and cmd["button"]==3:
                self.mouse_pressed = True
                self.last_mouse_pos = cmd["pos"]
        elif cmd_type == "mouse_move":
            # 处理鼠标移动事件
            if self.mouse_pressed and self.last_mouse_pos is not None:
                # 如果鼠标按下，进行拖拽操作
                new_x = self.current_pos[0] + cmd["pos"][0] - self.last_mouse_pos[0]
                new_y = self.current_pos[1] + cmd["pos"][1] - self.last_mouse_pos[1]
                self.current_pos = (new_x, new_y)
                self.last_mouse_pos = cmd["pos"]
        elif cmd_type == "mouse_release":
            # 处理鼠标释放事件
            self.mouse_pressed = False
            self.last_mouse_pos = None
        elif cmd_type == "key_press":
            # 处理键盘按下事件
            pass
        elif cmd_type == "wheel":
            if "delta" in cmd:
                # 处理鼠标滚轮事件
                delta = cmd["delta"]
                if delta > 0:
                    self.zoom_level *= 1.1  # 放大
                if delta < 0:
                    self.zoom_level /= 1.1  # 缩小
        else:
            print(f"Unknown input type: {cmd_type}")
        pass

    def get_render_data(self) -> dict:
        """返回殖民画面的渲染数据。

        TODO: 返回殖民网格、单位位置、行动范围等数据。
        """
        if self._viewport_size is None:
            return {
                "view": "colony",
                "camera": {
                    "offset": self.current_pos,
                    "zoom": self.zoom_level,
                },
                "sprites": [],
            }
        cam_x,cam_y=self.current_pos
        viewport_w,viewport_h=self._viewport_size#type:ignore
        zoom =self.zoom_level
        visible_left=cam_x
        visible_top=cam_y
        visible_right=cam_x+viewport_w/zoom
        visible_bottom=cam_y+viewport_h/zoom
        world_snapshot=self._world_snapshot.get(self.world_id,{})
        entities=world_snapshot.get("entities",{})
        sprites=[]
        for entity_id,entity_data in entities.items():
            components=entity_data.get("components",{})
            pos=components.get("PositionComp")
            sprite=components.get("SpriteComp")
            if pos is None or sprite is None:
                continue
            world_x = pos["x"] * TILE_SIZE
            world_y = pos["y"] * TILE_SIZE
            world_size = TILE_SIZE
            if (
                world_x + world_size < visible_left
                or world_x > visible_right
                or world_y + world_size < visible_top
                or world_y > visible_bottom
            ):
                continue
            screen_x=(world_x-cam_x)*zoom
            screen_y=(world_y-cam_y)*zoom
            screen_size=world_size*zoom
            sprites.append({
                "entity_id": entity_id,
                "screen_x": screen_x,
                "screen_y": screen_y,
                "screen_size": screen_size,
                "image_path": sprite.get("image_path", ""),
                "decoration_set": sprite.get("decoration_set", []),
            })
        return {
                "view": "colony",
                "camera": {
                    "offset": self.current_pos,
                    "zoom": self.zoom_level,
                },
                "sprites": sprites,
            }
    def on_enter(self) -> None:
        """进入殖民视图。"""
        self.current_pos = (0, 0)
        self.zoom_level = 1.0
        pass

    def on_exit(self) -> None:
        """离开殖民视图。"""
        pass
