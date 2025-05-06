# -*- coding:utf-8 -*-
# @Information  : 
# @Author       : ZGY
# @Date         : 2025-04-28 10:37:55
# @FilePath     : /f2_gui/f2/gui/controllers/download_worker.py
# @LastEditTime : 2025-04-28 18:32:46

"""
下载工作线程控制器
"""

import asyncio
import traceback
from typing import List, Dict, Any
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from pathlib import Path

from f2.apps.douyin.handler import DouyinHandler
from f2.apps.douyin.db import AsyncUserDB
from f2.apps.douyin.dl import DouyinDownloader
from f2.log.logger import logger
from f2.gui.models.history_manager import HistoryManager


class DownloadWorker(QObject):
    """
    下载工作线程
    """
    started = pyqtSignal()
    progress = pyqtSignal(str)
    finished = pyqtSignal()
    error = pyqtSignal(str)
    
    def __init__(self, user_ids: List[str], config: Dict[str, Any], parent=None):
        super().__init__(parent)
        self.user_ids = user_ids
        self.config = config
        self.is_running = False
        self.loop = None
        self.history_manager = None
        
    @pyqtSlot()
    def download(self):
        try:
            self.started.emit()
            self.is_running = True
            
            # 创建新的事件循环
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
            
            # 运行下载任务
            self.loop.run_until_complete(self.run_download_tasks())
            
            self.finished.emit()
        except Exception as e:
            self.error.emit(f"下载过程中出现错误: {str(e)}\n{traceback.format_exc()}")
        finally:
            self.is_running = False
            if self.loop:
                self.loop.close()
    
    @pyqtSlot()
    def download_video(self):
        """
        下载单个视频（one模式）
        """
        try:
            self.started.emit()
            self.is_running = True
            
            # 创建新的事件循环
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
            
            # 运行单个视频下载任务
            self.loop.run_until_complete(self.run_one_video_download())
            
            self.finished.emit()
        except Exception as e:
            self.error.emit(f"下载过程中出现错误: {str(e)}\n{traceback.format_exc()}")
        finally:
            self.is_running = False
            if self.loop:
                self.loop.close()
    
    async def download_user_posts(self, sec_user_id: str):
        """
        下载单个用户的所有作品
        """
        nickname = "未知用户"  # 初始化昵称，以便在异常处理中使用
        try:
            self.progress.emit(f"开始下载用户ID：{sec_user_id} 的作品...")
            
            # 使用传入的配置信息
            kwargs = self.config.copy()
            
            # 实例化下载器和处理器
            dydownloader = DouyinDownloader(kwargs)
            dyhandler = DouyinHandler(kwargs)
            
            # 获取用户信息并创建目录
            async with AsyncUserDB("douyin_users.db", **kwargs) as audb:
                user_path = await dyhandler.get_or_add_user_data(kwargs, sec_user_id, audb)
                
                # 获取用户基本信息
                user_info = await audb.get_user_info(sec_user_id)
                if user_info:
                    nickname = user_info.get("nickname", "未知用户")
                    self.progress.emit(f"用户名: {nickname}, 正在获取作品列表...")
                    
                    # 添加到历史记录 - 只在开始时标记为"下载中"，但不增加计数
                    if self.history_manager:
                        self.history_manager.add_history(sec_user_id, nickname, "下载中", 0)

            video_count = 0  # 总作品数
            updated_count = 0  # 实际更新的作品数
            download_success = False
            
            # 设置日期区间参数
            min_cursor = 0
            max_cursor = kwargs.get("max_cursor", 0)
            interval = kwargs.get("interval")
            page_counts = kwargs.get("page_counts", 20)
            max_counts = kwargs.get("max_counts")
            
            # 判断是否提供了interval参数
            if interval is not None and interval != "all":
                from f2.utils.utils import interval_2_timestamp
                # 倒序查找
                min_cursor = interval_2_timestamp(interval, date_type="start")
                max_cursor = interval_2_timestamp(interval, date_type="end")
                self.progress.emit(f"设置日期区间过滤: {interval}, 开始时间戳: {min_cursor}, 结束时间戳: {max_cursor}")
            
            # 获取作品列表，传入日期区间参数
            async for aweme_list in dyhandler.fetch_user_post_videos(
                sec_user_id=sec_user_id,
                min_cursor=min_cursor,
                max_cursor=max_cursor,
                page_counts=page_counts,
                max_counts=max_counts
            ):
                if not aweme_list:
                    self.progress.emit(f"无法获取用户作品信息: {sec_user_id}")
                    
                    # 更新历史记录状态 - 只在失败时更新状态，保持更新计数为0
                    if self.history_manager and not download_success:
                        self.history_manager.add_history(sec_user_id, nickname, "失败", 0)
                    return

                # 过滤作品
                video_list = aweme_list._to_list()
                video_count += len(video_list)
                self.progress.emit(f"获取到 {len(video_list)} 个作品，总计: {video_count} 个作品")
                
                # 创建下载任务并获取实际更新的作品数量
                batch_updated = await dydownloader.create_download_tasks(kwargs, video_list, user_path)
                if batch_updated is not None and isinstance(batch_updated, int):
                    updated_count += batch_updated
                    if batch_updated > 0:
                        self.progress.emit(f"本批次实际更新了 {batch_updated} 个新作品，总计更新: {updated_count} 个作品")
                
                download_success = True

            self.progress.emit(f"用户ID：{sec_user_id} 作品下载完成。总共获取 {video_count} 个作品，实际更新 {updated_count} 个新作品。")
            
            # 更新历史记录状态 - 无论是否有更新都更新状态和计数
            if self.history_manager and download_success:
                self.history_manager.add_history(sec_user_id, nickname, "成功", updated_count)
                
        except Exception as e:
            self.progress.emit(f"用户ID：{sec_user_id} 下载失败：{str(e)}")
            logger.error(f"用户ID：{sec_user_id} 下载失败：{e}")
            
            # 更新历史记录状态 - 只在异常时更新状态，保持更新计数为0
            if self.history_manager:
                self.history_manager.add_history(sec_user_id, nickname, "失败", 0)
    
    async def run_download_tasks(self):
        """
        批量启动作品下载任务
        """
        self.progress.emit("开始批量下载多个用户的作品")
        
        # 设置并发数
        max_tasks = self.config.get("max_tasks", 3)
        semaphore = asyncio.Semaphore(max_tasks)
        
        # 设置是否监控更新
        monitor_updates = self.config.get("monitor_updates", False)
        update_interval = self.config.get("update_interval", 60) * 60  # 转换为秒
        
        async def limited_download(sec_user_id):
            async with semaphore:
                if monitor_updates:
                    # 定期检查作品更新
                    while self.is_running:
                        await self.download_user_posts(sec_user_id)
                        # 等待指定的时间间隔
                        for i in range(update_interval):
                            if not self.is_running:
                                break
                            if i % 60 == 0 and i > 0:  # 每分钟报告一次
                                self.progress.emit(f"等待检查更新... 剩余 {(update_interval - i) // 60} 分钟")
                            await asyncio.sleep(1)
                else:
                    # 仅下载一次
                    await self.download_user_posts(sec_user_id)
        
        # 创建并发任务
        tasks = [asyncio.create_task(limited_download(sec_user_id)) for sec_user_id in self.user_ids]
        
        # 等待所有任务完成
        await asyncio.gather(*tasks)
    
    async def run_one_video_download(self):
        """
        下载单个视频
        """
        # 获取视频URL
        video_url = self.config.get("video_url")
        
        if not video_url:
            self.progress.emit("错误: 未指定视频URL")
            return
        
        self.progress.emit(f"开始处理单个视频下载: {video_url}")
        
        try:
            # 使用传入的配置信息
            kwargs = self.config.copy()
            
            # 实例化处理器和下载器
            dyhandler = DouyinHandler(kwargs)
            dydownloader = DouyinDownloader(kwargs)
            
            # 提取视频ID - 使用工具类中的方法而非直接调用handler的方法
            from f2.apps.douyin.utils import AwemeIdFetcher
            
            self.progress.emit("正在提取视频ID...")
            # 提取视频ID
            aweme_id = await AwemeIdFetcher.get_aweme_id(video_url)
            
            if not aweme_id:
                self.progress.emit("错误: 无法从URL中提取视频ID")
                return
            
            self.progress.emit(f"成功提取视频ID: {aweme_id}")
            
            # 获取视频详情 - 使用正确的handler方法获取单个作品详情
            self.progress.emit("正在获取视频详情...")
            video_detail = await dyhandler.fetch_one_video(aweme_id=aweme_id)
            
            if not video_detail:
                self.progress.emit("错误: 无法获取视频详情")
                return
            
            # 转换为列表
            if hasattr(video_detail, '_to_list'):
                video_info = video_detail._to_list()
                if not video_info:
                    self.progress.emit("错误: 视频数据转换失败")
                    return
            else:
                video_info = video_detail
                
            # 提取视频信息并显示
            try:
                if isinstance(video_info, dict):
                    desc = video_info.get('desc', '无描述')
                    author = video_info.get('author', {}).get('nickname', '未知作者')
                else:
                    desc = getattr(video_info, 'desc', '无描述')
                    author = getattr(getattr(video_info, 'author', None), 'nickname', '未知作者')
                    
                self.progress.emit(f"视频描述: {desc}")
                self.progress.emit(f"作者: {author}")
            except Exception as e:
                self.progress.emit(f"提取视频信息时出错: {str(e)}")
                # 继续下载流程，不影响主要功能
        except Exception as e:
            self.progress.emit(f"下载视频失败: {str(e)}")
            logger.error(f"下载视频失败: {e}")