"""
GameView - 游戏视图抽象基类

每个视图处理特定游戏画面的所有逻辑。
GameWindow 只是画布，不参与任何逻辑决策。
"""
from abc import ABC, abstractmethod
TILE_SIZE=32

class GameView(ABC):
    """视图基类。定义视图生命周期和核心接口。

    子类必须实现:
        handle_input(cmd) -> None   处理原始用户输入
        get_render_data() -> dict   返回渲染数据给 GameWindow
    """

    view_id: str = ""
    def __init__(self):
        self._command_queue = None
        self._world_snapshot:dict={}
        self._viewport_size=None
        self.current_pos=(0,0)
        self.zoom_level=1.0
        self.mouse_pressed=False
        self.last_mouse_pos=None
    def set_viewport_size(self,width:int,height:int):
        self._viewport_size=(width,height)
    def set_command_queue(self,queue):
        self._command_queue = queue
    def set_world_snapshot(self,snapshot:dict):
        self._world_snapshot = snapshot
    def _screen_to_grid(self,pos:tuple[int,int])->tuple[int,int]:
        """Transform screen position to world grid position."""
        if self.zoom_level <= 0:
            return (0, 0)
        screen_x,screen_y=pos
        world_x=self.current_pos[0]+screen_x/self.zoom_level
        world_y=self.current_pos[1]+screen_y/self.zoom_level
        return (int(world_x//TILE_SIZE),int(world_y//TILE_SIZE))
    def _start_camera_drag(self,pos:tuple[int,int])->None:
        """Start middle-button camera drag."""
        self.mouse_pressed=True
        self.last_mouse_pos=pos
    def _handle_camera_drag(self,pos:tuple[int,int]|None)->None:
        """Move camera while dragging."""
        if (
            not self.mouse_pressed
            or self.last_mouse_pos is None
            or pos is None
        ):
            return
        new_x=self.current_pos[0]-pos[0]+self.last_mouse_pos[0]
        new_y=self.current_pos[1]-pos[1]+self.last_mouse_pos[1]
        self.current_pos=(new_x,new_y)
        self.last_mouse_pos=pos
    def _stop_camera_drag(self)->None:
        """Stop camera drag state."""
        self.mouse_pressed=False
        self.last_mouse_pos=None
    def _handle_wheel_zoom(self,delta:int|None)->None:
        """Zoom camera by wheel delta."""
        if delta is None:
            return
        if delta > 0:
            self.zoom_level*=1.1
        if delta < 0:
            self.zoom_level/=1.1
        self.zoom_level=max(0.25,min(self.zoom_level,4.0))
    @abstractmethod
    def handle_input(self, cmd: dict) -> None:
        """处理原始用户输入，由视图自行解读并生成游戏 Command。

        Args:
            cmd: 原始输入 dict，包含 type, x, y, button 或 key 等字段。
        """
        ...

    @abstractmethod
    def get_render_data(self) -> dict:
        """返回当前帧的渲染数据，将直接推送给 GameWindow 绘制。

        Returns:
            dict 包含 entities, ui_overlay 等绘制所需的数据。
        """
        ...

    def on_enter(self) -> None:
        """视图激活时调用，可用于初始化状态、加载资源等。"""

    def on_exit(self) -> None:
        """视图停用时调用，可用于清理状态、保存进度等。"""
