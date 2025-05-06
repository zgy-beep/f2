"""
抖音下载器 - 配置管理器
"""

import os
from pathlib import Path
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PyQt5.QtCore import QObject, pyqtSignal, QDate

from f2.utils.conf_manager import ConfigManager
from f2.log.logger import logger
from f2.gui.utils.gui_config_manager import GUIConfigManager


class SettingsManager(QObject):
    """设置管理器"""
    
    # 信号
    settings_loaded = pyqtSignal()
    settings_saved = pyqtSignal()
    log_message = pyqtSignal(str)
    
    def __init__(self, settings_tab_ui):
        """初始化设置管理器
        
        Args:
            settings_tab_ui: 设置标签页UI组件
        """
        super().__init__()
        self.ui = settings_tab_ui
        self.config_manager = GUIConfigManager()
        
        # 绑定信号和槽
        self.setup_connections()
    
    def setup_connections(self):
        """设置信号和槽连接"""
        # 绑定UI控件
        self.ui.browse_button.clicked.connect(self.browse_download_path)
        self.ui.save_settings_button.clicked.connect(self.save_config)
        self.ui.download_all.stateChanged.connect(self.ui.toggle_date_range)
        
        # 连接自身信号
        self.log_message.connect(lambda msg: print(msg))  # 临时打印到控制台
    
    def set_log_handler(self, handler):
        """设置日志处理器
        
        Args:
            handler: 日志处理函数
        """
        self.log_message.connect(handler)
    
    def browse_download_path(self):
        """浏览下载路径"""
        dir_path = QFileDialog.getExistingDirectory(
            None, "选择下载路径", self.ui.download_path.text() or str(Path.home())
        )
        
        if dir_path:
            self.ui.download_path.setText(dir_path)
    
    def get_config(self):
        """获取当前配置
        
        Returns:
            dict: 配置字典
        """
        # 获取GUI配置
        gui_config = self.config_manager.get_config("douyin")
        
        # 基本配置
        config = {
            "headers": {
                "User-Agent": self.ui.user_agent.text() or "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0",
                "Referer": "https://www.douyin.com/",
            },
            "proxies": {"http://": None, "https://": None},
            "mode": "post",
            "max_tasks": self.ui.max_tasks.value(),
            "monitor_updates": self.ui.monitor_updates.isChecked(),
            "update_interval": self.ui.update_interval.value(),
            "naming": self.ui.naming_format.text() or "{create}_{desc}",
            "video": self.ui.download_video.isChecked(),
            "cover": self.ui.download_cover.isChecked(),
            "desc": self.ui.download_desc.isChecked(),
            "music": self.ui.download_music.isChecked(),
            "folderize": self.ui.folderize.isChecked(),
        }
        
        # 设置代理
        proxy_url = self.ui.proxy.text().strip()
        if proxy_url:
            config["proxies"] = {"http://": proxy_url, "https://": proxy_url}
        
        # 设置下载路径
        download_path = self.ui.download_path.text().strip()
        if download_path:
            config["path"] = download_path
            
        # 设置下载日期区间
        if not self.ui.download_all.isChecked():
            start_date = self.ui.start_date.date().toString("yyyy-MM-dd")
            end_date = self.ui.end_date.date().toString("yyyy-MM-dd")
            config["interval"] = f"{start_date}|{end_date}"
        else:
            config["interval"] = "all"

        # 合并F2的配置，特别是获取cookie
        try:
            f2_config = ConfigManager("conf/app.yaml").get_config("douyin")
            # 合并配置，但保留GUI中设置的值优先
            for key, value in f2_config.items():
                if key not in config:
                    config[key] = value
                elif key == "headers" and isinstance(value, dict) and isinstance(config[key], dict):
                    # 合并headers，保留GUI设置的值
                    for header_key, header_value in value.items():
                        if header_key not in config[key]:
                            config[key][header_key] = header_value
        except Exception as e:
            self.log_message.emit(f"加载F2配置失败: {str(e)}")
        
        # 如果GUI配置中有额外的设置，也一并添加
        for key, value in gui_config.items():
            if key not in config:
                config[key] = value
        
        return config
    
    def load_config(self):
        """加载配置"""
        try:
            # 从GUI配置加载
            gui_config = self.config_manager.get_config("douyin")
            
            # 设置界面值
            if "headers" in gui_config and "User-Agent" in gui_config["headers"]:
                self.ui.user_agent.setText(gui_config["headers"]["User-Agent"])
            
            if "proxies" in gui_config and "http://" in gui_config["proxies"]:
                proxy = gui_config["proxies"]["http://"]
                if proxy:
                    self.ui.proxy.setText(proxy)
            
            if "naming" in gui_config:
                self.ui.naming_format.setText(gui_config["naming"])
            
            if "max_tasks" in gui_config:
                self.ui.max_tasks.setValue(gui_config["max_tasks"])
            
            if "folderize" in gui_config:
                self.ui.folderize.setChecked(gui_config["folderize"])
            
            if "video" in gui_config:
                self.ui.download_video.setChecked(gui_config["video"])
            
            if "cover" in gui_config:
                self.ui.download_cover.setChecked(gui_config["cover"])
            
            if "desc" in gui_config:
                self.ui.download_desc.setChecked(gui_config["desc"])
            
            if "music" in gui_config:
                self.ui.download_music.setChecked(gui_config["music"])
            
            # 首先尝试获取path参数(优先)
            if "path" in gui_config:
                self.ui.download_path.setText(gui_config["path"])
            # 如果不存在，则尝试获取旧参数名download_path
            elif "download_path" in gui_config:
                self.ui.download_path.setText(gui_config["download_path"])
                
            if "monitor_updates" in gui_config:
                self.ui.monitor_updates.setChecked(gui_config["monitor_updates"])
                
            if "update_interval" in gui_config:
                self.ui.update_interval.setValue(gui_config["update_interval"])
            
            # 加载日期区间设置
            if "interval" in gui_config:
                interval = gui_config["interval"]
                if interval == "all":
                    self.ui.download_all.setChecked(True)
                    self.ui.toggle_date_range(True)
                else:
                    try:
                        # 解析日期区间，格式：年-月-日|年-月-日
                        dates = interval.split("|")
                        if len(dates) == 2:
                            start_date = QDate.fromString(dates[0], "yyyy-MM-dd")
                            end_date = QDate.fromString(dates[1], "yyyy-MM-dd")
                            
                            if start_date.isValid() and end_date.isValid():
                                self.ui.download_all.setChecked(False)
                                self.ui.toggle_date_range(False)
                                self.ui.start_date.setDate(start_date)
                                self.ui.end_date.setDate(end_date)
                    except Exception as e:
                        self.log_message.emit(f"解析日期区间失败: {str(e)}")
            
            self.log_message.emit(f"已从 {self.config_manager.get_config_file_path()} 加载配置")
            self.settings_loaded.emit()
        except Exception as e:
            self.log_message.emit(f"加载配置失败: {str(e)}")
    
    def save_config(self):
        """保存配置"""
        try:
            # 获取当前配置
            config = self.get_config()
            
            # 保存到GUI配置文件
            if self.config_manager.update_config("douyin", config):
                QMessageBox.information(None, "成功", "设置已保存")
                self.log_message.emit(f"配置已保存到 {self.config_manager.get_config_file_path()}")
                self.settings_saved.emit()
                return True
            else:
                QMessageBox.critical(None, "错误", "保存配置失败")
                return False
                
        except Exception as e:
            error_msg = f"保存配置失败: {str(e)}"
            QMessageBox.critical(None, "错误", error_msg)
            self.log_message.emit(f"错误: {error_msg}")
            return False