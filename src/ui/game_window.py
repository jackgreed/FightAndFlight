from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor,QPixmap
TILE_SIZE=32
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
        view_type=self._render_data.get("view")
        if view_type is None:
            return
        elif view_type == "colony":
            camera=self._render_data.get("camera")
            for tile in self._render_data.get("tiles",[]):
                self._draw_tile(painter,tile)
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
            return  
        elif view_type=="worldmap":
            camera=self._render_data.get("camera")
            selected_world_tile=None
            for world_tile in self._render_data.get("world_tiles",[]):
                self._draw_world_tile(painter,world_tile)
                if world_tile.get("is_selected",False):
                    selected_world_tile=world_tile
            if camera is not None:
                self._draw_grid(painter=painter,camera=camera)
            for sprite in self._render_data.get("world_sprites",[]):
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
            if selected_world_tile is not None:
                self._draw_world_tile_selection(painter,selected_world_tile)
            selected_tile=self._render_data.get("selected_tile")
            if selected_tile is not None:
                self._draw_world_tile_info(painter,selected_tile)
            return  
    def _draw_tile(self,painter:QPainter,tile:dict):
        """
        draw a terrain tile by terrain type
        """
        import math
        left = math.floor(tile.get("screen_left", 0))
        top = math.floor(tile.get("screen_top", 0))
        right = math.ceil(tile.get("screen_right", left))
        bottom = math.ceil(tile.get("screen_bottom", top))
        width = right - left
        height = bottom - top
        if width <= 0 or height <= 0:
            return
        terrain_type=tile.get("terrain_type","plain")
        painter.fillRect(left,top,width,height,QColor(TERRAIN_COLORS.get(terrain_type,"#4f6f3a")))
    def _draw_world_tile(self,painter:QPainter,tile:dict):
        import math
        left = math.floor(tile.get("screen_left", 0))
        top = math.floor(tile.get("screen_top", 0))
        right = math.ceil(tile.get("screen_right", left))
        bottom = math.ceil(tile.get("screen_bottom", top))
        width = right - left
        height = bottom - top
        if width <= 0 or height <= 0:
            return
        terrain_type=tile.get("terrain_type","plain")
        painter.fillRect(left,top,width,height,QColor(WORLD_TERRAIN_COLORS.get(terrain_type,"#4f6f3a")))
    def _draw_world_tile_selection(self,painter:QPainter,tile:dict):
        """
        draw selected world tile border
        """
        import math
        left=math.floor(tile.get("screen_left",0))
        top=math.floor(tile.get("screen_top",0))
        right=math.ceil(tile.get("screen_right",left))
        bottom=math.ceil(tile.get("screen_bottom",top))
        width=right-left
        height=bottom-top
        painter.setPen(QColor("white"))
        painter.drawRect(
            left,
            top,
            width,
            height,
        )
    def _draw_world_tile_info(self,painter:QPainter,selected_tile:dict):
        """
        draw selected world tile information
        """
        position=selected_tile.get("position",{})
        info=selected_tile.get("info",{})
        lines=[
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
        panel_x=12
        panel_y=12
        panel_width=230
        line_height=18
        panel_height=16+line_height*len(lines)
        painter.fillRect(
            panel_x,
            panel_y,
            panel_width,
            panel_height,
            QColor(6,9,24,220),
        )
        painter.setPen(QColor("white"))
        for index,line in enumerate(lines):
            painter.drawText(
                panel_x+10,
                panel_y+20+index*line_height,
                line,
            )
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

