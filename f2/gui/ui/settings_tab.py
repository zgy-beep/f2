"""
抖音下载器 - 设置标签页UI组件
"""

from PyQt5.QtWidgets import (QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                            QCheckBox, QFormLayout, QSpinBox, QGroupBox, QDateEdit)
from PyQt5.QtCore import Qt, QDate

class SettingsTabUI:
    """设置标签页UI组件"""

    def __init__(self, parent):
        """初始化设置标签页UI组件
        
        Args:
            parent: 父窗口组件
        """
        self.parent = parent
        
        # 初始化UI组件
        self.download_path = None
        self.naming_format = None
        self.start_date = None
        self.end_date = None
        self.download_all = None
        self.max_tasks = None
        self.monitor_updates = None
        self.update_interval = None
        self.download_video = None
        self.download_cover = None
        self.download_desc = None
        self.download_music = None
        self.folderize = None
        self.user_agent = None
        self.proxy = None
        self.save_settings_button = None
        
        # 设置UI
        self.setup_ui()
        
    def setup_ui(self):
        """设置设置标签页UI"""
        layout = QVBoxLayout(self.parent)
        
        # 基本设置组
        basic_group = QGroupBox("基本设置")
        basic_layout = QFormLayout()
        
        # 下载路径
        path_layout = QHBoxLayout()
        self.download_path = QLineEdit()
        self.download_path.setReadOnly(True)
        path_layout.addWidget(self.download_path, 1)
        
        self.browse_button = QPushButton("浏览...")
        path_layout.addWidget(self.browse_button)
        
        basic_layout.addRow("下载路径:", path_layout)
        
        # 命名格式
        self.naming_format = QLineEdit()
        self.naming_format.setPlaceholderText("{create}_{desc}")
        basic_layout.addRow("命名格式:", self.naming_format)
        
        # 命名格式帮助
        naming_help = QLabel("可用变量: {create}=创建时间, {desc}=视频描述, {aweme_id}=视频ID, {nickname}=用户昵称, {uid}=用户ID")
        naming_help.setWordWrap(True)
        basic_layout.addRow("", naming_help)
        
        # 日期区间
        date_range_layout = QHBoxLayout()
        self.start_date = QDateEdit()
        self.start_date.setCalendarPopup(True)
        self.start_date.setDisplayFormat("yyyy-MM-dd")
        self.start_date.setDate(QDate.currentDate().addYears(-1))  # 默认为一年前
        date_range_layout.addWidget(self.start_date)
        
        date_range_layout.addWidget(QLabel("至"))
        
        self.end_date = QDateEdit()
        self.end_date.setCalendarPopup(True)
        self.end_date.setDisplayFormat("yyyy-MM-dd")
        self.end_date.setDate(QDate.currentDate())  # 默认为当前日期
        date_range_layout.addWidget(self.end_date)
        
        self.download_all = QCheckBox("下载所有")
        self.download_all.setChecked(True)  # 默认下载所有
        date_range_layout.addWidget(self.download_all)
        
        basic_layout.addRow("下载区间:", date_range_layout)
        
        # 日期区间帮助提示
        date_range_help = QLabel("选择要下载的作品发布日期范围，勾选\"下载所有\"则不限制日期")
        date_range_help.setWordWrap(True)
        basic_layout.addRow("", date_range_help)
        
        # 最大并发数
        self.max_tasks = QSpinBox()
        self.max_tasks.setRange(1, 10)
        self.max_tasks.setValue(3)
        basic_layout.addRow("最大并发数:", self.max_tasks)
        
        # 检测更新
        self.monitor_updates = QCheckBox("定期检查更新")
        basic_layout.addRow("", self.monitor_updates)
        
        # 更新间隔
        self.update_interval = QSpinBox()
        self.update_interval.setRange(1, 1440)  # 1分钟到24小时
        self.update_interval.setValue(60)  # 默认1小时
        self.update_interval.setSuffix(" 分钟")
        basic_layout.addRow("更新间隔:", self.update_interval)
        
        basic_group.setLayout(basic_layout)
        layout.addWidget(basic_group)
        
        # 内容设置组
        content_group = QGroupBox("内容设置")
        content_layout = QVBoxLayout()
        
        # 下载内容类型
        self.download_video = QCheckBox("下载视频")
        self.download_video.setChecked(True)
        content_layout.addWidget(self.download_video)
        
        self.download_cover = QCheckBox("下载封面")
        self.download_cover.setChecked(True)
        content_layout.addWidget(self.download_cover)
        
        self.download_desc = QCheckBox("下载文案")
        self.download_desc.setChecked(True)
        content_layout.addWidget(self.download_desc)
        
        self.download_music = QCheckBox("下载原声")
        self.download_music.setChecked(True)
        content_layout.addWidget(self.download_music)
        
        self.folderize = QCheckBox("为每个视频创建单独文件夹")
        self.folderize.setChecked(True)
        content_layout.addWidget(self.folderize)
        
        content_group.setLayout(content_layout)
        layout.addWidget(content_group)
        
        # 网络设置组
        network_group = QGroupBox("网络设置")
        network_layout = QFormLayout()
        
        # 请求头设置
        self.user_agent = QLineEdit()
        self.user_agent.setPlaceholderText("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ...")
        network_layout.addRow("User-Agent:", self.user_agent)
        
        # 代理设置
        self.proxy = QLineEdit()
        self.proxy.setPlaceholderText("http://127.0.0.1:7890")
        network_layout.addRow("HTTP代理:", self.proxy)
        
        network_group.setLayout(network_layout)
        layout.addWidget(network_group)
        
        # 保存设置按钮
        self.save_settings_button = QPushButton("保存设置")
        layout.addWidget(self.save_settings_button)
        
        # 添加弹性空间
        layout.addStretch()
    
    def toggle_date_range(self, state):
        """启用或禁用日期区间选择器
        
        Args:
            state: 当前复选框状态
        """
        enabled = not bool(state)  # 如果下载所有被选中，则禁用日期选择
        self.start_date.setEnabled(enabled)
        self.end_date.setEnabled(enabled)