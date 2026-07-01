from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5.QtCore import Qt
from ui.game_window import GameWindow

BUTTON_STYLE = """
    QPushButton {
        background-color: rgba(10, 14, 39, 200);
        color: #00e5ff;
        font-family: "Consolas", "Courier New", monospace;
        font-size: 16px;
        font-weight: bold;
        padding: 14px 18px;
        border: 1px solid #00e5ff;
        border-radius: 4px;
        text-align: left;
        letter-spacing: 2px;
    }
    QPushButton:hover {
        background-color: rgba(0, 229, 255, 20);
        border: 1px solid #40f0ff;
        color: #40f0ff;
    }
    QPushButton:pressed {
        background-color: rgba(0, 229, 255, 40);
        border: 1px solid #80f8ff;
        color: #80f8ff;
    }
"""

MAIN_STYLE = """
    QMainWindow {
        background-color: #060918;
    }
    QWidget#central {
        background-color: #0a0e27;
    }
    QWidget#right_panel {
        background-color: rgba(6, 9, 24, 180);
        border-left: 1px solid #1a2a4a;
    }
"""


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet(MAIN_STYLE)

        self.left_widget = GameWindow()

        self.right_panel = QWidget()
        self.right_panel.setObjectName("right_panel")
        self.right_layout = QVBoxLayout()
        self.right_layout.setContentsMargins(12, 12, 12, 12)
        self.right_layout.setSpacing(0)
        self.right_panel.setLayout(self.right_layout)

        self.battle_button = QPushButton("BATTLE")
        self.battle_button.setStyleSheet(BUTTON_STYLE)
        self.battle_button.setCursor(Qt.PointingHandCursor)#type:ignore

        self.home_button = QPushButton("HOME")
        self.home_button.setStyleSheet(BUTTON_STYLE)
        self.home_button.setCursor(Qt.PointingHandCursor)#type:ignore

        self.inventory_button = QPushButton("INVENTORY")
        self.inventory_button.setStyleSheet(BUTTON_STYLE)
        self.inventory_button.setCursor(Qt.PointingHandCursor)#type:ignore

        self.allies_button = QPushButton("ALLIES")
        self.allies_button.setStyleSheet(BUTTON_STYLE)
        self.allies_button.setCursor(Qt.PointingHandCursor)#type:ignore

        self.world_map_button = QPushButton("WORLD")
        self.world_map_button.setStyleSheet(BUTTON_STYLE)
        self.world_map_button.setCursor(Qt.PointingHandCursor)#type:ignore

        self.right_layout.addStretch()
        self.right_layout.addWidget(self.battle_button)
        self.right_layout.addStretch()
        self.right_layout.addWidget(self.home_button)
        self.right_layout.addStretch()
        self.right_layout.addWidget(self.inventory_button)
        self.right_layout.addStretch()
        self.right_layout.addWidget(self.allies_button)
        self.right_layout.addStretch()
        self.right_layout.addWidget(self.world_map_button)
        self.right_layout.addStretch()
        
        self.main_layout = QHBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.main_layout.addWidget(self.left_widget, 4)
        self.main_layout.addWidget(self.right_panel, 1)

        self.central_widget = QWidget()
        self.central_widget.setObjectName("central")
        self.central_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.central_widget)
