# -*- coding:utf-8 -*-
# @Information  : 
# @Author       : ZGY
# @Date         : 2025-04-28 10:40:39
# @FilePath     : /f2_gui/f2/gui/views/main_window.py
# @LastEditTime : 2025-04-29 11:35:44

"""
抖音下载器主窗口
"""

from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QMessageBox, QStatusBar, QHBoxLayout, QPushButton, QLabel, QFrame, QStackedWidget)
from PyQt5.QtCore import QThread
from PyQt5.QtGui import QIcon

# 导入F2模块

# 导入GUI模块
from f2.gui.models.history_manager import HistoryManager
from f2.gui.ui.dialogs.history_dialog import HistoryDialog
from f2.gui.controllers.download_worker import DownloadWorker
from f2.gui.controllers.single_video_downloader import SingleVideoDownloader
from f2.gui.utils.output_redirector import OutputRedirector
from f2.gui.ui.theme import ThemeManager
from f2.gui.version import get_version
from f2.gui.resources.resource_manager import load_pixmap

# 导入分解后的UI组件
from f2.gui.ui.download_tab import DownloadTabUI
from f2.gui.ui.settings_tab import SettingsTabUI

# 导入控制器和模型
from f2.gui.controllers.user_manager import UserManager
from f2.gui.controllers.download_controller import DownloadController
from f2.gui.models.settings_manager import SettingsManager
from f2.gui.models.log_manager import LogManager


