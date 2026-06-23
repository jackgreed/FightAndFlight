from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor

class GameWindow(QWidget):
    player_command = pyqtSignal(dict)  
    def __init__(self, parent=None):
        super().__init__(parent)
        self._render_data:dict ={}
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.StrongFocus)#type: ignore
        
    def on_render_data(self,data:dict):
        self._render_data = data
        self.update()
    def paintEvent(self,event):
        #draw a black background
        painter=QPainter(self)
        painter.fillRect(self.rect(),QColor("black")) 
        if self._render_data is None:            
            return
        for sprite in self._render_data.get("sprites",[]):
            x=int(sprite["screen_x"])
            y=int(sprite["screen_y"])
            size=int(sprite["screen_size"])
            painter.fillRect(x,y,size,size,QColor("blue"))
        
    
    def mousePressEvent(self,event):
        self.setFocus()  # 确保窗口获得焦点以接收键盘事件
        self.player_command.emit({
            "type": "mouse_press",
            "pos": (event.x(), event.y()),
            "button": event.button(),
        })

    def mouseMoveEvent(self,event):
        self.player_command.emit({
            "type": "mouse_move",
            "pos": (event.x(), event.y()),
        })
    def mouseReleaseEvent(self,event):
        self.player_command.emit({
            "type": "mouse_release",
            "pos": (event.x(), event.y()),
            "button": event.button(),
        })
    def keyPressEvent(self,event):
        self.player_command.emit({
            "type": "key_press",
            "key": event.key(),
        })
    def wheelEvent(self,event):
        self.player_command.emit({
            "type": "wheel",
            "delta": event.angleDelta().y(),
        })
        