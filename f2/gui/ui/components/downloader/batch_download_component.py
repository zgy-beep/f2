"""
批量下载组件
"""

from PyQt5.QtWidgets import (QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTextEdit, 
                           QTableWidget, QTableWidgetItem, QHeaderView, QGroupBox)
from PyQt5.QtCore import pyqtSignal

from f2.gui.ui.components.base_component import BaseComponent

class BatchDownloadComponent(BaseComponent):
    """批量下载组件"""
    
    def __init__(self, parent=None):
        """初始化批量下载组件
        
        Args:
            parent: 父窗口组件
        """
        super().__init__(parent)
        
        # 初始化UI组件
        self.user_input = None
        self.user_table = None
        self.add_button = None
        self.history_button = None
        self.clear_input_button = None
        self.start_button = None
        self.stop_button = None
        self.clear_list_button = None
        
        # 下载统计相关组件
        self.user_count_label = None
        self.downloaded_user_label = None
        self.total_video_label = None
        self.updated_video_label = None
        self.download_status_label = None
        self.elapsed_time_label = None
        
        # 组件容器
        self.input_group = None
        self.list_group = None
        self.stats_group = None
        
        # 设置UI
        self.setup_ui()
    
    def setup_ui(self):
        """设置批量下载UI"""
        # 用户输入区域
        self.input_group = self._create_input_group()
        
        # 用户列表区域
        self.list_group = self._create_list_group()
        
        # 下载统计摘要区域
        self.stats_group = self._create_stats_group()
    
    def _create_input_group(self):
        """创建用户输入区域
        
        Returns:
            QGroupBox: 用户输入区域组件
        """
        input_group = QGroupBox("添加用户")
        input_layout = QVBoxLayout()
        
        # 输入说明
        help_label = QLabel("输入抖音用户ID (sec_user_id) 或用户主页链接，每行一个")
        help_label.setWordWrap(True)
        input_layout.addWidget(help_label)
        
        # 用户ID输入框
        self.user_input = QTextEdit()
        self.user_input.setPlaceholderText("例如：MS4wLjABAAAAMn__d0rqdcuqb1lVJKapsl-ssFNQnayKwd136gpbScI\n或者：https://www.douyin.com/user/MS4wLjABAAAAMn__d0rqdcuqb1lVJKapsl-ssFNQnayKwd136gpbScI")
        self.user_input.setMinimumHeight(100)
        input_layout.addWidget(self.user_input)
        
        # 按钮区域
        buttons_layout = QHBoxLayout()
        
        self.add_button = QPushButton("添加用户")
        buttons_layout.addWidget(self.add_button)
        
        self.history_button = QPushButton("历史记录")
        buttons_layout.addWidget(self.history_button)
        
        self.clear_input_button = QPushButton("清空输入")
        buttons_layout.addWidget(self.clear_input_button)
        
        input_layout.addLayout(buttons_layout)
        input_group.setLayout(input_layout)
        
        return input_group
    
    def _create_list_group(self):
        """创建用户列表区域
        
        Returns:
            QGroupBox: 用户列表区域组件
        """
        list_group = QGroupBox("下载队列")
        list_layout = QVBoxLayout()
        
        # 用户表格
        self.user_table = QTableWidget(0, 3)
        self.user_table.setHorizontalHeaderLabels(["用户ID", "用户名称", "操作"])
        self.user_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.user_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.user_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Fixed)
        self.user_table.setColumnWidth(2, 100)
        list_layout.addWidget(self.user_table)
        
        # 按钮区域
        control_layout = QHBoxLayout()
        
        self.start_button = QPushButton("开始下载")
        control_layout.addWidget(self.start_button)
        
        self.stop_button = QPushButton("停止下载")
        self.stop_button.setEnabled(False)
        control_layout.addWidget(self.stop_button)
        
        self.clear_list_button = QPushButton("清空列表")
        control_layout.addWidget(self.clear_list_button)
        
        list_layout.addLayout(control_layout)
        list_group.setLayout(list_layout)
        
        return list_group
    
    def _create_stats_group(self):
        """创建下载统计摘要区域
        
        Returns:
            QGroupBox: 下载统计摘要区域组件
        """
        stats_group = QGroupBox("下载统计")
        stats_layout = QHBoxLayout()
        
        # 用户数量
        user_stats_layout = QVBoxLayout()
        self.user_count_label = QLabel("用户数量: 0")
        user_stats_layout.addWidget(self.user_count_label)
        self.downloaded_user_label = QLabel("已完成用户: 0/0")
        user_stats_layout.addWidget(self.downloaded_user_label)
        stats_layout.addLayout(user_stats_layout)
        
        # 视频数量
        video_stats_layout = QVBoxLayout()
        self.total_video_label = QLabel("总视频数: 0")
        video_stats_layout.addWidget(self.total_video_label)
        self.updated_video_label = QLabel("已更新视频: 0")
        video_stats_layout.addWidget(self.updated_video_label)
        stats_layout.addLayout(video_stats_layout)
        
        # 下载状态
        status_stats_layout = QVBoxLayout()
        self.download_status_label = QLabel("下载状态: 空闲")
        status_stats_layout.addWidget(self.download_status_label)
        self.elapsed_time_label = QLabel("已用时间: 00:00:00")
        status_stats_layout.addWidget(self.elapsed_time_label)
        stats_layout.addLayout(status_stats_layout)
        
        stats_group.setLayout(stats_layout)
        
        return stats_group
    
    def update_stats_display(self, stats):
        """更新统计显示
        
        Args:
            stats: 包含统计信息的字典
        """
        # 更新用户统计
        self.user_count_label.setText(f"用户数量: {stats['total_users']}")
        self.downloaded_user_label.setText(f"已完成用户: {stats['completed_users']}/{stats['total_users']}")
        
        # 更新视频统计
        self.total_video_label.setText(f"总视频数: {stats['total_videos']}")
        self.updated_video_label.setText(f"已更新视频: {stats['updated_videos']}")
        
        # 更新下载状态
        if 'status' in stats:
            self.download_status_label.setText(f"下载状态: {stats['status']}")
        
        if 'elapsed_time' in stats:
            self.elapsed_time_label.setText(f"已用时间: {stats['elapsed_time']}")
    
    def get_input_widget(self):
        """获取用户输入区域组件
        
        Returns:
            QGroupBox: 用户输入区域组件
        """
        return self.input_group
        
    def get_list_widget(self):
        """获取用户列表区域组件
        
        Returns:
            QGroupBox: 用户列表区域组件
        """
        return self.list_group
        
    def get_stats_widget(self):
        """获取下载统计摘要区域组件
        
        Returns:
            QGroupBox: 下载统计摘要区域组件
        """
        return self.stats_group
        
    def clear_user_input(self):
        """清空用户输入框"""
        self.user_input.clear()
    
    def get_user_input_text(self):
        """获取用户输入框文本
        
        Returns:
            str: 用户输入框文本
        """
        return self.user_input.toPlainText()
    
    def add_user_to_table(self, user_id, user_name, remove_callback=None):
        """添加用户到表格
        
        Args:
            user_id: 用户ID
            user_name: 用户名称
            remove_callback: 移除按钮回调函数
        """
        row_count = self.user_table.rowCount()
        self.user_table.insertRow(row_count)
        
        # 设置用户ID和用户名称
        self.user_table.setItem(row_count, 0, QTableWidgetItem(user_id))
        self.user_table.setItem(row_count, 1, QTableWidgetItem(user_name))
        
        # 添加删除按钮
        if remove_callback:
            remove_button = QPushButton("删除")
            remove_button.clicked.connect(lambda: remove_callback(row_count))
            self.user_table.setCellWidget(row_count, 2, remove_button)
    
    def clear_user_table(self):
        """清空用户表格"""
        self.user_table.setRowCount(0)
    
    def get_user_count(self):
        """获取用户表格中的用户数量
        
        Returns:
            int: 用户数量
        """
        return self.user_table.rowCount()