"""
ColonyView - 战棋殖民视图

处理殖民逻辑：建筑建造、资源管理、单位生产等。
"""
from logic.views.base import GameView


class ColonyView(GameView):
    """战棋殖民视图。"""

    view_id = "colony"

    def handle_input(self, cmd: dict) -> None:
        """处理殖民视图下的用户输入。

        TODO: 实现殖民操作逻辑（建造建筑、管理资源、生产单位等）
        """
        print(f"ColonyView received input: {cmd}")
        pass

    def get_render_data(self) -> dict:
        """返回殖民画面的渲染数据。

        TODO: 返回殖民网格、单位位置、行动范围等数据。
        """
        return {
            "view": "colony",
            "entities": [],
            "overlay": "colony_placeholder",
        }

    def on_enter(self) -> None:
        """进入殖民视图。"""
        pass

    def on_exit(self) -> None:
        """离开殖民视图。"""
        pass
