"""
统一配置管理模块 - 为GUI组件提供一致的配置访问接口
"""

from f2.utils.conf_manager import ConfigManager
from f2.log.logger import logger
import f2
from pathlib import Path
import os
import yaml
from typing import Any, Dict, Optional

class GUIConfigProvider:
    """
    GUI配置提供者 - 单例模式
    
    为GUI组件提供统一的配置访问接口，管理配置的加载、保存和访问。
    该类使用单例模式，确保整个应用中只有一个配置实例。
    """
    
    _instance = None
    _config = {}
    _config_path = None
    _is_initialized = False
    
    def __new__(cls, *args, **kwargs):
        """确保类的单例模式"""
        if cls._instance is None:
            cls._instance = super(GUIConfigProvider, cls).__new__(cls)
        return cls._instance
    
    def __init__(self, config_path=None):
        """初始化配置提供者
        
        Args:
            config_path: 配置文件路径，默认为None，使用默认路径
        """
        if not self._is_initialized:
            self._config_path = config_path or os.path.join(
                os.path.dirname(os.path.abspath(__file__)), "gui_config.yaml"
            )
            self.load_config()
            self._is_initialized = True
    
    def load_config(self) -> bool:
        """加载配置
        
        Returns:
            bool: 加载成功返回True，否则返回False
        """
        try:
            if os.path.exists(self._config_path):
                with open(self._config_path, 'r', encoding='utf-8') as f:
                    self._config = yaml.safe_load(f) or {}
                logger.info(f"已从 {self._config_path} 加载配置")
                return True
            else:
                self._config = {}
                logger.info(f"配置文件 {self._config_path} 不存在，使用默认配置")
                return False
        except Exception as e:
            logger.error(f"加载配置失败: {str(e)}")
            self._config = {}
            return False
    
    def save_config(self) -> bool:
        """保存配置
        
        Returns:
            bool: 保存成功返回True，否则返回False
        """
        try:
            with open(self._config_path, 'w', encoding='utf-8') as f:
                yaml.dump(self._config, f, allow_unicode=True)
            logger.info(f"配置已保存到 {self._config_path}")
            return True
        except Exception as e:
            logger.error(f"保存配置失败: {str(e)}")
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置值
        
        Args:
            key: 配置键，支持点号分隔的嵌套路径，如 'ui.theme'
            default: 默认值，当键不存在时返回
            
        Returns:
            Any: 配置值或默认值
        """
        parts = key.split('.')
        value = self._config
        
        for part in parts:
            if isinstance(value, dict) and part in value:
                value = value[part]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any) -> None:
        """设置配置值
        
        Args:
            key: 配置键，支持点号分隔的嵌套路径，如 'ui.theme'
            value: 要设置的值
        """
        parts = key.split('.')
        config = self._config
        
        # 遍历路径，直到倒数第二个部分
        for i, part in enumerate(parts[:-1]):
            if part not in config or not isinstance(config[part], dict):
                config[part] = {}
            config = config[part]
        
        # 设置最后一个部分的值
        config[parts[-1]] = value
    
    def get_all(self) -> Dict:
        """获取所有配置
        
        Returns:
            Dict: 完整的配置字典
        """
        return self._config
    
    def get_section(self, section: str) -> Dict:
        """获取配置的特定部分
        
        Args:
            section: 部分名称，如 'ui', 'download'
            
        Returns:
            Dict: 该部分的配置字典
        """
        return self._config.get(section, {})
    
    def update_section(self, section: str, values: Dict) -> None:
        """更新配置的特定部分
        
        Args:
            section: 部分名称，如 'ui', 'download'
            values: 要更新的值字典
        """
        if section not in self._config:
            self._config[section] = {}
        
        self._config[section].update(values)
    
    def merge_with_app_config(self, app_name: str, section: Optional[str] = None) -> Dict:
        """与F2的应用配置合并
        
        从F2的配置管理器中获取应用配置，并与GUI配置合并
        
        Args:
            app_name: 应用名称，如 'douyin', 'tiktok'
            section: 要合并的配置部分，如 'download'，默认合并所有
            
        Returns:
            Dict: 合并后的配置字典
        """
        try:
            app_config = ConfigManager(f2.APP_CONFIG_FILE_PATH).get_config(app_name) or {}
            
            if section:
                gui_config = self.get_section(section) or {}
                # GUI配置覆盖应用配置中相同的键
                merged = {**app_config, **gui_config}
                return merged
            else:
                # 合并完整配置
                return {**app_config, **self._config}
        except Exception as e:
            logger.error(f"合并应用配置失败: {str(e)}")
            return self._config if not section else self.get_section(section) or {}