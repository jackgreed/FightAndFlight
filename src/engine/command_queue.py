from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any
from ecs.world import World

COMMAND_REGISTRY: dict[str, type["Command"]] = {}


class Command(ABC):
    def __init_subclass__(cls, **kwargs):
        """Register concrete Command subclasses by class name."""
        super().__init_subclass__(**kwargs)
        COMMAND_REGISTRY[cls.__name__] = cls

    @abstractmethod
    def __init__(self,world_id:str,*args,**kwargs):
        self.world_id=world_id
    @abstractmethod
    def execute(self,world:World):
        ...
    @abstractmethod
    def to_dict(self):
        ...
    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict[str, Any]) -> Command:
        ...
from PyQt5.QtCore import QMutex,QMutexLocker
class CommandQueue:
    def __init__(self):
        self.queue: list[Command] = []
        self.mutex = QMutex()
    def push(self, cmd: Command):
        locker=QMutexLocker(self.mutex)
        self.queue.append(cmd)
    def push_batch(self, cmds: list[Command]):
        locker=QMutexLocker(self.mutex)
        self.queue.extend(cmds)
    def drain_all(self) -> list[Command]:
        locker=QMutexLocker(self.mutex)
        cmds = self.queue.copy()
        self.queue.clear()
        return cmds
    def size(self) -> int:
        locker=QMutexLocker(self.mutex)
        return len(self.queue)
    def clear(self):
        locker=QMutexLocker(self.mutex)
        self.queue.clear()
