import copy
from pathlib import Path
from typing import Any

import game.components
from ecs import Entity,World,COMPONENT_REGISTRY
from game.entity_templates.loader import EntityTemplateLoader
ASSET_ROOT=(
    Path(__file__).resolve().parents[2]
    / "assets"
)
class EntityFactory:
    """
    use template to create entity
    """
    def __init__(self,loader:EntityTemplateLoader,asset_root:Path=ASSET_ROOT):
        self.loader=loader
        self.asset_root=asset_root
    def create_entity(self,world:World,template_id:str,overrides: dict[str, dict[str, Any]] | None = None,name: str | None = None):
        """
        create entity
        """
        template = self.loader.get_template(template_id)
        component_data = template["components"]
        overrides = overrides or {}  # determine the componets 
        for component_name, override_data in overrides.items():
            base_data = component_data.setdefault(
                component_name,
                {},
            )#empty first
            base_data.update(copy.deepcopy(override_data))

        components = []
        #create components one by one
        for component_name, data in component_data.items():
            component_class = COMPONENT_REGISTRY.get(
                component_name
            )
            if component_class is None:
                raise ValueError(
                    f"Unregistered component: {component_name}"
                )

            resolved_data = self._resolve_component_data(
                component_name,
                data,
            )

            try:
                component = component_class.from_dict(
                    resolved_data
                )
            except Exception as error:
                raise ValueError(
                    "Invalid component data: "
                    f"{template_id}.{component_name}"
                ) from error

            components.append(component)
        #create entity
        entity = world.create_entity(
            name=name or template["name"]
        )

        for component in components:
            entity.add_component(component)

        return entity

    def _resolve_component_data(
        self,
        component_name: str,
        data: dict[str, Any],
    ) -> dict[str, Any]:
        """resolve the path of assets"""
        resolved = copy.deepcopy(data)
        #currently only spritecomp need resolve,TODO:when we add audios and videos,update this
        if component_name == "SpriteComp":
        

            image_path = resolved.get("image_path")
            if not image_path:
                return resolved

            path = Path(image_path)
            if not path.is_absolute():
                resolved["image_path"] = str(
                    self.asset_root / path
                )

        return resolved       