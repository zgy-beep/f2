"""
单个视频下载组件
"""

from PyQt5.QtWidgets import (QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
                           QTextEdit, QGroupBox)

from f2.gui.ui.components.base_component import BaseComponent

class SingleDownloadComponent(BaseComponent):
    """单个视频下载组件"""
    
    def __init__(self, parent=None):
        """初始化单个视频下载组件
        
        Args:
            parent: 父窗口组件
        """
        super().__init__(parent)
        
        # UI组件
        self.video_link_input = None
        self.download_single_button = None
        self.clear_link_button = None
        
        # 组件容器
        self.input_group = None
        self.info_group = None
        
        # 设置UI
        self.setup_ui()
    
    def setup_ui(self):
        """设置单个视频下载UI"""
        # 视频链接输入区域
        self.input_group = self._create_input_group()
        
        # 说明信息区域
        self.info_group = self._create_info_group()
    
    def _create_input_group(self):
        """创建视频链接输入区域
        
        Returns:
            QGroupBox: 视频链接输入区域组件
        """
        input_group = QGroupBox("输入视频链接")
        input_layout = QVBoxLayout()
        
        # 输入说明
        help_label = QLabel("输入抖音视频链接，支持长短链接和混合文本")
        help_label.setWordWrap(True)
        input_layout.addWidget(help_label)
        
        # 视频链接输入框
        self.video_link_input = QTextEdit()
        self.video_link_input.setPlaceholderText("例如：https://v.douyin.com/iRNBho6u/\n或者：7.64 gOX:/ w@f.oD 05/14 世界这本书 https://v.douyin.com/iR2syBRn/ 复制此链接...")
        self.video_link_input.setMinimumHeight(100)
        input_layout.addWidget(self.video_link_input)
        
        # 按钮区域
        buttons_layout = QHBoxLayout()
        
        self.download_single_button = QPushButton("下载视频")
        buttons_layout.addWidget(self.download_single_button)
        
        self.clear_link_button = QPushButton("清空输入")
        buttons_layout.addWidget(self.clear_link_button)
        
        input_layout.addLayout(buttons_layout)
        input_group.setLayout(input_layout)
        
        return input_group
    
    def _create_info_group(self):
        """创建说明信息区域
        
        Returns:
            QGroupBox: 说明信息区域组件
        """
        info_group = QGroupBox("说明")
        info_layout = QVBoxLayout()
        
        info_text = QLabel(
            "1. 支持链接格式包括：\n"
            " - 长链接：https://www.douyin.com/video/7189137516285800764\n"
            " - 短链接：https://v.douyin.com/iRNBho6u/\n"
            " - 带文本信息的链接：可直接粘贴分享链接文本\n\n"
            "2. 系统会自动识别文本中的链接\n"
            "3. 下载进度和结果将显示在下方日志区域"
        )
        info_text.setWordWrap(True)
        info_layout.addWidget(info_text)
        
        info_group.setLayout(info_layout)
        
        return info_group
    
    def get_input_widget(self):
        """获取视频链接输入区域组件
        
        Returns:
            QGroupBox: 视频链接输入区域组件
        """
        return self.input_group
    
    def get_info_widget(self):
        """获取说明信息区域组件
        
        Returns:
            QGroupBox: 说明信息区域组件
        """
        return self.info_group
    
    def clear_link_input(self):
        """清空视频链接输入框"""
        self.video_link_input.clear()
    
    def get_link_input_text(self):
        """获取视频链接输入框文本
        
        Returns:
            str: 视频链接输入框文本
        """
        return self.video_link_input.toPlainText()