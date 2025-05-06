"""
抖音下载器 - 新设计的下载界面组件
"""

from PyQt5.QtWidgets import (
    QVBoxLayout, QWidget, QHBoxLayout, QPushButton, 
    QLabel, QFrame, QLineEdit, QListWidget, QGridLayout,
    QTextEdit, QSplitter, QListWidgetItem, QGroupBox, QTabWidget
)
from PyQt5.QtCore import Qt, pyqtSignal, QObject
from PyQt5.QtGui import QIcon, QFont

class DownloadUI(QObject):
    """下载界面组件 - 集成了批量下载和单个视频下载功能"""
    
    # 定义信号
    show_history_signal = pyqtSignal()  # 显示历史记录对话框的信号
    start_download_signal = pyqtSignal()  # 开始批量下载信号
    download_video_signal = pyqtSignal(str)  # 下载单个视频信号
    
    def __init__(self, parent):
        """初始化下载界面组件
        
        Args:
            parent: 父窗口组件
        """
        super().__init__()
        self.parent = parent
        
        # 设置UI
        self.setup_ui()
    
    def setup_ui(self):
        """设置下载界面UI - 采用更简洁的扁平化设计"""
        # 主布局
        main_layout = QVBoxLayout(self.parent)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 创建可分割的上下区域
        splitter = QSplitter(Qt.Vertical)
        splitter.setHandleWidth(1)
        
        # 创建上部内容区域
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(16, 16, 16, 16)
        content_layout.setSpacing(16)
        
        # 创建下部日志区域
        log_widget = QWidget()
        log_layout = QVBoxLayout(log_widget)
        log_layout.setContentsMargins(16, 8, 16, 16)
        
        # 创建下载区域 - 整合批量下载和单个视频下载
        self.setup_download_area(content_layout)
        
        # 创建日志组件
        self.setup_log_component(log_layout)
        
        # 添加组件到分割器
        splitter.addWidget(content_widget)
        splitter.addWidget(log_widget)
        
        # 设置分割器的初始大小
        splitter.setSizes([650, 150])
        
        # 添加分割器到主布局
        main_layout.addWidget(splitter)
    
    def setup_download_area(self, parent_layout):
        """设置下载区域 - 整合批量下载和单个视频下载"""
        # 创建下载卡片
        self.setup_user_download_card(parent_layout)
        self.setup_video_download_card(parent_layout)
        
        # 创建用户列表区域
        self.setup_user_list_area(parent_layout)
        
        # 创建控制区域
        self.setup_control_area(parent_layout)
    
    def setup_user_download_card(self, parent_layout):
        """设置用户下载卡片"""
        # 创建卡片
        card = QFrame()
        card.setObjectName("card")
        card.setFrameShape(QFrame.StyledPanel)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(16, 16, 16, 16)
        card_layout.setSpacing(12)
        
        # 标题
        title = QLabel("下载用户视频")
        title.setObjectName("cardTitle")
        title.setFont(QFont("", 12, QFont.Bold))
        
        # 描述
        description = QLabel("输入抖音用户ID或用户主页链接，添加到下载队列")
        description.setObjectName("cardDescription")
        
        # 输入区域
        input_layout = QHBoxLayout()
        input_layout.setSpacing(8)
        
        # 用户ID输入
        self.user_id_input = QLineEdit()
        self.user_id_input.setPlaceholderText("请输入抖音用户ID或用户主页链接...")
        self.user_id_input.setObjectName("userIdInput")
        
        # 添加按钮
        self.add_user_button = QPushButton("添加")
        self.add_user_button.setObjectName("primaryButton")
        self.add_user_button.setCursor(Qt.PointingHandCursor)
        
        # 历史按钮
        self.history_button = QPushButton("历史")
        self.history_button.setObjectName("secondaryButton")
        self.history_button.setCursor(Qt.PointingHandCursor)
        # 连接历史按钮
        self.history_button.clicked.connect(self.show_history_signal.emit)
        
        # 添加到输入布局
        input_layout.addWidget(self.user_id_input, 1)
        input_layout.addWidget(self.add_user_button)
        input_layout.addWidget(self.history_button)
        
        # 添加到卡片布局
        card_layout.addWidget(title)
        card_layout.addWidget(description)
        card_layout.addLayout(input_layout)
        
        # 添加到父布局
        parent_layout.addWidget(card)
    
    def setup_video_download_card(self, parent_layout):
        """设置视频下载卡片"""
        # 创建卡片
        card = QFrame()
        card.setObjectName("card")
        card.setFrameShape(QFrame.StyledPanel)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(16, 16, 16, 16)
        card_layout.setSpacing(12)
        
        # 标题
        title = QLabel("下载单个视频")
        title.setObjectName("cardTitle")
        title.setFont(QFont("", 12, QFont.Bold))
        
        # 描述
        description = QLabel("输入视频链接，直接下载单个视频")
        description.setObjectName("cardDescription")
        
        # 输入区域
        input_layout = QHBoxLayout()
        input_layout.setSpacing(8)
        
        # 视频链接输入
        self.link_input = QLineEdit()
        self.link_input.setPlaceholderText("请输入抖音视频链接...")
        self.link_input.setObjectName("linkInput")
        
        # 清除按钮
        self.clear_link_button = QPushButton("清除")
        self.clear_link_button.setObjectName("secondaryButton")
        self.clear_link_button.setCursor(Qt.PointingHandCursor)
        self.clear_link_button.clicked.connect(self.clear_link_input)
        
        # 下载按钮
        self.download_single_button = QPushButton("下载")
        self.download_single_button.setObjectName("primaryButton")
        self.download_single_button.setCursor(Qt.PointingHandCursor)
        # 连接下载按钮
        self.download_single_button.clicked.connect(self.on_download_video)
        
        # 添加到输入布局
        input_layout.addWidget(self.link_input, 1)
        input_layout.addWidget(self.clear_link_button)
        input_layout.addWidget(self.download_single_button)
        
        # 添加到卡片布局
        card_layout.addWidget(title)
        card_layout.addWidget(description)
        card_layout.addLayout(input_layout)
        
        # 添加到父布局
        parent_layout.addWidget(card)
    
    def setup_user_list_area(self, parent_layout):
        """设置用户列表区域"""
        # 创建卡片
        card = QFrame()
        card.setObjectName("card")
        card.setFrameShape(QFrame.StyledPanel)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(16, 16, 16, 16)
        card_layout.setSpacing(12)
        
        # 标题栏
        header_layout = QHBoxLayout()
        
        # 标题
        title = QLabel("下载队列")
        title.setObjectName("cardTitle")
        title.setFont(QFont("", 12, QFont.Bold))
        
        # 清空按钮
        self.clear_all_button = QPushButton("清空队列")
        self.clear_all_button.setObjectName("secondaryButton")
        self.clear_all_button.setCursor(Qt.PointingHandCursor)
        
        # 添加到标题栏
        header_layout.addWidget(title)
        header_layout.addStretch(1)
        header_layout.addWidget(self.clear_all_button)
        
        # 用户列表
        self.user_list = QListWidget()
        self.user_list.setObjectName("userList")
        self.user_list.setAlternatingRowColors(True)
        self.user_list.setMinimumHeight(100)
        
        # 添加到卡片布局
        card_layout.addLayout(header_layout)
        card_layout.addWidget(self.user_list)
        
        # 添加到父布局
        parent_layout.addWidget(card, 1)  # 列表区域占满剩余空间
    
    def setup_control_area(self, parent_layout):
        """设置控制区域"""
        # 创建布局
        control_layout = QHBoxLayout()
        control_layout.setContentsMargins(0, 0, 0, 0)
        
        # 左侧 - 统计信息
        stats_group = QGroupBox("下载统计")
        stats_group.setObjectName("statsGroup")
        stats_layout = QGridLayout(stats_group)
        
        # 统计标签
        self.total_users_label = QLabel("总用户数: 0")
        self.downloaded_users_label = QLabel("已下载: 0")
        self.status_label = QLabel("状态: 就绪")
        
        # 添加到网格布局
        stats_layout.addWidget(self.total_users_label, 0, 0)
        stats_layout.addWidget(self.downloaded_users_label, 0, 1)
        stats_layout.addWidget(self.status_label, 1, 0, 1, 2)
        
        # 右侧 - 控制按钮
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)
        
        # 开始按钮
        self.start_button = QPushButton("开始下载")
        self.start_button.setObjectName("primaryButton")
        self.start_button.setMinimumWidth(120)
        self.start_button.setCursor(Qt.PointingHandCursor)
        # 连接开始按钮
        self.start_button.clicked.connect(self.start_download_signal.emit)
        
        # 取消按钮
        self.cancel_button = QPushButton("取消")
        self.cancel_button.setObjectName("dangerButton")
        self.cancel_button.setMinimumWidth(120)
        self.cancel_button.setEnabled(False)
        self.cancel_button.setCursor(Qt.PointingHandCursor)
        
        # 添加到按钮布局
        buttons_layout.addStretch(1)
        buttons_layout.addWidget(self.start_button)
        buttons_layout.addWidget(self.cancel_button)
        
        # 添加到控制布局
        control_layout.addWidget(stats_group)
        control_layout.addStretch(1)
        control_layout.addLayout(buttons_layout)
        
        # 添加到父布局
        parent_layout.addLayout(control_layout)
    
    def setup_log_component(self, parent_layout):
        """设置日志组件"""
        # 日志标题栏
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 8)
        
        # 标题
        title = QLabel("运行日志")
        title.setObjectName("sectionTitle")
        title.setFont(QFont("", 11, QFont.Bold))
        
        # 按钮布局
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(8)
        
        # 清空日志按钮
        self.clear_log_button = QPushButton("清空日志")
        self.clear_log_button.setObjectName("secondaryButton")
        self.clear_log_button.setCursor(Qt.PointingHandCursor)
        
        # 保存日志按钮
        self.save_log_button = QPushButton("保存日志")
        self.save_log_button.setObjectName("secondaryButton")
        self.save_log_button.setCursor(Qt.PointingHandCursor)
        
        # 添加到按钮布局
        buttons_layout.addWidget(self.clear_log_button)
        buttons_layout.addWidget(self.save_log_button)
        
        # 添加到标题栏
        header_layout.addWidget(title)
        header_layout.addStretch(1)
        header_layout.addLayout(buttons_layout)
        
        # 日志文本框
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setObjectName("logOutput")
        self.log_output.setLineWrapMode(QTextEdit.NoWrap)
        
        # 添加到父布局
        parent_layout.addLayout(header_layout)
        parent_layout.addWidget(self.log_output)
        
        # 连接清空按钮
        self.clear_log_button.clicked.connect(self.clear_log)
    
    def clear_log(self):
        """清空日志"""
        self.log_output.clear()
    
    def clear_link_input(self):
        """清空链接输入框"""
        self.link_input.clear()
    
    def on_download_video(self):
        """下载单个视频"""
        video_url = self.link_input.text().strip()
        self.download_video_signal.emit(video_url)
    
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
    
    def get_link_input_text(self):
        """获取链接输入框文本"""
        return self.link_input.text()
    
    def get_user_count(self):
        """获取用户列表数量"""
        return self.user_list.count()
    
    def set_video_download_in_progress(self, in_progress):
        """设置视频下载是否正在进行中"""
        self.download_single_button.setEnabled(not in_progress)
        if in_progress:
            self.status_label.setText("状态: 下载视频中")
        else:
            self.status_label.setText("状态: 就绪")
    
    # 兼容原来的接口
    @property
    def batch_download(self):
        """返回批量下载组件 - 兼容原接口"""
        return self
    
    @property
    def single_download(self):
        """返回单个视频下载组件 - 兼容原接口"""
        return self