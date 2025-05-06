"""
抖音下载器 - 下载控制器
"""

import time
from datetime import datetime
from PyQt5.QtCore import QObject, pyqtSignal, QThread, QTimer

from f2.log.logger import logger


class DownloadController(QObject):
    """下载控制器"""
    
    # 信号
    download_started = pyqtSignal()
    download_progress = pyqtSignal(dict)  # 下载进度数据
    download_finished = pyqtSignal()
    download_error = pyqtSignal(str)
    log_message = pyqtSignal(str)
    
    def __init__(self, download_tab_ui, download_worker=None):
        """初始化下载控制器
        
        Args:
            download_tab_ui: 下载标签页UI组件
            download_worker: 下载工作器
        """
        super().__init__()
        self.ui = download_tab_ui
        self.download_worker = download_worker
        self.download_thread = None
        
        # 下载统计信息
        self.download_stats = {
            "total_users": 0,
            "completed_users": 0,
            "total_videos": 0,
            "updated_videos": 0,
            "start_time": None,
            "status": "空闲"
        }
        
        # 创建定时器
        self.stats_timer = QTimer()
        self.stats_timer.timeout.connect(self.update_elapsed_time)
        self.stats_timer.setInterval(1000)  # 每秒更新一次
        
        # 设置连接
        self.setup_connections()
    
    def setup_connections(self):
        """设置信号和槽连接"""
        # 绑定UI按钮，适配扁平化结构
        self.ui.start_button.clicked.connect(self.start_download)
        self.ui.cancel_button.clicked.connect(self.stop_download)
        
        # 绑定自身信号
        self.download_started.connect(self.on_download_started)
        self.download_progress.connect(self.on_download_progress)
        self.download_finished.connect(self.on_download_finished)
        self.download_error.connect(self.on_download_error)
        self.log_message.connect(self.ui.append_log)
    
    def set_download_worker(self, download_worker):
        """设置下载工作器
        
        Args:
            download_worker: 下载工作器对象
        """
        self.download_worker = download_worker
    
    def start_download(self):
        """开始下载任务"""
        if self.download_thread and self.download_thread.isRunning():
            self.log_message.emit("下载任务正在进行中")
            return
        
        if not self.download_worker:
            self.download_error.emit("下载工作器未初始化")
            return
        
        # 确保下载工作器是在主线程创建的
        if hasattr(self.download_worker, 'thread') and self.download_worker.thread() != QThread.currentThread():
            self.download_error.emit("下载工作器线程状态异常")
            return
            
        # 如果工作器已经在另一个线程中，需要先重置
        if self.download_worker.parent():
            self.download_worker.setParent(None)
        
        # 创建并启动下载线程
        self.download_thread = QThread()
        
        try:
            # 移动工作器到线程前断开所有之前的连接
            self.download_worker.started.disconnect()
            self.download_worker.progress.disconnect()
            self.download_worker.finished.disconnect()
            self.download_worker.error.disconnect()
        except (TypeError, RuntimeError):
            # 如果没有之前的连接，会引发异常，可以忽略
            pass
            
        # 移动工作器到线程
        self.download_worker.moveToThread(self.download_thread)
        
        # 连接信号和槽
        self.download_thread.started.connect(self.download_worker.download)
        self.download_worker.started.connect(self.download_started)
        self.download_worker.progress.connect(self.parse_progress_message)
        self.download_worker.finished.connect(self.download_finished)
        self.download_worker.error.connect(self.download_error)
        
        # 启动线程
        self.download_thread.start()
    
    def stop_download(self):
        """停止下载任务"""
        if self.download_worker and self.download_worker.is_running:
            self.log_message.emit("正在停止下载任务...")
            self.download_worker.is_running = False
            
            # 禁用停止按钮以防多次点击
            self.ui.cancel_button.setEnabled(False)
            
            # 给任务一些时间来清理
            QTimer.singleShot(3000, self.download_finished.emit)
    
    def parse_progress_message(self, message):
        """解析进度消息并更新统计信息
        
        Args:
            message: 进度消息
        """
        # 转发原始消息到日志
        self.log_message.emit(message)
        
        # 解析消息中的统计信息
        if "获取到" in message and "总计:" in message and "个作品" in message:
            try:
                total_part = message.split("总计:")[1].split("个作品")[0].strip()
                self.download_stats["total_videos"] = max(
                    self.download_stats["total_videos"], 
                    int(total_part)
                )
                self.update_stats_display()
            except (ValueError, IndexError):
                pass
        
        # 解析更新的视频数量
        elif "本批次实际更新了" in message and "总计更新:" in message:
            try:
                updated_part = message.split("总计更新:")[1].split("个作品")[0].strip()
                self.download_stats["updated_videos"] = max(
                    self.download_stats["updated_videos"], 
                    int(updated_part)
                )
                self.update_stats_display()
            except (ValueError, IndexError):
                pass
        
        # 检测用户完成情况
        elif "作品下载完成" in message or "下载失败" in message:
            self.download_stats["completed_users"] += 1
            self.update_stats_display()
    
    def on_download_started(self):
        """下载开始回调"""
        self.log_message.emit("==== 开始下载任务 ====")
        self.ui.start_button.setEnabled(False)
        self.ui.cancel_button.setEnabled(True)
        
        # 重置下载统计信息
        self.download_stats = {
            "total_users": self.ui.get_user_count(),
            "completed_users": 0,
            "total_videos": 0,
            "updated_videos": 0,
            "start_time": datetime.now(),
            "status": "进行中"
        }
        
        # 更新统计显示
        self.update_stats_display()
        
        # 启动计时器
        self.stats_timer.start()
    
    def on_download_progress(self, progress_data):
        """下载进度回调
        
        Args:
            progress_data: 进度数据字典
        """
        # 更新统计信息
        if 'total_videos' in progress_data:
            self.download_stats['total_videos'] = progress_data['total_videos']
        if 'updated_videos' in progress_data:
            self.download_stats['updated_videos'] = progress_data['updated_videos']
        if 'completed_users' in progress_data:
            self.download_stats['completed_users'] = progress_data['completed_users']
        
        # 更新统计显示
        self.update_stats_display()
    
    def on_download_finished(self):
        """下载完成回调"""
        self.log_message.emit("==== 下载任务已完成 ====")
        self.ui.start_button.setEnabled(True)
        self.ui.cancel_button.setEnabled(False)
        
        # 更新下载状态
        self.download_stats["status"] = "已完成"
        self.update_stats_display()
        
        # 停止计时器
        self.stats_timer.stop()
        
        # 安全清理线程
        if self.download_thread and self.download_thread.isRunning():
            # 先断开所有连接
            try:
                if self.download_worker:
                    self.download_thread.started.disconnect()
                    self.download_worker.started.disconnect()
                    self.download_worker.progress.disconnect()
                    self.download_worker.finished.disconnect()
                    self.download_worker.error.disconnect()
            except (TypeError, RuntimeError):
                # 忽略连接不存在的错误
                pass
                
            # 安全退出线程
            self.download_thread.quit()
            # 等待线程完成，设置超时避免永久阻塞
            if not self.download_thread.wait(5000):  # 等待最多5秒
                self.log_message.emit("警告: 下载线程无法正常退出，尝试强制终止")
                self.download_thread.terminate()
                self.download_thread.wait(1000)  # 再给1秒清理时间
    
    def on_download_error(self, error_message):
        """下载错误回调
        
        Args:
            error_message: 错误消息
        """
        self.log_message.emit(f"错误: {error_message}")
        self.on_download_finished()
    
    def update_stats_display(self):
        """更新统计显示"""
        self.ui.update_stats_display(self.download_stats)
    
    def update_elapsed_time(self):
        """更新已用时间"""
        if self.download_stats["start_time"]:
            elapsed = datetime.now() - self.download_stats["start_time"]
            hours, remainder = divmod(int(elapsed.total_seconds()), 3600)
            minutes, seconds = divmod(remainder, 60)
            elapsed_time = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            self.download_stats["elapsed_time"] = elapsed_time
            self.update_stats_display()