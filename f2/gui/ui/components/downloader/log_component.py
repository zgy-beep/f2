"""
日志组件
"""

from PyQt5.QtWidgets import (QVBoxLayout, QHBoxLayout, QGroupBox, 
                            QTextEdit, QPushButton)
from PyQt5.QtGui import QTextCursor

from f2.gui.ui.components.base_component import BaseComponent

class LogComponent(BaseComponent):
    """日志显示组件"""
    
    def __init__(self, parent=None):
        """初始化日志组件
        
        Args:
            parent: 父窗口组件
        """
        super().__init__(parent)
        
        # 日志相关组件
        self.log_output = None
        self.clear_log_button = None
        self.save_log_button = None
        
        # 设置UI
        self.setup_ui()
        
    def setup_ui(self):
        """设置日志UI组件"""
        self.group_box = QGroupBox("下载日志")
        layout = QVBoxLayout()
        
        # 日志输出区域
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setLineWrapMode(QTextEdit.NoWrap)
        self.log_output.setMinimumHeight(200)
        layout.addWidget(self.log_output)
        
        # 日志控制按钮
        control_layout = QHBoxLayout()
        
        self.clear_log_button = QPushButton("清空日志")
        control_layout.addWidget(self.clear_log_button)
        
        self.save_log_button = QPushButton("保存日志")
        control_layout.addWidget(self.save_log_button)
        
        layout.addLayout(control_layout)
        self.group_box.setLayout(layout)
    
    def append_log(self, message):
        """添加日志消息到日志输出框
        
        Args:
            message: 日志消息
        """
        self.log_output.append(message)
        # 滚动到底部
        self.log_output.moveCursor(QTextCursor.End)
    
    def clear_log(self):
        """清空日志内容"""
        self.log_output.clear()
    
    def get_widget(self):
        """获取组件的顶级窗口部件
        
        Returns:
            QGroupBox: 日志组件的顶级窗口部件
        """
        return self.group_box