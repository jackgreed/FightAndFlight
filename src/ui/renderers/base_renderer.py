import math

from PyQt5.QtGui import QColor, QPainter


TILE_SIZE = 32


class BaseRenderer:
    """Shared renderer helpers for game views."""

    def __init__(self, viewport):
        self.viewport = viewport

    def _draw_sprite(self, painter: QPainter, sprite: dict) -> None:
        """Draw sprite image or fallback color block."""
        x = int(sprite["screen_x"])
        y = int(sprite["screen_y"])
        size = int(sprite["screen_size"])
        image_path = str(sprite["image_path"])
        pixmap = self.viewport.get_pixmap(image_path=image_path)
        if pixmap is not None:
            painter.drawPixmap(x, y, size, size, pixmap)
        else:
            painter.fillRect(x, y, size, size, QColor("blue"))
        if sprite.get("is_selected", False):
            painter.setPen(QColor("white"))
            painter.drawRect(x, y, size, size)

    def _draw_grid(self, painter: QPainter, camera: dict) -> None:
        """Draw grid lines for the active map."""
        zoom = camera.get("zoom", 1.0)
        cam_x, cam_y = camera.get("offset", (0, 0))
        if zoom <= 0:
            print("[ERROR]zoom level should be above 0")
            return
        screen_tile_size = TILE_SIZE * zoom
        if screen_tile_size < 20:
            return
        visible_left = cam_x
        visible_top = cam_y
        visible_right = cam_x + self.viewport.width() / zoom
        visible_bottom = cam_y + self.viewport.height() / zoom

        first_grid_x = int(visible_left // TILE_SIZE) * TILE_SIZE
        first_grid_y = int(visible_top // TILE_SIZE) * TILE_SIZE
        painter.setPen(QColor("grey"))
        x = first_grid_x
        while x <= visible_right:
            screen_x = int((x - cam_x) * zoom)
            painter.drawLine(screen_x, 0, screen_x, self.viewport.height())
            x += TILE_SIZE

        y = first_grid_y
        while y <= visible_bottom:
            screen_y = int((y - cam_y) * zoom)
            painter.drawLine(0, screen_y, self.viewport.width(), screen_y)
            y += TILE_SIZE

    @staticmethod
    def _get_screen_rect(tile: dict) -> tuple[int, int, int, int]:
        """Return integer screen rect from render tile data."""
        left = math.floor(tile.get("screen_left", 0))
        top = math.floor(tile.get("screen_top", 0))
        right = math.ceil(tile.get("screen_right", left))
        bottom = math.ceil(tile.get("screen_bottom", top))
        return left, top, right - left, bottom - top
