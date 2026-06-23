from ecs.system import System
from .command_queue import Command,CommandQueue
from .eventbus import EventBus
from game.world_manager import WorldManager
from PyQt5.QtCore import QThread,pyqtSignal
class GameLoopThread(QThread):
    tick_completed=pyqtSignal(dict)
    def __init__(self,fps=60,parent=None):
        super().__init__(parent)
        self.world_manager=WorldManager()
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
            if self.world_manager.get_active_world() is None:
                QThread.msleep(100)  # Sleep for a short duration to avoid busy waiting
                continue
            cmds=self.command_queue.drain_all()
            for cmd in cmds:
                if target_world:=self.world_manager.get_world(cmd.world_id):
                    cmd.execute(target_world)
                else:
                    print(f"Warning: World '{cmd.world_id}' not found for command {cmd}.")
            for system in self.systems:
                for world in self.world_manager.worlds.values():
                    system.tick(world,self.event_bus)
            snapshot={}
            for world_id,world in self.world_manager.worlds.items():
                snapshot[world_id]=world.to_dict()
            self.tick_completed.emit(snapshot)
            QThread.msleep(int(1000/self.fps))