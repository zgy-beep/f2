# -*- coding:utf-8 -*-
# @Information  : 
# @Author       : ZGY
# @Date         : 2025-04-28 16:06:50
# @FilePath     : /f2_gui/f2/gui/ui/components/base_component.py
# @LastEditTime : 2025-04-28 16:06:55

"""
基础UI组件类
"""

from PyQt5.QtWidgets import QWidget

class BaseComponent:
    """基础UI组件类，所有UI组件的基类"""
    
    def __init__(self, parent=None):
        """初始化基础UI组件
        
        Args:
            parent: 父窗口组件
        """
        self.parent = parent
        
    def setup_ui(self):
        """设置UI组件，子类必须实现此方法"""
        raise NotImplementedError("子类必须实现setup_ui方法")