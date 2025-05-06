# -*- coding:utf-8 -*-
# @Information  : 
# @Author       : ZGY
# @Date         : 2025-04-29 10:58:14
# @FilePath     : /f2_gui/f2/gui/resources/resource_manager.py
# @LastEditTime : 2025-04-29 10:58:19

"""
资源管理器 - 处理程序中使用的资源文件
"""

import os
from PyQt5.QtGui import QIcon, QPixmap

# 获取资源目录的绝对路径
_RESOURCES_DIR = os.path.dirname(os.path.abspath(__file__))
_ICONS_DIR = os.path.join(_RESOURCES_DIR, "icons")


def get_icon_path(icon_name):
    """获取图标文件的绝对路径
    
    Args:
        icon_name: 图标文件名，可以包含或不包含扩展名
        
    Returns:
        str: 图标文件的绝对路径
    """
    # 支持的图标扩展名
    extensions = ['.ico', '.png', '.jpg']
    
    # 如果已经包含扩展名
    if any(icon_name.lower().endswith(ext) for ext in extensions):
        return os.path.join(_ICONS_DIR, icon_name)
    
    # 尝试不同的扩展名
    for ext in extensions:
        path = os.path.join(_ICONS_DIR, f"{icon_name}{ext}")
        if os.path.exists(path):
            return path
    
    # 默认为ico文件
    return os.path.join(_ICONS_DIR, f"{icon_name}.ico")


def load_icon(icon_name):
    """加载图标
    
    Args:
        icon_name: 图标文件名
        
    Returns:
        QIcon: 图标对象
    """
    icon_path = get_icon_path(icon_name)
    
    if os.path.exists(icon_path):
        print(f"正在加载图标: {icon_path}")
        return QIcon(icon_path)
    else:
        print(f"警告: 图标文件不存在: {icon_path}")
        return QIcon()


def load_pixmap(icon_name):
    """加载像素图
    
    Args:
        icon_name: 图标文件名
        
    Returns:
        QPixmap: 像素图对象
    """
    icon_path = get_icon_path(icon_name)
    
    if os.path.exists(icon_path):
        print(f"正在加载图标: {icon_path}")
        pixmap = QPixmap(icon_path)
        if pixmap.isNull():
            print(f"错误: 无法从文件创建像素图: {icon_path}")
        return pixmap
    else:
        print(f"警告: 图标文件不存在: {icon_path}")
        return QPixmap()