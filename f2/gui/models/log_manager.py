"""
抖音下载器 - 日志管理器
"""

import os
from datetime import datetime
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QFileDialog, QMessageBox

from f2.log.logger import logger


class LogManager(QObject):
    """日志管理器"""
    
    # 信号
    log_message = pyqtSignal(str)
    
    def __init__(self, download_tab_ui=None):
        """初始化日志管理器
        
        Args:
            download_tab_ui: 下载标签页UI组件
        """
        super().__init__()
        self.ui = download_tab_ui
        
        # 记录所有日志
        self.log_history = []
        
        # 设置连接
        if self.ui:
            self.setup_connections()
    
    def setup_connections(self):
        """设置信号和槽连接"""
        # 绑定UI按钮 - 适配重构后的扁平化结构
        self.ui.clear_log_button.clicked.connect(self.clear_log)
        
        # 绑定信号
        self.log_message.connect(self.append_log)
    
    def append_log(self, message):
        """添加日志
        
        Args:
            message: 日志消息
        """
        # 记录日志
        self.log_history.append(message)
        
        # 如果UI存在，更新UI
        if self.ui:
            self.ui.append_log(message)
    
    def clear_log(self):
        """清空日志"""
        # 清空记录
        self.log_history.clear()
        
        # 如果UI存在，清空UI
        if self.ui:
            self.ui.clear_log()
    
    def save_log(self):
        """保存日志到文件"""
        if not self.ui:
            return
            
        file_path, _ = QFileDialog.getSaveFileName(
            None, "保存日志", "", "文本文件 (*.txt);;所有文件 (*)"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(self.ui.log_output.toPlainText())
                QMessageBox.information(None, "成功", f"日志已保存到 {file_path}")
            except Exception as e:
                QMessageBox.critical(None, "错误", f"保存日志失败: {str(e)}")
    
    def add_target(self, target):
        """添加日志目标
        
        Args:
            target: 接收日志的对象或函数
        """
        self.log_message.connect(target)