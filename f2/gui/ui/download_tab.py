"""
抖音下载器 - 下载标签页UI组件
"""

from PyQt5.QtWidgets import (
    QVBoxLayout, QWidget, QTabWidget, QHBoxLayout, QPushButton, 
    QLabel, QFrame, QLineEdit, QListWidget, QGroupBox, QGridLayout,
    QTextEdit, QSplitter, QListWidgetItem
)
from PyQt5.QtCore import Qt, pyqtSignal, QObject
from PyQt5.QtGui import QIcon, QFont

class DownloadTabUI(QObject):
    """下载标签页UI组件 - 扁平化现代设计"""
    
    # 定义信号
    show_history_signal = pyqtSignal()  # 显示历史记录对话框的信号
    
    def __init__(self, parent):
        """初始化下载标签页UI组件
        
        Args:
            parent: 父窗口组件
        """
        super().__init__()  # 必须调用QObject的初始化方法，否则信号无法工作
        self.parent = parent
        
        # 设置UI
        self.setup_ui()
    
    def setup_ui(self):
        """设置下载标签页UI - 采用扁平化设计"""
        # 主布局
        main_layout = QVBoxLayout(self.parent)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 创建可分割的上下区域
        splitter = QSplitter(Qt.Vertical)
        splitter.setHandleWidth(1)  # 更细的分割线
        splitter.setStyleSheet("QSplitter::handle { background-color: #cccccc; }")
        
        # 创建上部内容区域（分页区域）
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        # 创建下部日志区域
        log_widget = QWidget()
        log_layout = QVBoxLayout(log_widget)
        log_layout.setContentsMargins(5, 5, 5, 5)
        
        # 创建选项卡控件（上部内容）
        self.tab_widget = QTabWidget()
        self.tab_widget.setObjectName("downloadTabs")
        self.tab_widget.setDocumentMode(True)  # 扁平化选项卡
        content_layout.addWidget(self.tab_widget)
        
        # 批量下载选项卡
        self.batch_tab = QWidget()
        self.setup_batch_download_tab(self.batch_tab)
        self.tab_widget.addTab(self.batch_tab, "批量下载")
        
        # 单个视频下载选项卡
        self.single_tab = QWidget()
        self.setup_single_download_tab(self.single_tab)
        self.tab_widget.addTab(self.single_tab, "单个视频下载")
        
        # 创建日志组件
        self.setup_log_component(log_layout)
        
        # 添加组件到分割器
        splitter.addWidget(content_widget)
        splitter.addWidget(log_widget)
        
        # 设置分割器的初始大小
        splitter.setSizes([600, 200])
        
        # 添加分割器到主布局
        main_layout.addWidget(splitter)
    
    def setup_batch_download_tab(self, parent):
        """设置批量下载选项卡UI"""
        # 创建布局
        layout = QVBoxLayout(parent)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        
        # 创建输入区域
        input_frame = QFrame()
        input_frame.setObjectName("inputFrame")
        input_layout = QHBoxLayout(input_frame)
        input_layout.setContentsMargins(15, 10, 15, 10)
        
        # 用户ID输入
        self.user_id_input = QLineEdit()
        self.user_id_input.setPlaceholderText("请输入抖音用户ID或用户主页链接...")
        self.user_id_input.setObjectName("userIdInput")
        
        # 添加按钮
        self.add_user_button = QPushButton("添加")
        self.add_user_button.setObjectName("primaryButton")
        self.add_user_button.setCursor(Qt.PointingHandCursor)
        
        # 历史记录按钮
        self.history_button = QPushButton("历史")
        self.history_button.setObjectName("secondaryButton")
        self.history_button.setCursor(Qt.PointingHandCursor)
        # 连接历史按钮到显示历史记录信号
        self.history_button.clicked.connect(self.show_history_signal.emit)
        
        # 将组件添加到输入布局
        input_layout.addWidget(self.user_id_input, 1)
        input_layout.addWidget(self.add_user_button)
        input_layout.addWidget(self.history_button)
        
        # 用户列表区域
        list_frame = QFrame()
        list_frame.setObjectName("listFrame")
        list_layout = QVBoxLayout(list_frame)
        list_layout.setContentsMargins(15, 10, 15, 10)
        
        # 添加列表标题
        list_header = QHBoxLayout()
        list_header.setContentsMargins(0, 0, 0, 5)
        
        list_title = QLabel("下载队列")
        list_title.setObjectName("sectionTitle")
        
        self.clear_all_button = QPushButton("清空")
        self.clear_all_button.setObjectName("secondaryButton")
        self.clear_all_button.setCursor(Qt.PointingHandCursor)
        
        list_header.addWidget(list_title)
        list_header.addStretch(1)
        list_header.addWidget(self.clear_all_button)
        
        # 添加用户列表
        self.user_list = QListWidget()
        self.user_list.setObjectName("userList")
        self.user_list.setAlternatingRowColors(True)
        
        # 添加到列表布局
        list_layout.addLayout(list_header)
        list_layout.addWidget(self.user_list)
        
        # 统计信息和控制区域
        stats_frame = QFrame()
        stats_frame.setObjectName("statsFrame")
        stats_layout = QHBoxLayout(stats_frame)
        stats_layout.setContentsMargins(15, 10, 15, 10)
        
        # 统计信息
        stats_group = QGroupBox("下载统计")
        stats_group.setObjectName("statsGroup")
        stats_grid = QGridLayout(stats_group)
        
        # 统计标签 - 移除进度条，只保留文本标签
        self.total_users_label = QLabel("总用户数: 0")
        self.downloaded_users_label = QLabel("已下载: 0")
        self.status_label = QLabel("状态: 空闲")
        
        # 添加统计标签到网格
        stats_grid.addWidget(self.total_users_label, 0, 0)
        stats_grid.addWidget(self.downloaded_users_label, 0, 1)
        stats_grid.addWidget(self.status_label, 1, 0, 1, 2)
        
        # 控制按钮 - 移除暂停按钮
        controls_layout = QVBoxLayout()
        controls_layout.setSpacing(10)
        
        self.start_button = QPushButton("开始下载")
        self.start_button.setObjectName("primaryButton")
        self.start_button.setCursor(Qt.PointingHandCursor)
        
        self.cancel_button = QPushButton("取消")
        self.cancel_button.setObjectName("dangerButton")
        self.cancel_button.setEnabled(False)
        self.cancel_button.setCursor(Qt.PointingHandCursor)
        
        # 添加按钮到控制布局
        controls_layout.addWidget(self.start_button)
        controls_layout.addWidget(self.cancel_button)
        controls_layout.addStretch(1)
        
        # 添加统计和控制到布局
        stats_layout.addWidget(stats_group, 1)
        stats_layout.addLayout(controls_layout)
        
        # 将所有区域添加到主布局
        layout.addWidget(input_frame)
        layout.addWidget(list_frame, 1)  # 列表区域伸展
        layout.addWidget(stats_frame)
    
    def setup_single_download_tab(self, parent):
        """设置单个视频下载选项卡UI"""
        # 创建布局
        layout = QVBoxLayout(parent)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)
        
        # 创建输入区域
        input_frame = QFrame()
        input_frame.setObjectName("inputFrame")
        input_layout = QHBoxLayout(input_frame)
        input_layout.setContentsMargins(15, 10, 15, 10)
        
        # 视频链接输入
        self.link_input = QLineEdit()
        self.link_input.setPlaceholderText("请输入抖音视频链接...")
        self.link_input.setObjectName("linkInput")
        
        # 清除按钮
        self.clear_link_button = QPushButton("清除")
        self.clear_link_button.setObjectName("secondaryButton")
        self.clear_link_button.setCursor(Qt.PointingHandCursor)
        # 连接清除按钮到清除输入框方法
        self.clear_link_button.clicked.connect(self.clear_link_input)
        
        # 下载按钮
        self.download_single_button = QPushButton("下载")
        self.download_single_button.setObjectName("primaryButton")
        self.download_single_button.setCursor(Qt.PointingHandCursor)
        
        # 添加到输入布局
        input_layout.addWidget(self.link_input, 1)
        input_layout.addWidget(self.clear_link_button)
        input_layout.addWidget(self.download_single_button)
        
        # 视频信息区域
        info_frame = QFrame()
        info_frame.setObjectName("infoFrame")
        info_layout = QVBoxLayout(info_frame)
        info_layout.setContentsMargins(15, 10, 15, 10)
        
        # 视频信息标题
        info_title = QLabel("视频信息")
        info_title.setObjectName("sectionTitle")
        
        # 视频信息显示
        self.video_info = QTextEdit()
        self.video_info.setReadOnly(True)
        self.video_info.setObjectName("videoInfo")
        self.video_info.setPlaceholderText("视频信息将显示在这里...")
        
        # 添加到信息布局
        info_layout.addWidget(info_title)
        info_layout.addWidget(self.video_info)
        
        # 将所有区域添加到主布局
        layout.addWidget(input_frame)
        layout.addWidget(info_frame, 1)  # 信息区域伸展
    
    def setup_log_component(self, parent_layout):
        """设置日志组件"""
        # 日志标题
        log_header = QHBoxLayout()
        log_header.setContentsMargins(0, 0, 0, 5)
        
        log_title = QLabel("运行日志")
        log_title.setObjectName("sectionTitle")
        
        # 添加两个按钮：清空日志和保存日志
        button_layout = QHBoxLayout()
        button_layout.setSpacing(8)
        
        self.clear_log_button = QPushButton("清空日志")
        self.clear_log_button.setObjectName("secondaryButton")
        self.clear_log_button.setCursor(Qt.PointingHandCursor)
        
        self.save_log_button = QPushButton("保存日志")
        self.save_log_button.setObjectName("secondaryButton")
        self.save_log_button.setCursor(Qt.PointingHandCursor)
        
        button_layout.addWidget(self.clear_log_button)
        button_layout.addWidget(self.save_log_button)
        
        log_header.addWidget(log_title)
        log_header.addStretch(1)
        log_header.addLayout(button_layout)
        
        # 日志文本框
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setObjectName("logOutput")
        self.log_output.setLineWrapMode(QTextEdit.NoWrap)  # 不自动换行
        
        # 添加到布局
        parent_layout.addLayout(log_header)
        parent_layout.addWidget(self.log_output)
        
        # 连接清空按钮
        self.clear_log_button.clicked.connect(self.clear_log)
    
    def clear_log(self):
        """清空日志"""
        self.log_output.clear()
    
    def clear_link_input(self):
        """清空链接输入框"""
        self.link_input.clear()
    
    def append_log(self, message):
        """添加日志消息"""
        self.log_output.append(message)
        # 滚动到底部
        scrollbar = self.log_output.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def update_stats_display(self, stats):
        """更新统计信息显示"""
        if 'total_users' in stats:
            self.total_users_label.setText(f"总用户数: {stats['total_users']}")
        
        if 'downloaded_users' in stats:
            self.downloaded_users_label.setText(f"已下载: {stats['downloaded_users']}")
        
        if 'status' in stats:
            self.status_label.setText(f"状态: {stats['status']}")
    
    # 单个视频下载相关方法
    def get_link_input_text(self):
        """获取链接输入框文本"""
        return self.link_input.text()
    
    def get_user_count(self):
        """获取当前用户列表数量
        
        Returns:
            int: 用户数量
        """
        return self.user_list.count()
    
    # 批量下载的辅助类
    @property
    def batch_download(self):
        """返回批量下载组件"""
        return self
        
    # 单个视频下载的辅助类
    @property
    def single_download(self):
        """返回单个视频下载组件"""
        return self