"""
视图层 - 每个视图处理特定游戏画面的逻辑。

GameWindow 只是画布，真正的逻辑由当前激活的视图负责。
"""
from logic.views.base import GameView
from logic.views.colony_view import ColonyView
from logic.views.combat_view import CombatView
from logic.views.diplomacy_view import DiplomacyView
from logic.views.loot_view import LootView
from logic.views.world_map_view import WorldMapView