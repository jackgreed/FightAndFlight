"""
MainWindowLogic - 视图管理器

管理视图切换，在 GameWindow（纯画布）和 GameView（逻辑）之间路由数据。

数据流向:
  GameWindow.player_command → MainWindowLogic → 激活的 GameView.handle_input()
  激活的 GameView.get_render_data() → MainWindowLogic → GameWindow.on_render_data()

视图切换:
  按钮点击 → MainWindowLogic → old_view.on_exit() → 切换 → new_view.on_enter()
"""
from PyQt5.QtCore import QObject
import random
from logic.views import GameView, ColonyView, CombatView, DiplomacyView, LootView,WorldMapView
from engine.game_loop import GameLoopThread
import game.systems as game_systems
from game.map_initializer import MapInitializer
class MainWindowLogic(QObject):
    """UI <-> 游戏逻辑 的中介层，同时管理视图切换。"""

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.game_window = main_window.left_widget

        
        self._active_view: GameView | None = None
        self.game_loop=GameLoopThread(fps=30)
        self.game_loop.add_system(game_systems.MovementSystem())
        self.game_loop.tick_completed.connect(self._on_tick)
        # 视图注册表
        self._views: dict[str, GameView] = {
            "colony": ColonyView(),
            #"combat": CombatView(self.game_loop),
            #"diplomacy": DiplomacyView(self.game_loop),
            #"loot": LootView(self.game_loop),
            "world_map":WorldMapView()
        }
        for view in self._views.values():
            view.set_command_queue(self.game_loop.command_queue)
        initer=MapInitializer(self.game_loop.world_manager)
        self.world_map_seed=random.randint(1,2**32-1)
        self.world_map=initer.initialize_specific_world_map(
            size=(11,11),
            noise_level={
                "elevation":2,
                "moisture":3,
                "temperature":4,
                "mineral":2
            },
            #TODO ask user to input the paraments above
            seed=self.world_map_seed,
            name="world_map"
        )
        self.colony_map_seed=random.randint(1,2**32-1)
        self.defaultColonyMap=initer.initalize_specific_colony(
            pos=(5,5),
            size=(100,100),
            seed=self.colony_map_seed,
            name="colony_main"
        )
        self.game_loop.world_manager.set_active_world("colony_main")
        """
        TEST CODE
        """
        entity=self.defaultColonyMap.create_entity("test")#type:ignore
        from game.components import MovementComp,PositionComp,AttributeComp,SpriteComp
        entity.add_component(PositionComp(0,0))
        entity.add_component(MovementComp(0,0))
        entity.add_component(AttributeComp(0.1))
        entity.add_component(SpriteComp())
        """
        /TEST CODE
        """
        self._connect_signals()
        self._connect_buttons()
        # 默认进入殖民地视图
        self._switch_view("colony")
        self.game_loop.start()

    # ─── 信号连接 ─────────────────────────────────────────────────
    def _on_tick(self, snapshot: dict):
        if self._active_view is not None:
            self._active_view.set_world_snapshot(snapshot)
        self._push_render_data()
    def _connect_signals(self):
        """GameWindow 原始输入 → 路由到激活的视图。"""
        self.game_window.player_command.connect(self._on_player_command)

    def _connect_buttons(self):
        """右侧按钮 → 视图切换。"""
        mw = self.main_window
        mw.home_button.clicked.connect(lambda: self._switch_view("colony"))
        mw.battle_button.clicked.connect(lambda: self._switch_view("combat"))
        mw.allies_button.clicked.connect(lambda: self._switch_view("diplomacy"))
        mw.inventory_button.clicked.connect(lambda: self._switch_view("loot"))
        mw.world_map_button.clicked.connect(lambda: self._switch_view("world_map"))

    # ─── 输入路由 ─────────────────────────────────────────────────

    def _on_player_command(self, cmd: dict):
        """将原始用户操作路由到当前激活的视图处理。"""
        if self._active_view is None:
            return
        self._active_view.handle_input(cmd)
        self._push_render_data()

    # ─── 视图切换 ─────────────────────────────────────────────────

    def _switch_view(self, view_id: str):
        """切换到指定视图。"""
        new_view = self._views.get(view_id)
        if new_view is None or new_view is self._active_view:
            return

        if self._active_view is not None:
            self._active_view.on_exit()

        self._active_view = new_view
        self._active_view.on_enter()
        self._push_render_data()

    # ─── 渲染数据推送 ─────────────────────────────────────────────

    def _push_render_data(self):
        """从激活的视图获取渲染数据，推送到 GameWindow。"""
        if self._active_view is None:
            return
        self._active_view.set_viewport_size(
            self.game_window.width(),
            self.game_window.height()
        )
        data = self._active_view.get_render_data()
        self.game_window.on_render_data(data)
