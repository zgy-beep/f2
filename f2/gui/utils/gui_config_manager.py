"""
GUI配置管理器：专门管理GUI相关的配置
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any


class GUIConfigManager:
    """
    GUI配置管理器，负责读取和保存GUI相关的配置
    """
    def __init__(self, config_file=None):
        """
        初始化配置管理器
        
        Args:
            config_file: 配置文件路径，如果为None则使用默认路径
        """
        if config_file is None:
            # 使用默认路径，将配置文件放在gui目录下
            dir_path = Path(__file__).parent.parent
            self.config_file = dir_path / "gui_config.yaml"
        else:
            self.config_file = Path(config_file)
        
        # 确保配置文件存在
        self._ensure_config_file()
        
        # 加载配置
        self.config = self._load_config()
    
    def _ensure_config_file(self):
        """确保配置文件存在，如果不存在则创建默认配置"""
        if not self.config_file.exists():
            # 获取gui目录下的download文件夹路径作为默认下载路径
            default_download_path = Path(__file__).parent.parent / "download"
            
            # 创建默认配置
            default_config = {
                "douyin": {
                    "headers": {
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0",
                        "Referer": "https://www.douyin.com/",
                    },
                    "proxies": {"http://": None, "https://": None},
                    "mode": "post",
                    "max_tasks": 3,
                    "monitor_updates": False,
                    "update_interval": 60,  # 分钟
                    "naming": "{create}_{desc}",
                    "video": True,
                    "cover": True,
                    "desc": True,
                    "music": True,
                    "folderize": True,
                    "path": str(default_download_path),  # 使用path而不是download_path
                }
            }
            
            # 确保父目录存在
            os.makedirs(self.config_file.parent, exist_ok=True)
            
            # 确保下载目录存在
            os.makedirs(default_download_path, exist_ok=True)
            
            # 保存默认配置
            with open(self.config_file, 'w', encoding='utf-8') as f:
                yaml.dump(default_config, f, default_flow_style=False, allow_unicode=True)
    
    def _load_config(self) -> Dict[str, Any]:
        """
        加载配置
        
        Returns:
            配置字典
        """
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        except Exception as e:
            print(f"加载配置文件失败: {e}")
            return {}
    
    def get_config(self, section=None) -> Dict[str, Any]:
        """
        获取配置
        
        Args:
            section: 配置节点名称，如果为None则返回整个配置
            
        Returns:
            配置字典
        """
        if section is None:
            return self.config
        
        return self.config.get(section, {})
    
    def update_config(self, section: str, config: Dict[str, Any]) -> bool:
        """
        更新配置
        
        Args:
            section: 配置节点名称
            config: 新的配置字典
            
        Returns:
            是否成功更新
        """
        try:
            # 更新内存中的配置
            self.config[section] = config
            
            # 写入文件
            with open(self.config_file, 'w', encoding='utf-8') as f:
                yaml.dump(self.config, f, default_flow_style=False, allow_unicode=True)
            
            return True
        except Exception as e:
            print(f"更新配置失败: {e}")
            return False
    
    def get_config_file_path(self) -> str:
        """
        获取配置文件路径
        
        Returns:
            配置文件路径
        """
        return str(self.config_file)