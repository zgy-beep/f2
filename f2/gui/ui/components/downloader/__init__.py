# -*- coding:utf-8 -*-
# @Information  : 
# @Author       : ZGY
# @Date         : 2025-04-28 16:08:17
# @FilePath     : /f2_gui/f2/gui/ui/components/downloader/__init__.py
# @LastEditTime : 2025-04-28 16:25:30

"""
下载组件模块初始化
"""

from f2.gui.ui.components.downloader.batch_download_component import BatchDownloadComponent
from f2.gui.ui.components.downloader.single_download_component import SingleDownloadComponent
from f2.gui.ui.components.downloader.log_component import LogComponent

__all__ = ['BatchDownloadComponent', 'SingleDownloadComponent', 'LogComponent']