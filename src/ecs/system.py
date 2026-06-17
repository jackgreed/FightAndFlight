from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any
from .world import World
class System(ABC):
    @abstractmethod
    def tick(self,world:World,*args,**kwargs):
        pass
