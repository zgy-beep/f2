# -*- coding:utf-8 -*-
# @Information  : 
# @Author       : ZGY
# @Date         : 2025-04-29 10:27:20
# @FilePath     : /f2_gui/f2/gui/ui/theme.py
# @LastEditTime : 2025-04-29 10:27:25

# -*- coding:utf-8 -*-
"""
主题管理器 - 处理应用程序的主题和样式
"""

from PyQt5.QtCore import QSettings
from f2.gui.utils.gui_config_manager import GUIConfigManager


class ThemeManager:
    """主题管理器
    
    负责管理应用程序的主题和样式，支持日间模式和夜间模式
    """
    
    # 主题常量
    LIGHT_THEME = "light"
    DARK_THEME = "dark"
    
    # 当前主题，默认为日间模式
    _current_theme = None
    
    @classmethod
    def get_current_theme(cls):
        """获取当前主题"""
        if cls._current_theme is None:
            # 从配置中加载主题设置
            config = GUIConfigManager()
            # 使用get_config方法获取配置，然后再使用字典的get方法获取theme值
            cls._current_theme = config.get_config().get("theme", cls.LIGHT_THEME)
        return cls._current_theme
    
    @classmethod
    def set_theme(cls, theme):
        """设置主题
        
        Args:
            theme: 主题名称，'light'或'dark'
        """
        if theme in [cls.LIGHT_THEME, cls.DARK_THEME]:
            cls._current_theme = theme
            
            # 保存主题设置
            config = GUIConfigManager()
            # 获取现有配置
            current_config = config.get_config()
            # 更新theme设置
            current_config["theme"] = theme
            # 保存更新后的配置
            config.update_config("", current_config)
    
    @classmethod
    def toggle_theme(cls):
        """切换主题"""
        current = cls.get_current_theme()
        new_theme = cls.DARK_THEME if current == cls.LIGHT_THEME else cls.LIGHT_THEME
        cls.set_theme(new_theme)
    
    @classmethod
    def get_style_sheet(cls):
        """获取当前主题的样式表"""
        theme = cls.get_current_theme()
        
        # 基本样式 - 扁平现代化设计
        base_style = """
        /* 全局样式 */
        QWidget {
            font-family: "Microsoft YaHei", "SimHei", "Segoe UI", sans-serif;
            font-size: 10pt;
        }
        
        /* 按钮样式 */
        QPushButton {
            padding: 6px 12px;
            border-radius: 4px;
            font-weight: 500;
            border: none;
        }
        
        QPushButton:hover {
            opacity: 0.9;
        }
        
        QPushButton:pressed {
            opacity: 0.8;
        }
        
        QPushButton:disabled {
            opacity: 0.5;
        }
        
        /* 主要按钮样式 */
        QPushButton#primaryButton {
            font-weight: bold;
        }
        
        /* 次要按钮样式 */
        QPushButton#secondaryButton {
            font-weight: normal;
        }
        
        /* 危险按钮样式 */
        QPushButton#dangerButton {
            font-weight: bold;
        }
        
        /* 工具栏按钮样式 */
        QPushButton#toolbarButton {
            background-color: transparent;
            border-radius: 4px;
            font-weight: normal;
        }
        
        /* 新导航按钮样式 */
        QPushButton#navButton {
            border-radius: 0px;
            padding: 8px 20px;
            font-weight: bold;
            font-size: 11pt;
        }
        
        QPushButton#toolButton {
            padding: 6px 12px;
            border-radius: 4px;
        }
        
        QPushButton#iconButton {
            border-radius: 18px;
            font-size: 18px;
            padding: 0px;
        }
        
        /* 卡片样式 */
        QFrame#card {
            border-radius: 8px;
            padding: 0px;
        }
        
        QLabel#cardTitle {
            font-weight: bold;
            font-size: 12pt;
        }
        
        QLabel#cardDescription {
            opacity: 0.7;
        }
        
        QLabel#appTitle {
            font-weight: bold;
            font-size: 14pt;
        }
        
        /* 应用栏样式 */
        QWidget#appBar {
            padding: 0px;
        }
        
        #separator {
            height: 1px;
        }
        
        /* 选项卡样式 */
        QTabWidget::pane {
            border: none;
            border-radius: 0px;
            top: 0px;
        }
        
        QTabBar::tab {
            padding: 10px 16px;
            margin-right: 2px;
            border: none;
            font-weight: bold;
        }
        
        QTabBar::tab:selected {
            border-bottom: 2px solid;
        }
        
        /* 输入框样式 */
        QLineEdit, QTextEdit {
            padding: 8px;
            border: 1px solid;
            border-radius: 4px;
        }
        
        QLineEdit:focus, QTextEdit:focus {
            border-width: 2px;
        }
        
        /* 列表样式 */
        QListWidget {
            border-radius: 4px;
            border: 1px solid;
            padding: 4px;
        }
        
        QListWidget::item {
            padding: 8px;
            border-radius: 2px;
            margin-bottom: 2px;
        }
        
        QListWidget::item:selected {
            font-weight: bold;
        }
        
        /* 分组框样式 */
        QGroupBox {
            font-weight: bold;
            border: 1px solid;
            border-radius: 4px;
            margin-top: 8px;
            padding-top: 16px;
        }
        
        QGroupBox::title {
            subcontrol-origin: margin;
            subcontrol-position: top left;
            padding: 0 5px;
            left: 10px;
        }
        
        /* 进度条样式 */
        QProgressBar {
            border: none;
            border-radius: 2px;
            text-align: center;
            font-weight: bold;
            height: 16px;
        }
        
        QProgressBar::chunk {
            border-radius: 2px;
        }
        
        /* 滚动条样式 */
        QScrollBar:vertical {
            border: none;
            width: 8px;
            margin: 0px;
        }
        
        QScrollBar::handle:vertical {
            min-height: 30px;
            border-radius: 4px;
        }
        
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            height: 0px;
        }
        
        QScrollBar:horizontal {
            border: none;
            height: 8px;
            margin: 0px;
        }
        
        QScrollBar::handle:horizontal {
            min-width: 30px;
            border-radius: 4px;
        }
        
        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
            width: 0px;
        }
        
        /* 状态栏样式 */
        #statusBar {
            padding: 5px 10px;
        }
        
        /* 日志区域样式 */
        #logOutput {
            font-family: 'Courier New', monospace;
            font-size: 9pt;
            padding: 5px;
        }
        """
        
        # 日间模式样式 - 扁平现代化
        light_style = """
        /* 日间模式颜色方案 */
        QWidget {
            background-color: #ffffff;
            color: #333333;
        }
        
        /* 按钮样式 */
        QPushButton {
            background-color: #e0e0e0;
            color: #333333;
        }
        
        QPushButton:hover {
            background-color: #d0d0d0;
        }
        
        QPushButton:pressed {
            background-color: #c0c0c0;
        }
        
        QPushButton:disabled {
            background-color: #f0f0f0;
            color: #999999;
        }
        
        /* 主要按钮样式 */
        QPushButton#primaryButton {
            background-color: #1976d2;
            color: white;
        }
        
        QPushButton#primaryButton:hover {
            background-color: #1565c0;
        }
        
        QPushButton#primaryButton:pressed {
            background-color: #0d47a1;
        }
        
        /* 次要按钮样式 */
        QPushButton#secondaryButton {
            background-color: #e0e0e0;
            color: #333333;
        }
        
        /* 危险按钮样式 */
        QPushButton#dangerButton {
            background-color: #f44336;
            color: white;
        }
        
        QPushButton#dangerButton:hover {
            background-color: #e53935;
        }
        
        /* 工具栏按钮样式 */
        QPushButton#toolbarButton {
            color: #1976d2;
        }
        
        QPushButton#toolbarButton:hover {
            background-color: rgba(25, 118, 210, 0.1);
        }
        
        /* 选项卡样式 */
        QTabBar::tab {
            background-color: transparent;
            color: #757575;
        }
        
        QTabBar::tab:selected {
            color: #1976d2;
            border-bottom-color: #1976d2;
        }
        
        QTabBar::tab:!selected:hover {
            color: #424242;
        }
        
        /* 输入框样式 */
        QLineEdit, QTextEdit {
            background-color: #ffffff;
            border-color: #bdbdbd;
            color: #333333;
        }
        
        QLineEdit:focus, QTextEdit:focus {
            border-color: #1976d2;
        }
        
        /* 列表样式 */
        QListWidget {
            background-color: #ffffff;
            border-color: #e0e0e0;
        }
        
        QListWidget::item {
            background-color: #f5f5f5;
        }
        
        QListWidget::item:hover {
            background-color: #eeeeee;
        }
        
        QListWidget::item:selected {
            background-color: #e3f2fd;
            color: #1976d2;
        }
        
        /* 分组框样式 */
        QGroupBox {
            border-color: #e0e0e0;
            color: #424242;
        }
        
        /* 进度条样式 */
        QProgressBar {
            background-color: #f5f5f5;
            color: #333333;
        }
        
        QProgressBar::chunk {
            background-color: #1976d2;
        }
        
        /* 滚动条样式 */
        QScrollBar:vertical, QScrollBar:horizontal {
            background-color: #f5f5f5;
        }
        
        QScrollBar::handle:vertical, QScrollBar::handle:horizontal {
            background-color: #bdbdbd;
        }
        
        QScrollBar::handle:vertical:hover, QScrollBar::handle:horizontal:hover {
            background-color: #9e9e9e;
        }
        
        /* 自定义组件样式 */
        #mainToolbar {
            background-color: #f5f5f5;
            border-bottom-color: #e0e0e0;
        }
        
        #toolbar_separator {
            background-color: #e0e0e0;
        }
        
        #versionLabel {
            color: #424242;
        }
        
        #inputFrame, #listFrame, #statsFrame, #infoFrame {
            background-color: #fafafa;
            border: 1px solid #eeeeee;
        }
        
        #logOutput {
            background-color: #f5f5f5;
            color: #333333;
            border: 1px solid #e0e0e0;
        }
        
        #statusBar {
            background-color: #f5f5f5;
            color: #616161;
            border-top: 1px solid #e0e0e0;
        }
        
        #sectionTitle {
            color: #1976d2;
        }
        """
        
        # 夜间模式样式 - 统一版
        dark_style = """
        /* 夜间模式统一配色方案 
         * 背景层次：
         * - 主背景: #202020
         * - 卡片/面板背景: #2d2d2d
         * - 控件背景: #383838
         * - 高亮背景: #484848
         * 
         * 文字层次：
         * - 主要文字: #f0f0f0
         * - 次要文字: #aaaaaa
         * - 标题文字: #ffffff
         * - 提示文字: #888888
         *
         * 强调色：
         * - 主要强调: #4f8cc9
         * - 次要强调: #356ea5
         * - 危险强调: #d73737
         */
        
        /* 全局背景和文字 */
        QWidget {
            background-color: #202020;
            color: #f0f0f0;
        }
        
        /* 表单标签透明背景 */
        QFormLayout QLabel {
            background-color: transparent;
        }
        
        /* 常规标签透明背景 */
        QLabel {
            background-color: transparent;
        }
        
        /* 帮助文本标签 */
        QLabel[wordWrap="true"] {
            background-color: transparent;
            color: #aaaaaa;
        }
        
        /* 设置分组框内的控件透明背景 */
        QGroupBox QLabel, QGroupBox QCheckBox {
            background-color: transparent;
        }
        
        /* 选择框透明背景 */
        QGroupBox QCheckBox {
            background-color: transparent;
        }
        
        /* 按钮基础样式 */
        QPushButton {
            background-color: #383838;
            color: #f0f0f0;
            border: none;
            padding: 6px 12px;
            border-radius: 4px;
        }
        
        QPushButton:hover {
            background-color: #484848;
        }
        
        QPushButton:pressed {
            background-color: #585858;
        }
        
        QPushButton:disabled {
            background-color: #2d2d2d;
            color: #888888;
        }
        
        /* 主要按钮样式 */
        QPushButton#primaryButton {
            background-color: #4f8cc9;
            color: #ffffff;
        }
        
        QPushButton#primaryButton:hover {
            background-color: #5a97d4;
        }
        
        QPushButton#primaryButton:pressed {
            background-color: #407ab5;
        }
        
        QPushButton#primaryButton:disabled {
            background-color: #356ea5;
            color: #c0c0c0;
        }
        
        /* 次要按钮样式 */
        QPushButton#secondaryButton {
            background-color: #383838;
            color: #f0f0f0;
        }
        
        QPushButton#secondaryButton:hover {
            background-color: #484848;
        }
        
        /* 危险按钮样式 */
        QPushButton#dangerButton {
            background-color: #d73737;
            color: #ffffff;
        }
        
        QPushButton#dangerButton:hover {
            background-color: #e24d4d;
        }
        
        /* 导航按钮样式 */
        QPushButton#navButton {
            background-color: transparent;
            border: none;
            padding: 8px 20px;
            border-radius: 0px;
            color: #aaaaaa;
        }
        
        QPushButton#navButton:checked {
            color: #ffffff;
            border-bottom: 2px solid #4f8cc9;
            background-color: #252525;
        }
        
        QPushButton#navButton:hover:!checked {
            color: #f0f0f0;
            background-color: #303030;
        }
        
        /* 工具按钮样式 */
        QPushButton#toolButton {
            background-color: #303030;
            color: #f0f0f0;
        }
        
        QPushButton#toolButton:hover {
            background-color: #404040;
        }
        
        /* 图标按钮样式 */
        QPushButton#iconButton {
            background-color: #383838;
            border-radius: 18px;
            padding: 0px;
        }
        
        QPushButton#iconButton:hover {
            background-color: #484848;
        }
        
        /* 卡片样式 */
        QFrame#card {
            background-color: #2d2d2d;
            border-radius: 6px;
            border: none;
        }
        
        /* 文本样式 */
        QLabel#cardTitle {
            color: #ffffff;
            font-weight: bold;
            font-size: 12pt;
        }
        
        QLabel#cardDescription {
            color: #aaaaaa;
        }
        
        QLabel#appTitle {
            color: #ffffff;
            font-weight: bold;
            font-size: 14pt;
        }
        
        QLabel#sectionTitle {
            color: #4f8cc9;
        }
        
        /* 输入框样式 */
        QLineEdit, QTextEdit {
            background-color: #383838;
            color: #f0f0f0;
            border: 1px solid #484848;
            border-radius: 4px;
            padding: 6px;
            selection-background-color: #4f8cc9;
            selection-color: #ffffff;
        }
        
        QLineEdit:focus, QTextEdit:focus {
            border: 1px solid #4f8cc9;
        }
        
        QLineEdit:disabled, QTextEdit:disabled {
            background-color: #2d2d2d;
            color: #888888;
        }
        
        /* 日期和数字输入框 */
        QDateEdit, QSpinBox {
            background-color: #383838;
            color: #f0f0f0;
            border: 1px solid #484848;
            border-radius: 4px;
            padding: 4px 8px;
        }
        
        QDateEdit:focus, QSpinBox:focus {
            border: 1px solid #4f8cc9;
        }
        
        QDateEdit::drop-down, QSpinBox::up-button, QSpinBox::down-button {
            subcontrol-origin: margin;
            background-color: #484848;
            border: none;
        }
        
        QDateEdit::drop-down:hover, QSpinBox::up-button:hover, QSpinBox::down-button:hover {
            background-color: #585858;
        }
        
        /* 列表样式 */
        QListWidget, QTreeView, QTableView {
            background-color: #2d2d2d;
            border: 1px solid #383838;
            border-radius: 4px;
            alternate-background-color: #333333;
            outline: none;
        }
        
        QListWidget::item {
            padding: 6px 8px;
            background-color: #2d2d2d;
            border-bottom: 1px solid #383838;
        }
        
        QListWidget::item:alternate {
            background-color: #333333;
        }
        
        QListWidget::item:hover {
            background-color: #383838;
        }
        
        QListWidget::item:selected {
            background-color: #4f8cc9;
            color: #ffffff;
        }
        
        /* 滚动条样式 */
        QScrollBar:vertical, QScrollBar:horizontal {
            background-color: #202020;
            border: none;
        }
        
        QScrollBar:vertical {
            width: 8px;
        }
        
        QScrollBar:horizontal {
            height: 8px;
        }
        
        QScrollBar::handle:vertical, QScrollBar::handle:horizontal {
            background-color: #484848;
            border-radius: 4px;
            min-height: 30px;
        }
        
        QScrollBar::handle:vertical:hover, QScrollBar::handle:horizontal:hover {
            background-color: #585858;
        }
        
        QScrollBar::add-line, QScrollBar::sub-line {
            height: 0px;
            width: 0px;
        }
        
        QScrollBar::add-page, QScrollBar::sub-page {
            background: none;
        }
        
        /* 分组框样式 */
        QGroupBox {
            border: 1px solid #383838;
            border-radius: 4px;
            margin-top: 12px;
            font-weight: bold;
            color: #f0f0f0;
            background-color: #2d2d2d;
        }
        
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0px 5px;
            color: #ffffff;
            background-color: transparent;
        }
        
        /* 进度条样式 */
        QProgressBar {
            background-color: #2d2d2d;
            color: #ffffff;
            border: none;
            border-radius: 2px;
            text-align: center;
        }
        
        QProgressBar::chunk {
            background-color: #4f8cc9;
            border-radius: 2px;
        }
        
        /* 分隔线样式 */
        QFrame[frameShape="4"],
        QFrame[frameShape="5"] {
            background-color: #383838;
        }
        
        /* 应用栏和工具栏样式 */
        QWidget#appBar {
            background-color: #252525;
            border-bottom: 1px solid #383838;
        }
        
        /* 分隔线 */
        #separator {
            background-color: #383838;
        }
        
        /* 日志区域样式 */
        #logOutput {
            background-color: #202020;
            color: #f0f0f0;
            border: 1px solid #383838;
            font-family: 'Consolas', 'Courier New', monospace;
            font-size: 9pt;
        }
        
        /* 状态栏样式 */
        #statusBar {
            background-color: #252525;
            color: #aaaaaa;
            border-top: 1px solid #383838;
            padding: 0px 8px;
        }

        /* 修复主页面背景 */
        QStackedWidget, QScrollArea, QWidget#centralWidget {
            background-color: #202020;
        }
        
        /* Tab样式 */
        QTabWidget::pane {
            border: 1px solid #383838;
            background-color: #2d2d2d;
        }
        
        QTabBar::tab {
            background-color: #252525;
            color: #aaaaaa;
            padding: 8px 16px;
            border: none;
            min-width: 100px;
        }
        
        QTabBar::tab:selected {
            background-color: #2d2d2d;
            color: #ffffff;
            border-bottom: 2px solid #4f8cc9;
        }
        
        QTabBar::tab:!selected:hover {
            background-color: #303030;
            color: #f0f0f0;
        }

        /* 对话框背景 */
        QDialog {
            background-color: #202020;
        }
        
        /* 菜单样式 */
        QMenu {
            background-color: #2d2d2d;
            border: 1px solid #383838;
            color: #f0f0f0;
            padding: 4px 0px;
        }
        
        QMenu::item {
            padding: 6px 24px 6px 12px;
            background: transparent;
        }
        
        QMenu::item:selected {
            background-color: #4f8cc9;
            color: #ffffff;
        }
        
        QMenu::separator {
            height: 1px;
            background-color: #383838;
            margin: 4px 0px;
        }
        
        /* 工具提示样式 */
        QToolTip {
            background-color: #484848;
            color: #f0f0f0;
            border: 1px solid #585858;
            padding: 4px 8px;
        }

        /* 复选框样式 */
        QCheckBox {
            background-color: transparent;
            spacing: 8px;
        }
        
        QCheckBox::indicator {
            width: 16px;
            height: 16px;
            border: 1px solid #484848;
            border-radius: 3px;
            background-color: #383838;
        }
        
        QCheckBox::indicator:unchecked:hover {
            border: 1px solid #5a97d4;
            background-color: #404040;
        }
        
        QCheckBox::indicator:checked {
            background-color: #4f8cc9;
            border: 1px solid #4f8cc9;
            image: url(data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxNCIgaGVpZ2h0PSIxNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9IiNmZmZmZmYiIHN0cm9rZS13aWR0aD0iMyIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIiBjbGFzcz0ibHVjaWRlIGx1Y2lkZS1jaGVjayI+PHBhdGggZD0iTTIwIDYgTDkgMTcgTDQgMTIiLz48L3N2Zz4=);
        }
        
        QCheckBox::indicator:checked:hover {
            background-color: #5a97d4;
        }
        
        QCheckBox::indicator:disabled {
            background-color: #2d2d2d;
            border-color: #383838;
        }
        
        QCheckBox::indicator:checked:disabled {
            background-color: #356ea5;
        }
        """
        
        # 根据当前主题返回相应的样式表
        return base_style + (light_style if theme == cls.LIGHT_THEME else dark_style)