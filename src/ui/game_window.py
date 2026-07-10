from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QColor, QPainter, QPixmap
from PyQt5.QtWidgets import QWidget

from ui.renderers import ColonyRenderer, WorldMapRenderer


class GameWindow(QWidget):
    player_command = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._render_data: dict = {}
        self._pixmap_cache: dict[str, QPixmap] = {}
        self._renderers = {
            "colony": ColonyRenderer(self),
            "worldmap": WorldMapRenderer(self),
        }
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.StrongFocus)  # type: ignore

    def get_pixmap(self, image_path: str) -> QPixmap | None:
        """Get pixmap from disk with cache."""
        if not image_path:
            return None
        pixmap = self._pixmap_cache.get(image_path)
        if pixmap is not None:
            return pixmap
        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            print("[WARN]PICTURE NOT FOUND IN PATH:", image_path)
            return None
        self._pixmap_cache[image_path] = pixmap
        return pixmap

    def on_render_data(self, data: dict):
        """Receive render data and request repaint."""
        self._render_data = data
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor("black"))
        if self._render_data is None:
            return
        view_type = self._render_data.get("view")
        renderer = self._renderers.get(view_type)
        if renderer is not None:
            renderer.draw(painter, self._render_data)

    def _button_name(self, button):
        """Transform Qt mouse button value to input button name."""
        if button == Qt.LeftButton:  # type: ignore
            return "left"
        if button == Qt.RightButton:  # type: ignore
            return "right"
        if button == Qt.MiddleButton:  # type: ignore
            return "middle"
        return "unknown"

    def mousePressEvent(self, event):
        self.setFocus()
        self.player_command.emit({
            "type": "mouse_press",
            "pos": (event.x(), event.y()),
            "button": self._button_name(event.button()),
        })

    def mouseMoveEvent(self, event):
        self.player_command.emit({
            "type": "mouse_move",
            "pos": (event.x(), event.y()),
        })

    def mouseReleaseEvent(self, event):
        self.player_command.emit({
            "type": "mouse_release",
            "pos": (event.x(), event.y()),
            "button": self._button_name(event.button()),
        })

    def keyPressEvent(self, event):
        self.player_command.emit({
            "type": "key_press",
            "key": event.key(),
        })

    def wheelEvent(self, event):
        self.player_command.emit({
            "type": "wheel",
            "delta": event.angleDelta().y(),
        })
