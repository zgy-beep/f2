# -*- coding:utf-8 -*-
"""
更新记录对话框
"""

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QScrollArea, 
    QWidget, QPushButton, QHBoxLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from f2.gui.version import get_version, get_changelog


class ChangelogDialog(QDialog):
    """更新记录对话框"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"更新记录 - v{get_version()}")
        self.setMinimumSize(500, 400)
        self.setup_ui()
        
    def setup_ui(self):
        """设置UI"""
        layout = QVBoxLayout(self)
        
        # 标题
        title_label = QLabel(f"抖音下载器 v{get_version()} - 更新记录")
        title_font = title_label.font()
        title_font.setBold(True)
        title_font.setPointSize(12)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # 创建滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        
        # 添加版本更新记录
        changelog = get_changelog()
        for version, info in sorted(changelog.items(), reverse=True):
            version_layout = QVBoxLayout()
            
            # 版本号和日期
            version_label = QLabel(f"版本 {version} - {info['日期']}")
            version_font = version_label.font()
            version_font.setBold(True)
            version_font.setPointSize(10)
            version_label.setFont(version_font)
            version_layout.addWidget(version_label)
            
            # 更新内容
            for item in info['更新内容']:
                item_label = QLabel(f"• {item}")
                # 设置自动换行
                item_label.setWordWrap(True)
                version_layout.addWidget(item_label)
            
            # 添加版本分隔线
            if version != list(changelog.keys())[-1]:  # 如果不是最后一个版本
                separator = QLabel("─" * 60)
                separator.setAlignment(Qt.AlignCenter)
                version_layout.addWidget(separator)
            
            # 添加到滚动区域
            scroll_layout.addLayout(version_layout)
            
        # 添加底部弹性空间
        scroll_layout.addStretch(1)
        
        # 设置滚动区域内容
        scroll_area.setWidget(scroll_content)
        layout.addWidget(scroll_area)
        
        # 底部按钮
        button_layout = QHBoxLayout()
        close_button = QPushButton("关闭")
        close_button.clicked.connect(self.accept)
        button_layout.addStretch(1)
        button_layout.addWidget(close_button)
        layout.addLayout(button_layout)