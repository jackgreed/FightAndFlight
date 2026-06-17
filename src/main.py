"""
游戏入口模块
"""
import sys
import os

# 确保 src/ 目录在 sys.path 中，支持直接运行和模块运行两种方式
_src_dir = os.path.dirname(os.path.abspath(__file__))
if _src_dir not in sys.path:
    sys.path.insert(0, _src_dir)

from PyQt5.QtWidgets import QApplication

from ui.main_window import MainWindow
from logic.main_window import MainWindowLogic

 
def main(): 
    app = QApplication(sys.argv)

    window = MainWindow()
    logic = MainWindowLogic(window)
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
