"""
历史记录管理器：负责记录和管理下载历史
"""

import json
from typing import List, Dict, Any
from pathlib import Path
from datetime import datetime
from f2.log.logger import logger


class HistoryManager:
    """
    历史记录管理器，用于记录下载过的用户信息
    """
    def __init__(self, history_file=None):
        """
        初始化历史记录管理器
        
        Args:
            history_file: 历史记录文件路径，如果为None则使用默认路径
        """
        if history_file is None:
            # 使用默认路径，将历史记录文件放在gui目录下
            dir_path = Path(__file__).parent.parent
            self.history_file = dir_path / "download_history.json"
        else:
            self.history_file = Path(history_file)
        
        # 加载历史记录
        self.history = self.load_history()
    
    def load_history(self) -> List[Dict[str, Any]]:
        """
        加载历史记录
        
        Returns:
            历史记录列表
        """
        if not self.history_file.exists():
            return []
        
        try:
            with open(self.history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"加载历史记录失败: {e}")
            return []
    
    def save_history(self) -> bool:
        """
        保存历史记录
        
        Returns:
            是否成功保存
        """
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            logger.error(f"保存历史记录失败: {e}")
            return False
    
    def add_history(self, user_id: str, nickname: str = None, status: str = "成功", update_count: int = 0) -> bool:
        """
        添加历史记录
        
        Args:
            user_id: 用户ID
            nickname: 用户昵称
            status: 下载状态
            update_count: 本次更新的作品数量
            
        Returns:
            是否成功添加
        """
        # 检查是否已存在相同用户ID的记录
        for item in self.history:
            if item.get("user_id") == user_id:
                # 更新现有记录
                item["nickname"] = nickname or item.get("nickname", "未知用户")
                current_time = datetime.now()
                current_time_str = current_time.strftime("%Y-%m-%d %H:%M:%S")
                
                # 先保存之前的下载时间，再更新当前下载时间
                last_time = item.get("last_download_time", "")
                item["last_download_time"] = current_time_str
                
                # 修复计数逻辑：当状态变为成功时更新下载次数
                if status == "成功":
                    # 如果之前状态不是成功，或者是新的下载会话，则增加下载计数
                    is_new_session = False
                    
                    # 检查是否是新的下载会话（不同日期或间隔较长）
                    if last_time:
                        try:
                            last_datetime = datetime.strptime(last_time, "%Y-%m-%d %H:%M:%S")
                            # 如果是不同日期或间隔超过30分钟，认为是新会话
                            time_diff = (current_time - last_datetime).total_seconds()
                            is_new_session = (current_time.date() != last_datetime.date()) or time_diff > 1800
                        except Exception as e:
                            logger.error(f"解析日期时间出错: {e}")
                            is_new_session = True
                    else:
                        is_new_session = True
                    
                    # 如果之前状态不是成功，或者是新的下载会话，则增加下载计数
                    if item.get("status") != "成功" or is_new_session:
                        item["download_count"] = item.get("download_count", 0) + 1
                
                # 记录本次更新的作品数量
                if update_count > 0:
                    item["last_update_count"] = update_count
                    item["total_update_count"] = item.get("total_update_count", 0) + update_count
                
                item["status"] = status
                return self.save_history()
        
        # 添加新记录
        new_record = {
            "user_id": user_id,
            "nickname": nickname or "未知用户",
            "first_download_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "last_download_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "download_count": 1,
            "status": status
        }
        
        # 添加更新计数字段
        if update_count > 0:
            new_record["last_update_count"] = update_count
            new_record["total_update_count"] = update_count
        
        self.history.append(new_record)
        
        return self.save_history()
    
    def get_history(self) -> List[Dict[str, Any]]:
        """
        获取历史记录
        
        Returns:
            历史记录列表
        """
        return self.history
    
    def clear_history(self) -> bool:
        """
        清空历史记录
        
        Returns:
            是否成功清空
        """
        self.history = []
        return self.save_history()