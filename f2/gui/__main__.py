"""
抖音批量下载器GUI项目入口文件
"""

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
import os
from pathlib import Path

# 导入主窗口
from f2.gui.views.main_window import DouyinDownloaderMainWindow


def main():
    """主函数"""
    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # 使用Fusion风格，在所有平台上都看起来不错
    
    # 设置应用程序图标
    icon_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                            "docs", "public", "f2-logo.ico")
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
    else:
        # 尝试备用图标
        alt_icon_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                                   "docs", "public", "f2-logo-with-shadow-mini.png")
        if os.path.exists(alt_icon_path):
            app.setWindowIcon(QIcon(alt_icon_path))
    
    # 创建并显示主窗口
    window = DouyinDownloaderMainWindow()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()