from PyQt5.QtGui import QColor, QPainter

from ui.renderers.base_renderer import BaseRenderer
from ui.renderers.panel_renderer import PanelRenderer


TERRAIN_COLORS = {
    "plain": "#4f6f3a",
    "grass": "#3f8f3a",
    "dry_plain": "#8a7a45",
    "desert": "#b99b55",
    "snow": "#d8e2e6",
    "ice": "#9ccfd8",
    "rock": "#5d5f63",
    "ore": "#7a6a8f",
    "water": "#245c8f",
    "forest": "#245f32",
}


class ColonyRenderer(BaseRenderer):
    """Draw colony view layers."""

    def __init__(self, viewport):
        super().__init__(viewport)
        self._panel_renderer = PanelRenderer()

    def draw(self, painter: QPainter, data: dict) -> None:
        """Draw colony render data."""
        camera = data.get("camera")
        for tile in data.get("tiles", []):
            self._draw_tile(painter, tile)
        if camera is not None:
            self._draw_grid(painter=painter, camera=camera)
        for sprite in data.get("sprites", []):
            self._draw_sprite(painter, sprite)
        info_panel = data.get("info_panel")
        if info_panel is not None:
            self._panel_renderer.draw_info_panel(painter, info_panel)

    def _draw_tile(self, painter: QPainter, tile: dict) -> None:
        """Draw a colony terrain tile by terrain type."""
        left, top, width, height = self._get_screen_rect(tile)
        if width <= 0 or height <= 0:
            return
        terrain_type = tile.get("terrain_type", "plain")
        painter.fillRect(
            left,
            top,
            width,
            height,
            QColor(TERRAIN_COLORS.get(terrain_type, "#4f6f3a")),
        )
