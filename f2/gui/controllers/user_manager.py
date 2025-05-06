"""
抖音下载器 - 用户管理控制器
"""

import asyncio
import threading
from PyQt5.QtWidgets import QTableWidgetItem, QPushButton, QMessageBox, QListWidgetItem
from PyQt5.QtCore import pyqtSignal, QObject
import yaml
import os

from f2.log.logger import logger
from f2.apps.douyin.handler import DouyinHandler
from f2.apps.douyin.db import AsyncUserDB


class UserManager(QObject):
    """用户管理控制器"""
    
    # 信号
    user_added = pyqtSignal(str, str)  # 用户ID, 用户昵称
    user_removed = pyqtSignal(int)     # 行索引
    user_updated = pyqtSignal(int, str)  # 行索引, 用户昵称
    log_message = pyqtSignal(str)      # 日志消息
    
    def __init__(self, download_tab_ui, history_manager):
        """初始化用户管理控制器
        
        Args:
            download_tab_ui: 下载标签页UI组件
            history_manager: 历史记录管理器
        """
        super().__init__()
        self.ui = download_tab_ui
        self.history_manager = history_manager
        
        # 用户列表 - 保存用户信息
        self.users = []  # [(user_id, nickname), ...]
        
        # 绑定信号和槽
        self.setup_connections()
        
    def setup_connections(self):
        """设置信号和槽连接"""
        # 从UI组件连接，适配扁平化结构
        self.ui.add_user_button.clicked.connect(self.add_users)
        self.ui.clear_all_button.clicked.connect(self.clear_user_list)
        
        # 连接自身的信号
        self.log_message.connect(self.ui.append_log)
        self.user_updated.connect(self.update_user_nickname)
    
    def add_users(self):
        """添加用户到列表"""
        input_text = self.ui.user_id_input.text().strip()
        if not input_text:
            QMessageBox.warning(None, "警告", "请输入用户ID或链接")
            return
        
        # 处理输入
        if not input_text:
            return
            
        # 提取sec_user_id
        sec_user_id = input_text
        
        # 检查是否是链接
        if "douyin.com" in input_text:
            # 简单解析，实际使用中应使用正则表达式或URL解析库
            if "/user/" in input_text:
                parts = input_text.split("/user/")
                if len(parts) > 1:
                    sec_user_id = parts[1].split("?")[0].strip()
                    
        # 检查是否已在列表中
        for i, (user_id, _) in enumerate(self.users):
            if user_id == sec_user_id:
                QMessageBox.information(None, "提示", f"用户ID {sec_user_id} 已在列表中")
                return
        
        # 添加到用户列表
        self.users.append((sec_user_id, "获取中..."))
        
        # 添加到列表控件
        self.add_user_to_list(sec_user_id, "获取中...")
        
        # 清空输入框
        self.ui.user_id_input.clear()
        
        # 尝试异步获取用户信息
        self.fetch_user_info(sec_user_id, len(self.users) - 1)
        
        # 更新统计信息
        self.update_stats()
    
    def add_user_to_list(self, user_id, nickname):
        """添加用户到列表控件
        
        Args:
            user_id: 用户ID
            nickname: 用户昵称
        """
        item_text = f"{nickname} ({user_id})"
        item = QListWidgetItem(item_text)
        self.ui.user_list.addItem(item)
    
    def add_user_from_history(self, user_id, nickname):
        """从历史记录中添加用户到下载队列
        
        Args:
            user_id: 用户ID
            nickname: 用户昵称
        """
        # 检查是否已在列表中
        for i, (existing_id, _) in enumerate(self.users):
            if existing_id == user_id:
                self.log_message.emit(f"用户ID {user_id} 已在下载队列中")
                return
        
        # 添加到用户列表
        self.users.append((user_id, nickname))
        
        # 添加到列表控件
        self.add_user_to_list(user_id, nickname)
        
        self.log_message.emit(f"已从历史记录添加用户: {nickname} ({user_id})")
        
        # 更新统计信息
        self.update_stats()
    
    def fetch_user_info(self, sec_user_id, index):
        """异步获取用户信息
        
        Args:
            sec_user_id: 用户ID
            index: 用户在列表中的索引
        """
        def run():
            try:
                # 创建临时事件循环获取用户信息
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                
                # 读取配置文件获取cookie和其他设置
                kwargs = {}
                config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "gui_config.yaml")
                try:
                    with open(config_path, 'r', encoding='utf-8') as f:
                        yaml_config = yaml.safe_load(f)
                        if yaml_config and 'douyin' in yaml_config:
                            kwargs = yaml_config['douyin'].copy()
                            logger.debug(f"已从配置文件加载cookie和其他设置")
                except Exception as e:
                    logger.error(f"读取配置文件失败: {e}")
                
                async def get_user_name():
                    try:
                        # 确保kwargs包含必要的请求头和代理设置
                        if 'headers' not in kwargs:
                            kwargs['headers'] = {
                                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0',
                                'Referer': 'https://www.douyin.com/'
                            }
                        if 'proxies' not in kwargs:
                            kwargs['proxies'] = {'http://': None, 'https://': None}
                        
                        async with AsyncUserDB("douyin_users.db") as audb:
                            # 尝试从数据库获取用户信息
                            user_info = await audb.get_user_info(sec_user_id)
                            
                            # 如果不存在，尝试添加
                            if not user_info:
                                handler = DouyinHandler(kwargs)
                                try:
                                    # 这里只是查询用户信息，不需要创建目录
                                    user_data = await handler.fetch_user_profile(sec_user_id)
                                    if user_data and hasattr(user_data, 'nickname'):
                                        nickname = user_data.nickname
                                        # 更新用户昵称
                                        self.user_updated.emit(index, nickname)
                                        self.log_message.emit(f"成功获取用户名称：{nickname}")
                                        return
                                except Exception as e:
                                    logger.error(f"通过API获取用户信息失败: {e}")
                            else:
                                nickname = user_info.get("nickname", "未知用户")
                                # 更新用户昵称
                                self.user_updated.emit(index, nickname)
                                self.log_message.emit(f"从数据库获取用户名称：{nickname}")
                                return
                    except Exception as e:
                        logger.error(f"获取用户信息失败: {e}")
                    
                    # 如果前面的尝试都失败了，设置为默认值，但不提示错误
                    self.user_updated.emit(index, "用户" + sec_user_id[-6:])
                    self.log_message.emit(f"无法获取完整用户信息，使用ID代替")
                
                loop.run_until_complete(get_user_name())
                loop.close()
            except Exception as e:
                logger.error(f"获取用户信息线程出错: {e}")
                self.user_updated.emit(index, "获取失败")
                
        # 创建线程获取用户信息
        thread = threading.Thread(target=run)
        thread.daemon = True
        thread.start()
    
    def update_user_nickname(self, index, nickname):
        """更新用户昵称（从子线程调用）
        
        Args:
            index: 用户在列表中的索引
            nickname: 用户昵称
        """
        if 0 <= index < len(self.users):
            # 更新内部用户列表
            user_id = self.users[index][0]
            self.users[index] = (user_id, nickname)
            
            # 更新列表控件显示
            if index < self.ui.user_list.count():
                self.ui.user_list.item(index).setText(f"{nickname} ({user_id})")
    
    def remove_user(self, index):
        """从列表中删除用户
        
        Args:
            index: 用户在列表中的索引
        """
        if 0 <= index < len(self.users):
            # 从内部列表移除
            self.users.pop(index)
            
            # 从列表控件移除
            if index < self.ui.user_list.count():
                self.ui.user_list.takeItem(index)
            
            # 更新统计信息
            self.update_stats()
    
    def clear_user_list(self):
        """清空用户列表"""
        # 清空内部列表
        self.users.clear()
        
        # 清空列表控件
        self.ui.user_list.clear()
        
        # 更新统计信息
        self.update_stats()
    
    def get_user_ids(self):
        """获取所有用户ID
        
        Returns:
            list: 用户ID列表
        """
        return [user_id for user_id, _ in self.users]
    
    def update_stats(self):
        """更新统计信息"""
        stats = {
            'total_users': len(self.users),
            'downloaded_users': 0,
            'status': '空闲',
            'progress': 0
        }
        self.ui.update_stats_display(stats)