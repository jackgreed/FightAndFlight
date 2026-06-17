"""
LootView - 物品/战利品视图

处理物品管理逻辑：装备浏览、词缀查看、物品比对等。
"""
from logic.views.base import GameView


class LootView(GameView):
    """物品/战利品视图。"""

    view_id = "loot"

    def handle_input(self, cmd: dict) -> None:
        """处理物品视图下的用户输入。

        TODO: 实现物品操作逻辑（查看、装备、丢弃等）
        """
        print(f"LootView received input: {cmd}")
        pass

    def get_render_data(self) -> dict:
        """返回物品画面的渲染数据。

        TODO: 返回物品列表、装备槽位、词缀详情等数据。
        """
        return {
            "view": "loot",
            "entities": [],
            "overlay": "loot_placeholder",
        }

    def on_enter(self) -> None:
        """进入物品视图。"""
        pass

    def on_exit(self) -> None:
        """离开物品视图。"""
        pass
