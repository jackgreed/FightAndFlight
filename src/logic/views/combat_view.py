"""
CombatView - 战棋战斗视图

处理战斗逻辑：网格移动、回合制、AI 战术等。
"""
from logic.views.base import GameView


class CombatView(GameView):
    """战棋战斗视图。"""

    view_id = "combat"

    def handle_input(self, cmd: dict) -> None:
        """处理战斗视图下的用户输入。

        TODO: 实现战棋操作逻辑（选择单位、移动、攻击等）
        """
        print(f"CombatView received input: {cmd}")
        pass

    def get_render_data(self) -> dict:
        """返回战斗画面的渲染数据。

        TODO: 返回战斗网格、单位位置、行动范围等数据。
        """
        return {
            "view": "combat",
            "entities": [],
            "overlay": "combat_placeholder",
        }

    def on_enter(self) -> None:
        """进入战斗视图。"""
        pass

    def on_exit(self) -> None:
        """离开战斗视图。"""
        pass
