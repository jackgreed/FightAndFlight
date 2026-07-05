import copy
import json
from pathlib import Path
from typing import Any
DEFAULT_TEMPLATE_PATH= (
    Path(__file__).resolve().parents[2]
    / "assets"
    / "data"
    / "entities.json"
)
#if mod want to add entity,need to change the path
class EntityTemplateLoader:
    def __init__(self,template_path:Path=DEFAULT_TEMPLATE_PATH):
        self.template_path=template_path
        self._templates:dict[str,dict[str,Any]]={}
    def load(self):
        """
        load from json file
        also validate them
        """
        with self.template_path.open("r",encoding="utf-8") as file:
            data=json.load(file)
        self._validate_templates(data)
        self._templates=data
    def get_template(self,template_id:str)->dict[str,Any]:
        """
        return the entity accroding to the id
        """
        template=self._templates.get(template_id)
        if template is None:
            raise KeyError(f"Entity template not found: {template_id}")
        return copy.deepcopy(template)
    def get_template_ids(self)->list[str]:
        """
        for debug check the template list
        """
        return list(self._templates)
    def add_template(self,template_path:Path):
        """
        add more template(use for mods)
        """

        with template_path.open("r",encoding="utf-8") as file:
            data=json.load(file)
        self._validate_templates(data)
        self._templates.update(data)
    @staticmethod
    def _validate_templates(data: object) -> None:
        """validate the template"""
        if not isinstance(data, dict):
            raise ValueError(
                "Entity template root must be an object"
            )

        for template_id, template in data.items():
            if not isinstance(template_id, str):
                raise ValueError("Template ID must be a string")

            if not isinstance(template, dict):
                raise ValueError(
                    f"Template must be an object: {template_id}"
                )

            name = template.get("name")
            if not isinstance(name, str) or not name:
                raise ValueError(
                    f"Template requires a name: {template_id}"
                )

            components = template.get("components")
            if not isinstance(components, dict):
                raise ValueError(
                    f"Template requires components: {template_id}"
                )

            for component_name, component_data in components.items():
                if not isinstance(component_name, str):
                    raise ValueError(
                        f"Invalid component name: {template_id}"
                    )

                if not isinstance(component_data, dict):
                    raise ValueError(
                        "Component data must be an object: "
                        f"{template_id}.{component_name}"
                    )