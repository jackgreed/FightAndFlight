from PyQt5.QtGui import QColor, QPainter


class PanelRenderer:
    """Draw info panel overlays."""

    def draw_info_panel(self, painter: QPainter, panel: dict) -> None:
        """Draw info panel overlay."""
        rect = panel.get("rect", [12, 12, 320, 180])
        close_rect = panel.get("close_rect", [306, 20, 18, 18])
        x, y, width, height = [int(value) for value in rect]
        close_x, close_y, close_width, close_height = [
            int(value) for value in close_rect
        ]

        painter.fillRect(x, y, width, height, QColor(6, 9, 24, 220))
        painter.setPen(QColor("white"))
        painter.drawRect(x, y, width, height)
        painter.drawText(x + 10, y + 22, str(panel.get("title", "")))

        painter.fillRect(
            close_x,
            close_y,
            close_width,
            close_height,
            QColor(80, 30, 30, 230),
        )
        painter.setPen(QColor("white"))
        painter.drawRect(close_x, close_y, close_width, close_height)
        painter.drawText(close_x + 5, close_y + 14, "X")

        actions = panel.get("actions")
        if actions:
            self._draw_info_panel_actions(painter, actions)
            return

        line_y = y + 48
        for line in str(panel.get("info", "")).splitlines():
            painter.drawText(x + 10, line_y, line[:80])
            line_y += 18
            if line_y > y + height - 10:
                break

    def _draw_info_panel_actions(
        self,
        painter: QPainter,
        actions: list,
    ) -> None:
        """Draw interaction action buttons."""
        for action in actions:
            rect = action.get("rect")
            if rect is None:
                continue
            x, y, width, height = [int(value) for value in rect]
            painter.fillRect(x, y, width, height, QColor(30, 45, 70, 230))
            painter.setPen(QColor("white"))
            painter.drawRect(x, y, width, height)
            painter.drawText(
                x + 8,
                y + 16,
                str(action.get("label", action.get("action_id", ""))),
            )
