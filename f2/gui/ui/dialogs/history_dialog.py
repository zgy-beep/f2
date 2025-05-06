# -*- coding:utf-8 -*-
# @Information  : 
# @Author       : ZGY
# @Date         : 2025-04-28 10:38:46
# @FilePath     : /f2_gui/f2/gui/ui/dialogs/history_dialog.py
# @LastEditTime : 2025-04-29 10:37:22

"""
历史记录对话框
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QTableWidget, QTableWidgetItem, 
                             QHeaderView, QPushButton, QMessageBox)
from PyQt5.QtCore import pyqtSignal, Qt, QTimer

from f2.gui.models.history_manager import HistoryManager
from f2.gui.models.user_update_checker import CheckUpdateWorker

class HistoryDialog(QDialog):
    """
    历史记录对话框
    """
    userSelected = pyqtSignal(str, str)  # 信号：用户ID, 用户昵称
    
    def __init__(self, history_manager: HistoryManager, parent=None):
        super().__init__(parent)
        self.history_manager = history_manager
        
        # 保存检查更新的工作线程
        self.check_workers = []
        # 保存检查结果
        self.update_results = {}
        
        self.setWindowTitle("下载历史记录")
        self.setGeometry(100, 100, 800, 500)
        
        # 初始化界面
        self.init_ui()
        
        # 加载历史记录
        self.load_history()
    
    def init_ui(self):
        """初始化用户界面"""
        # 主布局
        layout = QVBoxLayout(self)
        
        # 搜索区域
        search_layout = QHBoxLayout()
        search_label = QLabel("搜索用户:")
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("输入用户ID或昵称...")
        self.search_edit.textChanged.connect(self.filter_table)
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_edit)
        layout.addLayout(search_layout)
        
        # 历史记录表格
        self.history_table = QTableWidget(0, 7)  # 增加一列用于显示更新状态
        self.history_table.setHorizontalHeaderLabels(["用户ID", "用户昵称", "首次下载时间", "最近下载时间", "下载次数", "下载状态", "更新状态"])
        self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.history_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.history_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.history_table.doubleClicked.connect(self.on_table_double_clicked)
        layout.addWidget(self.history_table)
        
        # 按钮区域
        button_layout = QHBoxLayout()
        
        self.check_update_button = QPushButton("检查更新")
        self.check_update_button.clicked.connect(self.on_check_update)
        button_layout.addWidget(self.check_update_button)
        
        self.add_to_queue_button = QPushButton("添加到下载队列")
        self.add_to_queue_button.clicked.connect(self.on_add_to_queue)
        button_layout.addWidget(self.add_to_queue_button)
        
        self.clear_history_button = QPushButton("清空历史记录")
        self.clear_history_button.clicked.connect(self.on_clear_history)
        button_layout.addWidget(self.clear_history_button)
        
        self.close_button = QPushButton("关闭")
        self.close_button.clicked.connect(self.close)
        button_layout.addWidget(self.close_button)
        
        layout.addLayout(button_layout)
    
    def load_history(self):
        """
        加载历史记录到表格
        """
        history = self.history_manager.get_history()
        self.history_table.setRowCount(0)  # 清空表格
        
        for idx, item in enumerate(history):
            row = self.history_table.rowCount()
            self.history_table.insertRow(row)
            
            # 设置单元格内容
            self.history_table.setItem(row, 0, QTableWidgetItem(item.get("user_id", "")))
            self.history_table.setItem(row, 1, QTableWidgetItem(item.get("nickname", "未知用户")))
            self.history_table.setItem(row, 2, QTableWidgetItem(item.get("first_download_time", "")))
            self.history_table.setItem(row, 3, QTableWidgetItem(item.get("last_download_time", "")))
            self.history_table.setItem(row, 4, QTableWidgetItem(str(item.get("download_count", 0))))
            self.history_table.setItem(row, 5, QTableWidgetItem(item.get("status", "未知")))
            
            # 设置更新状态单元格，初始为"未检查"
            update_status = QTableWidgetItem("未检查")
            update_status.setTextAlignment(Qt.AlignCenter)
            self.history_table.setItem(row, 6, update_status)
    
    def filter_table(self):
        """
        根据搜索文本过滤表格
        """
        search_text = self.search_edit.text().lower()
        
        for row in range(self.history_table.rowCount()):
            user_id = self.history_table.item(row, 0).text().lower()
            nickname = self.history_table.item(row, 1).text().lower()
            
            if search_text in user_id or search_text in nickname:
                self.history_table.setRowHidden(row, False)
            else:
                self.history_table.setRowHidden(row, True)
    
    def on_table_double_clicked(self, index):
        """
        表格行双击事件，选择用户
        """
        row = index.row()
        user_id = self.history_table.item(row, 0).text()
        nickname = self.history_table.item(row, 1).text()
        self.userSelected.emit(user_id, nickname)
        self.close()
    
    def on_add_to_queue(self):
        """
        将选中的用户添加到下载队列
        """
        selected_rows = self.history_table.selectionModel().selectedRows()
        
        if not selected_rows:
            QMessageBox.warning(self, "警告", "请先选择要添加的用户")
            return
        
        for index in selected_rows:
            row = index.row()
            user_id = self.history_table.item(row, 0).text()
            nickname = self.history_table.item(row, 1).text()
            self.userSelected.emit(user_id, nickname)
        
        self.close()
    
    def on_clear_history(self):
        """
        清空历史记录
        """
        reply = QMessageBox.question(
            self, "确认", "确定要清空所有历史记录吗？此操作无法撤销。",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            if self.history_manager.clear_history():
                self.history_table.setRowCount(0)
                QMessageBox.information(self, "成功", "历史记录已清空")
            else:
                QMessageBox.warning(self, "失败", "清空历史记录失败")
    
    def on_check_update(self):
        """
        检查用户是否有更新
        """
        selected_rows = self.history_table.selectionModel().selectedRows()
        
        if not selected_rows:
            QMessageBox.warning(self, "警告", "请先选择要检查的用户")
            return
        
        # 禁用检查按钮，防止重复点击
        self.check_update_button.setEnabled(False)
        
        # 更新选中行的状态为"检查中..."
        for index in selected_rows:
            row = index.row()
            update_status = QTableWidgetItem("检查中...")
            update_status.setTextAlignment(Qt.AlignCenter)
            self.history_table.setItem(row, 6, update_status)
            
            # 获取用户ID和最后下载时间
            user_id = self.history_table.item(row, 0).text()
            last_download_time = self.history_table.item(row, 3).text()
            
            # 创建工作线程 - 使用新的检查器类
            worker = CheckUpdateWorker(user_id, last_download_time)
            
            # 连接信号到槽函数
            worker.finished.connect(self.on_check_update_finished)
            worker.error.connect(self.on_check_update_error)
            
            # 存储工作线程的引用
            self.check_workers.append(worker)
            
            # 启动线程
            worker.start()
        
        # 所有检查开始后，延迟2秒重新启用按钮
        QTimer.singleShot(2000, lambda: self.check_update_button.setEnabled(True))
    
    def on_check_update_finished(self, result):
        """
        检查更新完成的回调
        """
        user_id = result["user_id"]
        has_updates = result["has_updates"]
        
        # 更新表格中的状态
        for row in range(self.history_table.rowCount()):
            if self.history_table.item(row, 0).text() == user_id:
                update_status = QTableWidgetItem("有更新" if has_updates else "无更新")
                update_status.setTextAlignment(Qt.AlignCenter)
                
                # 设置不同的颜色
                if has_updates:
                    update_status.setBackground(Qt.green)
                else:
                    update_status.setBackground(Qt.lightGray)
                
                self.history_table.setItem(row, 6, update_status)
                break
        
        # 保存结果
        self.update_results[user_id] = result
    
    def on_check_update_error(self, error_msg):
        """
        检查更新出错的回调
        """
        QMessageBox.warning(self, "检查更新失败", error_msg)
    
    def closeEvent(self, event):
        """
        对话框关闭事件，确保停止所有工作线程
        """
        # 停止所有检查更新的工作线程
        for worker in self.check_workers:
            if worker.isRunning():
                # 先调用自定义的stop方法来标记线程应该停止
                worker.stop()
                # 等待一小段时间让线程自然结束
                if not worker.wait(500):  # 等待500毫秒
                    worker.terminate()  # 如果线程没有自然结束，则强制终止
                worker.wait()  # 确保线程真正结束
        
        # 清空工作线程列表
        self.check_workers.clear()
        
        # 接受关闭事件
        event.accept()