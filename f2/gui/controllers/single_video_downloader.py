"""
单个视频下载处理器

用于处理单个抖音视频的下载，支持短链接、长链接和混合文本中的链接。
"""

import asyncio
import traceback
from typing import Dict, Any, Optional, Union
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

from f2.apps.douyin.handler import DouyinHandler
from f2.apps.douyin.db import AsyncUserDB, AsyncVideoDB
from f2.apps.douyin.dl import DouyinDownloader
from f2.apps.douyin.utils import AwemeIdFetcher
from f2.log.logger import logger
from f2.gui.models.history_manager import HistoryManager


class SingleVideoDownloader(QObject):
    """单个视频下载处理器
    
    用于处理和下载单个抖音视频，支持多种链接格式和下载选项。
    """
    
    # 信号定义
    started = pyqtSignal()        # 开始下载信号
    progress = pyqtSignal(str)    # 下载进度信号
    finished = pyqtSignal()       # 下载完成信号
    error = pyqtSignal(str)       # 错误信号
    
    # 可配置参数默认值 - 便于未来扩展
    DEFAULT_CONFIG = {
        "interval": "all",        # 时间区间，默认为"all"
        "timeout": 5,             # 请求超时时间
        "download_config": {      # 下载相关配置
            "with_watermark": False,   # 是否下载带水印版本
            "with_music": False,       # 是否下载音频
            "quality": "hd",           # 视频质量 (hd, sd)
            "save_as_single_file": True  # 保存为单一文件而非拆分
        }
    }
    
    def __init__(self, video_link: str, config: Dict[str, Any], parent=None):
        """初始化单个视频下载处理器
        
        Args:
            video_link: 视频链接，可以是短链接、长链接或包含链接的混合文本
            config: 配置信息字典
            parent: 父对象
        """
        super().__init__(parent)
        self.video_link = video_link
        self.config = self._merge_config(config)
        self.is_running = False
        self.loop = None
        self.history_manager = None  # 历史记录管理器，可选
        self.download_handlers = {}  # 可扩展的下载处理器字典
        
        # 注册扩展点
        self._register_default_handlers()
    
    def _merge_config(self, user_config: Dict[str, Any]) -> Dict[str, Any]:
        """合并用户配置和默认配置
        
        Args:
            user_config: 用户提供的配置
            
        Returns:
            Dict[str, Any]: 合并后的配置
        """
        config = self.DEFAULT_CONFIG.copy()
        
        # 递归合并配置字典
        def _merge_dict(target, source):
            for key, value in source.items():
                if key in target and isinstance(target[key], dict) and isinstance(value, dict):
                    _merge_dict(target[key], value)
                else:
                    target[key] = value
        
        _merge_dict(config, user_config)
        return config
    
    def _register_default_handlers(self):
        """注册默认的下载处理器
        
        可以通过register_handler方法添加新的处理器
        """
        # 注册标准下载处理器
        self.register_handler("standard", self._standard_download_method)
        
        # 注册备用下载处理器
        self.register_handler("backup", self._backup_download_method)
    
    def register_handler(self, name: str, handler_func):
        """注册自定义下载处理器
        
        Args:
            name: 处理器名称
            handler_func: 处理器函数，需要接受kwargs参数并返回下载结果
        """
        self.download_handlers[name] = handler_func
    
    def set_history_manager(self, manager: HistoryManager):
        """设置历史记录管理器
        
        Args:
            manager: 历史记录管理器实例
        """
        self.history_manager = manager
    
    @pyqtSlot()
    def download(self):
        """开始下载视频
        
        这是Qt槽函数，会在新的事件循环中执行下载任务
        """
        try:
            self.started.emit()
            self.is_running = True
            
            # 创建新的事件循环
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
            
            # 运行下载任务
            self.loop.run_until_complete(self.download_one_video())
            
            self.finished.emit()
        except Exception as e:
            self.error.emit(f"下载过程中出现错误: {str(e)}\n{traceback.format_exc()}")
        finally:
            self.is_running = False
            if self.loop:
                self.loop.close()
    
    async def download_one_video(self):
        """下载单个视频的主流程
        
        配置下载参数，尝试使用注册的下载处理器下载视频
        """
        try:
            self.progress.emit(f"开始下载单个视频，链接：{self.video_link}")
            
            # 准备配置参数
            kwargs = self._prepare_download_config()
            
            # 尝试使用标准下载方法
            try:
                self.progress.emit("使用标准方法下载视频...")
                result = await self.download_handlers["standard"](kwargs)
                if result:
                    return True
            except Exception as e:
                self.progress.emit(f"标准下载方法失败: {str(e)}")
                logger.warning(f"标准下载方法失败: {e}")
            
            # 如果标准方法失败，尝试使用备用方法
            self.progress.emit("尝试使用备用下载方法...")
            return await self.download_handlers["backup"](kwargs)
            
        except Exception as e:
            self.progress.emit(f"视频下载失败：{str(e)}")
            logger.error(f"视频下载失败：{e}")
            raise
    
    def _prepare_download_config(self) -> Dict[str, Any]:
        """准备下载配置参数
        
        Returns:
            Dict[str, Any]: 下载配置参数
        """
        kwargs = self.config.copy()
        # 设置模式为 "one"，表示下载单个视频
        kwargs["mode"] = "one"
        # 设置URL参数
        kwargs["url"] = self.video_link
        # 重要：设置interval为"all"，避免时间过滤导致找不到视频
        kwargs["interval"] = "all"
        
        return kwargs
    
    def _add_to_history(self, result):
        """添加下载结果到历史记录
        
        Args:
            result: 下载结果对象
        """
        if (self.history_manager and 
            hasattr(result, "nickname") and 
            hasattr(result, "aweme_id")):
            nickname = getattr(result, "nickname", "未知用户")
            sec_user_id = getattr(result, "sec_user_id", "unknown")
            self.history_manager.add_history(sec_user_id, nickname, "成功", 1)
    
    async def _standard_download_method(self, kwargs: Dict[str, Any]) -> bool:
        """标准下载方法，使用F2内置的handler.handle_one_video方法
        
        Args:
            kwargs: 下载配置参数
            
        Returns:
            bool: 下载是否成功
        """
        # 创建DouyinHandler实例
        dyhandler = DouyinHandler(kwargs)
        
        self.progress.emit("解析视频链接中...")
        result = await dyhandler.handle_one_video()
        
        if result:
            self.progress.emit("视频下载成功")
            # 添加到历史记录
            self._add_to_history(result)
            return True
        return False
    
    async def _backup_download_method(self, kwargs: Dict[str, Any]) -> bool:
        """备用下载方法，当标准方法失败时使用
        
        Args:
            kwargs: 下载配置参数
            
        Returns:
            bool: 下载是否成功
        """
        try:
            # 获取视频ID
            aweme_id = await AwemeIdFetcher.get_aweme_id(kwargs.get("url"))
            if not aweme_id:
                self.progress.emit("无法从链接中提取视频ID")
                logger.error("无法从链接中提取视频ID")
                return False
            
            self.progress.emit(f"成功提取视频ID: {aweme_id}")
            logger.info(f"处理作品: {aweme_id} 数据")
            
            # 使用DouyinHandler的组件
            dyhandler = DouyinHandler(kwargs)
            downloader = DouyinDownloader(kwargs)
            
            # 获取视频详情
            try:
                aweme_data = await dyhandler.fetch_one_video(aweme_id)
                if not aweme_data:
                    self.progress.emit("无法获取视频详情")
                    return False
            except Exception as e:
                self.progress.emit(f"获取视频详情失败: {str(e)}")
                logger.error(f"获取视频详情失败: {e}")
                return False
            
            # 从视频数据中获取sec_user_id
            sec_user_id = aweme_data.sec_user_id
            if not sec_user_id:
                self.progress.emit("无法获取用户ID")
                return False
            
            # 创建用户目录
            async with AsyncUserDB("douyin_users.db") as db:
                try:
                    user_path = await dyhandler.get_or_add_user_data(kwargs, sec_user_id, db)
                    if not user_path:
                        self.progress.emit("无法创建用户目录")
                        return False
                except Exception as e:
                    self.progress.emit(f"创建用户目录失败: {str(e)}")
                    logger.error(f"创建用户目录失败: {e}")
                    # 继续执行，尝试下载视频
            
            # 将视频数据转换为字典并下载
            video_dict = aweme_data._to_dict()
            
            # 应用下载配置
            self._apply_download_options(kwargs, video_dict)
            
            self.progress.emit(f"准备下载视频: {aweme_data.desc}")
            
            # 创建下载任务
            try:
                self.progress.emit("开始下载视频...")
                await downloader.create_download_tasks(kwargs, video_dict, user_path)
                self.progress.emit("视频下载成功")
                
                # 添加到历史记录
                if self.history_manager:
                    nickname = getattr(aweme_data, "nickname", "未知用户")
                    self.history_manager.add_history(sec_user_id, nickname, "成功", 1)
                
                return True
            except Exception as e:
                self.progress.emit(f"下载视频失败: {str(e)}")
                logger.error(f"下载视频失败: {e}")
                return False
            
        except Exception as e:
            self.progress.emit(f"处理过程中出现错误: {str(e)}")
            logger.error(f"处理过程中出现错误: {e}")
            return False
    
    def _apply_download_options(self, kwargs: Dict[str, Any], video_dict: Dict[str, Any]):
        """应用下载选项配置
        
        Args:
            kwargs: 下载配置参数
            video_dict: 视频数据字典
        """
        # 获取下载配置
        download_config = kwargs.get("download_config", {})
        
        # 应用水印设置
        if "with_watermark" in download_config:
            kwargs["watermark"] = download_config["with_watermark"]
        
        # 应用音频设置
        if "with_music" in download_config:
            kwargs["music"] = download_config["with_music"]
        
        # 应用质量设置
        if "quality" in download_config:
            kwargs["quality"] = download_config["quality"]
        
        # 应用文件拆分设置
        if "save_as_single_file" in download_config:
            kwargs["save_as_single_file"] = download_config["save_as_single_file"]
            
    async def get_video_info(self, video_url: str) -> Optional[Dict[str, Any]]:
        """获取视频信息但不下载
        
        Args:
            video_url: 视频链接
            
        Returns:
            Optional[Dict[str, Any]]: 视频信息字典，失败时返回None
        """
        try:
            # 准备配置
            kwargs = self._prepare_download_config()
            kwargs["url"] = video_url
            
            # 获取视频ID
            aweme_id = await AwemeIdFetcher.get_aweme_id(video_url)
            if not aweme_id:
                logger.error("无法从链接中提取视频ID")
                return None
            
            # 使用DouyinHandler获取视频详情
            dyhandler = DouyinHandler(kwargs)
            aweme_data = await dyhandler.fetch_one_video(aweme_id)
            
            if not aweme_data:
                return None
                
            # 返回视频信息字典
            return aweme_data._to_dict()
            
        except Exception as e:
            logger.error(f"获取视频信息失败: {e}")
            return None
    
    async def batch_download(self, video_urls: list) -> Dict[str, bool]:
        """批量下载多个视频
        
        Args:
            video_urls: 视频链接列表
            
        Returns:
            Dict[str, bool]: 下载结果字典，键为URL，值为是否成功
        """
        results = {}
        for url in video_urls:
            try:
                # 保存当前链接
                old_url = self.video_link
                self.video_link = url
                
                # 下载视频
                self.progress.emit(f"开始下载: {url}")
                success = await self.download_one_video()
                results[url] = success
                
                # 恢复原始链接
                self.video_link = old_url
            except Exception as e:
                logger.error(f"下载视频 {url} 失败: {e}")
                results[url] = False
        
        return results