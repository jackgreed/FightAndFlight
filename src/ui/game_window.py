from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor,QPixmap
TILE_SIZE=32
class GameWindow(QWidget):
    player_command = pyqtSignal(dict)  
    def __init__(self, parent=None):
        super().__init__(parent)
        self._render_data:dict ={}
        self._pixmap_cache:dict[str,QPixmap]={}
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.StrongFocus)#type: ignore
    def _get_pixmap(self,image_path:str)->QPixmap|None:
        """
        get pixmap from disk (with cache)
        """
        if not image_path:
            return None
        pixmap=self._pixmap_cache.get(image_path)
        if pixmap is not None:
            return pixmap
        pixmap=QPixmap(image_path)
        if pixmap.isNull():
            print("[WARN]PICTURE NOT FOUND IN PATH:", image_path)
            return None
        self._pixmap_cache[image_path]=pixmap
        return pixmap
    def on_render_data(self,data:dict):
        self._render_data = data
        self.update()
    def paintEvent(self,event):
        #draw a black background
        painter=QPainter(self)
        painter.fillRect(self.rect(),QColor("black")) 
        if self._render_data is None:            
            return
        camera=self._render_data.get("camera")
        if camera is not None:
            self._draw_grid(painter=painter,camera=camera)
        for sprite in self._render_data.get("sprites",[]):
            x=int(sprite["screen_x"])
            y=int(sprite["screen_y"])
            size=int(sprite["screen_size"])
            image_path=str(sprite["image_path"])
            pixmap=self._get_pixmap(image_path=image_path)
            if pixmap is not None:
                painter.drawPixmap(x, y, size, size, pixmap)
            else:
                painter.fillRect(x, y, size, size, QColor("blue"))
            if sprite.get("is_selected",False):
                painter.setPen(QColor("white"))
                painter.drawRect(x,y,size,size)
    def _button_name(self,button):
        """
        transform QT mouse number to English word
        """
        if button == Qt.LeftButton:#type:ignore
            return "left"
        if button == Qt.RightButton:#type:ignore
            return "right"
        if button == Qt.MiddleButton:#type:ignore
            return "middle"
        return "unknown"   
    
    def mousePressEvent(self,event):
        self.setFocus()  # 确保窗口获得焦点以接收键盘事件
        self.player_command.emit({
            "type": "mouse_press",
            "pos": (event.x(), event.y()),
            "button": self._button_name(event.button())
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
            "button": self._button_name(event.button())
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
    def _draw_grid(self,painter:QPainter,camera:dict):
        """
        draw the grid lines for the map
        """
        zoom=camera.get("zoom",1.0)
        cam_x,cam_y=camera.get("offset",(0,0))
        if zoom<=0:
            print("[ERROR]zoom level should be above 0")
            return
        screen_tile_size=TILE_SIZE*zoom
        if screen_tile_size < 20:
            print("[INFO] tile size to small,skipping grid draw")
            return
        visible_left = cam_x
        visible_top = cam_y
        visible_right = cam_x + self.width() / zoom
        visible_bottom = cam_y + self.height() / zoom

        first_grid_x = int(visible_left // TILE_SIZE) * TILE_SIZE
        first_grid_y = int(visible_top // TILE_SIZE) * TILE_SIZE
        painter.setPen(QColor("grey"))
        x = first_grid_x
        while x <= visible_right:
            screen_x = int((x - cam_x) * zoom)
            painter.drawLine(screen_x, 0, screen_x, self.height())
            x += TILE_SIZE

        y = first_grid_y
        while y <= visible_bottom:
            screen_y = int((y - cam_y) * zoom)
            painter.drawLine(0, screen_y, self.width(), screen_y)
            y += TILE_SIZE

