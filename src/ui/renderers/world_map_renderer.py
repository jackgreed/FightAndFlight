from PyQt5.QtGui import QColor, QPainter

from ui.renderers.base_renderer import BaseRenderer


WORLD_TERRAIN_COLORS = {
    "water": "#28669B",
    "snow": "#DDE7E9",
    "mountain": "#777B7D",
    "tundra": "#98A58D",
    "desert": "#C9AD63",
    "forest": "#315D3A",
    "grass": "#6E9B4B",
    "plain": "#8A9859",
}


class WorldMapRenderer(BaseRenderer):
    """Draw world map view layers."""

    def draw(self, painter: QPainter, data: dict) -> None:
        """Draw world map render data."""
        camera = data.get("camera")
        selected_world_tile = None
        for world_tile in data.get("world_tiles", []):
            self._draw_world_tile(painter, world_tile)
            if world_tile.get("is_selected", False):
                selected_world_tile = world_tile
        if camera is not None:
            self._draw_grid(painter=painter, camera=camera)
        for sprite in data.get("world_sprites", []):
            self._draw_sprite(painter, sprite)
        if selected_world_tile is not None:
            self._draw_world_tile_selection(painter, selected_world_tile)
        selected_tile = data.get("selected_tile")
        if selected_tile is not None:
            self._draw_world_tile_info(painter, selected_tile)

    def _draw_world_tile(self, painter: QPainter, tile: dict) -> None:
        """Draw a world map terrain tile by terrain type."""
        left, top, width, height = self._get_screen_rect(tile)
        if width <= 0 or height <= 0:
            return
        terrain_type = tile.get("terrain_type", "plain")
        painter.fillRect(
            left,
            top,
            width,
            height,
            QColor(WORLD_TERRAIN_COLORS.get(terrain_type, "#4f6f3a")),
        )

    def _draw_world_tile_selection(
        self,
        painter: QPainter,
        tile: dict,
    ) -> None:
        """Draw selected world tile border."""
        left, top, width, height = self._get_screen_rect(tile)
        painter.setPen(QColor("white"))
        painter.drawRect(left, top, width, height)

    def _draw_world_tile_info(
        self,
        painter: QPainter,
        selected_tile: dict,
    ) -> None:
        """Draw selected world tile information."""
        position = selected_tile.get("position", {})
        info = selected_tile.get("info", {})
        lines = [
            f"Position: {position.get('x', 0)}, {position.get('y', 0)}",
            f"Terrain: {selected_tile.get('terrain_type', 'plain')}",
            f"Elevation: {info.get('elevation', 0):.2f}",
            f"Moisture: {info.get('moisture', 0):.2f}",
            f"Temperature: {info.get('temperature', 0):.2f}",
            f"Fertility: {info.get('fertility', 0):.2f}",
            f"Forest: {info.get('forest', 0):.2f}",
            f"Mineral: {info.get('mineral', 0):.2f}",
            f"Water: {info.get('water', 0):.2f}",
        ]
        panel_x = 12
        panel_y = 12
        panel_width = 230
        line_height = 18
        panel_height = 16 + line_height * len(lines)
        painter.fillRect(
            panel_x,
            panel_y,
            panel_width,
            panel_height,
            QColor(6, 9, 24, 220),
        )
        painter.setPen(QColor("white"))
        for index, line in enumerate(lines):
            painter.drawText(
                panel_x + 10,
                panel_y + 20 + index * line_height,
                line,
            )