class DouyinDownloaderMainWindow(QMainWindow):
    """
    抖音下载器GUI主窗口 - 重新设计的现代简洁界面
    """
    def __init__(self):
        super().__init__()
        
        # 窗口设置
        self.setWindowTitle("抖音下载工具")
        self.setGeometry(100, 100, 1000, 700)
        
        # 创建主窗口部件
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # 主布局
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # 创建顶部应用栏
        self.create_app_bar()
        
        # 创建主内容区域
        self.create_main_content()
        
        # 创建状态栏
        self.statusBar = QStatusBar()
        self.statusBar.setObjectName("statusBar")
        self.statusBar.setFixedHeight(28)
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage(f"抖音下载工具 v{get_version()} | 准备就绪")
        
        # 初始化模型
        self.history_manager = HistoryManager()
        self.log_manager = LogManager(self.download_ui)
        self.settings_manager = SettingsManager(self.settings_ui)
        
        # 初始化控制器
        self.user_manager = UserManager(self.download_ui, self.history_manager)
        self.download_controller = DownloadController(self.download_ui)
        
        # 单个视频下载控制器
        self.single_video_downloader = None
        self.single_video_thread = None
        
        # 设置日志连接
        self.setup_logs()
        
        # 设置信号和槽
        self.setup_connections()
        
        # 初始化输出重定向
        self.setup_output_redirect()
        
        # 加载配置
        self.settings_manager.load_config()
        
        # 应用当前主题
        self.apply_current_theme()
    
    def create_app_bar(self):
        """创建顶部应用栏"""
        app_bar = QWidget()
        app_bar.setObjectName("appBar")
        app_bar.setFixedHeight(56)
        app_bar_layout = QHBoxLayout(app_bar)
        app_bar_layout.setContentsMargins(16, 0, 16, 0)
        
        # 应用标志和标题
        app_info_layout = QHBoxLayout()
        app_info_layout.setSpacing(12)
        
        # 图标
        app_icon = QLabel()
        app_icon.setFixedSize(32, 32)
        app_icon.setObjectName("appIcon")
        app_icon_pixmap = load_pixmap("f2-logo")
        if not app_icon_pixmap.isNull():
            app_icon.setPixmap(app_icon_pixmap)
            app_icon.setScaledContents(True)
        
        app_title = QLabel("抖音下载工具")
        app_title.setObjectName("appTitle")
        
        app_info_layout.addWidget(app_icon)
        app_info_layout.addWidget(app_title)
        
        # 主导航按钮 - 使用现代的分段控件替代标签页
        self.nav_buttons = QFrame()
        self.nav_buttons.setObjectName("navButtons")
        nav_layout = QHBoxLayout(self.nav_buttons)
        nav_layout.setContentsMargins(0, 0, 0, 0)
        nav_layout.setSpacing(1)
        
        self.download_button = QPushButton("下载")
        self.download_button.setObjectName("navButton")
        self.download_button.setCheckable(True)
        self.download_button.setChecked(True)
        
        self.settings_button = QPushButton("设置")
        self.settings_button.setObjectName("navButton")
        self.settings_button.setCheckable(True)
        
        nav_layout.addWidget(self.download_button)
        nav_layout.addWidget(self.settings_button)
        
        # 右侧工具按钮
        tools_layout = QHBoxLayout()
        tools_layout.setSpacing(8)
        
        self.history_button = QPushButton("历史记录")
        self.history_button.setObjectName("toolButton")
        self.history_button.setIcon(QIcon.fromTheme("history", QIcon()))
        
        self.theme_button = QPushButton()
        self.theme_button.setObjectName("iconButton")
        self.theme_button.setFixedSize(36, 36)
        self.theme_button.setToolTip("切换主题")
        
        tools_layout.addWidget(self.history_button)
        tools_layout.addWidget(self.theme_button)
        
        # 添加到应用栏
        app_bar_layout.addLayout(app_info_layout)
        app_bar_layout.addStretch(1)
        app_bar_layout.addWidget(self.nav_buttons)
        app_bar_layout.addStretch(1)
        app_bar_layout.addLayout(tools_layout)
        
        # 添加到主布局
        self.main_layout.addWidget(app_bar)
        
        # 添加分隔线
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setObjectName("separator")
        separator.setFixedHeight(1)
        self.main_layout.addWidget(separator)
    
    def create_main_content(self):
        """创建主内容区域"""
        # 创建内容堆栈
        self.content_stack = QStackedWidget()
        self.main_layout.addWidget(self.content_stack)
        
        # 创建下载页面
        self.download_page = QWidget()
        self.download_ui = DownloadTabUI(self.download_page)
        self.content_stack.addWidget(self.download_page)
        
        # 创建设置页面
        self.settings_page = QWidget()
        self.settings_ui = SettingsTabUI(self.settings_page)
        self.content_stack.addWidget(self.settings_page)
    
    def toggle_theme(self):
        """切换主题"""
        ThemeManager.toggle_theme()
        self.apply_current_theme()
    
    def apply_current_theme(self):
        """应用当前主题到整个应用程序"""
        stylesheet = ThemeManager.get_style_sheet()
        self.setStyleSheet(stylesheet)
        
        # 更新主题按钮图标
        if ThemeManager.get_current_theme() == ThemeManager.LIGHT_THEME:
            self.theme_button.setText("🌙")  # 夜间模式图标
        else:
            self.theme_button.setText("☀️")  # 日间模式图标
        
        # 记录主题变更
        theme_name = "日间模式" if ThemeManager.get_current_theme() == ThemeManager.LIGHT_THEME else "夜间模式"
        if hasattr(self, 'log_manager'):
            self.log_manager.log_message.emit(f"已切换到{theme_name}")
    
    def setup_logs(self):
        """设置日志连接"""
        self.settings_manager.set_log_handler(self.log_manager.log_message.emit)
    
    def setup_connections(self):
        """设置信号和槽连接"""
        # 导航按钮
        self.download_button.clicked.connect(lambda: self.switch_page(0))
        self.settings_button.clicked.connect(lambda: self.switch_page(1))
        
        # 工具按钮
        self.history_button.clicked.connect(self.show_history)
        self.theme_button.clicked.connect(self.toggle_theme)
        
        # 下载相关按钮
        self.download_ui.show_history_signal.connect(self.show_history)
        self.download_ui.start_button.clicked.connect(self.prepare_download)
        self.download_ui.download_single_button.clicked.connect(self.download_single_video)
    
    def switch_page(self, index):
        """切换页面"""
        # 更新导航按钮状态
        self.download_button.setChecked(index == 0)
        self.settings_button.setChecked(index == 1)
        
        # 切换到相应页面
        self.content_stack.setCurrentIndex(index)
    
    def setup_output_redirect(self):
        """设置输出重定向"""
        self.output_redirector = OutputRedirector()
        self.output_redirector.outputWritten.connect(self.log_manager.log_message.emit)
    
    def show_history(self):
        """显示历史记录对话框"""
        history_dialog = HistoryDialog(self.history_manager, self)
        history_dialog.userSelected.connect(self.user_manager.add_user_from_history)
        history_dialog.exec_()
    
    def prepare_download(self):
        """准备开始下载"""
        # 检查用户列表是否为空
        user_ids = self.user_manager.get_user_ids()
        if not user_ids:
            QMessageBox.warning(self, "提示", "下载队列为空，请先添加用户")
            return
        
        # 获取配置
        config = self.settings_manager.get_config()
        
        # 创建下载工作器
        download_worker = DownloadWorker(user_ids, config)
        download_worker.history_manager = self.history_manager
        
        # 设置下载控制器的工作器
        self.download_controller.set_download_worker(download_worker)
        
        # 开始下载
        self.download_controller.start_download()
    
    def download_single_video(self):
        """下载单个视频"""
        # 获取视频链接
        video_link = self.download_ui.get_link_input_text().strip()
        
        if not video_link:
            QMessageBox.warning(self, "提示", "请输入视频链接")
            return
        
        # 检查是否已经在下载中
        if self.single_video_thread and self.single_video_thread.isRunning():
            QMessageBox.warning(self, "提示", "正在下载视频，请等待当前下载完成")
            return
        
        # 获取配置
        config = self.settings_manager.get_config()
        
        # 创建单个视频下载器
        self.single_video_downloader = SingleVideoDownloader(video_link, config)
        self.single_video_downloader.history_manager = self.history_manager
        
        # 连接信号
        self.single_video_downloader.started.connect(self.on_single_video_download_started)
        self.single_video_downloader.progress.connect(self.log_manager.log_message.emit)
        self.single_video_downloader.finished.connect(self.on_single_video_download_finished)
        self.single_video_downloader.error.connect(self.on_single_video_download_error)
        
        # 创建线程
        self.single_video_thread = QThread()
        self.single_video_downloader.moveToThread(self.single_video_thread)
        
        # 启动线程
        self.single_video_thread.started.connect(self.single_video_downloader.download)
        self.single_video_thread.start()
    
    def on_single_video_download_started(self):
        """单个视频下载开始回调"""
        self.log_manager.log_message.emit("==== 开始下载视频 ====")
        self.download_ui.set_video_download_in_progress(True)
        self.statusBar.showMessage("正在下载视频...")
    
    def on_single_video_download_finished(self):
        """单个视频下载完成回调"""
        self.log_manager.log_message.emit("==== 视频下载完成 ====")
        self.download_ui.set_video_download_in_progress(False)
        self.statusBar.showMessage(f"抖音下载工具 v{get_version()} | 准备就绪")
    
    def on_single_video_download_error(self, error_message):
        """单个视频下载错误回调"""
        self.log_manager.log_message.emit(f"错误: {error_message}")
        QMessageBox.critical(self, "下载错误", error_message)
        self.on_single_video_download_finished()
    
    def closeEvent(self, event):
        """窗口关闭事件"""
        # 检查批量下载是否在进行
        batch_download_running = (hasattr(self, 'download_controller') and 
            hasattr(self.download_controller, 'download_worker') and 
            self.download_controller.download_worker and 
            self.download_controller.download_worker.is_running)
            
        # 检查单个视频下载是否在进行
        single_download_running = (self.single_video_thread and 
            self.single_video_thread.isRunning() and 
            self.single_video_downloader and 
            self.single_video_downloader.is_running)
            
        if batch_download_running or single_download_running:
            reply = QMessageBox.question(
                self, "确认", "下载任务正在进行，确定要退出吗？",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                # 停止批量下载
                if batch_download_running:
                    self.download_controller.download_worker.is_running = False
                    
                    if (hasattr(self.download_controller, 'download_thread') and 
                        self.download_controller.download_thread and 
                        self.download_controller.download_thread.isRunning()):
                        self.download_controller.download_thread.quit()
                        self.download_controller.download_thread.wait(3000)  # 等待3秒
                
                # 停止单个视频下载
                if single_download_running:
                    self.single_video_downloader.is_running = False
                    self.single_video_thread.quit()
                    self.single_video_thread.wait(3000)  # 等待3秒
                
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()