"""
WorldView -show the world map

"""
from logic.views.base import GameView
from game.commands import MovementCommand
TILE_SIZE=32
class WorldMapView(GameView):
    """world map displayer"""
    view_id="world_map"
    def __init__(self,world_id:str="world_map"):
        super().__init__()
        self.world_id=world_id
        self.current_pos=(0,0)
        self.zoom_level=1.0
        self.mouse_pressed=False
        self.last_mouse_pos = None
        self.selected_entity_id=None
    def handle_input(self, cmd: dict) -> None:
        """
        handle input
        """
        cmd_type=cmd.get("type")
        if cmd_type =="mouse_press":
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
        elif cmd_type=="mouse_move":
            # 处理鼠标移动事件
            if self.mouse_pressed and self.last_mouse_pos is not None:
                # 如果鼠标按下，进行拖拽操作
                new_x = self.current_pos[0] - cmd["pos"][0] + self.last_mouse_pos[0]
                new_y = self.current_pos[1] - cmd["pos"][1] + self.last_mouse_pos[1]
                self.current_pos = (new_x, new_y)
                self.last_mouse_pos = cmd["pos"]
        elif cmd_type=="mouse_release":
            self.mouse_pressed = False
            self.last_mouse_pos = None
        elif cmd_type=="wheel":
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
    def get_render_data(self) -> dict:
        """
        return render data
        """
        if self._viewport_size is None:
            return{
                "view":"worldmap",
                "camera": {
                    "offset": self.current_pos,
                    "zoom": self.zoom_level,
                },
                "world_tiles":[],
                "world_sprites":[],#current empty,leave for further use
                "selected_tile":None,
            }
        cam_x,cam_y=self.current_pos
        viewport_w,viewport_h=self._viewport_size
        zoom=self.zoom_level
        vis_l=cam_x
        vis_t=cam_y
        vis_r=cam_x+viewport_w/zoom
        vis_b=cam_y+viewport_h/zoom
        world_snapshot=self._world_snapshot.get(self.world_id,{})
        entities=world_snapshot.get("entities",{})
        world_tiles=[]
        world_sprites=[]
        selected_tile=None
        for entity_id,entity_data in entities.items():
            components=entity_data.get("components",{})
            pos=components.get("PositionComp")
            world_tile=components.get("WorldTileComp")
            world_sprite=components.get("SpriteComp")
            if pos is None:
                continue
            world_x = pos["x"] * TILE_SIZE
            world_y = pos["y"] * TILE_SIZE
            world_size = TILE_SIZE
            if (
                world_x + world_size < vis_l
                or world_x > vis_r
                or world_y + world_size < vis_t
                or world_y > vis_b
            ):
                continue
            screen_x=(world_x-cam_x)*zoom
            screen_y=(world_y-cam_y)*zoom
            screen_size=world_size*zoom
            if world_tile is not None:
                screen_left = (world_x - cam_x) * zoom
                screen_top = (world_y - cam_y) * zoom
                screen_right = (world_x + world_size - cam_x) * zoom
                screen_bottom = (world_y + world_size - cam_y) * zoom
                elevation=world_tile.get("elevation")
                water=world_tile.get("water")
                temperature=world_tile.get("temperature")
                moisture=world_tile.get("moisture")
                forest=world_tile.get("forest")
                fertility=world_tile.get("fertility")
                if elevation < 0.32 or water >= 0.72:
                    terrain_type = "water"
                elif elevation >= 0.75:
                    terrain_type = "snow" if temperature < 0.30 else "mountain"
                elif temperature < 0.25:
                    terrain_type = "tundra"
                elif moisture < 0.28 and temperature > 0.55:
                    terrain_type = "desert"
                elif forest >= 0.62:
                    terrain_type = "forest"
                elif fertility >= 0.55:
                    terrain_type = "grass"
                else:
                    terrain_type = "plain"
                world_tiles.append({
                    "screen_left": screen_left,
                    "screen_top": screen_top,
                    "screen_right": screen_right,
                    "screen_bottom": screen_bottom,
                    "terrain_type":terrain_type,
                    "is_selected":entity_id==self.selected_entity_id,
                })
                if entity_id == self.selected_entity_id:
                    selected_tile={
                        "position":{
                            "x":pos["x"],
                            "y":pos["y"],
                        },
                        "terrain_type":terrain_type,
                        "info":world_tile,
                    }
            if world_sprite is not None:
                world_sprites.append({
                    "screen_x": screen_x,
                    "screen_y": screen_y,
                    "screen_size": screen_size,
                    "image_path": world_sprite.get("image_path", ""),
                    "decoration_set": world_sprite.get("decoration_set", []),
                    "is_selected":entity_id==self.selected_entity_id,
                })
        return{
                "view":"worldmap",
                "camera": {
                    "offset": self.current_pos,
                    "zoom": self.zoom_level,
                },
                "world_tiles":world_tiles,
                "world_sprites":world_sprites,#current empty,leave for further use
                "selected_tile":selected_tile,
            }
    def on_enter(self) -> None:
        """
        enter
        """
        self.current_pos = (0, 0)
        self.zoom_level = 1.0
        self.selected_entity_id=None
        pass

    def on_exit(self) -> None:
        """leave"""
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
            if pos is None:
                continue
            if int(pos["x"])==grid[0] and int(pos["y"])==grid[1]:
                return entity_id
        return None
