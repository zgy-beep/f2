# -*- coding:utf-8 -*-
# @Information  : 
# @Author       : ZGY
# @Date         : 2025-04-29 10:14:51
# @FilePath     : /f2_gui/f2/gui/version.py
# @LastEditTime : 2025-04-29 10:18:58

# -*- coding:utf-8 -*-
"""
GUI版本管理模块
"""

__version__ = "0.0.3"

# 版本更新记录
__changelog__ = {
    "0.0.3": {
        "日期": "2025-04-29",
        "更新内容": [
            "支持批量下载抖音视频",
            "支持单个视频下载",
            "支持日志查看",
            "支持日间/夜间主题切换"
        ]
    },
    "0.0.2": {
        "日期": "2025-04-28",
        "更新内容": [
            "Beta版本发布",
            "实现基础下载功能",
            "添加用户界面基本组件"
        ]
    },
    "0.0.1": {
        "日期": "2025-04-28",
        "更新内容": [
            "界面原型设计",
            "基础架构搭建"
        ]
    }
}

def get_version():
    """获取当前GUI版本号"""
    return __version__

def get_changelog():
    """获取完整更新记录"""
    return __changelog__

def get_latest_changes():
    """获取最新版本的更新内容"""
    return __changelog__[__version__]