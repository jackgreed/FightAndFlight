from ecs.world import World
from ecs.system import System
from .command_queue import Command,CommandQueue
from .eventbus import EventBus
from PyQt5.QtCore import QThread,pyqtSignal
class GameLoopThread(QThread):
    tick_completed=pyqtSignal(dict)
    def __init__(self,fps=60,parent=None):
        super().__init__(parent)
        self.world=World()
        self.command_queue=CommandQueue()
        self.event_bus=EventBus()
        self.systems: list[System] = []
        self.fps=fps
        self.running=True
    def add_system(self,system:System):
        if system not in self.systems:
            self.systems.append(system)
    def remove_system(self,system:System):
        if system in self.systems:
            self.systems.remove(system)
    def push_command(self,cmd:Command):
        self.command_queue.push(cmd)
    def set_fps(self,fps:int):
        self.fps=fps
    def stop(self):
        self.running=False
    def run(self):
        while self.running:
            cmds=self.command_queue.drain_all()
            for cmd in cmds:
                cmd.execute(self.world)
            for system in self.systems:
                system.tick(self.world,self.event_bus)
            snapshot=self.world.to_dict()
            self.tick_completed.emit(snapshot)
            QThread.msleep(int(1000/self.fps))