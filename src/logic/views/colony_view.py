"""
ColonyView - 战棋殖民视图

处理殖民逻辑：建筑建造、资源管理、单位生产等。
"""
from logic.views.base import GameView
from game.commands import MovementCommand
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
        self.selected_entity_id=None
    def handle_input(self, cmd: dict) -> None:
        """处理殖民视图下的用户输入。

        TODO: 实现殖民操作逻辑（建造建筑、管理资源、生产单位等）
        """
        cmd_type = cmd.get("type")
        
        if cmd_type == "mouse_press":
            # 处理鼠标点击事件   
            if "pos" in cmd and cmd.get("button")=="left":
                grid=self._screen_to_grid(cmd["pos"])
                self.selected_entity_id = self._get_entity_at_grid(grid)
            if "pos" in cmd and cmd.get("button")=="right":
                if self.selected_entity_id is not None and self._command_queue is not None:
                    grid=self._screen_to_grid(cmd["pos"])
                    self._command_queue.push(
                        MovementCommand(
                            self.world_id,
                            self.selected_entity_id,
                            grid[0],
                            grid[1],
                        )
                    )
            if "pos" in cmd and cmd.get("button")=="middle":
                self.mouse_pressed = True
                self.last_mouse_pos = cmd["pos"]
        elif cmd_type == "mouse_move":
            # 处理鼠标移动事件
            if self.mouse_pressed and self.last_mouse_pos is not None:
                # 如果鼠标按下，进行拖拽操作
                new_x = self.current_pos[0] - cmd["pos"][0] + self.last_mouse_pos[0]
                new_y = self.current_pos[1] - cmd["pos"][1] + self.last_mouse_pos[1]
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
                self.zoom_level = max(0.25, min(self.zoom_level, 4.0))
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
                "tiles": [],
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
        tiles=[]
        sprites=[]
        for entity_id,entity_data in entities.items():
            components=entity_data.get("components",{})
            pos=components.get("PositionComp")
            tile=components.get("TileComp")
            sprite=components.get("SpriteComp")
            if pos is None:
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
            if tile is not None:
                screen_left = (world_x - cam_x) * zoom
                screen_top = (world_y - cam_y) * zoom
                screen_right = (world_x + world_size - cam_x) * zoom
                screen_bottom = (world_y + world_size - cam_y) * zoom
                tiles.append({
                    "screen_left": screen_left,
                    "screen_top": screen_top,
                    "screen_right": screen_right,
                    "screen_bottom": screen_bottom,
                    "terrain_type": tile.get("terrain_type", "plain"),
                })
            if sprite is not None:
                sprites.append({
                    "screen_x": screen_x,
                    "screen_y": screen_y,
                    "screen_size": screen_size,
                    "image_path": sprite.get("image_path", ""),
                    "decoration_set": sprite.get("decoration_set", []),
                    "is_selected":entity_id==self.selected_entity_id,
                })
        return {
                "view": "colony",
                "camera": {
                    "offset": self.current_pos,
                    "zoom": self.zoom_level,
                },
                "tiles": tiles,
                "sprites": sprites,
            }
    def on_enter(self) -> None:
        """进入殖民视图。"""
        self.current_pos = (0, 0)
        self.zoom_level = 1.0
        self.selected_entity_id=None
        pass

    def on_exit(self) -> None:
        """离开殖民视图。"""
        pass
    def _screen_to_grid(self,pos:tuple[int,int])->tuple[int,int]:
        """
        transform screen x,y to world x,y
        """
        if self.zoom_level <= 0:
            return (0, 0)
        screen_x,screen_y=pos
        world_x=self.current_pos[0]+screen_x/self.zoom_level
        world_y=self.current_pos[1]+screen_y/self.zoom_level
        return (int(world_x//TILE_SIZE),int(world_y//TILE_SIZE))
    def _get_entity_at_grid(self,grid:tuple[int,int])->str|None:
        """
        find the entity_id accroding to the given pos
        """
        world_snapshot=self._world_snapshot.get(self.world_id,{})
        entities=world_snapshot.get("entities",{})
        for entity_id,entity_data in entities.items():
            components=entity_data.get("components",{})
            pos=components.get("PositionComp")
            sprite=components.get("SpriteComp")
            if pos is None or sprite is None:
                continue
            if int(pos["x"])==grid[0] and int(pos["y"])==grid[1]:
                return entity_id
        return None
