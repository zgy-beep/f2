# -*- coding:utf-8 -*-
# @Information  : 
# @Author       : ZGY
# @Date         : 2025-04-29 09:36:56
# @FilePath     : /f2_gui/f2/gui/models/user_update_checker.py
# @LastEditTime : 2025-04-29 10:00:19

"""
历史记录对话框中用于检查用户更新的工具类
"""

import asyncio
import traceback
from datetime import datetime
from PyQt5.QtCore import QThread, pyqtSignal

from f2.log.logger import logger
from f2.utils.conf_manager import ConfigManager
from f2.cli.cli_console import RichConsoleManager


class UserUpdateChecker:
    """用户更新检查工具类"""
    
    @staticmethod
    async def check_user_updates(user_id, last_download_time):
        """
        检查用户是否有新作品更新
        
        Args:
            user_id: 用户ID
            last_download_time: 上次下载时间字符串
            
        Returns:
            bool: 是否有更新
        """
        handler = None
        try:
            from f2.apps.douyin.handler import DouyinHandler
            from f2.apps.douyin.db import AsyncUserDB
            import logging

            # 临时降低aiohttp的日志级别，避免过多警告
            logging.getLogger('aiohttp').setLevel(logging.ERROR)
            
            # 获取用户最后下载时间的时间戳
            last_timestamp = None
            if last_download_time:
                try:
                    dt = datetime.strptime(last_download_time, "%Y-%m-%d %H:%M:%S")
                    last_timestamp = int(dt.timestamp())
                    logger.debug(f"上次下载时间: {last_download_time}, 时间戳: {last_timestamp}")
                except Exception as e:
                    logger.error(f"解析最后下载时间失败: {e}")
            
            # 从配置文件获取抖音参数
            kwargs = {
                "headers": {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0",
                    "Referer": "https://www.douyin.com/",
                },
                "proxies": {"http://": None, "https://": None},
                "timeout": 10,
                "max_counts": 1,
                "page_counts": 1
            } | ConfigManager("conf/app.yaml").get_config("douyin")
            
            # 创建处理器
            handler = DouyinHandler(kwargs)
            
            # 先获取用户信息验证ID是否有效
            logger.debug(f"正在获取用户 {user_id} 的资料...")
            user_profile = await handler.fetch_user_profile(sec_user_id=user_id)
            
            if not user_profile or not user_profile.sec_user_id:
                logger.error(f"无法获取用户信息: {user_id}")
                return False
            
            logger.debug(f"用户 {user_id} 资料获取成功: {user_profile.nickname}")
            
            # 获取用户最新作品
            logger.debug(f"正在获取用户 {user_id} 的最新作品...")
            
            # 避免使用异步生成器，直接获取最新一条作品的数据
            from f2.apps.douyin.crawler import DouyinCrawler
            from f2.apps.douyin.model import UserPost
            from f2.apps.douyin.filter import UserPostFilter
            
            # 直接使用爬虫获取一条数据
            async with DouyinCrawler(kwargs) as crawler:
                params = UserPost(
                    sec_user_id=user_id,
                    count=1,
                    max_cursor=0
                )
                response = await crawler.fetch_user_post(params)
                latest_post = UserPostFilter(response)
            
            # 检查是否有作品
            if not latest_post or not latest_post.has_aweme:
                logger.debug(f"用户 {user_id} 作品列表为空")
                return False
            
            # 获取最新作品ID
            aweme_ids = latest_post.aweme_id
            if not aweme_ids or len(aweme_ids) == 0:
                logger.debug(f"用户 {user_id} 获取作品ID失败")
                return False
            
            # 获取原始数据
            raw_data = latest_post._to_raw()
            if not raw_data or not raw_data.get("aweme_list") or len(raw_data["aweme_list"]) == 0:
                logger.debug(f"用户 {user_id} 获取原始数据失败")
                return False
            
            # 获取最新作品的发布时间戳
            latest_post_item = raw_data["aweme_list"][0]
            latest_timestamp = int(latest_post_item.get("create_time", 0))
            latest_time_str = datetime.fromtimestamp(latest_timestamp).strftime("%Y-%m-%d %H:%M:%S")
            logger.debug(f"最新作品发布时间: {latest_time_str}, 时间戳: {latest_timestamp}")
            
            # 对比时间戳判断是否有更新
            if last_timestamp and latest_timestamp > last_timestamp:
                logger.info(f"用户 {user_id} 有新作品更新! 最新时间: {latest_time_str}, 上次下载时间: {last_download_time}")
                return True
            
            logger.debug(f"用户 {user_id} 没有新作品更新")
            return False
            
        except Exception as e:
            logger.error(f"检查用户更新失败: {e}")
            logger.debug(traceback.format_exc())
            return False
        finally:
            # 确保关闭资源
            if handler and hasattr(handler, 'downloader'):
                try:
                    await handler.downloader.close()
                except Exception as e:
                    logger.error(f"关闭下载器失败: {e}")


class CheckUpdateWorker(QThread):
    """
    检查用户是否有更新内容的工作线程
    """
    finished = pyqtSignal(dict)  # 信号：完成信号，返回检查结果
    error = pyqtSignal(str)      # 信号：错误信号
    
    def __init__(self, user_id, last_download_time):
        super().__init__()
        self.user_id = user_id
        self.last_download_time = last_download_time
        self.is_running = True
        
    def run(self):
        """线程运行函数"""
        try:
            # 确保在线程内创建新的事件循环
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            # 执行检查
            has_updates = loop.run_until_complete(
                UserUpdateChecker.check_user_updates(
                    self.user_id, 
                    self.last_download_time
                )
            )
            loop.close()
            
            # 检查是否已请求终止
            if not self.is_running:
                return
                
            # 发送结果信号
            result = {
                "user_id": self.user_id,
                "has_updates": has_updates,
                "last_check_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            self.finished.emit(result)
            
        except Exception as e:
            # 捕获并发送错误信号
            if self.is_running:  # 仅在线程仍在运行时发送信号
                error_msg = f"检查更新失败: {str(e)}\n{traceback.format_exc()}"
                logger.error(error_msg)
                self.error.emit(error_msg)
    
    def stop(self):
        """安全停止线程"""
        self.is_running = False