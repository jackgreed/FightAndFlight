from typing import Any

from ecs.component import Component
class InfoPanelComp(Component):
    def __init__(self,panel_id:str,title:str,info:str):
        self.panel_id=panel_id
        self.title=title
        self.info=info
    def to_dict(self):
        return {            
            "panel_id":self.panel_id,
            "title":self.title,
            "info":self.info,
        }
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "InfoPanelComp":
        return cls(
            panel_id=data["panel_id"],
            title=data["title"],
            info=data["info"]
        )
