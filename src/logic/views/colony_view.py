"""
ColonyView - 战棋殖民视图

处理殖民逻辑：建筑建造、资源管理、单位生产等。
"""
from logic.views.base import GameView
from logic.views.colony_input import handle_colony_input
from game.commands import (
    MovementCommand,
    PathfindCommand,
)
from game.interactions import ActionProxy
TILE_SIZE=32

class ColonyView(GameView):
    """战棋殖民视图。"""

    view_id = "colony"
    def __init__(self,world_id:str="colony_main"):
        super().__init__()
        self.world_id=world_id
        self.selected_entity_id=None
        self._interaction_target_entity_id=None
        self._entities_by_grid={}
        self._components_by_entity={}
        self._camera_initialized=False
    def set_world_snapshot(self, snapshot: dict):
        """Update world snapshot and rebuild query indexes."""
        super().set_world_snapshot(snapshot)
        self._rebuild_entity_indexes()

    def _rebuild_entity_indexes(self) -> None:
        """Build lightweight indexes from the latest world snapshot."""
        self._entities_by_grid={}
        self._components_by_entity={}
        world_snapshot=self._world_snapshot.get(self.world_id,{})
        entities=world_snapshot.get("entities",{})

        for entity_id,entity_data in entities.items():
            components=entity_data.get("components",{})
            self._components_by_entity[entity_id]=components
            pos=components.get("PositionComp")
            if pos is None:
                continue
            grid=(int(pos["x"]),int(pos["y"]))
            self._entities_by_grid.setdefault(grid,[]).append(entity_id)
    def handle_input(self, cmd: dict) -> None:
        """处理殖民视图下的用户输入。

        TODO: 实现殖民操作逻辑（建造建筑、管理资源、生产单位等）
        """
        handle_colony_input(self, cmd)

    def _get_current_info_panel(self) -> dict | None:
        """Return active info panel render data."""
        world_snapshot = self._world_snapshot.get(self.world_id, {})
        entities = world_snapshot.get("entities", {})
        return self._get_info_panel_render_data(entities)

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
                "info_panel": None,
            }
        viewport_w,viewport_h=self._viewport_size#type:ignore
        zoom =self.zoom_level
        world_snapshot=self._world_snapshot.get(self.world_id,{})
        entities=world_snapshot.get("entities",{})
        if not self._camera_initialized:
            self._center_camera_on_player(
                entities,
                viewport_w,
                viewport_h,
            )
        cam_x,cam_y=self.current_pos
        visible_left=cam_x
        visible_top=cam_y
        visible_right=cam_x+viewport_w/zoom
        visible_bottom=cam_y+viewport_h/zoom
        tiles=[]
        sprites=[]
        selected_sprites=[]
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
                sprite_data={
                    "screen_x": screen_x,
                    "screen_y": screen_y,
                    "screen_size": screen_size,
                    "image_path": sprite.get("image_path", ""),
                    "decoration_set": sprite.get("decoration_set", []),
                    "is_selected":entity_id==self.selected_entity_id,
                }
                if entity_id==self.selected_entity_id:
                    selected_sprites.append(sprite_data)
                else:
                    sprites.append(sprite_data)
        sprites.extend(selected_sprites)
        return {
                "view": "colony",
                "camera": {
                    "offset": self.current_pos,
                    "zoom": self.zoom_level,
                },
                "tiles": tiles,
                "sprites": sprites,
                "info_panel": self._get_info_panel_render_data(entities),
            }
    def on_enter(self) -> None:
        """进入殖民视图。"""
        if not self._camera_initialized:
            self.current_pos = (0, 0)
            self.zoom_level = 1.0
        self.selected_entity_id=None

    def on_exit(self) -> None:
        """离开殖民视图。"""
        pass
    def _center_camera_on_player(
        self,
        entities:dict,
        viewport_width:int,
        viewport_height:int,
    )->None:
        """Center the camera once when player snapshot data is available."""
        for entity_data in entities.values():
            components=entity_data.get("components",{})
            character=components.get("CharacterComp")
            position=components.get("PositionComp")
            if (
                character is None
                or position is None
                or character.get("character_type") is not True
            ):
                continue
            zoom=max(self.zoom_level,0.01)
            player_center_x=(float(position["x"])+0.5)*TILE_SIZE
            player_center_y=(float(position["y"])+0.5)*TILE_SIZE
            self.current_pos=(
                max(0.0,player_center_x-viewport_width/(2*zoom)),
                max(0.0,player_center_y-viewport_height/(2*zoom)),
            )
            self._camera_initialized=True
            return
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
    def _select_entity_at_grid(self, grid: tuple[int, int]) -> str | None:
        """Cycle selectable entities at the given grid position."""
        entity_ids = self._get_selectable_entities_at_grid(grid)
        if not entity_ids:
            return None

        if self.selected_entity_id not in entity_ids:
            return entity_ids[0]

        current_index = entity_ids.index(self.selected_entity_id)
        return entity_ids[(current_index + 1) % len(entity_ids)]

    def _get_selectable_entities_at_grid(
        self,
        grid: tuple[int, int],
    ) -> list[str]:
        """Return selectable entity ids at the given grid position."""
        result=[]
        for entity_id in self._entities_by_grid.get(grid,[]):
            components=self._components_by_entity.get(entity_id,{})
            sprite=components.get("SpriteComp")
            if sprite is None:
                continue
            result.append(entity_id)
        return result
    def _get_interactable_entity_at_grid(
        self,
        grid: tuple[int, int],
    ) -> str | None:
        """Find an interactable entity at the given grid position."""
        for entity_id in self._entities_by_grid.get(grid,[]):
            components=self._components_by_entity.get(entity_id,{})
            interactable=components.get("InteractableComp")
            if interactable is None:
                continue
            return entity_id
        return None
    def _get_entity_grid(self, entity_id: str) -> tuple[int, int] | None:
        """Return entity grid position from snapshot."""
        components=self._components_by_entity.get(entity_id,{})
        pos=components.get("PositionComp")
        if pos is None:
            return None
        return (int(pos["x"]), int(pos["y"]))

    def _push_move_command(
        self,
        entity_id: str,
        grid: tuple[int, int],
    ) -> None:
        """Push pathfind or direct movement command for entity."""
        if self._command_queue is None:
            return

        if self._entity_has_component(entity_id,"PathComp"):
            self._command_queue.push(
                PathfindCommand(
                    self.world_id,
                    entity_id,
                    grid[0],
                    grid[1]
                )
            )
            return

        self._command_queue.push(
            MovementCommand(
                self.world_id,
                entity_id,
                grid[0],
                grid[1],
            )
        )
    def _entity_has_component(
    self,
    entity_id: str,
    component_name: str,
) -> bool:
        components = self._components_by_entity.get(entity_id, {})
        return component_name in components
    def _get_info_panel_render_data(self, entities: dict) -> dict | None:
        """Return active info panel data in screen coordinates."""
        panel_x = 12
        panel_y = 12
        panel_width = 320
        panel_height = 180
        close_size = 18

        for entity_data in entities.values():
            components = entity_data.get("components", {})
            panel = components.get("InfoPanelComp")
            if panel is None:
                continue

            render_data = {
                "panel_id": panel.get("panel_id", "panel"),
                "title": panel.get("title", ""),
                "info": panel.get("info", ""),
                "rect": [
                    panel_x,
                    panel_y,
                    panel_width,
                    panel_height,
                ],
                "close_rect": [
                    panel_x + panel_width - close_size - 8,
                    panel_y + 8,
                    close_size,
                    close_size,
                ],
            }
            if render_data["panel_id"] == "interaction_menu":
                render_data["actions"] = self._get_interaction_actions(
                    render_data,
                )
            return render_data

        return None

    @staticmethod
    def _get_interaction_actions(panel: dict) -> list[dict]:
        """Return action button data for an interaction menu."""
        rect = panel.get("rect", [12, 12, 320, 180])
        panel_x, panel_y, panel_width, _panel_height = [
            int(value) for value in rect
        ]
        action_x = panel_x + 10
        action_y = panel_y + 48
        action_width = panel_width - 20
        action_height = 22
        action_gap = 6
        actions = []

        for index, line in enumerate(str(panel.get("info", "")).splitlines()):
            action_id = line.strip()
            if not action_id:
                continue
            top = action_y + len(actions) * (action_height + action_gap)
            actions.append({
                "action_id": action_id,
                "label": ActionProxy.get_label(action_id),
                "rect": [
                    action_x,
                    top,
                    action_width,
                    action_height,
                ],
            })

        return actions
